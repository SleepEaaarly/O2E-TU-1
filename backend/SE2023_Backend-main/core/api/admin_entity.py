from django.http import HttpRequest

from backend.settings import BASE_DIR
from .milvus_utils import get_milvus_connection, milvus_delete, disconnect_milvus
from .sign_up import get_avatar
from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.api.auth import jwt_auth
from django.views.decorators.http import require_http_methods
from core.models import User, Results, Expert, ResMultipic, Enterprise_info
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from core.models.results import rst_pic_delete, multipic_delete
from core.models.user import icon_delete
from core.api.ai_chat import get_hitbert_embedding
from urllib import parse
import time
import math


def check(email: str):
    import re
    print(11)
    pattern = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    print(10)
    if re.match(pattern, email):
        print(12)
        return True
    else:
        print(13)
        return False


def check1(email: str):
    if User.objects.filter(email=email).__len__() != 0:
        return False
    return True

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_http_methods('GET')
def get_all_unaudited_result_info(request: HttpRequest, page: int):
    start = 10 * (page - 1)
    end = 10 * page
    models = Results.objects.filter(state=0)
    page_num = models.__len__()
    models = models[start:end]
    data = list()
    for rst in models:
        data.append(rst.to_dict())
    return success_api_response({
        "page_num": page_num,
        "data": data,
    })

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_http_methods('GET')
def get_all_result_info(request: HttpRequest, page: int):
    start = 10 * (page - 1)
    end = 10 * page
    models = Results.objects.all()
    page_num = models.__len__()
    models = models[start:end]
    data = list()
    for rst in models:
        data.append(rst.to_dict())
    return success_api_response({
        "page_num": page_num,
        "data": data,
    })


# 测一下
@csrf_exempt
@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def delete_result(request: HttpRequest):
    data: dict = parse_data(request)
    pid = data.get('id')
    print("delete_result 1", pid)
    if Results.objects.filter(pk=pid).exists() is False:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, 'Your required result to delete is not found!')
    result = Results.objects.get(pk=pid)
    print("delete_result 2", result)
    if result.state == 1:
        get_milvus_connection()
        # milvus_delete("O2E_RESULT_HIT", result.vector_hit)
        milvus_delete("O2E_RESULT", result.vector_sci)
        disconnect_milvus()
    print("delete_result 3")
    experts = Expert.objects.all()
    pics = ResMultipic.objects.all()
    result.expert_results.remove(*experts)
    multipics = result.multipic.all()
    result.multipic.remove(*pics)
    for pic in multipics:
        multipic_delete(pic)
    print("delete_result 4")
    result.delete()
    print("delete_result 5")
    return success_api_response({"result": "Ok, all result info has been provided."})


@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_http_methods('POST')
def multi_pic_test(request: HttpRequest):
    print('1111')
    # pid = request.POST.get('id')
    data: dict = request.POST
    pid = data.get('id')
    result = Results.objects.get(pk=pid)

    for pic in result.multipic.all():
        print(pic)
    return success_api_response({})


@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_http_methods('POST')
def change_result_info(request: HttpRequest):
    data: dict = parse_data(request)
    pid = data.get('id')
    title = data.get('title')
    scholars = data.get('scholars')
    period = data.get('period')
    field = data.get('field')
    rst = Results.objects.filter(pk=pid).first()

    print(pid, title, scholars, period, field)

    rst.title = title
    rst.scholars = scholars
    rst.period = period
    rst.field = field

    rst.save()

    return success_api_response({"result": "Ok, the user info has been changed."})


