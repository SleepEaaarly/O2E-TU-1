from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import HttpRequest
from pytz import timezone
import functools
from core.api.utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.models.user import User
from core.models.enterprise_info import Enterprise_info
from core.api.auth import jwt_auth
from core.models.need import Need
from core.models.order import Order
from django.utils import timezone
from core.api.platforms.need_api import finish_need
import pytz
from core.api.platforms.utils import format_time, get_order_state

def get_info(s):
    max = 20
    if len(s) > max:
        s = s[:20] + '...'
    return s
        

def get_now_time():
    """获取当前时间"""
    tz = pytz.timezone('Asia/Shanghai')
    # 返回时间格式的字符串
    now_time = timezone.now().astimezone(tz=tz)
    now_time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
    return now_time_str


def get_diff_time(time):

    if time == None:
        return time
    diff = str(timezone.now()-time)

    if diff.__contains__("day"):
        diff = int(diff[0:diff.find('day') - 1])
        if diff <= 30:
            return str(diff) + "天前"
        else:
            return str(time)[0:10]
    elif diff.startswith('0:00'):
        return str(int(diff[5:7])) + "秒前"
    elif diff.startswith('0:'):
        diff = diff[diff.find(':') + 1: diff.find(':')+ 3]
        return str(int(diff)) + '分钟前'
    else:
        return diff[0:diff.find(':')] + "小时前"


def cmp(x, y):
    if x['state'] < y['state']:
        return -1
    elif x['state'] > y['state']:
        return 1
    else: 
        if x['state'] == 0 or x['state'] == 1:
            if x['create_time'] > y['create_time']:
                return -1
            else: return 1
        else:
            if x['end_time'] > y['end_time']:
                return -1
            else: return 1

