import random
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import HttpRequest
from django.db.models import Q

from core.api.milvus_utils import get_milvus_connection, disconnect_milvus, milvus_insert
from core.api.utils import (failed_api_response, ErrorCode,
                            success_api_response, parse_data,
                            wrapped_api, response_wrapper)
from core.models.user import User
from core.models.enterprise_info import Enterprise_info
from core.models.expert import Expert
from core.api.auth import jwt_auth
from core.models.need import Need
from core.models.needContact import NeedContact
from core.models.order import Order
import pytz
from django.utils import timezone
from core.api._platform.utils import get_field, get_need_state

from core.api.ai_report import generate_requirement_report
from core.api.ai_recommend import get_scibert_embedding
from django.views.decorators.csrf import csrf_exempt

from core.api.utils import trans_zh2en


def get_now_time():
    """获取当前时间"""
    tz = pytz.timezone('Asia/Shanghai')
    # 返回时间格式的字符串
    now_time = timezone.now().astimezone(tz=tz)
    now_time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
    return now_time_str[0:10]


def get_info(s):
    max = 60
    if len(s) > max:
        s = s[:max] + '...'
    return s

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_POST
def transform_need(request: HttpRequest, uid: int, id: int):
    try:
        enterrpise: User = User.objects.get(id=uid)
        need: Need = Need.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    except Need.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist need")

    if enterrpise.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")
    if need.enterprise != enterrpise:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not the enterpreise's need")

    if need.state != 2:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not a saved need")

    need.state = 0
    need.save()
    return success_api_response({})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_GET
def expert_recommend(request: HttpRequest, id: int):
    try:
        need = Need.objects.get(id=id)
    except Need.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist need")

    experts = User.objects.filter(state=4).all()

    lst = []

    print(experts.count())

    index = random.randint(0, experts.count() - 1)

    expert = experts[index]
    lst.append({"expert_id": expert.id, "scholar_id": expert.expert_info.scholarID, "name": expert.expert_info.name,
                "phone": expert.expert_info.phone, "profile": expert.expert_info.self_profile,
                "organization": expert.expert_info.organization, "paper": expert.expert_info.paper})

    # for expert in experts:

    # for expert in experts:
    #     if random.randint(1, 2) == 1:
    #         lst.append(
    #             {"expert_id": expert.id, "scholar_id": expert.expert_info.scholarID, "name": expert.expert_info.name,
    #              "phone": expert.expert_info.phone, "profile": expert.expert_info.self_profile,
    #              "organization": expert.expert_info.organization, "paper": expert.expert_info.paper})

    # if not lst:
    #     expert = experts[random.randint(0, experts.count() - 1)]
    #     lst.append({"expert_id": expert.id, "scholar_id": expert.expert_info.scholarID, "name": expert.expert_info.name,
    #                 "phone": expert.expert_info.phone, "profile": expert.expert_info.self_profile,
    #                 "organization": expert.expert_info.organization, "paper": expert.expert_info.paper})

    return success_api_response({"data": lst})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_GET
def get_need_contact(request: HttpRequest):
    data = request.GET.dict()
    enterprise_id = data.get('enterprise_id')
    expert_id = data.get("expert_id")
    try:
        enterprise = User.objects.get(id=enterprise_id)
        expert = User.objects.get(id=expert_id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "enterprise or expert or need not found")
    if enterprise.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")
    if expert.state != 4:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-expert user")

    if NeedContact.objects.filter(expert=expert, enterprise=enterprise).exists():
        need_contact = NeedContact.objects.get(
            expert=expert, enterprise=enterprise)
        info: dict = {"need_id": need_contact.need.id}
        return success_api_response(info)
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find need")

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_POST
def create_need_contact(request: HttpRequest):
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "data not found")
    enterprise_id = data.get('enterprise_id')
    expert_id = data.get('expert_id')
    need_id = data.get('need_id')
    try:
        enterprise = User.objects.get(id=enterprise_id)
        expert = User.objects.get(id=expert_id)
        need = Need.objects.get(id=need_id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "enterprise or expert or need not found")
    if enterprise.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")
    if expert.state != 4:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-expert user")

    if NeedContact.objects.filter(expert=expert, enterprise=enterprise).exists():
        NeedContact.objects.filter(
            expert=expert, enterprise=enterprise).update(need=need)
    else:
        needContact = NeedContact(
            expert=expert, enterprise=enterprise, need=need)
        needContact.save()
    return success_api_response({})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_GET
