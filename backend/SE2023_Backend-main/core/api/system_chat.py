from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone
from django.core import serializers
from django.http import HttpResponse

from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)
from core.api.platform.utils import get_now_time
from core.models import User, Chatroom, Message, SystemChatroom, CardMessage
from core.models import SwitchMessage, ImageMessage


"""
    create system chatroom
    [method]: POST
    [route]: /api/system_chat/create

    parms:
        - uId: int 用户ID
        
    return:
        - id: system chatroom id
"""


@jwt_auth()
@require_POST
@response_wrapper
def create_system_chat(request: HttpRequest):

    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "Invalid request args.")
    # username = data.get('username')
    uid = data.get('uId')

    try:
        user = User.objects.get(id=uid)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad User ID.")

    # 先查看是否已经存在聊天，则不用创建
    if user.system_chatroom_list.all().exists():
        return success_api_response({'id': user.system_chatroom_list.get().id})

    # 否则新建
    system_chatroom = SystemChatroom(owner=user, isai=SystemChatroom.MANUAL_REPLY,
                                     last_message_time=get_now_time(), unread_message_num=0)
    system_chatroom.save()
    ret_data = {'id': system_chatroom.id}
    return success_api_response(ret_data)


"""
    get system chat

    [method]: GET

    [route]: /api/system_chat/get

    parms:
		- uId: int
	return:
	    - messages
        - noreadnum: int 未读信息数
"""


@jwt_auth()
@require_GET
@response_wrapper
def get_system_chat(request: HttpRequest):
    data = request.GET.dict()
    user_id = data.get('uId')
    try:
        owner = User.objects.get(id=user_id)
        system_chatroom = SystemChatroom.objects.get(owner=owner)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad System Chatroom ID.")
    ret_data = {}
    messages = []
    for m in system_chatroom.messages.all():
        a_message = {}
        if(m.from_user is owner):
            a_message['isme'] = True
            a_message['user_pic'] = owner.icon
        else:
            a_message['isme'] = False
            a_message['user_pic'] = ''
        # type, message, cardInfo
        if(isinstance(m, CardMessage)):
            a_message['type'] = 'card'
            a_message['cardInfo'] = m.generate_card()
        elif(isinstance(m, SwitchMessage)):
            a_message['type'] = 'switch_info'
            a_message['message'] = m.content
        elif(isinstance(m, ImageMessage)):
            a_message['type'] = 'pic'
            a_message['message'] = m.content
        else:
            a_message['type'] = 'text'
            a_message['message'] = m.content
        # created_at
        a_message['created_at'] = m.created_at
        messages.append(a_message)
    ret_data['messages'] = messages
    ret_data['noreadnum'] = system_chatroom.unread_message_num
    return success_api_response(ret_data)


"""
    向数据库中新增一条聊天记录
    [method]: POST
    
    [route]: /api/system_chat/push
    
    parms:
        - uId: int, 用户ID向系统发送了一条数据
        - content: str, 文本内容等
        - isme: Who is the sender? 0 for user, 1 for platform
        
    return:
        'system_chatroom_id': system_chatroom_id
        'message_id': message_id
"""


@jwt_auth()
@require_POST
@response_wrapper
def push_system_message(request: HttpRequest):
    data: dict = parse_data(request)
    user: User = User.objects.get(id=data.get('uId'))
    content = data.get('content')
    # 暂时约定平台方为None
    try:
        system_chatroom: SystemChatroom = SystemChatroom.objects.get(
            owner=user)
        if(data.get('isme') == 0):
            from_user = user
            to_user = User.objects.get(id=0)
        else:
            from_user = User.objects.get(id=0)
            to_user = user
        message_id = Message.new_message(
            from_user=from_user,
            to_user=to_user,
            content=content)
        print(message_id)
        if system_chatroom.add_message(message_id) is False:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Add message failed.")
        system_chatroom.save()
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad System Chatroom ID or add message failed.")

    return success_api_response({'system_chatroom_id': system_chatroom.id,
                                 'message_id': message_id})


"""
    将聊天窗口中所有消息都标为已读
    [method]: POST
    [route]: /api/system_chat/read
    parms:
        - uId: int, 用户ID
        
    return:
        - 是否成功
"""


