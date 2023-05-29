"""
utils for generating api responses
"""
import json
import traceback
import numpy as np
from enum import Enum, unique

from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods

from pygtrans import Translate

from django.views.decorators.csrf import csrf_exempt


@unique
class ErrorCode(Enum):
    """
    api error code enumeration
    """
    SUCCESS = 200
    INVALID_REQUEST_ARGS = 400
    UNAUTHORIZED = 401
    REFUSE_ACCESS = 403
    WRONG_CONFIRM_CODE = 402
    ITEM_ALREADY_EXISTS = 409
    SERVER_ERROR = 500
    FIVE_ZERO_ONE = 501


def _api_response(success, data) -> dict:
    """
    wrap an api response dict obj
    :param success: whether the request is handled successfully
    :param data: requested data
    :return: a dictionary object, like {'success': success, 'data': data}
    """
    return {'success': success, 'data': data}


def failed_api_response(code, error_msg=None) -> dict:
    """
    wrap an failed response dict obj
    :param code: error code, refers to ErrorCode, can be an integer or a str (error name)
    :param error_msg: external error information
    :return: an api response dictionary
    """
    code = ErrorCode(code)

    if error_msg is None:
        error_msg = str(code)
    else:
        error_msg = str(code) + ': ' + error_msg

    status_code = code.value
    return _api_response(
        success=False,
        data={
            'code': status_code,
            'error_msg': error_msg
        })


def success_api_response(data) -> dict:
    """
    wrap a success response dict obj
    :param data: requested data
    :return: an api response dictionary
    """
    return _api_response(True, data)


def response_wrapper(func):
    """
    decorate a given api-function, parse its return value from a dict to a HttpResponse
    :param func: a api-function
    :return: wrapped function
    """

    def _inner(*args, **kwargs):
        _response = func(*args, **kwargs)
        if isinstance(_response, dict):
            if _response['success']:
                _response = JsonResponse(_response['data'], safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                status_code = _response.get("data").get("code")
                _response = JsonResponse(_response['data'])
                _response.status_code = status_code
        return _response

    return _inner


def wrapped_api(api_dict: dict):
    """
    wrap apis together with 4 methods(get/post/put/delete)
    :param api_dict: dict as {'get': get_api, 'post': post_api ...}
    :return: a api
    """
    assert isinstance(api_dict, dict)
    api_dict = {k.upper(): v for k, v in api_dict.items()}
    assert set(api_dict.keys()).issubset(['GET', 'POST', 'PUT', 'DELETE'])

    @csrf_exempt
    @require_http_methods(api_dict.keys())
    def _api(request, *args, **kwargs):
        print("wrapped api")
        return api_dict[request.method](request, *args, **kwargs)

    return _api


def parse_data(request: HttpRequest):
    """Parse request body and generate python dict

    Args:
        request (HttpRequest): all http request

    Returns:
        | request body is malformed = None
        | otherwise                 = python dict
    """
    try:
        return json.loads(request.body.decode())
    except json.JSONDecodeError:
        return None


def read_json_data(path):
    """
    :param path: 文件路径
    :return: 获取的数据
    """
    try:
        # path = complete_path(path)
        with open(file=path, mode="r", encoding="utf8") as f:
            return json.load(f)
    except Exception as e:
        print(traceback.format_exc())
        print(e)
    return None


def trans_zh2en(sent):
    print("enter trans_zh2en")
    client = Translate()
    ans = ""
    print("initiate translate")
    lan = client.detect(sent)
    # print(lan.language)
    if lan is None:
        return sent
    if lan.language == 'en':
        ans = sent
    else:
        ans = client.translate(sent, target='en').translatedText
    return ans


def cos_simi(x,y):
   num = x.dot(y.T)
   denom = np.linalg.norm(x) * np.linalg.norm(y)
   return num / denom