def search_need(request: HttpRequest, *args, **kwargs):
    data = request.GET.dict()
    key_word = data.get('key_word')
    if key_word is None or key_word == '':  # not key_word 是判空，也可以判None
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "none key word")

    key_words = key_word.split()

    results = []
    needs = Need.objects.none()
    for key_word in key_words:
        needs = needs.union(Need.objects.filter(Q(title__icontains=key_word) | Q(description__icontains=key_word)
                                                | Q(key_word__icontains=key_word)
                                                | Q(address__icontains=key_word) | Q(enterprise__enterprise_info__name__icontains=key_word)).all().filter(state=0))
        print(needs.count())

    for need in needs:
        need_info = {"need_id": need.id, "title": need.title, "description": get_info(need.description),
                     "start_time": need.start_time, "money": need.money, "key_word": need.key_word,
                     "end_time": need.end_time, "field": need.field, "state": need.state, "emergency": need.emergency,
                     "address": need.address}
        results.append(need_info)
    return success_api_response({"data": results})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_http_methods(['DELETE'])
def delete_need(request: HttpRequest, uid: int, id: int):
    try:
        enterrpise: User = User.objects.get(id=uid)
        need: Need = Need.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    except Need.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist need")

    if enterrpise.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")
    if need.enterprise != enterrpise:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not the enterpreise's need")

    need.delete()
    return success_api_response({})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_GET
def get_need_info(request: HttpRequest, id: int):
    try:
        need = Need.objects.get(id=id)
    except Need.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist need")

    enterprise: User = need.enterprise

    need_info = {"need_id": need.id, "title": need.title, "description": need.description, "money": need.money,
                 "start_time": need.start_time,
                 "end_time": need.end_time, "key_word": need.key_word, "field": need.field, "address": need.address,
                 "state": need.state,
                 "emergency": need.emergency,
                 "enterprise_id": enterprise.id, "enterprise_name": enterprise.enterprise_info.name,
                 "enterprise_pic": str(enterprise.icon)}
    order = list()
    orders = need.need_order.exclude(state=2)
    for o in orders:
        order_info = {
            "order_id": o.id,
            "order_state": o.state,
            "expert_id": o.user.id,
            "expert_icon": str(o.user.icon),
            "expert_name": o.user.expert_info.name,
            "enterprise_id": o.enterprise.id
        }
        order.append(order_info)
    need_info['order'] = order
    return success_api_response(need_info)

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_POST
def create_need(request: HttpRequest):
    """
    create need

    [method]: POST

    [route]: /api/need
    """
    print("enter create_need")
    data: dict = parse_data(request)
    print(data)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "data is none")

    id = data.get('company_id')
    if not id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "id not found")
    print("id=", id)
    try:
        user: User = User.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    print("user=", user)
    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")

    title = data.get('title')
    print("before trans",type(title))
    title_en = trans_zh2en(title)
    print("after trans")
    description = data.get('description')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    key_word = data.get('key_word')
    address = data.get('address')

    try:
        money = int(data.get('money'))
        # predict = int(data.get('predict'))
        # real = int(data.get('real'))
        emergency = int(data.get('emergency'))
        state = int(data.get('state'))
        field = int(data.get('field'))
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-digit value(some digit value is wrong)")

    print("title", title)
    print("title_eng", title_en)
    print("descrption", description)
    print("money", money)
    print("start_time", start_time)
    print("end_time", end_time)
    print("key_word", key_word)
    print("field", field)
    print("address", address)
    print("emergency", emergency)
    # print("predict", predict)
    # print("real", real)
    print("state", state)

    if title is None or description is None or money is None or start_time is None or key_word is None \
            or field is None or address is None or emergency is None or state is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid requset value")

    if not title or not description or not start_time:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "title or description or start_time cannot be empty")

    need = Need(title=title, title_eng=title_en, description=description, money=money, start_time=start_time,
                end_time=end_time, key_word=key_word, field=field, address=address,
                enterprise=user, state=state, emergency=emergency, predict=4, real=0)
    need.save()
    # 为需求生成报告
    generate_requirement_report(need.id)
    # 向milvus库插入向量
    sci_vec = get_scibert_embedding(title_en)
    get_milvus_connection()
    mid_sci = milvus_insert("O2E_NEED", data=[[sci_vec], [need.id]])
    disconnect_milvus()
    need.vector_sci = mid_sci[0]
    need.save()
    return success_api_response({})

