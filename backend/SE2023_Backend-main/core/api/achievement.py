from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)

from core.models import Papers, Patents, Projects, User, Expert, Results, ResMultipic
from core.api.ai_report import generate_result_report
from core.api.milvus_utils import milvus_insert, get_milvus_connection, disconnect_milvus, milvus_confirm_item_exist
from core.api.ai_chat import get_hitbert_embedding
from core.api.ai_recommend import get_scibert_embedding
from core.api.utils import trans_zh2en
from django.views.decorators.csrf import csrf_exempt

'''
    add paper
    [method]: POST
    [route]: /api/paper/add
    
    params:
        - title
        - cites
        - pyear
        - isEI
        - isSCI
        - url
        - scholars
    
    return 
        - OK
'''

@csrf_exempt
@jwt_auth()
@require_POST
@response_wrapper
def add_paper(request: HttpRequest):
    # 审核过程 TODO
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "Invalid request args.")
    print(data)

    title = data.get('title')
    cites = data.get('cites')
    pyear = data.get('pyear').split('-')[0]
    isEI = data.get('isEI')
    isSCI = data.get('isSCI')
    url = data.get('url')
    scholars = data.get('scholars')
    id = data.get('id')

    paper = Papers(title=title, cites=cites, pyear=pyear, isEI=isEI, isSCI=isSCI,
                   url=url, scholars=scholars)
    paper.save()

    user = User.objects.get(id=id)
    expert_id = user.expert_info_id

    expert = Expert.objects.get(id=expert_id)
    expert.papers.add(paper)
    expert.save()

    return success_api_response({})


'''
    add patent
    [method]: POST
    [route]: /api/patent/add
    
    params:
        - title
        - pyear
        - url
        - scholars
    
    return 
        - OK
'''

@csrf_exempt
@jwt_auth()
@require_POST
@response_wrapper
def add_patent(request: HttpRequest):
    # 审核过程 TODO
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "Invalid request args.")
    print(data)

    title = data.get('title')
    pyear = data.get('pyear').split('-')[0]
    url = data.get('url')
    scholars = data.get('scholars')
    id = data.get('id')

    patent = Patents(title=title, pyear=pyear, url=url, scholars=scholars)
    patent.save()

    user = User.objects.get(id=id)
    expert_id = user.expert_info_id

    expert = Expert.objects.get(id=expert_id)
    expert.patents.add(patent)
    expert.save()

    return success_api_response({})


'''
    add project
    [method]: POST
    [route]: /api/project/add

    params:
        - title
        - start_year
        - end_year
        - type_first
        - type_second
        - type_third
        - url
        - scholars

    return 
        - OK
'''

@csrf_exempt
@jwt_auth()
@require_POST
@response_wrapper
def add_project(request: HttpRequest):
    # 审核过程 TODO
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "Invalid request args.")
    print(data)

    title = data.get('title')
    start_year = data.get('start_time').split('-')[0]
    end_year = data.get('end_time').split('-')[0]
    type_first = data.get('type_first', None)
    type_second = data.get('type_second', None)
    type_third = data.get('type_third', None)
    url = data.get('url')
    scholars = data.get('scholars')
    id = data.get('id')

    print("2")

    project = Projects(title=title, startYear=start_year, endYear=end_year, url=url, scholars=scholars,
                       typeFirst=type_first, typeSecond=type_second, typeThird=type_third)

    print("3")
    project.save()
    user = User.objects.get(id=id)
    expert_id = user.expert_info_id
    expert = Expert.objects.get(id=expert_id)
    expert.projects.add(project)
    expert.save()

    return success_api_response({})


@csrf_exempt
@require_POST
@response_wrapper
def add_result(request: HttpRequest):
    title = request.POST.get('title')
    abstract = request.POST.get('abstract')
    scholars = request.POST.get('scholars')
    pyear = request.POST.get('pyear').split('-')[0]
    field = request.POST.get('field')
    period = request.POST.get('period')
    id = request.POST.get('id')
    content = request.POST.get('content')
    picture = request.FILES.get("picture")

    multipic = request.FILES.getlist('multipic')

    result = Results(title=title, abstract=abstract, scholars=scholars, pyear=pyear, field=field,
                     period=period, picture=picture, content=content, state=0)

    print(multipic)

    result.save()

    for p in multipic:
        a = ResMultipic(picture=p)
        a.save()
        result.multipic.add(a)

    result.save()
    # print("4")
    user = User.objects.get(id=id)
    expert_id = user.expert_info_id
    expert = Expert.objects.get(id=expert_id)
    # print("5")
    # print(expert)
    expert.results.add(result)
    expert.save()
    # print("6")
    return success_api_response({})


"""
应该添加一个认证成功提示
"""
# @jwt_auth()

@csrf_exempt
@response_wrapper
@require_http_methods('GET')
def agree_result(request: HttpRequest, id: int):
    print(id)
    result = Results.objects.get(id=id)
    if result.state != 0:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid result state")
    result.state = 1
    title_en = trans_zh2en(result.title)
    result.title_eng = title_en
    # print('debug 1')
    hit_vec = get_hitbert_embedding(title_en)
    # print('debug 1.5')
    sci_vec = get_scibert_embedding(title_en)
    print('debug 2')

    get_milvus_connection()
    # mid_hit = milvus_confirm_item_exist("O2E_RESULT_HIT", "result_id", id)
    # if mid_hit < 0:
    #     mid_hit = milvus_insert("O2E_RESULT_HIT", data=[[hit_vec], [id]])[0]
        
    print('debug 2.5')
    mid_sci = milvus_confirm_item_exist("O2E_RESULT", "result_id", id)
    if mid_sci < 0:
        mid_sci = milvus_insert("O2E_RESULT", data=[[sci_vec], [id]])[0]
    print('debug 3')

    disconnect_milvus()
    result.vector_sci = mid_sci
    # result.vector_hit = mid_hit
    # print('debug 4')
    result.save()
    # 审核通过后将生成成果报告
    print(result.id)
    generate_result_report(result.id)
    # print('debug 5')
    return success_api_response("success")


"""
应该添加一个认证失败提示
"""
# @jwt_auth()

@csrf_exempt
@response_wrapper
@require_http_methods('GET')
def refuse_result(request: HttpRequest, id: int):
    result = Results.objects.get(id=id)
    print(1)
    if result.state != 0:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid result state")
    result.state = 2
    result.save()
    print(4)
    return success_api_response("success")


# @jwt_auth()
@csrf_exempt
@response_wrapper
@require_GET
def get_resultInfo(request: HttpRequest, id: int):
    print('get result info')
    print(id)
    result = Results.objects.get(id=id)
    print(result)
    # if result.state != 1:
    #     return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid result state")
    print('debug 1')
    expert = Expert.objects.filter(results=id)[0]
    user = User.objects.get(expert_info=expert.id)

    multipic = result.multipic.all()

    m_list = []
    for m in multipic:
        m_list.append(m.get_pic())

    return success_api_response({
        "title": result.title,
        "abstract": result.abstract,
        "scholars": result.scholars,
        "pyear": result.pyear,
        "field": result.field,
        "period": result.period,
        "content": result.content,
        "state": result.state,
        "relate_expert_id": expert.id,
        "expert_name": expert.name,
        "expert_title": expert.title,
        "expert_organization": expert.organization,
        "expert_logo": user.get_icon(),
        "uid": user.id,
        "result_pic": result.get_pic(),
        "expert_email": user.email,
        "result_multipic": m_list,
    })
