from core.models.expert import Expert
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.api.auth import jwt_auth, getUserInfo
from core.models.user import User
import json
import requests
import os
import demjson
from core.models.papers import Papers
from core.models.projects import Projects
from core.models.patents import Patents

@response_wrapper
# @jwt_auth
@require_http_methods("GET")
def get_expert_info(request: HttpRequest, uid: int):
    
    try:
        user: User = User.objects.get(id=uid)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")

    if user.state != 4:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist expert")

    data = request.GET.dict()
    tab = data.get('tab')

    # https://github.com/imingx?tab=repositories

    if not tab:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non tab")

    if tab == "papers":
        papers = user.expert_info.papers.all()
        res = []    
        for paper in papers:
            res.append(paper.to_dict())
        return success_api_response({"data": res})
    elif tab == "projects":
        projects = user.expert_info.projects.all()
        res = []
        for project in projects:
            res.append(project.to_dict())
        return success_api_response({"data": res})
    elif tab == "patents":
        patents = user.expert_info.patents.all()
        res = []
        for patent in patents:
            res.append(patent.to_dict())
        return success_api_response({"data": res})
    elif tab == "results":
        results = user.expert_info.results.all()
        res = []
        for result in results:
            res.append(result.to_dict())
        return success_api_response({"data": res})
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not a useful tab")
    

    

@response_wrapper
@require_http_methods('POST')
def setinfo(request:HttpRequest):
    id = request.POST.get("id", None)
    if not id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid id")
    name = request.POST.get("name", None)
    if not name:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid name")
    paper = request.POST.get("paper", None)
    patent = request.POST.get("patent", None)
    if not patent and not paper:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need at least one paper or patent")
    organization = request.POST.get("organization", None)
    if not organization:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid organization")
    field = request.POST.get("field", None)
    if not field:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid field")
    ID_num = request.POST.get("ID_num", None)
    if not ID_num:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid ID_num")
    scholar_ID = request.FILES.get("scholar_ID", None)
    scholar_profile = request.POST.get("scholar_profile", None)
    if not scholar_profile:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid scholar_profile")
    phone = request.POST.get("phone", None)
    if not phone:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid phone")
    user = User.objects.get(id=id)
    if user.expert_info is not None:
        expert = user.expert_info
        expert.name = name
        expert.organization = organization
        expert.field = field
        expert.ID_num = ID_num
        expert.ID_pic = scholar_ID
        expert.self_profile = scholar_profile
        expert.phone = phone
        expert.patent = patent
        expert.paper = paper
        expert.save()
        user.state = 1
        user.save()
    else:
        expert = Expert()
        expert.name = name
        expert.organization = organization
        expert.field = field
        expert.ID_num = ID_num
        expert.ID_pic = scholar_ID
        expert.self_profile = scholar_profile
        expert.phone = phone
        expert.patent = patent
        expert.paper = paper
        expert.save()
        user.expert_info = expert
        user.state = 1
        user.save()
    return success_api_response("correct")


"""
应该添加一个认证成功提示
"""
#@jwt_auth()
@response_wrapper
@require_http_methods('GET')
def agree_expert(request:HttpRequest, id:int):
    data = request.GET.dict()
    scholarID = data.get('scholarID')
    url = data.get('url')
    print(scholarID)
    print(url)
    print(id)
    user = User.objects.get(id=id)
    if user.state != 1:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid user state")
    user.state = 4
    expert_info = user.expert_info
    expert_info.scholarID = scholarID
    expert_info.url = url
    expert_info.save()
    user.save()
    return success_api_response("success")


"""
应该添加一个认证失败提示
对于专家信息的删除可能有bug，这里需要测试一下
"""
#@jwt_auth()
@response_wrapper
@require_http_methods('GET')
def refuse_expert(request:HttpRequest, id:int):
    print(0)
    user = User.objects.get(id=id)
    print(1)
    if user.state != 1:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid user state")
    user.state = 0
    user.save()
    print(4)
    return success_api_response("success")


