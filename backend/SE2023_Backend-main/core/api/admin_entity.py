from django.http import HttpRequest

from .milvus_utils import get_milvus_connection, milvus_delete
from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.api.auth import jwt_auth
from django.views.decorators.http import require_http_methods
from core.models import User, Results
from django.db.models import Q


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


@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def delete_result(request: HttpRequest):
    data: dict = parse_data(request)
    pid = data.get('id')
    if Results.objects.filter(pk=pid).exists() is False:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, 'Your required result to delete is not found!')
    result = Results.objects.get(pk=pid)
    get_milvus_connection()
    milvus_delete("O2E_RESULT_HIT", result.vector_hit)
    milvus_delete("O2E_RESULT", result.vector_sci)
    result.delete()
    return success_api_response({"result": "Ok, all result info has been provided."})


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