@response_wrapper
# @jwt_auth()
@require_GET
def get_user_orderid_byneedID(request: HttpRequest, id: int):
    need_id = id

    try:
        need = Need.objects.get(id=need_id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist usr or need")
    
    res = []
    
    orders = need.need_order.exclude(state=2)
    for order in orders:
        res.append(order.id)
    return success_api_response({"data": res})
    
@response_wrapper
# @jwt_auth()
@require_GET
def admin_get_all_order(request: HttpRequest):
    orders = Order.objects.all()
    data = []
    for order in orders:
        data.append(order.to_dict())
    return success_api_response({"data": data}) 

@response_wrapper
# @jwt_auth()
@require_http_methods("DELETE")
def admin_delete_order(request: HttpRequest, id: int):
    try:
        order = Order.objects.get(id=id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist order")
    need = order.need

    """
    ORDER_STATE = (
    (0, "待接受"),
    (1, "正在合作中"),
    (2, "已拒绝"),
    (3, "合作结束"),
    )
    """

    # if order.state == 1 or order.state == 3:
    #     need.real -= 1

    Order.objects.filter(id=id).delete()
    return success_api_response({})

@response_wrapper
# @jwt_auth()
@require_GET
def get_all_order(request: HttpRequest, uid: int):
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    
    
    if user.state == 5:
        # 企业
        order_list = user.enterprise_order.all()
    elif user.state == 4:
        # 专家
        order_list = user.expert_order.all()
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "user type is not expert or company")
    
    orders = []
    orders_reject = []
    for order in order_list:
        expert: User = order.user
        enterprise: User = order.enterprise
        need: Need = order.need
        order_info = {"order_id": order.id, "create_time": (order.create_time), "end_time": (order.end_time),
            "state": order.state, "expert_id":expert.id, "expert_name": expert.expert_info.name, 
            "expert_pic": str(expert.icon),
            "need":{
                "need_id": need.id,
                "title": need.title,
                "enterprise_id": enterprise.id,
                "enterprise_name": enterprise.enterprise_info.name,
                "enterprise_pic": str(enterprise.icon),
                "enterprise_description": get_info(enterprise.enterprise_info.instruction),
            }}
        expert_description = expert.expert_info.organization
        if expert.expert_info.title != None:
            expert_description += ' ' + expert.expert_info.title
        else:
            expert_description += " 副教授 硕导"
        order_info['expert_description'] = expert_description
        if order.state == 2:
            orders_reject.append(order_info)
        else:
            orders.append(order_info)
    orders.sort(key=functools.cmp_to_key(cmp))
    orders_reject.sort(key=functools.cmp_to_key(cmp))
    orders.extend(orders_reject)
    for order in orders:
        order["create_time"] = get_diff_time(order['create_time'])
        order["end_time"] = get_diff_time(order['end_time'])
    
    return success_api_response({"data": orders})


@response_wrapper
# @jwt_auth()
@require_GET
def get_order_id(request: HttpRequest):
    data = request.GET.dict()
    enterprise_id = data.get('enterprise_id')
    expert_id = data.get("expert_id")
    need_id = data.get('need_id')
    
    try:
        enterprise = User.objects.get(id=enterprise_id)
        expert = User.objects.get(id=expert_id)
        need = Need.objects.get(id=need_id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid id")

    if expert.state != 4:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-expert user")
    if enterprise.state != 5 :
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")

    if Order.objects.filter(enterprise=enterprise, need=need, user=expert).exclude(state=2).exists():
        order = Order.objects.filter(enterprise=enterprise, need=need, user=expert).exclude(state=2)[0]
        
        return success_api_response({"order_id": order.id})
    else:
        return success_api_response({"order_id": 0})


@response_wrapper
# @jwt_auth()
@require_GET
def get_finished_order(request: HttpRequest, uid: int):
    """
    get finished order

    [method]: GET

    parms:
        - uid: 企业或专家的id 
    """ 
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    
    
    if user.state == 5:
        # 企业
        order_list = user.enterprise_order.filter(state__in=[3])
    elif user.state == 4:
        # 专家
        order_list = user.expert_order.filter(state__in=[3])
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "user type is not expert or company")
    
    orders = []
    for order in order_list:
        expert: User = order.user
        enterprise: User = order.enterprise
        need: Need = order.need
        order_info = {"order_id": order.id, "create_time": order.create_time, "end_time": order.end_time,
            "state": order.state, "expert_id":expert.id, "expert_name": expert.expert_info.name, 
            "expert_pic": str(expert.icon),
            "need":{
                "need_id": need.id,
                "title": need.title,
                "enterprise_id": enterprise.id,
                "enterprise_name": enterprise.enterprise_info.name,
                "enterprise_pic":  str(enterprise.icon),
                "enterprise_description": get_info(enterprise.enterprise_info.instruction),
            }}
        expert_description = expert.expert_info.organization
        if expert.expert_info.title != None:
            expert_description += ' ' + expert.expert_info.title
        else:
            expert_description += " 副教授 硕导"
        order_info['expert_description'] = expert_description
        orders.append(order_info)
    
    orders.sort(key=lambda x: (x['state'], x["end_time"]), reverse=True)
    for order in orders:
        order["create_time"] = get_diff_time(order['create_time'])
        order["end_time"] = get_diff_time(order['end_time'])
    
    return success_api_response({"data":orders})



@response_wrapper
# @jwt_auth()
@require_GET
def get_pending_order(request: HttpRequest, uid: int):
    """
    get proceding order

    [method]: GET

    parms:
        - uid: 企业或专家的id
    """
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    
    
    if user.state == 5:
        # 企业
        order_list = user.enterprise_order.filter(state=0)
    elif user.state == 4:
        # 专家
        order_list = user.expert_order.filter(state=0)
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "user type is not expert or company")
    
    orders = []
    for order in order_list:
        expert: User = order.user
        enterprise: User = order.enterprise
        need: Need = order.need
        order_info = {"order_id": order.id, "create_time": order.create_time, "end_time": order.end_time,
            "state": order.state, "expert_id":expert.id, "expert_name": expert.expert_info.name, 
            "expert_pic": str(expert.icon),
            "need":{
                "need_id": need.id,
                "title": need.title,
                "enterprise_id": enterprise.id,
                "enterprise_name": enterprise.enterprise_info.name,
                "enterprise_pic":  str(enterprise.icon),
                "enterprise_description": get_info(enterprise.enterprise_info.instruction),
            }}
        expert_description = expert.expert_info.organization
        if expert.expert_info.title != None:
            expert_description += ' ' + expert.expert_info.title
        else:
            expert_description += " 副教授 硕导"
        order_info['expert_description'] = expert_description
        orders.append(order_info)

    orders.sort(key=lambda x: x["create_time"], reverse=True)
    for order in orders:
        order["create_time"] = get_diff_time(order['create_time'])
        order["end_time"] = get_diff_time(order['end_time'])

    return success_api_response({"data": orders})