'''
@response_wrapper
# @jwt_auth()
@require_http_methods('POST')
def change_result_info(request: HttpRequest):
    data: dict = parse_data(request)
    pid = data.get('id')
    title = data.get('title')
    scholars = data.get('scholars')
    period = data.get('period')
    field = data.get('field')
    pyear = data.get('pyear')
    content = data.get('content')
    state = data.get('state')
    abstract = data.get('abstract')

    rst = Results.objects.filter(pk=pid).first()

    print(pid, title, scholars, period, field)

    rst.title = title
    rst.scholars = scholars
    rst.period = period
    rst.field = field
    rst.pyear = pyear
    rst.content = content
    rst.state = state
    rst.abstract = abstract

    rst.save()

    return success_api_response({"result": "Ok, the user info has been changed."})

'''


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def search_result_by_name(request: HttpRequest):
    data = parse_data(request)
    title = parse.unquote(data.get('title'))
    print(title)
    page = int(data.get('page'))
    if title == '' or title is None:
        results = Results.objects.all()
    else:
        results = Results.objects.filter(Q(title__icontains=title))

    start = 10 * (page - 1)
    end = 10 * page
    d = list()
    for rst in results:
        d.append(rst.to_dict())
    d = d[start: end]
    return success_api_response({
        "page_num": math.ceil(results.__len__() / 10),
        "data": d
    })


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def search_user_by_name(request: HttpRequest):
    data: dict = parse_data(request)
    username = parse.unquote(data.get('username'))
    print(username)
    page = int(data.get('page'))
    if username == '' or username is None:
        users = User.objects.all()
    else:
        users = User.objects.filter(Q(username__icontains=username))
    start = 10 * (page - 1)
    end = 10 * page
    d = list()
    for user in users:
        d.append(user.to_dict())
        print(user.to_dict())
    d = d[start: end]
    return success_api_response({
        "page_num": math.ceil(users.__len__() / 10),
        "data": d
    })


