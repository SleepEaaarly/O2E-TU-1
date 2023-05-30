"""JSON Web Token API
Nowadays, it locates at {workspace}/core/api/
Maybe someday it will be moved to {workspace}/auth/
"""


from datetime import timedelta

import json
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from core.api.utils import (ErrorCode, failed_api_response, response_wrapper,
                            success_api_response,parse_data)
from core.models.auth_record import AuthRecord
# from core.models.auth_record import AuthRecord2

from core.models.user import User
# from core.models.user import AdminUser
# from core.models.user import super_authenticate
from django.views.decorators.csrf import csrf_exempt

def auth_failed(message: str):
    """shorten
    """
    return failed_api_response(ErrorCode.UNAUTHORIZED, message)


def generate_access_token(user_id: int, access_token_delta: int = 1) -> str:
    """generate jwt

    Args:
        user_id (str): user.id
        access_token_delta (int, optional): time to expire. Defaults to 1 (hour).
    """
    current_time = timezone.now()
    access_token_payload = {
        "user_id": user_id,
        "exp": current_time + timedelta(hours=access_token_delta),
        "iat": current_time,
        "type": "access_token",
    }

    return jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")


def generate_refresh_token(user: User, refresh_token_delta: int = 6 * 24) -> str:
    """generate jwt

    Args:
        user (User): User object
        refresh_token_delta (int, optional): time to expire. Defaults to 6 days (7 * 24 hours).
    """
    current_time = timezone.now()
    auth_record = AuthRecord(user=user, login_at=current_time,
                             expires_by=current_time + timedelta(hours=refresh_token_delta))
    print(user, current_time, current_time+timedelta(hours=refresh_token_delta))
    print(auth_record)
    auth_record.save()

    refresh_token_payload = {
        "user_id": user.id,
        "record_pk": auth_record.id,
        "iat": current_time,
        "type": "refresh_token",
    }

    return jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm="HS256")
'''
def generate_refresh_token2(user: User, refresh_token_delta: int = 6 * 24) -> str:
    """generate jwt

    Args:
        user (User): User object
        refresh_token_delta (int, optional): time to expire. Defaults to 6 days (7 * 24 hours).
    """
    current_time = timezone.now()
    auth_record = AuthRecord2(user=user, login_at=current_time,
                             expires_by=current_time + timedelta(hours=refresh_token_delta))
    auth_record.save()

    refresh_token_payload = {
        "user_id": user.id,
        "record_pk": auth_record.id,
        "iat": current_time,
        "type": "refresh_token",
    }

    return jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm="HS256")
'''


def verify_jwt_token(request: HttpRequest) -> (bool, str, int):
    """[summary]
    """
    # get header
    
    flag = True
    message = ""
    user_id = ""
    header = request.META.get("HTTP_AUTHORIZATION")
    try:
        if header is None:
            raise jwt.InvalidTokenError

        auth_info = header.split(" ")
        if len(auth_info) != 2:
            raise jwt.InvalidTokenError
        auth_type, auth_token = auth_info

        if auth_type != "Bearer":
            raise jwt.InvalidTokenError
        # print("Before decode")
        token = jwt.decode(
            auth_token, settings.SECRET_KEY, algorithms="HS256")
        # print("After decode")
        if token.get("type") != "access_token":
            raise jwt.InvalidTokenError
        user_id = token["user_id"]
    except jwt.ExpiredSignatureError:
        flag, message = False, "Token expired."
    except jwt.InvalidTokenError:
        flag, message = False, "Invalid token."
    return (flag, message, user_id)

'''
def verify_jwt_token2(request: HttpRequest) -> (bool, str, int):
    """[summary]
    """
    # get header
    
    flag = True
    message = ""
    user_id = ""
    header = request.META.get("HTTP_TOKEN")
    try:
        if header is None:
            raise jwt.InvalidTokenError

        auth_info = header.split(" ")
        if len(auth_info) != 2:
            raise jwt.InvalidTokenError
        auth_type, auth_token = auth_info

        if auth_type != "Bearer":
            raise jwt.InvalidTokenError
        token = jwt.decode(
            auth_token, settings.SECRET_KEY, algorithms="HS256")
        if token.get("type") != "access_token":
            raise jwt.InvalidTokenError
        user_id = token["user_id"]
        print("[DEBUG]:current SUPER user is"+str(user_id))
    except jwt.ExpiredSignatureError:
        flag, message = False, "Token expired."
    except jwt.InvalidTokenError:
        flag, message = False, "Invalid token."
    return (flag, message, user_id)
'''

