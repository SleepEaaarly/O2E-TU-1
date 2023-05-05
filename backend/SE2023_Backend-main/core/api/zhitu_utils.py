from django.http import HttpRequest
import json
import requests


def search_expertID_by_paperID(id: int):
    """
    通过论文知兔ID获得作者知兔ID
    """
    url = "https://zhitulist.com/zhitu-data-service/search/paper?id="+str(id)
    response = requests.get(url)
    dic = json.loads(response.text)["data"]
    scholar_ids = []
    title = None
    if dic is not None and dic.__contains__("scholars"):
        scholars = dic["scholars"]
        for scholar in scholars:
            scholar_id = scholar["scholarId"]
            scholar_ids.append(scholar_id)
    if dic is not None and dic.__contains__("title"):
        title = dic["title"]
    return scholar_ids, title


def get_expertInfo_by_expertId(id: int):
    url = "https://zhitulist.com/zhitu-data-service/search/scholar?id="+str(id)
    response = requests.get(url)
    expert_name = None
    expert_organization = None
    expert_scholarprofile = None
    expert_phone = None
    dic = json.loads(response.text)['data']
    if dic is not None and dic.__contains__("scholarName"):
        expert_name = dic["scholarName"]
    if dic is not None and dic.__contains__("org"):
        expert_organization = dic["org"]
    if dic is not None and dic.__contains__("info"):
        expert_scholarprofile = dic["info"]
    if dic is not None and dic.__contains__("phone"):
        expert_phone = dic["phone"]
    ans = {
        "id": None,
        "username": None,
        "userpic": None,
        "nickname": None,
        "email": None,
        "institution": None,
        "usertype": None,
        "total_post": 0,
        "total_like": 0,
        "total_fan": 0,
        "is_following": False,
        "is_followed": False,
        "type": 4,
        "expert_name": expert_name,
        "expert_organization": expert_organization,
        "expert_field": None,
        "expert_scholarprofile": expert_scholarprofile,
        "expert_phone": expert_phone
    }
    return ans
