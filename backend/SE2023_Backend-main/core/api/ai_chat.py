import json
import os

import numpy as np
import torch
from transformers import BertModel, BertTokenizer
from django.http import HttpRequest
from core.models import Question
from django.views.decorators.http import require_POST, require_GET

import requests
import copy
from copy import deepcopy
from core.models.ai_report import AIReport
from core.models.card_message import CardMessage
from core.models.system_chat import SystemChatroom

from django.utils import timezone
import pytz

import traceback
from ltp import LTP

from core.api.utils import (
    response_wrapper,
    success_api_response, failed_api_response,
    read_json_data
)
from core.api.milvus_utils import (
    milvus_search,
    get_milvus_connection,
    milvus_query_set_question_by_id,
    milvus_query_expert_by_id,
    milvus_query_enterprise_by_id,
    milvus_query_result_hit_by_id,
)

from core.models.user import User
from core.models.results import Results

RES_PATH = os.path.abspath(os.getcwd()).split("\\core\\api")[0] + "\\resource"
# print(RES_PATH)
# assert 0

def get_now_time():
    """获取当前时间"""
    tz = pytz.timezone('Asia/Shanghai')
    # 返回时间格式的字符串
    now_time = timezone.now().astimezone(tz=tz)
    now_time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
    return now_time_str