@csrf_exempt
@response_wrapper
@require_POST
def obtain_jwt_token(request: HttpRequest):
    """Handle requests which are to obtain jwt token

    [route]: /api/token-auth

    [method]: POST
    """
    print("enter jwt token")
    data: dict = json.loads(request.body.decode())
    print(data)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")

    user = authenticate(username=data.get('username'), password=data.get('password'))

    if user is None:
        return failed_api_response(ErrorCode.UNAUTHORIZED, "用户名不存在或密码错误")

    state = user.state
    if state == 3:
        return failed_api_response(ErrorCode.REFUSE_ACCESS, "用户被封禁")
    print(user)
    '''
    if not user:
        user = super_authenticate(data.get('username'), data.get('password'))
        if not user:
            return failed_api_response(ErrorCode.UNAUTHORIZED, "Login or superuser Login required.")
        userInfo = getAdminUserInfo(user)
        
        result = {
            "userInfo":userInfo,
            "access_token": generate_access_token(user.id),
            "refresh_token": generate_refresh_token2(user),
        }
        
        return failed_api_response(ErrorCode.UNAUTHORIZED, "Login required.")
    '''

    userInfo = getUserInfo(user)
    print(userInfo)
    if(userInfo['institution']==None):
        userInfo['institution'] = ""
    result = {
        "userInfo":userInfo,
        "access_token": generate_access_token(user.id),
        "refresh_token": generate_refresh_token(user),
    }
    print(result)
    return success_api_response(result)


@csrf_exempt
@response_wrapper
@require_POST
def obtain_jwt_token_admin(request: HttpRequest):

    data: dict = json.loads(request.body.decode())
    print(data)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    user = authenticate(username=data.get('username'), password=data.get('password'))
    if user.is_superuser != 1:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "You are not superuser.")
    print(user)
    if user is None:
        return failed_api_response(ErrorCode.UNAUTHORIZED, "用户名不存在或密码错误")
    '''
    if not user:
        user = super_authenticate(data.get('username'), data.get('password'))
        if not user:
            return failed_api_response(ErrorCode.UNAUTHORIZED, "Login or superuser Login required.")
        userInfo = getAdminUserInfo(user)

        result = {
            "userInfo":userInfo,
            "access_token": generate_access_token(user.id),
            "refresh_token": generate_refresh_token2(user),
        }

        return failed_api_response(ErrorCode.UNAUTHORIZED, "Login required.")
    '''

    userInfo = getUserInfo(user)
    # print(userInfo)
    result = {
        "userInfo": userInfo,
        "access_token": generate_access_token(user.id),
        "refresh_token": generate_refresh_token(user),
    }
    # print(result)
    return success_api_response(result)

@csrf_exempt
@response_wrapper
@require_GET
def refresh_jwt_token(request: HttpRequest):
    """Handle requests which are to refresh the expired tokens

    [route]: /api/token-refresh

    [method]: GET
    """
    try:
        header = request.META.get("HTTP_AUTHORIZATION")
        if header is None:
            raise jwt.InvalidTokenError

        auth_info = header.split(" ")
        if len(auth_info) != 2:
            raise jwt.InvalidTokenError
        auth_type, auth_token = auth_info
        if auth_type != "Bearer":
            raise jwt.InvalidTokenError
        token = jwt.decode(auth_token, settings.SECRET_KEY, algorithms="HS256")
        if token.get("type") != "refresh_token":
            raise jwt.InvalidTokenError
        auth_record = AuthRecord.objects.filter(
            pk=token.get("record_pk")).first()
        if auth_record is None:
            raise jwt.InvalidTokenError
        if auth_record and auth_record.expires_by < timezone.now():
            raise jwt.ExpiredSignatureError
        user=User.objects.filter(id=token.get("user_id")).first()
        userInfo=getUserInfo(user)
        return success_api_response({"access_token": generate_access_token(token.get("user_id")),"userInfo":userInfo})
    except jwt.ExpiredSignatureError:
        return auth_failed("Token expired.")
    except jwt.InvalidTokenError:
        return auth_failed("Invalid token.")

