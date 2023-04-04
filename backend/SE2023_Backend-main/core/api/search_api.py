import random
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import HttpRequest
from django.db.models import Q

from core.api.utils import (failed_api_response, ErrorCode,
                            success_api_response, parse_data,
                            wrapped_api, response_wrapper)
from core.models.user import User
from core.models.expert import Expert
from core.models.enterprise_info import Enterprise_info
from core.models.results import Results


@response_wrapper
# @jwt_auth()
@require_http_methods('GET')
def search_expert(request: HttpRequest, *args, **kwargs):
    data = request.GET.dict()
    key_word = data.get('key_word')
    organization = data.get('organization')
    field = data.get('field')
    title = data.get('title')

    key_words = ''
    if not (key_word is None or key_word == ''):  # not key_word 是判空，也可以判None
        key_words = key_word.split()
    print(key_words)
    data_results = []
    experts = Expert.objects.none()
    if key_words != '':
        for key_word in key_words:
            print(key_word)

            experts = experts.union(Expert.objects.filter(
                Q(name__icontains=key_word) | Q(organization__icontains=key_word) |
                Q(field__icontains=key_word) | Q(self_profile__icontains=key_word) |
                Q(phone__icontains=key_word) | Q(patent__icontains=key_word) |
                Q(paper__icontains=key_word) | Q(title__icontains=key_word)
            )
            )
        print(experts.count())
    else:
        experts = Expert.objects.all()
#    print(experts)
    # 专家库有脏数据，下面这个循环全部遍历会报错
    for expert in experts:

        if not (organization is None or organization == ''):
            if expert.organization != organization:
                continue
        if not (field is None or field == ''):
            fields = expert.field.split()
            if not fields.__contains__(field):
                continue
        if not (title is None or title == ''):
            if not expert.title != title:
                continue

        # print(expert)
        user = User.objects.get(expert_info=expert.id)
        expert_info = {
            "user_id": user.id,
            "expert_id": expert.id,
            "name": expert.name,
            "organization": expert.organization,
            "field": expert.field,
            "self_profile": expert.self_profile,
            "title": expert.title,
            "userpic": str(user.icon)
        }
    #    print(expert.id)
        data_results.append(expert_info)

    data_results = data_results[:10]
    print(data_results)
    return success_api_response({"data": data_results})


@response_wrapper
# @jwt_auth()
@require_http_methods('GET')
def search_enterprise(request: HttpRequest, *args, **kwargs):
    data = request.GET.dict()
    key_word = data.get('key_word')
    field = data.get('field')

    address = data.get('address')
    key_words = ''
    if not (key_word is None or key_word == ''):  # not key_word 是判空，也可以判None
        key_words = key_word.split()
    print(key_words)
    key_words = key_word.split()


    data_results = []
    enterprises = Enterprise_info.objects.none()

    if key_words != '':
        for key_word in key_words:
            enterprises = enterprises.union(Enterprise_info.objects.filter(
                Q(name__icontains=key_word) | Q(address__icontains=key_word) |
                Q(website__icontains=key_word) | Q(instruction__icontains=key_word) |
                Q(legal_representative__icontains=key_word) | Q(field__icontains=key_word) |
                Q(title__icontains=key_word)
            )
            )
        print(enterprises.count())
    else:
        enterprises = Enterprise_info.objects.all()

    for enterprise in enterprises:
        if not (address is None or address == ''):
            if enterprise.address != address:
                continue
        if not (field is None or field == ''):
            fields = enterprise.field.split()
            if not fields.__contains__(field):
                continue

        user = User.objects.get(enterprise_info=enterprise.id)
        enterprise_info = {
            "user_id": user.id,
            "enterprise_id": user.enterprise_info_id,
            "name": user.enterprise_info.name,
            "address": enterprise.address,
            "website": enterprise.website,
            "instruction": enterprise.instruction,
            "phone": enterprise.phone,
            "legal_representative": enterprise.legal_representative,
            "register_capital": enterprise.register_capital,
            "field": user.enterprise_info.field,
            "business_license": str(enterprise.business_license),
            "legal_person_ID": str(enterprise.legal_person_ID),
            "userpic": str(user.icon)
        }
        data_results.append(enterprise_info)
    data_results = data_results[:10]
    print(data_results)
    return success_api_response({"data": data_results})


