from django.http import HttpRequest
from core.api.utils import (failed_api_response, ErrorCode,
                            success_api_response, parse_data,
                            wrapped_api, response_wrapper)

@response_wrapper
def test0524(request: HttpRequest):
    data: dict = parse_data(request)

    print(data["data"])

    return success_api_response({})