'''
@response_wrapper
@require_GET
def refresh_jwt_token2(request: HttpRequest):
    """Handle requests which are to refresh the expired tokens

    [route]: /api/token-refresh

    [method]: GET
    """
    print('[DEBUG] now is refreshing superuser login')
    try:
        header = request.META.get("HTTP_TOKEN")
        if header is None:
            raise jwt.InvalidTokenError

        auth_info = header.split(" ")
        if len(auth_info) != 2:
            raise jwt.InvalidTokenError
        auth_type, auth_token = auth_info
        if auth_type != "Bearer":
            raise jwt.InvalidTokenError
        token = jwt.decode(auth_token, settings.SECRET_KEY, algorithms="HS256")
        if token.get("type") != "refresh_token":
            raise jwt.InvalidTokenError
        auth_record = AuthRecord2.objects.filter(
            pk=token.get("record_pk")).first()
        if auth_record is None:
            raise jwt.InvalidTokenError
        if auth_record and auth_record.expires_by < timezone.now():
            raise jwt.ExpiredSignatureError
        user = AdminUser.objects.filter(id=token.get("user_id")).first()
        userInfo = getAdminUserInfo(user)
        return success_api_response({"access_token": generate_access_token(token.get("user_id")),"userInfo":userInfo})
    except jwt.ExpiredSignatureError:
        return auth_failed("Token expired.")
    except jwt.InvalidTokenError:
        return auth_failed("Invalid token.")
'''


def jwt_auth():
    """JWT authorization and permission control decorator for REST APIs
    """
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            (flag, message, user_id) = verify_jwt_token(request)
            if not flag:
                return auth_failed(message)
            request_user = User.objects.filter(pk=user_id).first()
            if request_user is None:
                return auth_failed("Sorry, your account has been disabled.")
            request.user = request_user
            # permission check
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def getUserInfo(user):
    all_post = user.created_by.all().distinct()
    total_like = 0
    for post in all_post:
        total_like += post.likers.count()

    if user.state == 0 or user.state == 1 or user.state == 2:
        userInfo={
            'id': user.id,
            'username': user.username,
            'userpic': user.get_icon(),
            'nickname': user.nick_name,
            'email': user.email,
            'institution': user.institution,
            'usertype': user.user_type,
            'total_post': user.created_by.count(),
            'total_like': total_like,
            'total_fan': user.user_set.count(),
            'is_following': user.user_set.filter(id=user.id).exists(),
            'is_followed': user.followers.filter(id=user.id).exists(),
            'type': user.state,
        }
    elif user.state == 5:
        userInfo={
            'id': user.id,
            'username': user.username,
            'userpic': user.get_icon(),
            'nickname': user.nick_name,
            'email': user.email,
            'institution': user.institution,
            'usertype': user.user_type,
            'total_post': user.created_by.count(),
            'total_like': total_like,
            'total_fan': user.user_set.count(),
            'is_following': user.user_set.filter(id=user.id).exists(),
            'is_followed': user.followers.filter(id=user.id).exists(),
            'type': user.state,
            'enterprise_name': user.enterprise_info.name,
            'enterprise_address': user.enterprise_info.address,
            'enterprise_website': user.enterprise_info.website,
            'enterprise_instruction': user.enterprise_info.instruction,
            'enterprise_phone': user.enterprise_info.phone,
            'enterprise_legal_representative': user.enterprise_info.legal_representative,
            'enterprise_register_capital': user.enterprise_info.register_capital,
            'enterprise_field': user.enterprise_info.field
        }
    else:
        userInfo = {
            'id': user.id,
            'username': user.username,
            'userpic': user.get_icon(),
            'nickname': user.nick_name,
            'email': user.email,
            'institution': user.institution,
            'usertype': user.user_type,
            'total_post': user.created_by.count(),
            'total_like': total_like,
            'total_fan': user.user_set.count(),
            'is_following': user.user_set.filter(id=user.id).exists(),
            'is_followed': user.followers.filter(id=user.id).exists(),
            'type': user.state,
            'expert_name': user.expert_info.name,
            'expert_organization': user.expert_info.organization,
            'expert_field': user.expert_info.field,
            'expert_scholarprofile': user.expert_info.self_profile,
            'expert_phone': user.expert_info.phone,
        }
    return userInfo


def getAdminUserInfo(user):
    userInfo={
        'id': user.id,
        'username': user.nick_name,
    }
    return userInfo

'''
def super_authenticate(nickname,password):
    user = AdminUser.objects.filter(nick_name=nickname).first()
    if not user:
        return None
    if user.super_authenticate(nickname, password) is False:
        return None
    return user
'''
