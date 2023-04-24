import torch
from django.db.models import Avg
from django.http import HttpRequest
from django.views.decorators.http import require_GET

from core.api.utils import (response_wrapper, success_api_response)
from core.models.expert import Expert
from core.models.papers import Papers
from core.models.need import Need
from core.models.user import User
from core.models.results import Results
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from core.api.auth import getUserInfo

from core.api.milvus_utils import (
    get_milvus_connection,
    milvus_search, milvus_insert,
    milvus_query_paper_by_id,
    milvus_query_need_by_id,
    milvus_query_result_by_id,
)


from core.api.zhitu_utils import get_expertInfo_by_expertId, search_expertID_by_paperID
import requests


class ContrastiveSciBERT(nn.Module):
    def __init__(self, out_dim, tau, device='cpu'):
        """⽤于对⽐学习的SciBERT模型
        :param out_dim: int 输出特征维数
        :param tau: float 温度参数τ
        :param device: torch.device, optional 默认为CPU
        """
        super().__init__()
        self.tau = tau
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(
            'allenai/scibert_scivocab_uncased')
        self.model = AutoModel.from_pretrained(
            'allenai/scibert_scivocab_uncased').to(device)
        self.linear = nn.Linear(
            self.model.config.hidden_size, out_dim).to(device)

    def get_embeds(self, texts, max_length=64):
        """将⽂本编码为向量
        :param texts: List[str] 输⼊⽂本列表，⻓度为N


        # Press the green button in the gutter to run the script.
        if __name__ == '__main__':
            print("success")
        :param max_length: int, optional padding最⼤⻓度，默认为64
        :return: tensor(N, d_out)
        """
        encoded = self.tokenizer(
            texts, padding='max_length', truncation=True, max_length=max_length, return_tensors='pt'
        ).to(self.device)
        return self.linear(self.model(**encoded).pooler_output)

    def calc_sim(self, texts_a, texts_b):
        """计算两组⽂本的相似度
        :param texts_a: List[str] 输⼊⽂本A列表，⻓度为N
        :param texts_b: List[str] 输⼊⽂本B列表，⻓度为N
        :return: tensor(N, N) 相似度矩阵，S[i, j] = cos(a[i], b[j]) / τ
        """
        embeds_a = self.get_embeds(texts_a)  # (N, d_out)
        embeds_b = self.get_embeds(texts_b)  # (N, d_out)
        embeds_a = embeds_a / embeds_a.norm(dim=1, keepdim=True)
        embeds_b = embeds_b / embeds_b.norm(dim=1, keepdim=True)
        return embeds_a @ embeds_b.t() / self.tau

    def forward(self, texts_a, texts_b):
        """计算两组⽂本的对⽐损失（直接返回损失）
        :param texts_a: List[str] 输⼊⽂本A列表，⻓度为N
        :param texts_b: List[str] 输⼊⽂本B列表，⻓度为N
        :return: tensor(N, N), float A对B的相似度矩阵，对⽐损失
        """
        # logits_ab等价于预测概率，对⽐损失等价于交叉熵损失
        logits_ab = self.calc_sim(texts_a, texts_b)
        logits_ba = logits_ab.t()
        labels = torch.arange(len(texts_a), device=self.device)
        loss_ab = F.cross_entropy(logits_ab, labels)
        loss_ba = F.cross_entropy(logits_ba, labels)
        loss = (loss_ab + loss_ba) / 2
        return loss


# model = torch.load("model.pt", map_location='cpu')
state_dict = torch.load("model.pt", map_location='cpu')
model = ContrastiveSciBERT(out_dim=128, tau=0.07)
model.load_state_dict(state_dict)


def get_scibert_embedding(sent):
    return model.get_embeds([sent]).tolist()[0]


