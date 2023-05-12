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
        milvus_delete("O2E_RESULT_HIT", result.vector_hit)
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
    title = data.get('title')
    page = int(data.get('page'))
    results = Results.objects.filter(Q(title__icontains=title))

    start = 10 * (page - 1)
    end = 10 * page

    d = list()
    for rst in results:
        d.append(rst.to_dict())
    return success_api_response({
        "page_num": page,
        "data": d
    })


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def search_user_by_name(request: HttpRequest):
    data: dict = request.POST
    username = data.get('username')
    page = int(data.get('page'))
    users = User.objects.filter(Q(username__icontains=username))

    start = 10 * (page - 1)
    end = 10 * page

    d = list()
    for user in users:
        d.append(user.to_dict())
    return success_api_response({
        "page_num": page,
        "user_data": d
    })


def create_a_user(username, password, email):
    print("create_user:" + password)
    user = User.objects.create_user(username=username, email=email, password=password, is_confirmed=True)
    try:
        avatar = get_avatar(email)
        print(BASE_DIR)
        with open(BASE_DIR + "/static/" + "images/default/icons/" + username + ".jpg", 'wb') as f:
            f.write(avatar.content)
        user.icon = 'images/default/icons/' + username + ".jpg"
    except Exception:
        print("error")
    user.save()
    return user


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def add_user(request: HttpRequest):
    data: dict = request.POST
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    user = create_a_user(username, password, email)
    return success_api_response({'id': user.id})


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def add_expert(request: HttpRequest):
    data: dict = request.POST
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    print('add_expert:password' + password)
    user = create_a_user(username, password, email)
    print(user.password)
    name = data.get('name')
    organization = data.get('organization')
    ID_num = data.get('ID_num')
    expert = Expert.objects.create(name=name, organization=organization, ID_num=ID_num)
    expert.save()
    user.state = 4
    user.expert_info = expert
    user.save()
    return success_api_response({'user_id': user.id, 'expert_id': expert.id})


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def add_enterprise(request: HttpRequest):
    data: dict = request.POST
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    user = create_a_user(username, password, email)
    name = data.get('name')
    address = data.get('address')
    enterprise = Enterprise_info.objects.create(name=name, address=address)
    enterprise.save()
    enterprise_id = enterprise.id
    user.enterprise_info = enterprise
    user.state = 5
    user.save()
    return success_api_response({'user_id': user.id, 'enterprise_id': enterprise_id})


@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def set_result(request: HttpRequest):
    title = request.POST.get('title')
    abstract = request.POST.get('abstract')
    pyear = request.POST.get('pyear').split('-')[0]
    field = request.POST.get('field')
    period = request.POST.get('period')
    id = request.POST.get('id')
    content = request.POST.get('content')
    picture = request.FILES.get("picture")

    multipic = request.FILES.getlist('multipic')
    result = Results.objects.get(pk=id)
    rst_pic_delete(result)
    all_multipic = ResMultipic.objects.all()
    res_multipic = result.multipic.all()
    result.multipic.remove(*all_multipic)
    for pic in res_multipic:
        multipic_delete(pic)
    res_multipic.delete()

    result.save()
    result.title = title
    result.abstract = abstract
    result.pyear = pyear
    result.field = field
    result.period = period
    result.content = content

    result.picture = picture

    for p in multipic:
        a = ResMultipic(picture=p)
        a.save()
        result.multipic.add(a)

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