def create_a_user(username, password, email):
    user = User.objects.create_user(username=username, email=email, password=password, is_confirmed=True)
    # try:
    #     avatar = get_avatar(email)
    #     print(BASE_DIR)
    #     with open(BASE_DIR + "/static/" + "images/default/icons/" + username + ".jpg", 'wb') as f:
    #         f.write(avatar.content)
    #     user.icon = 'images/default/icons/' + username + ".jpg"
    # except Exception:
    #     print("error")
    user.save()
    return user


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def add_user(request: HttpRequest):
    data: dict = parse_data(request)
    print(data)
    username = data.get('username')
    print(1)
    print(2)
    password = data.get('password')
    email = data.get('email')
    if check(str(email)) is False:
        print(3)
        return success_api_response({'code': 501, 'message': "邮箱格式错误"})
    print(3)
    try:
        user = create_a_user(username, password, email)
    except Exception:
        return success_api_response({'code': 410})
    
    return success_api_response({'id': user.id})


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def add_expert(request: HttpRequest):
    print(0)
    data: dict = parse_data(request)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if check(str(email)) is False:
        return success_api_response({'code': 501, 'message': "邮箱格式错误"})
    print('add_expert:password' + password)
    try:
        user = create_a_user(username, password, email)
    except Exception:
        return success_api_response({'code': 410})
    # print(user.password)
    print(1)
    name = data.get('name')
    organization = data.get('organization')
    ID_num = data.get('ID_num')
    print(2)
    expert = Expert.objects.create(name=name, organization=organization, ID_num=ID_num)
    print(3)
    expert.save()
    # # 插向量
    # get_milvus_connection()
    # vec = get_hitbert_embedding(name)
    # mid = milvus_confirm_item_exist("O2E_EXPERT_HIT", "expert_id", expert.id)
    # if mid < 0:
    #     mid = milvus_insert("O2E_EXPERT_HIT", data=[[vec], [expert.id]])[0]
    # disconnect_milvus()
    # expert.vector_hit = mid
    # expert.save()
    user.state = 4
    user.expert_info = expert
    print(4)
    user.save()
    return success_api_response({'user_id': user.id, 'expert_id': expert.id})


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def add_enterprise(request: HttpRequest):
    data: dict = parse_data(request)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if check(str(email)) is False:
        return success_api_response({'code': 501, 'message': "邮箱格式错误"})
    try:
        user = create_a_user(username, password, email)
    except Exception:
        return success_api_response({'code': 410})
    name = data.get('name')
    address = data.get('address')
    enterprise = Enterprise_info.objects.create(name=name, address=address)
    enterprise.save()
    enterprise_id = enterprise.id
    # # 插向量
    # get_milvus_connection()
    # vec = get_hitbert_embedding(name)
    # mid = milvus_confirm_item_exist("O2E_ENTERPRISE_HIT", "enterprise_id", enterprise.id)
    # if mid < 0:
    #     mid = milvus_insert("O2E_ENTERPRISE_HIT", data=[[vec], [enterprise.id]])[0]
    # disconnect_milvus()
    # enterprise.vector_hit = mid
    # enterprise.save()
    user.enterprise_info = enterprise
    user.state = 5
    user.save()
    return success_api_response({'user_id': user.id, 'enterprise_id': enterprise_id})


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def set_result(request: HttpRequest):
    print(request.POST)
    data: dict = parse_data(request)
    # print("data:")
    # print(data)
    # title = request.get('title')
    # abstract = request.POST.get('abstract')
    # pyear = request.POST.get('pyear').split('-')[0] if request.POST.get('pyear') else None
    # field = request.POST.get('field')
    # period = request.POST.get('period')
    # id = request.POST.get('id')
    # content = request.POST.get('content')
    title = data['title']
    abstract = data['abstract']
    pyear = data['pyear'].split('-')[0] if data['pyear'] else None
    field = data['field']
    period = data['period']
    id = data['id']
    content = data['content']
    # print(title, abstract, pyear, field, period, id, content)
    print(1)
    result = Results.objects.get(pk=id)
    print(result)

    # 改向量
    # if result.state == 1 and title != result.title:
    #     title_en = trans_zh2en(title)
    #     result.title_eng = title_en

    #     hit_vec = get_hitbert_embedding(title_en)
    #     sci_vec = get_scibert_embedding(title_en)

    #     get_milvus_connection()

    #     milvus_delete("O2E_RESULT_HIT", result.vector_hit)
    #     milvus_delete("O2E_RESULT", result.vector_sci)


    #     mid_hit = milvus_confirm_item_exist("O2E_RESULT_HIT", "result_id", id)
    #     while mid_hit >= 0:
    #         print("waiting vec_hit to be delete...")
    #         time.sleep(1)
    #         mid_hit = milvus_confirm_item_exist("O2E_RESULT_HIT", "result_id", id)
    #     mid_hit = milvus_insert("O2E_RESULT_HIT", data=[[hit_vec], [id]])[0]
        
    #     mid_sci = milvus_confirm_item_exist("O2E_RESULT", "result_id", id)
    #     while mid_sci >= 0:
    #         print("waiting vec_sci to be delete...")
    #         time.sleep(1)
    #         mid_sci = milvus_confirm_item_exist("O2E_RESULT", "result_id", id)
    #     mid_sci = milvus_insert("O2E_RESULT", data=[[sci_vec], [id]])[0]

    #     disconnect_milvus()

    #     result.vector_sci = mid_sci
    #     result.vector_hit = mid_hit

    result.title = title
    result.abstract = abstract
    result.pyear = pyear
    result.field = field
    result.period = period
    result.content = content

    result.save()
    return success_api_response({})


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def set_user(request: HttpRequest):
    id = request.POST.get('id')
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    if check(str(email)) is False:
        return success_api_response({'code': 501, 'message': "邮箱格式错误"})
    if check1(str(email)) is False:
        return success_api_response({'code': 501, 'message': "邮箱格式错误"})
    institution = request.POST.get('institution')
    # icon = request.FILES.get('icon')
    biography = request.POST.get('biography')

    user = User.objects.get(pk=id)
    icon_delete(user)
    user.username = username
    user.set_password(password)
    user.email = email
    user.institution = institution
    # user.icon = icon
    user.biogrpahy = biography

    user.save()
    return success_api_response({})