@response_wrapper
# @jwt_auth()
@require_GET
def get_needs_info(request: HttpRequest):
    """
    get all need
    """
    needs = Need.objects.all()
    data = []
    for need in needs:
        need_info = {"need_id": need.id, "title": need.title, "description": get_info(need.description),
                     "start_time": str(need.start_time)[0:10], "money": need.money, "key_word": need.key_word,
                     "end_time": str(need.end_time)[0:10], "field": get_field(need.field),
                     "state": get_need_state(need.state),
                     "emergency": need.emergency,
                     "enterprise_name": need.enterprise.enterprise_info.name,
                     "address": need.address}
        data.append(need_info)
    return success_api_response({"data": data})


# 获取需求已对接全部专家id与头像url
@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_GET
def get_oneneed_allexperts(request: HttpRequest, id: int):
    try:
        need = Need.objects.get(id=id)
    except Need.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist need")

    exp_users = Order.objects.filter(need__id=id).values('user').distinct()

    data = []
    for u in exp_users:
        # print(u)
        expert = User.objects.get(id=u["user"])
        data.append({"expert_id": expert.id,
                     "scholar_id": expert.expert_info.scholarID,
                     "name": expert.expert_info.name,
                     "icon_url": str(expert.icon)
                     })

    return success_api_response({"data": data})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_GET
def get_all_need(request: HttpRequest):
    """
    get all need whose state == 0
    """
    time = get_now_time()
    needs = Need.objects.filter(Q(state=0) & Q(end_time__gt=time))

    need_finish = Need.objects.filter(Q(end_time__lt=time) & Q(state=0))
    need_finish.update(state=1)
    for need in need_finish:
        need.need_order.update(state=3)
        # need.need_contact.all().delete()

    data = []
    for need in needs:
        need_info = {"need_id": need.id, "title": need.title, "description": get_info(need.description),
                     "start_time": str(need.start_time)[0:10], "money": need.money, "key_word": need.key_word,
                     "end_time": str(need.end_time)[0:10], "field": need.field, "state": need.state,
                     "emergency": need.emergency, "address": need.address}
        experts = list()
        orders = need.need_order.filter(Q(state=1) | Q(state=3) | Q(state=0))
        for order in orders:
            expert = {
                'expert_id': order.user.id,
                'expert_icon': str(order.user.icon),
                'expert_name': order.user.expert_info.name,
            }
            if expert not in experts:
                experts.append(expert)
        need_info['experts'] = experts
        data.append(need_info)
    data.sort(key=lambda x: x["end_time"])
    return success_api_response({"data": data})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_GET
def get_finished_need(request: HttpRequest, uid: int):
    """
    get user(id = uid, enterprise) finished need
    """
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")

    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")

    needs = user.enterprise_need.filter(state=1)
    data = []
    for need in needs:
        need_info = {"need_id": need.id, "title": need.title, "description": get_info(need.description),
                     "start_time": (need.start_time)[0:10], "money": need.money, "key_word": need.key_word,
                     "end_time": (need.end_time)[0:10], "field": need.field, "state": need.state,
                     "emergency": need.emergency, "address": need.address}
        experts = list()
        orders = need.need_order.filter(Q(state=1) | Q(state=3) | Q(state=0))
        for order in orders:
            expert = {
                'expert_id': order.user.id,
                'expert_icon': str(order.user.icon),
                'expert_name': order.user.expert_info.name,
            }
            if expert not in experts:
                experts.append(expert)
        need_info['experts'] = experts
        data.append(need_info)
    data.sort(key=lambda x: x["end_time"])
    return success_api_response({"data": data})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_GET
