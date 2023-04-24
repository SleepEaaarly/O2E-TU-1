import json

import requests
from core.api.zhitu_utils import get_expertInfo_by_expertId, search_expertID_by_paperID
import torch
from django.db.models import Avg
from django.http import HttpRequest
from django.views.decorators.http import require_GET, require_POST
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)
from core.models.papers import Papers
from core.models.need import Need
from core.models.user import User
from core.models.results import Results
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from core.api.auth import getUserInfo
from django.core.exceptions import ObjectDoesNotExist
from core.api.auth import jwt_auth
from core.models.ai_report import AIReport
from core.models.enterprise_info import Enterprise_info
from core.models.system_chat import SystemChatroom
from core.api._platform.utils import get_now_time
from core.models.card_message import CardMessage

""" 调用chatGPT生成需求报告

    路径：
        api/need_report/generate
    
    请求方法：
        POST
        
    请求参数:
        - id: 需求id
    
    返回参数:
        - 无
"""
def generate_requirement_report(need_id):
    try:
        need = Need.objects.get(id=need_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Requirement ID.")

    # 形成询问prompt
    demand1 = "请将以下的企业需求转化成一份详细的需求报告，包括功能点的划分，每个功能点的形式化表述、详细描述以及其参考技术路线。"
    require_title = "该需求的标题为"+need.title+", "
    require_description = "该需求的描述为"+need.description+", "
    require_keywords = "请同时考虑该需求的关键字"+need.key_word+", "
    require_field = "以及该需求涉及的领域"+need.field+"。"
    format = "报告采用markdown格式，设三级标题。对于每个功能点，形式化表述、详细描述和参考技术路线，请分条叙述。"
    demand2 = "报告首先有一个总标题，但是不用写引言、不用写总结、不用写参考文献。总字数不超过2000字，请对内容进行精炼。"
    msg = demand1+require_title+require_description + \
        require_keywords+require_field+format+demand2

    # 整合请求体
    url = f"https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer $OPEN_API_KEY"}
    sent_data = []
    sent_data['model'] = "gpt-3.5-turbo"
    sent_data['message'] = {"role": "user", "content": msg.encode("utf-8")}
    sent_data['temperature'] = 0.7
    response = requests.post(url, headers=headers, data=sent_data)

    # 存储生成报告
    newAIReport = AIReport(type=AIReport.TO_EXPERT, involved_id=need_id,
                           content=response.content.decode('utf-8'))
    newAIReport.save()


""" 调用chatGPT生成成果报告

    路径：
        api/work_report/submit
    
    请求方法：
        POST
        
    请求参数:
        - id: 成果id
    
    返回参数:
        - 无
"""
def generate_result_report(result_id):
    try:
        result = Results.objects.get(id=result_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Result ID.")

    # 形成询问prompt
    demand1 = "请将以下的专家成果转化成一份详细的成果报告，旨在给出该成果不包含具体学科领域知识的通俗形象的解释，使企业人员能够看懂该成果。"
    result_title = "该成果的标题为"+result.title+", "
    result_description = "该成果的描述为"+result.content+", "
    result_field = "请同时考虑该成果的领域"+result.field+"。 "
    format = "报告采用markdown格式，最多设三级标题。请分条叙述。"
    demand2 = "报告首先有一个总标题，但是不用写引言、不用写总结、不用写参考文献。总字数不超过2000字，请对内容进行精炼。"
    msg = demand1+result_title+result_description + \
        result_field+format+demand2

    # 整合请求体
    url = f"https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer $OPEN_API_KEY"}
    sent_data = []
    sent_data['model'] = "gpt-3.5-turbo"
    sent_data['message'] = {"role": "user", "content": msg.encode("utf-8")}
    sent_data['temperature'] = 0.7
    response = requests.post(url, headers=headers, data=sent_data)

    # 存储生成报告
    newAIReport = AIReport(type=AIReport.TO_ENTERPRISE,
                           involved_id=result_id, content=response.content.decode('utf-8'))
    newAIReport.save()


""" 获取需求报告

    路径：
        api/need_report/get
    
    请求方法：
        GET
        
    请求参数:
        - id: int, 需求id
    
    返回参数:
        - content: str, 需求报告内容
"""


@jwt_auth()
@require_GET
@response_wrapper
def get_requirement_report(request: HttpRequest):
    data = request.GET.dict()
    need_id = data.get('id')
    try:
        ret_report = AIReport.objects.get(
            involved_id=need_id, type=AIReport.TO_EXPERT)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Need ID.")
    requirement: Need = Need.objects.get(id=need_id)
    company: User = Need.objects.get(id=need_id).enterprise
    companyInfo = {}
    companyInfo['companyId'] = company.id
    companyInfo['companyName'] = company.enterprise_info.name
    companyInfo['companyAddress'] = company.enterprise_info.address
    companyInfo['companyLogoPath'] = company.icon.path
    companyInfo['companyArea'] = company.enterprise_info.address
    requireInfo = {}
    requireInfo['requireId'] = requirement.id
    requireInfo['requireName'] = requirement.title
    requireInfo['requireIntro'] = requirement.description
    requireInfo['requireKeywords'] = requirement.key_word
    return success_api_response({"content": ret_report.content,
                                 "companyInfo": companyInfo,
                                 "requireInfo": requireInfo,
                                 })


