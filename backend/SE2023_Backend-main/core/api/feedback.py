from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.models.feedback import Feedback
from core.models.user import User

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_http_methods('GET')
def get_user_replied_feedback(request: HttpRequest, id: int):
    try:
        user = User.objects.get(id=id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    feedbacks_list = []

    feedbacks = user.user_feedback.filter(flag=1)
    for feedback in feedbacks:
        data = {
            "feedback_id": feedback.id,
            "user_id": feedback.user.id,
            "name": feedback.name,
            "email": feedback.email,
            "sex": get_sex(feedback.sex),
            "qtype": get_type(feedback.qtype),
            "description": feedback.description,
            "datatime": str(feedback.dataTime).split(' ')[0],
            "flag": feedback.flag,
            "message": feedback.message,
        }
        feedbacks_list.append(data)
    return success_api_response({"data": feedbacks_list})


@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_http_methods('GET')
def get_user_unreplied_feedback(request: HttpRequest, id: int):
    try:
        user = User.objects.get(id=id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")

    feedbacks_list = []
    feedbacks = user.user_feedback.filter(flag=0)
    for feedback in feedbacks:
        data = {
            "feedback_id": feedback.id,
            "user_id": feedback.user.id,
            "name": feedback.name,
            "email": feedback.email,
            "sex": get_sex(feedback.sex),
            "qtype": get_type(feedback.qtype),
            "description": feedback.description,
            "datatime": str(feedback.dataTime).split(' ')[0],
            "flag": feedback.flag,
            "message": feedback.message,
        }
        feedbacks_list.append(data)
    return success_api_response({"data": feedbacks_list})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_http_methods('POST')
def reply_feedback(request: HttpRequest):
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "data is none")
    id = data.get("feedback_id")
    message = data.get("message")
    print(id, message)
    try:
        feedback = Feedback.objects.get(id=id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist feedback")
    
    if feedback.flag == 1:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "feedback has already existed")
    
    feedback.flag = 1
    feedback.message = message
    feedback.save()
    return success_api_response({})



@csrf_exempt
@response_wrapper
#@jwt_auth()
@require_http_methods('GET')
def get_feedback(request:HttpRequest):
    feedbacks = Feedback.objects.all()
    datas = []
    for feedback in feedbacks:
        data = {
            "feedback_id": feedback.id,
            "user_id": feedback.user.id,
            "name": feedback.name,
            "email": feedback.email,
            "sex": get_sex(feedback.sex),
            "qtype": get_type(feedback.qtype),
            "description": feedback.description,
            "datatime": str(feedback.dataTime).split(' ')[0],
            "flag": feedback.flag,
            "message": feedback.message,
        }
        datas.append(data)
    return success_api_response({"data": datas})


def get_sex(sex):
    if sex == 0:
        return "男"
    elif sex == 1:
        return "女"
    else:
        return "未知"


def get_type(qtype):

    dic = {
        0: "订单相关",
        1: "支付相关",
        2: "账号相关",
        3: "安全相关",
        4: "反馈建议",
        5: "其他"
    }

    types = list(qtype)
    print(types)
    ans = []
    i = 0
    while i < 6:
        if types[i] == '1':
            ans.append(dic[i])
        i += 1
    return ans

@csrf_exempt
@response_wrapper
#@jwt_auth()
@require_http_methods('POST')
def make_feedback(request:HttpRequest):
    """
    name = request.GET.get("name")
    email = request.GET.get("email")
    sex = request.GET.get("sex")
    qtype_temp = request.GET.get("qtype")
    qtype = get_qtype(qtype_temp)
    description = request.GET.get("description")
    feedback = Feedback()
    feedback.name = name
    feedback.email = email
    feedback.sex = sex
    feedback.qtype = qtype
    feedback.description = description
    feedback.save()
    """
    data: dict = parse_data(request)
    name = data["name"]
    email = data["email"]
    user_id = data["id"]

    try:
        user = User.objects.get(id=user_id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")

    sex = data["sex"]
    qtype_temp = data["qtype"]
    qtype = get_qtype(qtype_temp)
    description = data["description"]
    feedback = Feedback()
    feedback.name = name
    feedback.email = email
    feedback.sex = sex
    feedback.qtype = qtype
    feedback.description = description
    feedback.user = user
    feedback.save()
    return success_api_response("success")


def get_qtype(qtype_temp):
    l = ['0', '0', '0', '0', '0', '0']
    for qtype in qtype_temp:
        l[qtype] = '1'
    return ''.join(l)
