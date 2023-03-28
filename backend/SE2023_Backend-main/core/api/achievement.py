from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)

from core.models import Papers, Patents, Projects

'''
    add paper
    [method]: POST
    [route]: /api/paper/add
    
    params:
        - title
        - cites
        - pyear
        - isEI
        - isSCI
        - url
        - scholars
    
    return 
        - OK
'''


@jwt_auth()
@require_POST
@response_wrapper
def add_paper(request: HttpRequest):
    # 审核过程 TODO
    title = request.POST.get('title', None)
    if title is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid title")
    cites = request.POST.get('cites', None)
    if cites is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid cites")
    pyear = request.POST.get('pyear', None)
    if pyear is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid publish_year")
    isEI = request.POST.get('isEI', None)
    if isEI is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid isEI")
    isSCI = request.POST.get('isSCI', None)
    if isSCI is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid isSCI")
    url = request.POST.get('url', None)
    if url is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid url")
    scholars = request.POST.get('scholars', None)
    if scholars is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid scholars")

    paper = Papers(title=title, cites=cites, pyear=pyear, isEI=isEI, isSCI=isSCI,
                   url=url, scholars=scholars)

    paper.save()

    return success_api_response({})


'''
    add patent
    [method]: POST
    [route]: /api/patent/add
    
    params:
        - title
        - pyear
        - url
        - scholars
    
    return 
        - OK
'''


@jwt_auth()
@require_POST
@response_wrapper
def add_patent(request: HttpRequest):
    # 审核过程 TODO

    title = request.POST.get('title', None)
    if title is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid title")
    pyear = request.POST.get('pyear', None)
    if pyear is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid publish_year")
    url = request.POST.get('url', None)
    if url is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid url")
    scholars = request.POST.get('scholars', None)
    if scholars is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid scholars")

    patent = Patents(title=title, pyear=pyear, url=url, scholars=scholars)
    patent.save()

    return success_api_response({})


'''
    add project
    [method]: POST
    [route]: /api/project/add

    params:
        - title
        - start_year
        - end_year
        - type_first
        - type_second
        - type_third
        - url
        - scholars

    return 
        - OK
'''


@jwt_auth()
@require_POST
@response_wrapper
def add_project(request: HttpRequest):
    # 审核过程 TODO

    title = request.POST.get('title')
    if title is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid title")
    start_year = request.POST.get('start_year')
    if start_year is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid start_year")
    end_year = request.POST.get('end_year')
    if end_year is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid end_year")
    type_first = request.POST.get('type_first', None)
    type_second = request.POST.get('type_second', None)
    type_third = request.POST.get('type_third', None)
    url = request.POST.get('url')
    if url is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid url")
    scholars = request.POST.get('scholars')
    if scholars is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid scholars")

    project = Projects(title=title, start_year=start_year, end_year=end_year, type_first=type_first,
                       type_second=type_second, type_third=type_third, url=url, scholars=scholars)
    project.save()

    return success_api_response({})