"""
通过id获得相应用户申请成为企业的信息
"""
#@jwt_auth()
@response_wrapper
@require_http_methods('GET')
def get_expertInfo(request:HttpRequest, id:int):
    user = User.objects.get(id=id)
    if user.state != 1:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid user state")
    expert_info = user.expert_info
    return success_api_response({
        "name": expert_info.name,
        "ID_num": expert_info.ID_num,
        "organization": expert_info.organization,
        "field": field_decode(expert_info.field),
        "self_profile": expert_info.self_profile,
        "phone": expert_info.phone,
        "ID_pic": str(expert_info.ID_pic),
        "paper": expert_info.paper,
        "patent": expert_info.patent
    })

"""
获取全部申请专家的用户基本信息
"""
#@jwt_auth()
@response_wrapper
@require_http_methods('GET')
def get_all_expert(request:HttpRequest):
    users = User.objects.filter(state=1)
    data = list()
    for user in users:
        if user.is_superuser != 1:
            dic = getUserInfo(user)
            dic['profile'] = user.expert_info.self_profile
            dic['create_time'] = user.expert_info.create_time
            data.append(dic)
    return success_api_response(data)


def field_decode(field):
    ans = []
    dic = {
        0: '信息技术',
        1: '装备制造',
        2: '新材料',
        3: '新能源',
        4: '节能环保',
        5: '生物医药',
        6: '科学创意',
        7: '检验检测',
        8: '其他'
    }
    i = 0
    while i < 9:
        if field[i] == '1':
            print(dic[i])
            ans.append(dic[i])
        i = i + 1
    return ans




"""
以下为更新数据库所用的api
"""
@response_wrapper
@require_http_methods('GET')
def get_json(request:HttpRequest):
    f = open("computer_paper.txt",'rb')
    num = 0
    while num < 50:
        line = f.readline()[:-1].decode('utf-8')
        num += 1
        dic = demjson.decode(line)
        add_expert(dic)
    f.close()
    return success_api_response("success")



name_num = 0
password_num = 0
email_num = 0
def add_expert(dic):
    global name_num
    global  password_num
    global email_num
    #dic = {'id': '3733221342', 'title': 'Nonlinear Modeling Method Based on RBF Neural Network Trained by AFSA with Adaptive Adjustment', 'keywords': ['Radial basis function', 'Neural network', 'Artificial fish swarm algorithm', 'Nonlinear function']}
    id = dic['id']
    url = "https://zhitulist.com/zhitu-data-service/search/paper?id="+id
    response = requests.get(url)
    dic = json.loads(response.text)["data"]
    op = True
    if dic is not None and dic.__contains__("scholars"):
        scholars = dic["scholars"]
        for scholar in scholars:
            scholarId = scholar['scholarId']
            users = User.objects.all()
            for user in users:
                if user.expert_info is not None and int(scholarId) == int(user.expert_info.scholarID):
                    op = False
                    break
            if op is False:
                op = True
                continue
            name_num += 1
            password_num += 1
            email_num += 1

            #new_user = User()
            #new_user.username = "expert"+str(name_num)
            #new_user.password = "200145"+str(password_num)
            #new_user.email = "expert"+str(email_num)+"@163.com"
            #new_user.is_confirmed = True

            new_user = User.objects.create_user(
                username="expert" + str(name_num), password="123456", email=("expert" + str(email_num) + "@163.com"),
                is_confirmed=True)
            new_user.save()

            expert_info = Expert()
            expert_info.scholarID = scholarId
            url1 = "https://zhitulist.com/zhitu-data-service/search/scholar?id="+str(scholarId)
            response = requests.get(url1)
            dic1 = json.loads(response.text)["data"]
            if dic1 is not None and dic1.__contains__("scholarName"):
                expert_info.name = dic1["scholarName"]
            if dic1 is not None and dic1.__contains__("org"):
                expert_info.organization = dic1["org"]
            if dic1 is not None and dic1.__contains__("url"):
                expert_info.url = dic1["url"]
            if dic1 is not None and dic1.__contains__("info"):
                expert_info.self_profile = dic1["info"]
            if dic1 is not None and dic1.__contains__("phone"):
                expert_info.phone = dic1["phone"]
            if dic1 is not None and dic1.__contains__("title"):
                expert_info.title = dic1["title"]
            expert_info.save()
            new_user.save()
            new_user.state = 5
            new_user.expert_info = expert_info
            new_user.save()