@require_GET
@response_wrapper
def recommend(request: HttpRequest, id: int):
    get_milvus_connection()
    need = Need.objects.get(id=id)
    keyword = [need.key_word]
    key_vector = model.get_embeds(keyword)
    key_vector = key_vector / key_vector.norm(dim=1, keepdim=True)
    b = key_vector.detach().numpy().tolist()
    id_lists = milvus_search(collection_name="O2E_TEMP", query_vectors=b, topk=10,
                             partition_names=None)[0]
    cites = []
    register_experts = []
    scholarIDs = []
    for id in id_lists:
        paper = Papers.objects.get(vector=str(id))
        title = paper.title
        expert_possible = paper.expert_papers.all()
        for expert in expert_possible:
            cite = 0
            papers = expert.papers.all()
            for paper in papers:
                cite += paper.cites
            cites.append(cite)
            scholarIDs.append(expert.scholarID)
            user = expert.expert_info
            dic = getUserInfo(user)
            dic['title'] = title
            avg = list()
            avg_taste = user.expert_rate.aggregate(
                Avg('rate_taste')).get('rate_taste__avg')
            if avg_taste is None:
                avg_taste = 5
            avg.append(avg_taste)

            avg_speed = user.expert_rate.aggregate(
                Avg('rate_speed')).get('rate_speed__avg')
            if avg_speed is None:
                avg_speed = 5
            avg.append(avg_speed)

            avg_level = user.expert_rate.aggregate(
                Avg('rate_level')).get('rate_level__avg')
            if avg_level is None:
                avg_level = 5
            avg.append(avg_level)
            dic['comment'] = avg
            register_experts.append(dic)
    max_cite = max(cites)
    i = 0
    while i < len(register_experts):
        j = i + 1
        while j < len(register_experts):
            if max_cite != 0:
                score_i = sum(
                    register_experts[i]["comment"]) + cites[i] / max_cite
                score_j = sum(
                    register_experts[j]["comment"]) + cites[j] / max_cite
            else:
                score_i = sum(register_experts[i]["comment"]) + cites[i]
                score_j = sum(register_experts[j]["comment"]) + cites[j]
            if score_j > score_i:
                temp = register_experts[i]
                register_experts[i] = register_experts[j]
                register_experts[j] = temp
            j += 1
        i += 1

    # 未注册专家推荐
    possible_experts = []
    id_lists = milvus_search(collection_name="O2E_PAPER", query_vectors=b, topk=3, partition_names=None)[0]
    s = '['
    for id in id_lists:
        s = s + str(id) + ','
    if len(s) != 1:
        s = s[:-1]
    s += ']'
    query = "milvus_id in " + s
    paper_ids = milvus_query_paper_by_id(query)
    for paper_id in paper_ids:
        num = 0
        expert_ids, title = search_expertID_by_paperID(paper_id['paper_id'])
        for expert_id in expert_ids:
            op = True
            for scholarID in scholarIDs:
                if expert_id == scholarID:
                    op = False
                    break
            if op and num < 3:
                num += 1
                expert_list = get_expertInfo_by_expertId(expert_id)
                expert_list['title'] = title
                possible_experts.append(expert_list)
    return success_api_response({
        "register": register_experts[:3],
        "other": possible_experts[:3]
    })


@require_GET
@response_wrapper
def need_recommend(request: HttpRequest, id: int):
    get_milvus_connection()
    user = User.objects.get(id=id)
    papers = user.expert_info.papers.all()
    titles = []
    for paper in papers:
        titles.append(paper.title)
    key_vector = model.get_embeds(titles)
    key_vector = key_vector / key_vector.norm(dim=1, keepdim=True)
    key_vector = key_vector.detach().numpy().tolist()
    id_lists = milvus_search(
        "O2E_NEED", query_vectors=key_vector, topk=2, partition_names=None)
    ids = '['
    for id_list in id_lists:
        for milvus_id in id_list:
            ids += str(milvus_id) + ','
    ids = ids[:-1] + ']'
    query = "milvus_id in " + ids
    need_ids = milvus_query_need_by_id(query)
    need_infos = []
    for need_id in need_ids:
        need = Need.objects.get(pk=need_id['need_id'])
        if need.state == 0:
            enterprise: User = need.enterprise
            need_info = {
                "need_id": need.id, "title": need.title, "description": need.description, "money": need.money,
                "start_time": need.start_time,
                "end_time": need.end_time, "key_word": need.key_word, "field": need.field, "address": need.address,
                "state": need.state,
                "emergency": need.emergency,
                "enterprise_id": enterprise.id, "enterprise_name": enterprise.enterprise_info.name,
                "enterprise_pic": str(enterprise.icon)
            }
            order = list()
            orders = need.need_order.exclude(state=2)
            for o in orders:
                order_info = {
                    "order_id": o.id,
                    "order_state": o.state,
                    "expert_id": o.user.id,
                    "expert_icon": str(o.user.icon),
                    "expert_name": o.user.expert_info.name,
                    "enterprise_id": o.enterprise.id
                }
                order.append(order_info)
            need_info['order'] = order
            need_infos.append(need_info)

    return success_api_response({"needs": need_infos[:3]})


@require_GET
@response_wrapper
def result_recommend_for_expert(request: HttpRequest, id: int):
    get_milvus_connection()
    user = User.objects.get(id=id)
    papers = user.expert_info.papers.all()
    print('check milvus connection:[1]')
    print('Papers:')
    print(papers)
    if not papers:
        return success_api_response({"results": []})
    titles = []
    for paper in papers:
        titles.append(paper.title)
    key_vector = model.get_embeds(titles)
    print('check milvus connection:[2]')

    key_vector = key_vector / key_vector.norm(dim=1, keepdim=True)
    key_vector = key_vector.detach().numpy().tolist()
    id_lists = milvus_search(
        "O2E_RESULT", query_vectors=key_vector, topk=20, partition_names=None)
    print(id_lists)
    ids = '['
    for id_list in id_lists:
        for milvus_id in id_list:
            ids += str(milvus_id) + ','
    if ids == '[':
        return success_api_response({"results": []})
    ids = ids[:-1] + ']'
    query = "milvus_id in " + ids
    print(query)
    result_ids = milvus_query_result_by_id(query)
    print(result_ids)
    result_infos = []
    for result_id in result_ids:
        result = Results.objects.get(pk=result_id['result_id'])
        expert = Expert.objects.filter(results__id=result.id)[0]
        user = User.objects.get(expert_info__id=expert.id)
        if result.state == 1:
            result_info = {
                "user_id": user.id,
                "result_id": result.id,
                "expert_id": expert.id,
                "title": result.title,
                "abstract": result.abstract,
                "scholars": result.scholars,
                "pyear": result.pyear,
                "field": result.field,
                "period": result.period,
                "content": result.content,
                "state": result.state,
                "result_pic": result.get_pic(),
                "expert_icon": str(user.icon)
            }
            result_infos.append(result_info)
    print(result_infos)
    return success_api_response({"results": result_infos})