@jwt_auth()
@require_POST
@response_wrapper
def system_message_read(request: HttpRequest):
    data: dict = parse_data(request)
    user: User = User.objects.get(id=data.get('uId'))

    try:
        system_chatroom = SystemChatroom.objects.get(owner=user)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad System Chatroom.")

    try:
        for message in system_chatroom.messages.all():
            message.set_read()
        system_chatroom.unread_message_num = 0
        system_chatroom.save()
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Message ID.")

    return success_api_response(None)


"""
    切换该系统聊天的模式
    [method]: POST
    
    [route]: /api/system_chat/show
    
    Params:
        - uId: int, 用户ID
        - show: bool, 是否显示该聊天
    Returns:
        - 成功或失败信息
"""


@jwt_auth()
@require_POST
@response_wrapper
def alter_systemchat_visible(request: HttpRequest):
    data: dict = parse_data(request)
    user: User = User.objects.get(id=data.get('uId'))

    try:
        system_chatroom = SystemChatroom.objects.get(owner=user)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad System Chatroom")

    if(data.get('show') == 0):
        content = 'AI'
    else:
        content = "Manual"
    switch_message = SwitchMessage.new_switch_message(from_user=user, to_user=None,
                                                      content=content)
    system_chatroom.add_message(switch_message)
    system_chatroom.alter_mode(data.get('show'))
    return success_api_response(None)


"""
    管理端： 获取所有用户的平台聊天
    [method]: GET
    
    [route]: /api/system_chat/getAll
    
    Params:
        - None
    
    Returns:
        - 结构较为复杂，详情请见设计文档
"""


@jwt_auth()
@require_GET
@response_wrapper
def get_all_system_chatrooms(request: HttpRequest):
    ret_all_list = {}
    try:
        for sys_chat in SystemChatroom.all():
            ret_data = {}
            messages = []
            owner = sys_chat.owner
            user_info = {
                "uId": owner.id,
                "email": owner.email
            }
            for m in sys_chat.messages.all():
                a_message = {}
                if(m.from_user is owner):
                    a_message['isme'] = True
                    a_message['user_pic'] = owner.icon
                else:
                    a_message['isme'] = False
                    a_message['user_pic'] = ''
                # type, message, cardInfo
                if(isinstance(m, CardMessage)):
                    a_message['type'] = 'card'
                    a_message['cardInfo'] = m.generate_card()
                elif(isinstance(m, SwitchMessage)):
                    a_message['type'] = 'switch_info'
                    a_message['message'] = m.content
                elif(isinstance(m, ImageMessage)):
                    a_message['type'] = 'pic'
                    a_message['message'] = m.content
                else:
                    a_message['type'] = 'text'
                    a_message['message'] = m.content
                # created_at
                a_message['created_at'] = m.created_at
                messages.append(a_message)
            ret_data['messages'] = messages
            ret_data['noreadnum'] = sys_chat.unread_message_num
            ret_data['userInfo'] = user_info
            ret_all_list.append(ret_data)
        return success_api_response(ret_all_list)
    except Exception:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Fail to get all system chatrooms information")


"""
    管理员发送消息
    [method]: POST
    
    [route]: /api/system_chat/push
    
    Params:
        - uId, int 用户ID
        - content, str 文本消息
    Returns:
        - 成功信息
    
"""


@jwt_auth()
@require_POST
@response_wrapper
def push_system_message_by_admin(request: HttpRequest):
    data: dict = parse_data(request)
    user: User = User.objects.get(id=data.get('uId'))
    content = data.get('content')
    # 暂时约定平台方为None
    try:
        system_chatroom: SystemChatroom = SystemChatroom.objects.get(
            owner=user)
        from_user = None
        to_user = user
        message_id = Message.new_message(
            from_user=from_user,
            to_user=to_user,
            content=content)
        if system_chatroom.add_message(message_id) is False:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Add message failed.")
        system_chatroom.save()
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad System Chatroom ID or add message failed.")

    return success_api_response({'system_chatroom_id': system_chatroom.id,
                                 'message_id': message_id})