@response_wrapper
# @jwt_auth()
@require_POST
def search_result(request: HttpRequest):
    data = parse_data(request)
    key_word = data.get('key_word')
    period = data.get('period')
    field = data.get('field')
    key_words = ''
    if not (key_word is None or key_word == ''):  # not key_word 是判空，也可以判None
        key_words = key_word.split()

    data_results = []
    results = Results.objects.none()
    if key_words != '':
        for key_word in key_words:
            results = results.union(Results.objects.filter(
                Q(title__icontains=key_word) | Q(abstract__icontains=key_word) |
                Q(scholars__icontains=key_word) | Q(period__icontains=key_word) |
                Q(content__icontains=key_word) | Q(field__icontains=key_word) | Q(pyear__icontains=key_word)
            )
            )
        print(results.count())
    else:
        results = Results.objects.all()

    for result in results:
        if not (period is None or period == ''):
            if result.address != result:
                continue
        if not (field is None or field == ''):
            fields = result.field.split()
            if not fields.__contains__(field):
                continue

        expert = Expert.objects.filter(expert_results=result.id)[0]
        user = User.objects.get(expert_info=expert.id)

        result_info = {
            "result_id": result.id,
            "expert_id": expert.id,
            "title": result.title,
            "abstract": result.abstract,
            "scholars": result.scholars,
            "pyear": result.pyear,
            "field": result.field,
            "period": result.period,
            "content": result.content,
            "state": result.state,
            "result_pic": result.get_pic(),
            "expert_icon": str(user.icon)
        }
        data_results.append(result_info)
    data_results = data_results[:10]
    return success_api_response({"data": data_results})


@response_wrapper
# @jwt_auth()
@require_POST
def search_mixture(request: HttpRequest):
    data = parse_data(request)
    key_word = data.get('key_word')
    key_words = ''
    if not (key_word is None or key_word == ''):  # not key_word 是判空，也可以判None
        key_words = key_word.split()
    data_res = []
    results = Results.objects.none()
    if key_words != '':
        for key_word in key_words:
            results = results.union(Results.objects.filter(
                Q(title__icontains=key_word) | Q(abstract__icontains=key_word) |
                Q(scholars__icontains=key_word) | Q(period__icontains=key_word) |
                Q(content__icontains=key_word) | Q(field__icontains=key_word) | Q(pyear__icontains=key_word)
            )
            )

        print(results.count())
    else:
        results = Results.objects.all()

    for result in results:

        expert = Expert.objects.filter(expert_results=result.id)[0]
        user = User.objects.get(expert_info=expert.id)

        result_info = {
            "result_id": result.id,
            "expert_id": expert.id,
            "title": result.title,
            "abstract": result.abstract,
            "scholars": result.scholars,
            "pyear": result.pyear,
            "field": result.field,
            "period": result.period,
            "content": result.content,
            "state": result.state,
            "result_pic": result.get_pic(),
            "expert_icon": str(user.icon)
        }
        data_res.append(result_info)
    data_res = data_res[:5]

    data_ent = []
    enterprises = Enterprise_info.objects.none()
    if key_words != '':
        for key_word in key_words:
            enterprises = enterprises.union(Enterprise_info.objects.filter(
                Q(name__icontains=key_word) | Q(address__icontains=key_word) |
                Q(website__icontains=key_word) | Q(instruction__icontains=key_word) |
                Q(legal_representative__icontains=key_word) | Q(field__icontains=key_word) |
                Q(title__icontains=key_word)
            )
            )
        print(enterprises.count())
    else:
        enterprises = Enterprise_info.objects.all()

    for enterprise in enterprises:
        user = User.objects.get(enterprise_info=enterprise.id)
        enterprise_info = {
            "user_id": user.id,
            "enterprise_id": user.enterprise_info_id,
            "name": user.enterprise_info.name,
            "address": enterprise.address,
            "website": enterprise.website,
            "instruction": enterprise.instruction,
            "phone": enterprise.phone,
            "legal_representative": enterprise.legal_representative,
            "register_capital": enterprise.register_capital,
            "field": user.enterprise_info.field,
            "business_license": str(enterprise.business_license),
            "legal_person_ID": str(enterprise.legal_person_ID),
            "userpic": str(user.icon)
        }
        data_ent.append(enterprise_info)
    data_ent = data_ent[:5]

    data_exp = []
    experts = Expert.objects.none()

    if key_words != '':
        for key_word in key_words:
            print(key_word)

            experts = experts.union(Expert.objects.filter(
                Q(name__icontains=key_word) | Q(organization__icontains=key_word) |
                Q(field__icontains=key_word) | Q(self_profile__icontains=key_word) |
                Q(phone__icontains=key_word) | Q(patent__icontains=key_word) |
                Q(paper__icontains=key_word) | Q(title__icontains=key_word)
            )
            )
        print(experts.count())
    else:
        experts = Expert.objects.all()

    for expert in experts:
        user = Expert.objects.get(expert_info=expert.id)
        expert_info = {
            "user_id": user.id,
            "expert_id": expert.id,
            "name": expert.name,
            "organization": expert.organization,
            "field": expert.field,
            "self_profile": expert.self_profile,
            "title": expert.title,
            "userpic": str(user.icon)
        }
        data_exp.append(expert_info)
    data_exp = data_exp[:5]

    data_results = [data_exp, data_res, data_ent]

    return success_api_response({"data": data_results})

