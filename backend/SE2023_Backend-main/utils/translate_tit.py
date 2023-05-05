from sql_util import get_all_entity, update

from urllib import request, parse
import json
from faker import Faker
from core.api.chatgpt import get_chatgpt_response
import time
from translate import Translator
from pygtrans import Translate

'''
class Trans(object):
    def __init__(self):
        self.url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

    def tran(self, text):
        index = text.find("http")
        text = text[:index]
        text = text.replace('\n', '').replace('#', '').replace('RT ', '').replace(':', '')
        ua = Faker().user_agent()
        headers = {
            'User-Agent': ua,
            'Host': 'fanyi.youdao.com',
            'Origin': 'http://fanyi.youdao.com',
            'Referer': 'http://fanyi.youdao.com/',
        }
        # 表单数据
        from_data = {
            'i': text,
            'from': 'UTO',
            'to': 'UTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
        }
        from_data = parse.urlencode(from_data).encode('utf-8')
        req = request.Request(self.url, from_data, headers)
        res = request.urlopen(req).read().decode("utf-8")
        target = json.loads(res)
        try:
            result = target['translateResult'][0][0]['tgt']
        except:
            result = "Translate failed"
        return result


def trans(content: str):
    pre = "如果以下内容是中文，将以下内容翻译为英文:"
    instr = pre + "\'" + content + "\'"
    return get_chatgpt_response(instr)
'''

entity_name = "core_need"

collection = get_all_entity(entity_name)

client = Translate()

for item in collection:
    lan = client.detect(item[1])
    if lan.language == 'en':
        update(entity_name, "title_eng", item[1], item[0])
    title_eng = client.translate(item[1], target='en')
    update(entity_name, "title_eng", title_eng.translatedText, item[0])