@response_wrapper
# @jwt_auth()
@require_GET
def get_cooperating_order(request: HttpRequest, uid: int):
    """
    get proceding order

    [method]: GET

    parms:
        - uid: 企业或专家的id
    """
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    
    
    if user.state == 5:
        # 企业
        order_list = user.enterprise_order.filter(state=1)
    elif user.state == 4:
        # 专家
        order_list = user.expert_order.filter(state=1)
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "user type is not expert or company")
    
    orders = []
    for order in order_list:
        expert: User = order.user
        enterprise: User = order.enterprise
        need: Need = order.need
        order_info = {"order_id": order.id, "create_time": order.create_time, "end_time": order.end_time,
            "state": order.state, "expert_id":expert.id, "expert_name": expert.expert_info.name, 
            "expert_pic": str(expert.icon),
            "need":{
                "need_id": need.id,
                "title": need.title,
                "enterprise_id": enterprise.id,
                "enterprise_name": enterprise.enterprise_info.name,
                "enterprise_pic": str(enterprise.icon),
                "enterprise_description": get_info(enterprise.enterprise_info.instruction),
            }}
        expert_description = expert.expert_info.organization
        if expert.expert_info.title != None:
            expert_description += ' ' + expert.expert_info.title
        else:
            expert_description += " 副教授 硕导"
        order_info['expert_description'] = expert_description
        orders.append(order_info)
    orders.sort(key=lambda x: x["create_time"], reverse=True)
    for order in orders:
        order["create_time"] = get_diff_time(order['create_time'])
        order["end_time"] = get_diff_time(order['end_time'])

    return success_api_response({"data": orders})


""" path('order', create_order),  # 企业创建新订单
    path('order/<int:id>', get_order_info), # 获取某个订单的信息
    path('user/<int:uid>/order/<int:id>/refuse', refuse_order), # 专家拒绝订单
    path('user/<int:uid>/order/<int:id>/accept', accept_order), # 专家接受订单
    path('user/<int:uid>/order/<int:id>/finish', finish_order), # 企业结束订单
ok  path('user/<int:uid>/order/finished', get_finished_order), # 获取某个用户（企业或专家）已完成订单（拒绝和结束）
ok  path('user/<int:uid>/order/pending', get_pending_order), # 获取某个用户（企业或专家）新请求的订单
ok  path('user/<int:uid>/order/cooperating', get_cooperating_order), # 获取某个用户（企业或专家）正在合作的订单
"""


@response_wrapper
# @jwt_auth()
@require_POST
def finish_order(request: HttpRequest, uid: int, id: int):
    try:
        enterprise: User = User.objects.get(id=uid)
        order: Order = Order.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist enterprise")
    except Order.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist order")
    
    if order.enterprise != enterprise:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not the enterprise's order")

    if enterprise.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")

    if order.state == 1 or order.state == 0:
        # if order.state == 1:
            # need = order.need
            # if need.need_order.filter(state=3).count() + 1 >= need.predict:
            #     finish_need(request, uid, need.id)
        order.state = 3
        order.end_time = get_now_time()
        order.save()
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "The order is not in cooperation")

    return success_api_response({})


@response_wrapper
# @jwt_auth()
@require_POST
def accept_order(request: HttpRequest, uid: int, id: int):
    """
    expert accept the order
    turn state=0 to state=1
    """
    try:
        expert: User = User.objects.get(id=uid)
        order: Order = Order.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist expert")
    except Order.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist order")
    
    if order.user != expert:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not the expert's order")

    if expert.state != 4:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-expert user")

    need: Need = order.need 
    # if need.real >= need.predict:
    #     return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need is full")

    if order.state == 0:
        Order.objects.filter(id=id).update(state=1)
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "The order is not pending state(state=0)")

    # need.real = need.real + 1
    need.save()
    return success_api_response({})


