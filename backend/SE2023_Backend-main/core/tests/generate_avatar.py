from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import HttpRequest
from core.api.utils import (failed_api_response, ErrorCode,
                            success_api_response, parse_data,
                            wrapped_api, response_wrapper)
from core.models.user import User
from core.api.sign_up import get_avatar
from backend.settings import BASE_DIR

@response_wrapper
def avatar(request: HttpRequest):
    users = User.objects.filter(icon='images/default_user_icon.jpg')
    # for user in users:
    for user in users:
        email = user.email
        username = user.username
        print(username)
        try:
            avatar = get_avatar(email)
            with open(BASE_DIR + "/static/" + "images/202205/02/icons/"  + username + ".jpg", 'wb') as f:
                f.write(avatar.content)
            user.icon = 'images/202205/02/icons/' + username + ".jpg"
            user.save()
        except Exception as e:
            print(e)
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "error generating avatar")
    return success_api_response({})

@response_wrapper
@require_GET
def get_user_num(request: HttpRequest):
    
    count = User.objects.count() - 3

    return success_api_response({"count": count})