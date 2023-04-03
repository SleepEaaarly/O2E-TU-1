from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)

from core.models import Papers, Patents, Projects, User, Expert, Results

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
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "Invalid request args.")
    print(data)

    title = data.get('title')
    cites = data.get('cites')
    pyear = data.get('pyear').split('-')[0]
    isEI = data.get('isEI')
    isSCI = data.get('isSCI')
    url = data.get('url')
    scholars = data.get('scholars')
    id = data.get('id')

    paper = Papers(title=title, cites=cites, pyear=pyear, isEI=isEI, isSCI=isSCI,
                   url=url, scholars=scholars)
    paper.save()

    user = User.objects.get(id=id)
    expert_id = user.expert_info_id

    expert = Expert.objects.get(id=expert_id)
    expert.papers.add(paper)
    expert.save()

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
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "Invalid request args.")
    print(data)

    title = data.get('title')
    pyear = data.get('pyear').split('-')[0]
    url = data.get('url')
    scholars = data.get('scholars')
    id = data.get('id')

    patent = Patents(title=title, pyear=pyear, url=url, scholars=scholars)
    patent.save()

    user = User.objects.get(id=id)
    expert_id = user.expert_info_id

    expert = Expert.objects.get(id=expert_id)
    expert.patents.add(patent)
    expert.save()

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
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "Invalid request args.")
    print(data)

    title = data.get('title')
    start_year = data.get('start_time').split('-')[0]
    end_year = data.get('end_time').split('-')[0]
    type_first = data.get('type_first', None)
    type_second = data.get('type_second', None)
    type_third = data.get('type_third', None)
    url = data.get('url')
    scholars = data.get('scholars')
    id = data.get('id')

    print("2")

    project = Projects(title=title, startYear=start_year, endYear=end_year, url=url, scholars=scholars,
                       typeFirst=type_first, typeSecond=type_second, typeThird=type_third)

    print("3")
    project.save()
    user = User.objects.get(id=id)
    expert_id = user.expert_info_id
    expert = Expert.objects.get(id=expert_id)
    expert.projects.add(project)
    expert.save()

    return success_api_response({})


@jwt_auth()
@require_POST
@response_wrapper
def add_result(request: HttpRequest):

    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "Invalid request args.")
    print(data)

    title = data.get('title')
    abstract = data.get('abstract')
    scholars = data.get('scholars')
    pyear = data.get('pyear').split('-')[0]
    field = data.get('field')
    period = data.get('period')
    picture = data.get('picture')
    content = data.get('content')
    file = data.get('file')
    id = data.get('id')

    print("2")

    result = Results(title=title, abstract=abstract, scholars=scholars, pyear=pyear, field=field,
                     period=period, picture=picture, content=content, file=file, state=0)

    print("3")
    result.save()
    user = User.objects.get(id=id)
    expert_id = user.expert_info_id
    expert = Expert.objects.get(id=expert_id)
    expert.results.add(result)
    expert.save()

    return success_api_response({})
