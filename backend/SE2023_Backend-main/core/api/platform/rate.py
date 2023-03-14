from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import HttpRequest
from pytz import timezone
from core.api.utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.models.user import User
from core.models.enterprise_info import Enterprise_info
from core.api.auth import jwt_auth
from core.models.need import Need
from core.models.order import Order
from django.utils import timezone
from core.models.rate import Rate
from django.db.models import Avg

##############################################################
# POST METHOD
##############################################################

@response_wrapper
# @jwt_auth()
@require_POST
def rate_order(request: HttpRequest):
    data = parse_data(request=request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find data")

    formData = data.get('formData')
    
    if not formData:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find formData")

    rate_taste = formData.get('rate_taste')
    rate_speed = formData.get('rate_speed')
    rate_level = formData.get('rate_level')
    description = formData.get('description')
    datetime = formData.get('datetime')
    order_id = formData.get('order_id')

    if not rate_taste or not rate_speed or not rate_level or not datetime or not order_id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "parameter wrong")

    try:
        order = Order.objects.get(id=order_id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find orderid")

    if Rate.objects.filter(order=order).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "rate has already existed")

    rate = Rate(rate_taste=rate_taste, rate_speed=rate_speed, rate_level=rate_level, 
        datetime=datetime, order_id=order_id, expert_id=order.user_id, enterprise_id=order.enterprise_id)

    if description:
        rate.description = description
    rate.save()
    return success_api_response({})


##############################################################
# GET METHOD
##############################################################


@response_wrapper
# @jwt_auth()
@require_GET
def get_order_rate(request: HttpRequest, id: int):
    order_id = id
    try:
        order = Order.objects.get(id=order_id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find order")
    
    # rate = order.order_rate.last()
 
    # rate_info = rate.to_dict()
    flag = 0
    data = dict()
    if Rate.objects.filter(order=order).exists():
        flag = 1

        rate = Rate.objects.get(order=order)
        data.update(rate.to_dict())

    return success_api_response({"flag": flag, "data": data})


@response_wrapper
# @jwt_auth()
@require_GET
def get_user_rate(request: HttpRequest, id: int):
    # enterprise_id = id 
    try:
        user = User.objects.get(id=id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find user")
    if user.state != 5 and user.state != 4:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise or expert user")
    
    data = []

    if user.state == 5: 
        rates = user.enterprise_rate.all()
    else:
        rates = user.expert_rate.all()

    for rate in rates:
        info = dict()
        info["rate"] = rate.to_dict()
        info["order"] = {
            'order_name': rate.order.need.title,
        }
        info['expert'] = {
            'expert_id': rate.expert.id,
            "expert_name": rate.expert.expert_info.name,
            'expert_icon': str(rate.expert.icon)
        }
        info["enterprise"] = {
            "enterprise_id": rate.enterprise.id,
            "enterprise_name": rate.enterprise.enterprise_info.name,
            "enterprise_icon": str(rate.enterprise.icon)
        }
        data.append(info)
    flag = 0
    if data:
        flag = 1
    if user.state == 4:
        # 专家获取平均数
        avg = dict()
        avg['rate_taste'] = user.expert_rate.aggregate(Avg('rate_taste')).get('rate_taste__avg')
        avg['rate_speed'] = user.expert_rate.aggregate(Avg('rate_speed')).get('rate_speed__avg')
        avg['rate_level'] = user.expert_rate.aggregate(Avg('rate_level')).get('rate_level__avg')

        # print(user.expert_rate.all().values_list('rate_taste', 'rate_speed', 'rate_level'))
        return success_api_response({"data": data, "avg": avg, "flag": flag})
    else:
        return success_api_response({"data": data, "flag": flag, "avg": {
            "rate_taste": 0,
            "rate_speed": 0,
            "rate_level": 0
        }})