def get_saved_need(request: HttpRequest, uid: int):
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")

    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")

    needs = user.enterprise_need.filter(state=2)
    data = []
    for need in needs:
        need_info = {"need_id": need.id, "title": need.title, "description": get_info(need.description),
                     "start_time": (need.start_time)[0:10], "money": need.money, "key_word": need.key_word,
                     "end_time": (need.end_time)[0:10], "field": need.field, "state": need.state,
                     "emergency": need.emergency, "address": need.address}
        experts = list()
        orders = need.need_order.filter(Q(state=1) | Q(state=3) | Q(state=0))
        for order in orders:
            expert = {
                'expert_id': order.user.id,
                'expert_icon': str(order.user.icon),
                'expert_name': order.user.expert_info.name,
            }
            if expert not in experts:
                experts.append(expert)
        need_info['experts'] = experts
        data.append(need_info)
    data.sort(key=lambda x: x["end_time"])
    return success_api_response({"data": data})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_POST
def finish_need(request: HttpRequest, uid: int, id: int):
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")

    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")

    try:
        need: Need = Need.objects.get(id=id)
    except Need.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist need")

    if need.enterprise != user:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Not the enterprise's need")

    Need.objects.filter(id=id).update(state=1)

    need.need_order.update(state=3)

    # need.need_contact.all().delete()

    return success_api_response({})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_GET
def get_proceeding_need(request: HttpRequest, uid: int):
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")

    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")
    needs = user.enterprise_need.filter(state=0)
    data = []
    for need in needs:
        need_info = {"need_id": need.id, "title": need.title, "description": get_info(need.description),
                     "start_time": (need.start_time)[0:10], "money": need.money, "key_word": need.key_word,
                     "end_time": (need.end_time)[0:10], "field": need.field, "state": need.state,
                     "emergency": need.emergency, "address": need.address}

        experts = list()
        orders = need.need_order.filter(Q(state=1) | Q(state=3) | Q(state=0))
        for order in orders:
            expert = {
                'expert_id': order.user.id,
                'expert_icon': str(order.user.icon),
                'expert_name': order.user.expert_info.name,
            }
            if expert not in experts:
                experts.append(expert)
        need_info['experts'] = experts
        data.append(need_info)
    data.sort(key=lambda x: x["end_time"])
    return success_api_response({"data": data})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_POST
def edit_need(request: HttpRequest, uid: int, id: int):
    try:
        user: User = User.objects.get(id=uid)
        need: Need = Need.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    except Need.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist need")

    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")
    if need.enterprise != user:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not the enterprise's need")

    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "data is none")

    title = data.get('title')
    description = data.get('description')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    key_word = data.get('key_word')
    address = data.get('address')

    try:
        money = int(data.get('money'))
        emergency = int(data.get('emergency'))
        field = int(data.get('field'))
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-digit value(some digit value is wrong)")

    if title is None or description is None or money is None or start_time is None or end_time is None or key_word is None \
            or field is None or address is None or emergency is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid requset value")

    if not title or not description or not start_time:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "title or description or start_time cannot be empty")

    Need.objects.filter(id=id).update(title=title, description=description, money=money,
                                      start_time=start_time, end_time=end_time, key_word=key_word, field=field,
                                      address=address,
                                      emergency=emergency)

    return success_api_response({})

@csrf_exempt
@response_wrapper
# @jwt_auth()
@require_http_methods(['DELETE'])
def admin_delete_need(request: HttpRequest, id: int):
    try:
        need: Need = Need.objects.get(id=id)
    except Need.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist need")
    need.delete()
    return success_api_response({})
