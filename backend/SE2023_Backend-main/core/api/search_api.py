import random
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import HttpRequest
from django.db.models import Q

from core.api.expert import field_decode
from core.api.utils import (failed_api_response, ErrorCode,
                            success_api_response, parse_data,
                            wrapped_api, response_wrapper)
from core.models.user import User
from core.models.expert import Expert
from core.models.enterprise_info import Enterprise_info
from core.models.results import Results


@response_wrapper
# @jwt_auth()
@require_POST
def search_expert(request: HttpRequest):
    data = parse_data(request)
    key_word = data.get('key_word')
    organization = data.get('organization')
    field = data.get('field')
    title = data.get('title')
    if key_word is None or key_word == '':  # not key_word 是判空，也可以判None
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "none key word")

    key_words = key_word.split()

    data_results = []
    experts = Expert.objects.none()
    for key_word in key_words:
        experts = experts.union(Expert.objects.filter(Q(name__icontains=key_word) | Q(organization__icontains=key_word)
                                                | Q(field__icontains=key_word)
                                                | Q(self_profile__icontains=key_word) | Q(phone__icontains=key_word)
                                                | Q(patent__icontains=key_word) | Q(paper__icontains=key_word) |
                                                      Q(title__icontains=key_word)).all().filter(state=0))
        print(experts.count())

    for expert in experts:
        if not (organization is None or organization == ''):
            if expert.organization != organization:
                continue
        if not (field is None or field == ''):
            if expert.field != field:
                continue
        if not (title is None or title == ''):
            titles = expert.title.split()
            if not titles.__contains__(title):
                continue

        user = Expert.objects.get(expert_info_id=expert.id)
        expert_info = {
            "user_id": user.id,
            "expert_id": expert.id,
            "name": expert.name,
            "ID_num": expert.ID_num,
            "organization": expert.organization,
            "field": field_decode(expert.field),
            "self_profile": expert.self_profile,
            "phone": expert.phone,
            "ID_pic": str(expert.ID_pic),
            "paper": expert.paper,
            "patent": expert.patent
        }
        data_results.append(expert_info)
    data_results = data_results[:10]
    return success_api_response({"data": data_results})


@response_wrapper
# @jwt_auth()
@require_POST
def search_enterprise(request: HttpRequest):
    data = parse_data(request)
    key_word = data.get('key_word')
    address = data.get('address')
    field = data.get('field')
    if key_word is None or key_word == '':  # not key_word 是判空，也可以判None
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "none key word")

    key_words = key_word.split()

    data_results = []
    enterprises = Enterprise_info.objects.none()
    for key_word in key_words:
        enterprises = Enterprise_info.union(Enterprise_info.objects.filter(Q(name__icontains=key_word) | Q(address__icontains=key_word)
                                                      | Q(website__icontains=key_word)
                                                      | Q(instruction__icontains=key_word) | Q(legal_representative__icontains=key_word)
                                                      | Q(field__icontains=key_word) |
                                                      Q(title__icontains=key_word)).all().filter(state=0))
        print(enterprises.count())

    for enterprise in enterprises:
        if not (address is None or address == ''):
            if enterprise.address != address:
                continue
        if not (field is None or field == ''):
            if enterprise.field != field:
                continue

        user = Enterprise_info.objects.get(enterprise_info_id=enterprise.id)
        expert_info = {
            "user_id": user.id,
            "enterprise_id": enterprise.id,
            "name": enterprise.name,
            "address": enterprise.address,
            "website": enterprise.website,
            "instruction": enterprise.instruction,
            "phone": enterprise.phone,
            "legal_representative": enterprise.legal_representative,
            "register_capital": enterprise.register_capital,
            "field": enterprise.field,
            "business_license": str(enterprise.business_license),
            "legal_person_ID": str(enterprise.legal_person_ID)
        }
        data_results.append(expert_info)
    data_results = data_results[:10]
    return success_api_response({"data": data_results})


@response_wrapper
# @jwt_auth()
@require_POST
def search_result(request: HttpRequest):
    data = parse_data(request)
    key_word = data.get('key_word')
    period = data.get('period')
    field = data.get('field')
    if key_word is None or key_word == '':  # not key_word 是判空，也可以判None
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "none key word")

    key_words = key_word.split()

    data_results = []
    results = Results.objects.none()
    for key_word in key_words:
        results = Results.union(Results.objects.filter(Q(title__icontains=key_word) | Q(abstract__icontains=key_word)
                                                      | Q(scholars__icontains=key_word)
                                                      | Q(instruction__icontains=key_word) | Q(legal_representative__icontains=key_word)
                                                      | Q(field__icontains=key_word) |
                                                      Q(title__icontains=key_word)).all().filter(state=0))
        print(enterprises.count())

    for enterprise in enterprises:
        if not (address is None or address == ''):
            if enterprise.address != address:
                continue
        if not (field is None or field == ''):
            if enterprise.field != field:
                continue

        user = Enterprise_info.objects.get(enterprise_info_id=enterprise.id)
        expert_info = {
            "user_id": user.id,
            "enterprise_id": enterprise.id,
            "name": enterprise.name,
            "address": enterprise.address,
            "website": enterprise.website,
            "instruction": enterprise.instruction,
            "phone": enterprise.phone,
            "legal_representative": enterprise.legal_representative,
            "register_capital": enterprise.register_capital,
            "field": enterprise.field,
            "business_license": str(enterprise.business_license),
            "legal_person_ID": str(enterprise.legal_person_ID)
        }
        data_results.append(expert_info)
    data_results = data_results[:10]
    return success_api_response({"data": data_results})