@require_GET
@response_wrapper
def result_recommend_for_enterprise(request: HttpRequest, id: int):
    get_milvus_connection()
    needs = Need.objects.filter(enterprise_id=id)
    if not needs:
        return success_api_response({"results": []})
    titles = []
    for need in needs:
        titles.append(need.title)
    key_vector = model.get_embeds(titles)
    key_vector = key_vector / key_vector.norm(dim=1, keepdim=True)
    key_vector = key_vector.detach().numpy().tolist()
    id_lists = milvus_search(
        "O2E_RESULT", query_vectors=key_vector, topk=20, partition_names=None)
    ids = '['
    for id_list in id_lists:
        for milvus_id in id_list:
            ids += str(milvus_id) + ','
    if ids == '[':
        return success_api_response({"results": []})
    ids = ids[:-1] + ']'
    query = "milvus_id in " + ids
    result_ids = milvus_query_result_by_id(query)
    result_infos = []
    for result_id in result_ids:
        result = Results.objects.get(pk=result_id['result_id'])
        expert = Expert.objects.filter(results__id=result.id)[0]
        user = User.objects.get(expert_info__id=expert.id)
        if result.state == 1:
            result_info = {
                "user_id": user.id,
                "result_id": result.id,
                "expert_id": expert.id,
                "title": result.title,
                "abstract": result.abstract,
                "scholars": result.scholars,
                "pyear": result.pyear,
                "field": result.field,
                "period": result.period,
                "content": result.content,
                "state": result.state,
                "result_pic": result.get_pic(),
                "expert_icon": str(user.icon)
            }
            result_infos.append(result_info)

    return success_api_response({"results": result_infos})

#
# def insert_need_sci(nid: int):
#     get_milvus_connection()
#     need = Need.objects.get(pk=nid)
#     keyword = [need.key_word]
#     key_vector = model.get_embeds(keyword)
#     # key_vector = key_vector / key_vector.norm(dim=1, keepdim=True)
#     key_vector = key_vector.detach().numpy().tolist()
#     milvus_id = milvus_insert("O2E_NEED", [key_vector, [nid]])
#     print(milvus_id)
#     return milvus_id

#
# def insert_result_sci(rid: int):
#     get_milvus_connection()
#     result = Results.objects.get(pk=rid)
#     keyword = [result.title, result.abstract]
#     key_vector = model.get_embeds(keyword)
#     # key_vector = key_vector / key_vector.norm(dim=1, keepdim=True)
#     key_vector = key_vector.detach().numpy().tolist()
#     milvus_id = milvus_insert("O2E_RESULT", [key_vector, [rid]])
#     print(milvus_id)
#     return milvus_id


@require_GET
@response_wrapper
def generate_requirement_book(request: HttpRequest, require):
    # start a new conversation
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer $OPEN_API_KEY"}
    # start to ask
    url = f"https://api.openai.com/v1/chat/completions"

    demand1 = "请将以下的企业需求转化成一份详细的需求报告，包括功能点的划分，每个功能点的形式化表述、详细描述以及其参考技术路线。"
    prompt = require
    format = "报告采用markdown格式，设三级标题。对于每个功能点，形式化表述、详细描述和参考技术路线，请分条叙述。"
    demand2 = "报告首先有一个总标题，但是不用写引言、不用写总结、不用写参考文献。总字数不超过2000字，请对内容进行精炼。报告生成结束请回复完毕二字。"
    msg = demand1+prompt+format+demand2

    
    # Create the request headers and body
    data = []
    data['model'] = "gpt-3.5-turbo"
    data['message'] = {"role": "user", "content": msg.encode("utf-8")}
    data['temperature'] = 0.7
    # Send the POST request to the API endpoint
    response = requests.post(url, headers=headers, data=data)
    print(response.content.decode('utf-8'))
    return success_api_response({"requirement_book": response.content.decode('utf-8')})

if __name__ == '__main__':
    state_dict = torch.load("E:\\lcm\\Course\\软件工程\\O2E-TU-2\\代码\\后端\\O2E-TU-2-训练\\model.pt", map_location='cpu')
    model = ContrastiveSciBERT(out_dim=128, tau=0.07)
    model.load_state_dict(state_dict)
    vector = model.get_embeds(["哈哈哈","hhh"])
    print(vector)

    