@response_wrapper
@require_http_methods('GET')
def add_papers(request:HttpRequest):
    experts = Expert.objects.all()
    for expert in experts:
        if expert.scholarID is not None:
            url = "https://zhitulist.com/zhitu-data-service/search/scholar?id="+expert.scholarID
            response = requests.get(url)
            dic = json.loads(response.text)["data"]
            papers = dic["papers"]["content"]
            for paper in papers:
                op = True
                ps = Papers.objects.all()
                for p in ps:
                    if p.title == paper['title']:
                        expert.papers.add(p)
                        expert.save()
                        op = False
                        break

                if op:
                    p = Papers()
                    p.title = paper["title"]
                    p.cites = paper["cites"]
                    p.isEI = paper['isEI']
                    p.isSCI = paper['isSCI']
                    p.pyear = paper['pyear']
                    p.url = paper['url']
                    p.save()
                    expert.papers.add(p)
                    expert.save()


    return success_api_response("success")


@response_wrapper
@require_http_methods('GET')
def add_patents(request:HttpRequest):
    experts = Expert.objects.all()
    for expert in experts:
        if expert.scholarID is not None:
            url = "https://zhitulist.com/zhitu-data-service/search/scholar?id=" + expert.scholarID
            response = requests.get(url)
            dic = json.loads(response.text)["data"]
            patents = dic["patents"]["content"]
            if patents != None:
                for patent in patents:
                    op = True
                    ps = Patents.objects.all()
                    for p in ps:
                        if p.title == patent['title']:
                            expert.patents.add(p)
                            expert.save()
                            op = False
                            break

                    if op:
                        p = Patents()
                        p.title = patent["title"]
                        p.pyear = patent['pyear']
                        p.url = patent['url']
                        p.save()
                        expert.patents.add(p)
                        expert.save()

    return success_api_response("success")


@response_wrapper
@require_http_methods('GET')
def add_projects(request:HttpRequest):
    experts = Expert.objects.all()
    for expert in experts:
        if expert.scholarID is not None:
            url = "https://zhitulist.com/zhitu-data-service/search/scholar?id=" + expert.scholarID
            response = requests.get(url)
            dic = json.loads(response.text)["data"]
            projects = dic["projects"]["content"]
            if projects != None:
                for project in projects:
                    op = True
                    ps = Projects.objects.all()
                    for p in ps:
                        if p.title == project['title']:
                            expert.projects.add(p)
                            expert.save()
                            op = False
                            break

                    if op:
                        p = Projects()
                        p.title = project["title"]
                        p.startYear = project['startYear']
                        p.endYear = project['endYear']
                        p.typeFirst = project['typeFirst']
                        p.typeSecond = project['typeSecond']
                        p.typeThird = project['typeThird']
                        p.url = project['url']
                        p.save()
                        expert.projects.add(p)
                        expert.save()

    return success_api_response("success")


@response_wrapper
@require_http_methods('GET')
def add_patents_scholars(request:HttpRequest):
    patents = Patents.objects.all()
    for patent in patents:
        url = patent.url
        patent_id = url[28:]
        url = "https://zhitulist.com/zhitu-data-service/search/patent?id="+patent_id
        response = requests.get(url)
        dic = json.loads(response.text)["data"]
        scholars = dic["scholars"]
        s = ""
        if scholars != None:
            for scholar in scholars:
                s = s + scholar["scholarName"] + ","
        patent.scholars = s[:-1]
        patent.save()
    return success_api_response("success")


@response_wrapper
@require_http_methods('GET')
def add_papers_scholars(request:HttpRequest):
    papers = Papers.objects.all()
    for paper in papers:
        url = paper.url
        paper_id = url[27:]
        url = "https://zhitulist.com/zhitu-data-service/search/paper?id=" + paper_id
        response = requests.get(url)
        dic = json.loads(response.text)["data"]
        scholars = dic["scholars"]
        s = ""
        if scholars != None:
            for scholar in scholars:
                s = s + scholar["scholarName"] + ","
            paper.scholars = s[:-1]
            paper.save()
    return success_api_response("success")


@response_wrapper
@require_http_methods('GET')
def add_projects_scholars(request:HttpRequest):
    projects = Projects.objects.all()
    for project in projects:
        experts = project.expert_projects.all()
        expert = experts[0]
        project.scholars = expert.name
        project.save()
    return success_api_response("success")