class HitBert:
    def __init__(self, hitModelPath, device):
        self.hit_tokenizer = BertTokenizer.from_pretrained(hitModelPath)
        self.hit_model = BertModel.from_pretrained(hitModelPath, local_files_only=True)
        self.device = device
        self.hit_model.to(device)
        self.hit_model.eval()

    def encode(self, sent):
        encode_tensors = self.hit_tokenizer.encode_plus(sent, add_special_tokens=True, return_tensors='pt',
                                                        max_length=None)
        input_ids = encode_tensors['input_ids']
        lengths = torch.from_numpy(
            np.array([input_ids.shape[1] for _ in range(input_ids.shape[0])])).float()
        # padding_mask = get_padding_mask(lengths)  # transformers==2.3.0
        padding_mask = encode_tensors['attention_mask']  # transformers>3.0
        with torch.no_grad():
            outputs = self.hit_model(input_ids.to(
                self.device), attention_mask=padding_mask.to(self.device))[0]
            outputs.masked_fill_(
                padding_mask[:, :, None].to(self.device) == 0, 0)
            outputs = outputs[:, 1:-1, :].sum(dim=1).to(
                self.device) / (lengths[:, None] - 2).to(self.device)
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
        self.ltp = LTP()
        self.ltp.add_words(words=self.list1)

    def renew_all_data(self, dict_replace1, dict_replace2, model, n_gram, list_disltp):
        self.__init__(dict_replace1, dict_replace2, model, n_gram, list_disltp)

    def change_model(self, model):
        """
        更改ltp模型
        """
        self.ltp = LTP()
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
        # segment, hidden = self.ltp.seg([sent_replaced])
        # pos = self.ltp.pos(hidden)
        seg = self.ltp.pipeline([sent_replaced], tasks=["cws", "pos"])
        # print(segment.cws, segment.pos)
        i = 0
        sent_cut = []
        segment = seg.cws[0]
        pos = seg.pos[0]
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
    def __init__(self, hit_obj, ques_thresh, exp_thresh, ent_thresh, res_thresh):
        """
        问题/关键词识别器
        :param hit_obj: HitBert对象
        :param ques_thresh: 确认匹配预设问题的阈值
        :param exp_thresh: 确认匹配专家名的阈值
        :param ent_thresh: 确认匹配企业名的阈值
        :param res_thresh: 确认匹配成果标题的阈值
        """
        self.hit = hit_obj
        self.thresh_dict = {
            "SET_QUESTION": ques_thresh,
            "O2E_EXPERT_HIT": exp_thresh,
            "O2E_ENTERPRISE_HIT": ent_thresh,
            "O2E_RESULT_HIT": res_thresh,
        }
        self.milvus_key_dict = {
            "SET_QUESTION": "question_id",
            "O2E_EXPERT_HIT": "expert_id",
            "O2E_ENTERPRISE_HIT": "enterprise_id",
            "O2E_RESULT_HIT": "result_id",
        }
        self.milvus_fn_dict = {
            "SET_QUESTION": milvus_query_set_question_by_id,
            "O2E_EXPERT_HIT": milvus_query_expert_by_id,
            "O2E_ENTERPRISE_HIT": milvus_query_enterprise_by_id,
            "O2E_RESULT_HIT": milvus_query_result_hit_by_id,
        }

    def renew_all_data(self, hit_obj, ques_thresh, exp_thresh, ent_thresh, res_thresh):
        """
        问题/关键词识别器
        :param hit_obj: HitBert对象
        :param ques_thresh: 确认匹配预设问题的阈值
        :param exp_thresh: 确认匹配专家名的阈值
        :param ent_thresh: 确认匹配企业名的阈值
        :param res_thresh: 确认匹配成果标题的阈值
        """
        self.hit = hit_obj
        self.thresh_dict = {
            "SET_QUESTION": ques_thresh,
            "O2E_EXPERT_HIT": exp_thresh,
            "O2E_ENTERPRISE_HIT": ent_thresh,
            "O2E_RESULT_HIT": res_thresh,
        }

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
            matched_id = self.matcher(ques, "SET_QUESTION")
            if matched_id < 0:
                return True, res
            q_info = Question.objects.get(pk=matched_id)
            res["matched_q"] = q_info.question
            res["answer"] = q_info.ans
            res["multipic"] = q_info.multipic
            res["transfer"] = "False"
            return True, res
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return False, None

    def recognize_words(self, sent_cut):
        """
        识别传入分词结果能否匹配至数据库实体名
        :param sent_cut: 分词结果 [{'val':名字,'type':类型},{}]
        :param sent_in: 句子 字符串
        :return: (
            未出错标志, {
                "direct": "True/False（是否直接将问题输入给chatGPT）",
                "entity": {
                    "expert": ["专家id1", "专家id2"],
                    "enterprise": ["企业id1", "企业id2"],
                    "result": ["成果id1", "成果id2"]
                }
            }
        )
        """

        res = {
            "direct": "True",
            "entity": {
                "expert": [],
                "enterprise": [],
                "result": []
            }
        }
        sentence = None
        if sent_cut[-1].get("note") == "question":
            sentence = sent_cut[-1].get("val")
        else:
            for val in sent_cut:
                if val.get("note") == "question":
                    sentence = sent_cut[-1].get("val")
                    break
        if sentence is None:
            raise Exception("没有问题输入")

        try:
            if not sent_cut:
                print('未接收到分词结果')
                return False, res
            for word in sent_cut:
                if sentence.find(word['val']) == -1:
                    continue
                matched_id = self.matcher(word['val'], "O2E_EXPERT_HIT")
                if matched_id != -1:
                    res["direct"] = "False"
                    res["entity"]["expert"].append(matched_id)
                    sentence = sentence.replace(word['val'], '')
                    continue
                matched_id = self.matcher(word['val'], "O2E_ENTERPRISE_HIT")
                if matched_id != -1:
                    res["direct"] = "False"
                    res["entity"]["enterprise"].append(matched_id)
                    sentence = sentence.replace(word['val'], '')
                    continue
                matched_id = self.matcher(word['val'], "O2E_RESULT_HIT")
                if matched_id != -1:
                    res["direct"] = "False"
                    res["entity"]["result"].append(matched_id)
                    sentence = sentence.replace(word['val'], '')
            return True, res
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return False, None

    def matcher(self, target_sent, milvus_collection, n_cand=5):
        """
        计算句向量，寻找编码矩阵中离该句向量最近的n_cand个向量
        :param target_sent: 待计算问句
        :param milvus_collection: milvus库表名
        :param n_cand: 候选数量
        :return: 最佳匹配的数据库id
        """
        cand_id = -1
        target_vec = self.hit.encode_2_list(target_sent)
        id_lists = milvus_search(collection_name=milvus_collection, query_vectors=[target_vec],
                                 topk=n_cand, eps=self.thresh_dict[milvus_collection], partition_names=None)
        if not id_lists or not id_lists[0]:
            return cand_id

        ids = '['
        for id_list in id_lists:
            for milvus_id in id_list:
                ids += str(milvus_id) + ','
        ids = ids[:-1] + ']'
        query = "milvus_id in " + ids
        ques_ids = self.milvus_fn_dict[milvus_collection](query)
        # todo: 目前是直接选top1，应该改进为选top5/10后用其他方法再判断
        cand_id = ques_ids[0][self.milvus_key_dict[milvus_collection]]
        return cand_id


