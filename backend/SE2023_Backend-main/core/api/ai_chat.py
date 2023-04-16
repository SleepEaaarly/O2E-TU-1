import numpy as np
import torch
from transformers import BertModel, BertTokenizer

from copy import deepcopy
import traceback
from ltp import LTP

from core.api.utils import {
    response_wrapper, 
    success_api_response, failed_api_response,
    read_json_data
}

RES_PATH = "../../resource"


class hitBert:
    def __init__(self, hitModelPath, device):
        self.hit_tokenizer = BertTokenizer.from_pretrained(hitModelPath)
        self.hit_model = BertModel.from_pretrained(hitModelPath)
        self.device = device
        self.hit_model.to(device)
        self.hit_model.eval()

    def encode(self, sent):
        encode_tensors = self.hit_tokenizer.encode_plus(sent, add_special_tokens=True, return_tensors='pt',
                                                        max_length=None)
        input_ids = encode_tensors['input_ids']
        lengths = torch.from_numpy(np.array([input_ids.shape[1] for _ in range(input_ids.shape[0])])).float()
        # padding_mask = get_padding_mask(lengths)  # transformers==2.3.0
        padding_mask = encode_tensors['attention_mask']  # transformers>3.0
        with torch.no_grad():
            outputs = self.hit_model(input_ids.to(self.device), attention_mask=padding_mask.to(self.device))[0]
            outputs.masked_fill_(padding_mask[:, :, None].to(self.device) == 0, 0)
            outputs = outputs[:, 1:-1, :].sum(dim=1).to(self.device) / (lengths[:, None] - 2).to(self.device)
        # return outputs[0].cpu().numpy().tolist()
        return outputs

    def encode_2_list(self, sent):
        return self.encode(sent)[0].cpu().numpy().tolist()


class Preprocessor:
    def __init__(self, dict_replace1, dict_replace2, model, n_gram, list_disltp):
        """
        预处理器
        :param dict_replace1: 句子替换词典
        :param dict_replace2: 词语替换词典
        :param model: LTP模型名称
        :param n_gram: 分词后拼接词数
        :param list_disltp: 分词词表
        """
        self.words = {
            'val': 'None',
            'note': 'None',
        }
        self.dict1 = dict_replace1
        self.model = model
        self.dict2 = dict_replace2
        self.n_gram = n_gram
        self.list1 = list_disltp
        self.ltp = LTP(path=self.model)
        self.ltp.add_words(words=self.list1)

    def renew_all_data(self, dict_replace1, dict_replace2, model, n_gram, list_disltp):
        self.words = {
            'val': 'None',
            'note': 'None',
        }
        self.dict1 = dict_replace1
        self.model = model
        self.dict2 = dict_replace2
        self.n_gram = n_gram
        self.list1 = list_disltp
        self.ltp = LTP(path=self.model)
        self.ltp.add_words(words=self.list1)

    def change_model(self, model):
        """
        更改ltp模型
        """
        self.ltp = LTP(path=model)
        self.ltp.add_words(words=self.list1)

    def preprocess(self, sent):
        """
        对传入数据进行处理。
        """
        flag = True
        try:
            if not sent:
                print('未接收到数据')
                flag = False
            sent_replaced = self.replacesentword(sent)
            if not sent_replaced:
                flag = False
            sent_cut = self.segment(sent_replaced)
            sent_cut_replaced = self.replacecutword(sent_cut)
            if not sent_cut_replaced:
                flag = False
            result = self.joinword(sent_cut_replaced)
            self.words = {
                'val': sent_replaced,
                'note': 'question',
            }
            if not result:
                flag = False
            result.append(deepcopy(self.words))
            return flag, result
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return False, None

    def replacesentword(self, sent):
        """
        第一次替换词，将句子中的停用词删去。
        例：空客A320的载客量是多少？
        替换词典为{'的':'','是':'','?':''}
        输出为：空客A320载客量多少
        """
        replacedsent = sent
        for replacedword, replaceword in self.dict1.items():
            if replacedword in replacedsent:
                replacedsent = replacedsent.replace(replacedword, replaceword)
        return replacedsent

    def segment(self, sent_replaced):
        """
        分词，并将分词结果改为需要格式。
        """
        segment, hidden = self.ltp.seg([sent_replaced])
        pos = self.ltp.pos(hidden)
        i = 0
        sent_cut = []
        segment = segment[0]
        pos = pos[0]
        for cutword in segment:
            self.words['val'] = cutword
            self.words['note'] = pos[i]
            if self.words['note'][0] == 'n':
                self.words['note'] = 'n'
            sent_cut.append(deepcopy(self.words))
            i += 1
        # i = 0
        # for cuted_word in sent_cut:
        #     if i == len(sent_cut) - 1:
        #         break
        #     if cuted_word['val'] == '最' or cuted_word['val'] == '前':
        #         for c in range(1, len(sent_cut) - i):
        #             if sent_cut[i + 1]['note'] == 'a' or sent_cut[i + 1]['note'] == 'm':
        #                 cuted_word['val'] = f"{cuted_word['val']}{sent_cut[i + 1]['val']}"
        #                 cuted_word['note'] = 'a'
        #                 del sent_cut[i + 1]
        #                 continue
        #             break
        #     i += 1
        return sent_cut

    def replacecutword(self, sent_cut):
        """
        第二次分词，删除停用词，替换词
        """
        sent_cut_result = copy.deepcopy(sent_cut)
        for i, word in enumerate(sent_cut):
            if word.get("val") in self.dict2:
                if len(self.dict2.get(word.get("val"))) == 0:
                    sent_cut_result.remove(word)
                else:
                    sent_cut_result[i]["val"] = self.dict2.get(word.get("val"))
        return sent_cut_result

    def joinword(self, sent_cut_replaced):
        """
        拼接根据n_gram对分词结果进行拼接
        """
        length = len(sent_cut_replaced)
        i = 0
        for word in sent_cut_replaced[0:length - 1]:
            flag = 0
            self.words['val'] = word['val']
            self.words['note'] = word['note']
            for word1 in sent_cut_replaced[i + 1:length]:
                if word1['note'] == word['note'] and flag < (self.n_gram - 1):
                    flag += 1
                    if flag != 0:
                        for word2 in sent_cut_replaced[i + flag:i + flag + 1]:
                            self.words['val'] = f"{self.words['val']}{word2['val']}"
                        sent_cut_replaced.append(deepcopy(self.words))
                    continue
                else:
                    break
            i += 1
        """
        对分词结果进行排序，长的放在前面。
        """
        for a in range(0, len(sent_cut_replaced)):
            for b in range(a + 1, len(sent_cut_replaced)):
                if len(sent_cut_replaced[a]['val']) < len(sent_cut_replaced[b]['val']):
                    sent_cut_replaced[a], sent_cut_replaced[b] = sent_cut_replaced[b], sent_cut_replaced[a]
        return sent_cut_replaced


