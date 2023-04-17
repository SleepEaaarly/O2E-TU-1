from django.http import HttpRequest
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist

from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)
from core.api.platform.utils import get_now_time
from core.models import User, SystemMessage, SystemChatroom, CardMessage
from core.models import SwitchMessage, ImageMessage
from core.models import Order, Need, Enterprise_info

@jwt_auth()
@require_GET
@response_wrapper
def get_order_report(request: HttpRequest):
    data = request.GET.dict()
    order_id = data.get('id')
    try:
        selected_order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad order ID.")
    ret_data = {}
    ret_data['needInfo'] ={}
    ret_data['expertInfo'] = {}
    ret_data['enterpriseInfo'] = {}
    ref_need : Need = selected_order.need
    # 基本信息
    ret_data['needInfo']['needPostTime'] = ref_need.start_time
    ret_data['needInfo']['orderStartTime'] = selected_order.create_time
    ret_data['needInfo']['orderEndTime'] = selected_order.end_time
    ret_data['needInfo']['needName'] = ref_need.title
    # 专家信息
    ref_expert = selected_order.user
    ret_data['expertInfo']['expertLogoPath'] = ref_expert.icon.path
    ret_data['expertInfo']['expertName'] = ref_expert.username
    ret_data['expertInfo']['expertProfile'] = ref_expert.biogrpahy
    # 企业信息
    ref_enterprise: Enterprise_info = selected_order.enterprise.enterprise_info
    ret_data['enterpriseInfo']['enterpriseLogoPath'] = ref_enterprise.legal_person_ID.path
    ret_data['enterpriseInfo']['enterpriseName'] = ref_enterprise.name
    ret_data['enterpriseInfo']['enterProfile'] = ref_enterprise.instruction
    

    
    