hit = HitBert(hitModelPath=RES_PATH + "/bert", device="cpu")

sentence_replace_dict = read_json_data(
    RES_PATH + "/sentence_replace_dict.json")
word_replace_dict = read_json_data(RES_PATH + "/word_replace_dict.json")
ltpParticipleDict = []  # todo: 要从数据库得到
process = Preprocessor(sentence_replace_dict,
                       word_replace_dict, "small", 4, ltpParticipleDict)

recognizer = Recognizer(hit, ques_thresh=0.7,
                        exp_thresh=0.95, ent_thresh=0.95, res_thresh=0.7)


def get_hitbert_embedding(sent):
    return hit.encode_2_list(sent)


@require_POST
@response_wrapper
def answer_set_question(request: HttpRequest):
    get_milvus_connection()
    data = request.POST.dict()
    question = data.get('input')
    print()
    ques = process.replacesentword(question)
    flag, result = recognizer.recognize_whole(ques)
    if not flag:
        return failed_api_response(500, error_msg="预设问题识别过程失败")

    result["code"] = 200
    return success_api_response(result)


def expert_to_info_str(exp_id):
    print("expert to info str")
    user = User.objects.get(id=exp_id)
    print("expert to info str2")
    expert = user.expert_info
    info_str = f"{expert.name}，在{expert.organization}工作，" + \
               f"头衔为{expert.title}，" + \
               f"擅长的研究领域有{expert.field}，" + \
               f"他/她这样介绍自己：{expert.self_profile}。"
    print("try to get all papers")
    papers = expert.papers.all()
    print("get all papers")
    if len(papers) > 0:
        paper_info = f"{expert.name}的论文有："
        for index, paper in enumerate(papers):
            paper_info += f"{index + 1}. {paper.title}. "
        info_str += paper_info
    patents = expert.patents.all()
    print("get all patents")
    if len(patents) > 0:
        patent_info = f"{expert.name}的专利有："
        for index, patent in enumerate(patents):
            patent_info += f"{index + 1}. {patent.title}. "
        info_str += patent_info
    projects = expert.projects.all()
    print("get all projects")
    if len(projects) > 0:
        project_info = f"{expert.name}的项目有："
        for index, project in enumerate(projects):
            project_info += f"{index + 1}. {project.title}. "
        info_str += project_info
    results = expert.results.all()
    print("get all results")
    if len(results) > 0:
        result_info = f"{expert.name}的成果有："
        for index, result in enumerate(results):
            result_info += f"{index + 1}. {result.title}. "
        info_str += result_info
    card_info = {
        "cardType": "expert", "id": exp_id, "title": expert.name,
        "avatar": user.icon, "info": expert.self_profile
    }
    return info_str, card_info


def enterprise_to_info_str(ent_id):
    user = User.objects.get(id=ent_id)
    enterprise = user.enterprise_info
    info_str = f"{enterprise.name}，坐落在{enterprise.address}，" + \
               f"主营业务有{enterprise.field}，" + \
               f"企业简介：{enterprise.self_profile}。"
    card_info = {
        "cardType": "enterprise", "id": ent_id, "title": enterprise.name,
        "avatar": user.icon, "info": enterprise.instruction
    }
    return info_str, card_info


def result_to_info_str(rst_id):
    result = Results.get(id=rst_id)
    info_str = f"{result.field}领域的技术成果《{result.title}》，{result.abstract}。"
    card_info = {
        "cardType": "technique", "id": rst_id, "title": result.title,
        "avatar": result.picture, "info": result.abstract
    }
    return info_str, card_info