class Recognizer:
    def __init__(self, ques_thresh):
        """
        预设问题识别器
        :param ques_thresh: 确认匹配预设问题的阈值
        :param ques_list: 预设问题库-回答列表
        """
        self.ques_thresh = ques_thresh

    def renew_all_data(self, ques_thresh):
        """
        :param ques_thresh: 确认匹配预设问题的阈值
        :param ques_list: 预设问题库-回答列表
        """
        self.ques_thresh = ques_thresh

    def recognize_whole(self, ques):
        """
        识别传入问题能否匹配至题库问题
        :param ques: 问题（整句）
        :return: (
            未出错标志, {
                "transfer": "True/False（是否建议转人工）",
                "matched_q": "匹配到的预设问题",
                "answer": "不建议转人工时自动回复的内容"
            }
        )
        """
        res = {"transfer": "True", "matched_q": "", "answer": ""}
        try:
            if not ques:
                print('未接收到数据')
                return False, res
            matched_id = self.matcher(ques)
            if matched_id < 0:
                return True, res
            # todo: 下述均不是确定的对象名属性名，等数据库建好表记得改
            q_info = Questions.objects.get(pk=matched_id) 
            res["matched_q"] = q_info.question
            res["answer"] = q_info.answer
            res["transfer"] = "False"
            return True, res
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return False, None

    def matcher(self, target_sent, n_cand=1):
        """
        计算问题句向量，寻找编码矩阵中离该句向量最近的n_cand个向量
        :param target_sent: 待计算问句
        :param n_cand: 候选问题数量
        :return: 最佳匹配问题的数据库id
        """ 
        cand_id = -1
        target_vec = hit.encode_2_list(target_sent)
        id_lists = milvus_search(collection_name="SET_QUESTION", query_vectors=[target_vec], 
                                 topk=n_cand, eps=self.ques_thresh, partition_names=None)
        if not id_lists or not id_lists[0]:
            return cand_id
        
        ids = '['
        for id_list in id_lists:
            for milvus_id in id_list:
                ids += str(milvus_id) + ','
        ids = ids[:-1] + ']'
        query = "milvus_id in " + ids
        ques_ids = milvus_query_set_question_by_id(query)
        # todo: 目前是直接选top1，应该改进为选top5/10后用其他方法再判断
        cand_id = ques_ids[0]["question_id"]
        return cand_id


hit = hitBert(hitModelPath=RES_PATH+"/bert", device="cpu")

sentence_replace_dict = read_json_data(RES_PATH+"/sentence_replace_dict.json")
word_replace_dict = read_json_data(RES_PATH+"/word_replace_dict.json")
ltpParticipleDict = [] # todo: 要从数据库得到
process = Preprocessor(sentence_replace_dict, word_replace_dict, "small", 2, ltpParticipleDict)

recognizer = Recognizer(ques_thresh=0.5)


@require_GET
@response_wrapper
def answer_set_question(request:HttpRequest):
    get_milvus_connection()
    data = request.GET.dict()
    question = data.get('input')
    ques = process.replacesentword(question)
    flag, data = recognizer.recognize_whole(ques)
    if not flag:
        return failed_api_response(500, error_msg="预设问题识别过程失败")
    data["code"] = 200
    return success_api_response(data)


@require_GET
@response_wrapper
def answer_free_question(request:HttpRequest):
    # todo
    get_milvus_connection()
    data = request.GET.dict()
    question = data.get('input')
    ques = process.replacesentword(question)
    flag, data = recognizer.recognize_whole(ques)
    if not flag:
        return failed_api_response(500, error_msg="非预设问题识别过程失败")
    data["code"] = 200
    return success_api_response(data)