@response_wrapper
# @jwt_auth()
@require_POST
def refuse_order(request: HttpRequest, uid: int, id: int):
    """
    expert accept the order
    turn state=0 to state=1
    """
    try:
        expert: User = User.objects.get(id=uid)
        order: Order = Order.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist expert")
    except Order.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist order")
    
    if order.user != expert:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not the expert's order")

    if expert.state != 4:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-expert user")

    if order.state == 0:
        order.state=2
        order.end_time = get_now_time()
        order.save()
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "The order is not pending state(state=0)")
    return success_api_response({})


@response_wrapper
# @jwt_auth()
@require_GET
def get_order_info(request: HttpRequest, id: int):
    try:
        order: Order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist order")
    
    expert: User = order.user
    enterprise: User = order.enterprise
    need: Need = order.need
    order_info = {"order_id": order.id, "create_time": format_time(order.create_time), "end_time": format_time(order.end_time),
        "address": need.address, "description": need.description, "phone": enterprise.enterprise_info.phone,
        "state": order.state, "expert_id":expert.id, "expert_name": expert.expert_info.name, "need":{
            "need_id": need.id,
            "title": need.title,
            "enterprise_id": enterprise.id,
            "enterprise_name": enterprise.enterprise_info.name
        }}

    return success_api_response(order_info)


@response_wrapper
# @jwt_auth()
@require_POST
def create_order(request: HttpRequest):
    data = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")


    need_id = data.get("need_id")
    expert_id = data.get("expert_id")
    enterprise_id = data.get("enterprise_id")
    print(need_id, expert_id, enterprise_id)
    try:
        need = Need.objects.get(id=need_id)
        expert = User.objects.get(id=expert_id)
        enterprise = User.objects.get(id=enterprise_id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find need or expert or enterprise obj")
    
    if expert.state != 4:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-expert user")
    if enterprise.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")
    if need.state == 1:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "the need is finished")
    if Order.objects.filter(user_id=expert_id, enterprise_id=enterprise_id, need_id=need_id).exclude(state=2).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "already exist order")

    # if need.real >= need.predict:
    #     return failed_api_response(ErrorCode.INVAzLID_REQUEST_ARGS, "the need recruitment is full")
    order: Order = Order(user_id=expert_id, enterprise_id=enterprise_id, need_id=need_id, state=0)
    order.save()
    return success_api_response({})


@response_wrapper
# @jwt_auth()
@require_POST
def abandon_order(request: HttpRequest, uid: int, id: int):
    try:
        enterprise: User = User.objects.get(id=uid)
        order: Order = Order.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist enterprise")
    except Order.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist order")
    
    if order.enterprise != enterprise:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not the enterprise's order")

    if enterprise.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")

    if order.state == 1 or order.state == 0:
        # if order.state == 1:
        #     need = order.need
        #     need.real -= 1
        order.delete()
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "The order is not in cooperation")
    return success_api_response({})


@response_wrapper
# @jwt_auth()
@require_GET
def get_order_byID(request:HttpRequest, id:int):
    need = Need.objects.get(id=id)
    orders = need.need_order.all()
    data = []
    for order in orders:
        expert: User = order.user
        enterprise: User = order.enterprise
        need: Need = order.need
        order_info = {"order_id": order.id, "create_time": format_time(order.create_time),
                      "end_time": format_time(order.end_time),
                      "address": need.address, "description": need.description,
                      "phone": enterprise.enterprise_info.phone,
                      "state": get_order_state(order.state), "expert_id": expert.id, "expert_name": expert.expert_info.name, "need": {
                "need_id": need.id,
                "title": need.title,
                "enterprise_id": enterprise.id,
                "enterprise_name": enterprise.enterprise_info.name
            }}
        data.append(order_info)
    return success_api_response({"data":data})