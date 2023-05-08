from codecs import register_error
from core.models.enterprise_info import Enterprise_info
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest

from .ai_recommend import get_scibert_embedding
from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.api.auth import jwt_auth, getUserInfo
from core.models.user import User
from core.api.milvus_utils import milvus_insert, get_milvus_connection, disconnect_milvus
from django.views.decorators.csrf import csrf_exempt

#@jwt_auth()
@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def set_info(request:HttpRequest):
    id = request.POST.get("id", None)
    print(id)
    if not id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid id")
    name = request.POST.get('name', None)
    print(name)
    if not name:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid name")
    address = request.POST.get('address', None)
    print(address)
    if not address:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid address")
    website = request.POST.get("website", None)
    print(website)
    if not website:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid website")
    instruction = request.POST.get("instruction", None)
    print(instruction)
    if not instruction:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid instruction")
    phone = request.POST.get("phone", None)
    print(phone)
    if not phone:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid phone")
    legal_representative = request.POST.get("legal_representative", None)
    print(legal_representative)
    if not legal_representative:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid legal_representative")
    register_capital = request.POST.get("register_capital", None)

    try:
        register_capital = int(register_capital)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "包含非数字字符")   

    print(register_capital)
    if not register_capital:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid register_capital")
    field = request.POST.get("field", None)
    print(field)
    if not field:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid field")
    business_license = request.FILES.get("business_license", None)
    if not business_license:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid business_license")
    legal_person_ID = request.FILES.get("legal_person_ID", None)
    if not legal_person_ID:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid legal_person_ID")

    user = User.objects.get(id=id)
    name_vec = get_scibert_embedding(name)
    get_milvus_connection()
    mid = milvus_insert("O2E_ENTERPRISE_HIT", data=[[name_vec], [id]])
    disconnect_milvus()
    if user.enterprise_info is None:
        enterprise_info = Enterprise_info()
        enterprise_info.name = name
        enterprise_info.address = address
        enterprise_info.website = website
        enterprise_info.instruction = instruction
        enterprise_info.phone = phone
        enterprise_info.legal_representative = legal_representative
        enterprise_info.register_capital = register_capital
        enterprise_info.field = field
        enterprise_info.business_license = business_license
        enterprise_info.legal_person_ID = legal_person_ID
        enterprise_info.vector_hit = mid[0]
        enterprise_info.save()
        user.enterprise_info = enterprise_info
        user.state = 2
        user.save()
    else:
        enterprise_info = user.enterprise_info
        enterprise_info.name = name
        enterprise_info.address = address
        enterprise_info.website = website
        enterprise_info.instruction = instruction
        enterprise_info.phone = phone
        enterprise_info.legal_representative = legal_representative
        enterprise_info.register_capital = register_capital
        enterprise_info.field = field
        enterprise_info.business_license = business_license
        enterprise_info.legal_person_ID = legal_person_ID
        enterprise_info.vector_hit = mid[0]
        enterprise_info.save()
        user.state = 2
        user.save()

    return success_api_response("enterprise register successfully")


'''
@jwt_auth()
@response_wrapper
@require_http_methods('POST')
def get_info(request:HttpRequest):
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    id = data.get("id")
    user = User.objects.get(id=id)
    enterprise_info = user.enterprise_info
    dic = {
        "name": enterprise_info.name,
        "address": enterprise_info.address,
        "website": enterprise_info.website,
        "instruction": enterprise_info.instruction,
        "phone": enterprise_info.phone,
        "legal_representative": enterprise_info.legal_representative,
        "register_capital": enterprise_info.register_capital,
        "field": enterprise_info.field,
    }
    return success_api_response(dic)
'''


"""
应该添加一个认证成功提示
"""
#@jwt_auth()
@csrf_exempt
@response_wrapper
@require_http_methods('GET')
def agree_enterprise(request:HttpRequest, id: int):
    user = User.objects.get(id=id)
    if user.state != 2:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "wrong user state")
    user.state = 5
    user.save()
    return success_api_response("success")


"""
应该添加一个认证失败提示
对于企业信息的删除可能有bug，这里需要测试一下
"""
#@jwt_auth()
@csrf_exempt
@response_wrapper
@require_http_methods('GET')
def refuse_enterprise(request:HttpRequest, id: int):
    user = User.objects.get(id=id)
    if user.state != 2:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "wrong user state")
    user.state = 0
    user.save()
    return success_api_response("success")


"""
通过id获得相应用户申请成为企业的信息
"""

#@jwt_auth()
@csrf_exempt
@response_wrapper
@require_http_methods('GET')
def get_enterpriseInfo(request: HttpRequest, id: int):
    user = User.objects.get(id=id)
    if user.state != 2:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "wrong user state")
    enterprise_info = user.enterprise_info
    return success_api_response({
        "name": enterprise_info.name,
        "address": enterprise_info.address,
        "website": enterprise_info.website,
        "instruction": enterprise_info.instruction,
        "phone": enterprise_info.phone,
        "legal_representative": enterprise_info.legal_representative,
        "register_capital": enterprise_info.register_capital,
        "field": enterprise_info.field,
        "business_license": str(enterprise_info.business_license),
        "legal_person_ID": str(enterprise_info.legal_person_ID)
    })


"""
获取全部申请企业的用户基本信息
"""
#@jwt_auth()
@csrf_exempt
@response_wrapper
@require_http_methods('GET')
def get_all_enterprise(request:HttpRequest):
    users = User.objects.filter(state=2)
    data = list()
    for user in users:
        if user.is_superuser != 1:
            dic = getUserInfo(user)
            dic['profile'] = user.enterprise_info.instruction
            dic['create_time'] = user.enterprise_info.create_time
            data.append(dic)
    return success_api_response(data)