@require_POST
@response_wrapper
def answer_free_question(request: HttpRequest):
    # print(0)
    # get_milvus_connection()
    # print(1.1)
    # # data = request.POST.dict()
    data: dict = json.loads(request.body.decode())
    # print(data)
    question = data.get('input')
    #
    # flag, result = process.preprocess(question)
    # print(result)
    # print(1)
    # if not flag:
    #     return failed_api_response(500, error_msg="非预设问题预处理过程失败")
    # flag, result2 = recognizer.recognize_words(result)
    # print(result2)
    # print(2)
    # if not flag:
    #     return failed_api_response(500, error_msg="非预设问题提取关键词过程失败")
    # print(3)
    """
    result2 = {
        "direct": "True/False（是否直接将问题输入给chatGPT）",
        "entity": {
            "expert": ["专家id1", "专家id2"],
            "enterprise": ["企业id1", "企业id2"],
            "result": ["成果id1", "成果id2"]
        }
    }
    """
    result2 = {
        "direct": "True",
        "entity": {
            "expert": ["专家id1", "专家id2"],
            "enterprise": ["企业id1", "企业id2"],
            "result": ["成果id1", "成果id2"]
        }
    }
    for ent in ["expert", "enterprise", "result"]:
        result2["entity"][ent] = list(set(result2["entity"][ent]))
    final = {
        "code": 200,
        "answer": "",
        "card": {
            "expert": [],
            "enterprise": [],
            "result": [],
        }
    }

    user_id = data.get("uId")
    sender: User = User.objects.get(id=user_id)
    system_chatroom: SystemChatroom = None
    if sender.system_chatroom_list.all().exists():
        system_chatroom = sender.system_chatroom_list.get().id
    else:
        system_chatroom = SystemChatroom(owner=sender, isai=SystemChatroom.MANUAL_REPLY,
                                         last_message_time=get_now_time(), unread_message_num=0)
        system_chatroom.save()
    print(4)
    # 注：当result2["direct"] == "True"时，不需要查数据库，直接跳过该步骤
    # (1)
    #   在result2["entity"][?]拿id --> 数据库查这个id的属性 --> 把查到的东西拼接成一段话，放进final["answer"]
    #   如果result2有很多个id，那就把分别得到的“一段话”拼成一大段话放进final["answer"]
    # (2)
    #   根据张凯歌给的前端卡片信息展示需求（cardInfo），把信息放到final["card"][?]。
    #   （列表元素是一个个dict：{"cardType": xx, "id": xx, "title": xx, "avatar": xx, "info": xx}）
    #   result2["entity"]有多少个元素，final["card"]就得对应上

    if result2["direct"] == "False":

        for exp_id in result2["entity"]["expert"]:
            info_str, card_info = expert_to_info_str(exp_id)
            final["answer"] += info_str
            final["card"]["expert"].append(card_info)
            print(card_info)
            new_card_message_id = CardMessage.new_card_message(sender, 0, card_info['info'],
                                                               card_type=0, title=card_info['title'],
                                                               avatar=card_info['avatar'], involved_id=card_info['id'])
            print(new_card_message_id)
            system_chatroom.add_message(new_card_message_id)

        for ent_id in result2["entity"]["enterprise"]:
            info_str, card_info = enterprise_to_info_str(ent_id)
            final["answer"] += info_str
            final["card"]["enterprise"].append(card_info)
            new_card_message_id = CardMessage.new_card_message(sender, 0, card_info['info'],
                                                               card_type=1, title=card_info['title'],
                                                               avatar=card_info['avatar'], involved_id=card_info['id'])
            system_chatroom.add_message(new_card_message_id)

        for rst_id in result2["entity"]["result"]:
            info_str, card_info = result_to_info_str(rst_id)
            final["answer"] += info_str
            final["card"]["result"].append(card_info)
            new_card_message_id = CardMessage.new_card_message(sender, 0, card_info['info'],
                                                               card_type=3, title=card_info['title'],
                                                               avatar=card_info['avatar'], involved_id=card_info['id'])
            system_chatroom.add_message(new_card_message_id)

    # todo 荆睿涛：
    #   将final["answer"]和question拼接起来送进chatGPT，然后用chatGPT的回复替换final["answer"]的内容
     # 形成询问prompt
    print(5)
    demand1 = "请结合已有的信息，回答以下的问题"
    partial_answer = "其中已知信息为" + final['answer']
    msg = demand1+partial_answer+", 问题是"+question

    # 整合请求体
    url = f"https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer $OPEN_API_KEY"}
    sent_data = []
    sent_data['model'] = "gpt-3.5-turbo"
    sent_data['message'] = {"role": "user", "content": msg.encode("utf-8")}
    sent_data['temperature'] = 0.7
    response = requests.post(url, headers=headers, data=sent_data)

    final['answer'] = response.content.decode('utf-8')

    return success_api_response(final)
