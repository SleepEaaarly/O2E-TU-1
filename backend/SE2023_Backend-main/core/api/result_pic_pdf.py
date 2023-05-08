from core.models.user import User
from django.http.request import HttpRequest
from core.api.utils import (require_http_methods, ErrorCode,
                            response_wrapper, wrapped_api,
                            success_api_response, failed_api_response)
from core.api.auth import jwt_auth
import os
from django.http import HttpResponse
from backend.settings import BASE_DIR
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@jwt_auth()
@response_wrapper
@require_http_methods('GET')
def get_res_pic(request: HttpRequest):
    """
    get result picture
    :param request:
    :return:
    """
    p = request.result
    return success_api_response({
        "pic": str(p.get_pic()),
    })

@csrf_exempt
#@jwt_auth()
@response_wrapper
@require_http_methods('POST')
def change_res_pic(request):
    """
    change result picture
    :param request:
        pic: new result picture
        res: the result id
    :return:
    """
    pic = request.FILES.get('pic')
    res_id = request.POST.get("res")
    res = User.objects.filter(id=res_id).first()
    res.picture = pic
    res.save()

    return success_api_response({
        "pic": str(res.picture),
    })

@csrf_exempt
@jwt_auth()
@response_wrapper
@require_http_methods('GET')
def get_res_pdf(request: HttpRequest):
    """
    get result pdf
    :param request:
    :return:
    """
    p = request.result
    return success_api_response({
        "pdf": str(p.get_pdf()),
    })


# @jwt_auth()
@csrf_exempt
@response_wrapper
@require_http_methods('POST')
def change_res_pdf(request):
    """
    change result picture
    :param request:
        file: new result pdf
        res: the result id
    :return:
    """
    pdf = request.FILES.get('file')
    res_id = request.POST.get("res")
    res = User.objects.filter(id=res_id).first()
    res.file = pdf
    res.save()

    return success_api_response({
        "pdf": str(res.file),
    })

@csrf_exempt
@response_wrapper
@require_http_methods('GET')
def read_pic(request: HttpRequest, year, day, file_name):
    imagepath = os.path.join(BASE_DIR, "static/images/{}/{}/res_pic/{}".format(year, day, file_name))
    with open(imagepath, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type="image/png")

@csrf_exempt
@response_wrapper
@require_http_methods('GET')
def read_default_pic(request: HttpRequest):

    imagepath=os.path.join(BASE_DIR, "static/images/default_result_pic.jpg")

    with open(imagepath, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type="image/png")


RES_PIC_API = wrapped_api({
    "GET": get_res_pic,
    "POST": change_res_pic,
})

RES_PDF_API = wrapped_api({
    "GET": get_res_pdf,
    "POST": change_res_pdf,
})
