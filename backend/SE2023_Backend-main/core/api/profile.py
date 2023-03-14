
from core.models.interpretation import Interpretation
from django.http import HttpRequest
from django.views.decorators.http import require_GET
from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)
from core.models.user import User


@response_wrapper
@jwt_auth()
@require_GET
def get_profile(request: HttpRequest):
    data: dict = request.GET.dict()
    user = request.user
    print(user.id)
    if data is not None:
        user_id = data.get('user_id')
        if user_id is not None:
            if User.objects.filter(pk=user_id).exists() is False:
                return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                           'User is not exist')
            user = User.objects.get(pk=user_id)

    all_post = user.created_by.all().distinct()
    total_like = 0
    total_collect = 0
    total_comment = 0

    for post in all_post:
        total_like += post.likers.count()
        total_collect += post.collectors.count()
        if post.id in Interpretation.objects.values_list('pk', flat=True):
            interpretation = Interpretation.objects.filter(pk=post.id).all()[0]
            total_comment += interpretation.comment_list.count()

    total_mycollect = 0

    for interpretation in Interpretation.objects.all():
        if user in interpretation.collectors.all():
            total_mycollect += 1

    if user.state == 0 or user.state == 1 or user.state == 2:
        data = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nick_name,
            'userpic': str(user.icon),
            'email': user.email,
            'type' : user.state,
            'institution': user.institution,
            'total_post': user.created_by.count(),
            'total_like': total_like,
            'total_collect': total_collect,
            'total_comment': total_comment,
            'total_mycollect': total_mycollect,
            'total_fan': user.user_set.count(),
            'total_follow': user.followers.count(),
            'is_following': user.user_set.filter(id=request.user.id).exists(),
            'is_followed': user.followers.filter(id=request.user.id).exists(),
            'state': user.state
        }
    elif user.state == 5:
        data = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nick_name,
            'userpic': str(user.icon),
            'email': user.email,
            'type': user.state,
            'institution': user.institution,
            'total_post': user.created_by.count(),
            'total_like': total_like,
            'total_collect': total_collect,
            'total_comment': total_comment,
            'total_mycollect': total_mycollect,
            'total_fan': user.user_set.count(),
            'total_follow': user.followers.count(),
            'is_following': user.user_set.filter(id=request.user.id).exists(),
            'is_followed': user.followers.filter(id=request.user.id).exists(),
            'state': user.state,
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
        data = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nick_name,
            'userpic': str(user.icon),
            'email': user.email,
            'type': user.state,
            'institution': user.institution,
            'total_post': user.created_by.count(),
            'total_like': total_like,
            'total_collect': total_collect,
            'total_comment': total_comment,
            'total_mycollect': total_mycollect,
            'total_fan': user.user_set.count(),
            'total_follow': user.followers.count(),
            'is_following': user.user_set.filter(id=request.user.id).exists(),
            'is_followed': user.followers.filter(id=request.user.id).exists(),
            'state': user.state,
            'expert_name': user.expert_info.name,
            'expert_organization': user.expert_info.organization,
            'expert_field': user.expert_info.field,
            'expert_scholarprofile': user.expert_info.self_profile,
            'expert_phone': user.expert_info.phone,
            'expert_title': user.expert_info.title,
        }
    return success_api_response(data)