""" 获取成果报告

    路径：
        api/work_report/get
    
    请求方法：
        GET
        
    请求参数:
        - id: int, 成果id
    
    返回参数:
        - content: str, 成果报告内容
"""


@jwt_auth()
@require_GET
@response_wrapper
def get_result_report(request: HttpRequest):
    data = request.GET.dict()
    result_id = data.get('id')
    try:
        ret_report = AIReport.objects.get(
            involved_id=result_id, type=AIReport.TO_ENTERPRISE)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Result ID.")
    involved_result = Results.objects.filter(id=result_id).first()
    expert_id = involved_result.expert_results.filter(
        results_id=result_id).first().expert_id
    expert: User = User.objects.get(id=expert_id)
    expertInfo = {}
    expertInfo['expertId'] = expert.id
    expertInfo['expertName'] = expert.username
    expertInfo['expertTitle'] = expert.expert_info.title
    expertInfo['expertOrganization'] = expert.institution
    expertInfo['expertLogoPath'] = expert.icon.path
    expertInfo['expertEmail'] = expert.email
    workInfo = {}
    workInfo['workId'] = involved_result.id
    workInfo['workName'] = involved_result.title
    workInfo['workAbstruct'] = involved_result.abstract
    workInfo['workPic'] = involved_result.picture
    workInfo['workPeriod'] = involved_result.period
    workInfo['workField'] = involved_result.field
    return success_api_response({"content": ret_report.content,
                                 "workInfo": workInfo,
                                 "expertInfo": expertInfo,
                                 })

"""发送成果报告的卡片，插入到用户-平台聊天中

    路径：
        api/work_report/generateCard
    
    请求方法：
        POST
        
    请求参数:
        - id: int, 成果id
        - uId: int, 用户id
    
    返回参数:
        - 无
"""
@jwt_auth()
@require_POST
@response_wrapper
def generate_result_report_card(request: HttpRequest):
    data = parse_data(request)
    user_id = data.get('uId')
    result_id = data.get('id')
    try:
        owner = User.objects.get(id=user_id)
        involved_report = AIReport.objects.get(
            involved_id=result_id, type=AIReport.TO_ENTERPRISE)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Result ID or bad user id.")
    system_chatroom: SystemChatroom = None
    if owner.system_chatroom_list.all().exists():
        system_chatroom = owner.system_chatroom_list.get().id
    else:
        system_chatroom = SystemChatroom(owner=owner, isai=SystemChatroom.MANUAL_REPLY,
                                         last_message_time=get_now_time(), unread_message_num=0)
        system_chatroom.save()
    new_card_message_id = CardMessage.new_message(owner=owner, is_to_system=0, content=involved_report.content,
                                                  type=CardMessage.ENTERPRISE)
    system_chatroom.add_message(new_card_message_id)
    return success_api_response()
    

"""发送需求报告的卡片，插入到用户-平台聊天中

    路径：
        api/need_report/generateCard
    
    请求方法：
        POST
        
    请求参数:
        - id: int, 成果id
        - uId: int, 需求id
    
    返回参数:
        - 无
"""
@jwt_auth()
@require_POST
@response_wrapper
def generate_requirement_report_card(request: HttpRequest):
    data: dict = parse_data(request)
    user_id = data.get('uId')
    requirement_id = data.get('id')
    print(user_id, requirement_id)
    try:
        owner = User.objects.get(id=user_id)
        print(owner)
        involved_report = AIReport.objects.get(
            involved_id=requirement_id, type=AIReport.TO_EXPERT)
        print(involved_report)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Requirement ID or bad user id.")
    system_chatroom: SystemChatroom = None
    if owner.system_chatroom_list.all().exists():
        system_chatroom = owner.system_chatroom_list.get(owner_id=user_id)
    else:
        system_chatroom = SystemChatroom(owner=owner, isai=SystemChatroom.MANUAL_REPLY,
                                         last_message_time=get_now_time(), unread_message_num=0)
        system_chatroom.save()
    print("system_chatroom",system_chatroom)
    involved_need:Need = Need.objects.get(id=requirement_id)
    print("need", involved_need)
    new_card_message_id = CardMessage.new_card_message(owner=owner, is_to_system=0, content=involved_report.content,
                                                  title=involved_need.title,card_type=2,avatar="",involved_id=requirement_id)
    print("card_message_id", new_card_message_id)
    t=system_chatroom.add_message(new_card_message_id)
    print(t)
    return success_api_response({})
    
    