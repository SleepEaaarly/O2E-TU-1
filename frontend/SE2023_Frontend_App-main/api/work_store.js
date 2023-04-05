import axios from '@/config/requestConfig.js';

import {
    picUrl
} from './common.js'


//获取 专家-搜索
export const getWorkList = async (paras) => {
    console.log("getWorkList OK.")
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    let ret = await axios.get('search/work?key_word=' + paras.key_word,
        paras,
        headers)
    let result = ret.data
    if (result && result.length) {
        result = result.map((item) => {
            return {
                "result_id": item.result_id,
                "expert_id": item.expert_id,
                "userpic": picUrl + item.expert_icon, //picUrl + item.userpic,
                "field": item.field,
                'authorLogoPath': '', //picUrl + item.authorLogoPath,
                'author': item.scholars,
                'title': item.title,
                'abstract': item.abstract,
                'intro': item.self_profile,
                'date': item.pyear,
                'period': item.period,
                'content': item.content,
                'state': item.state,
                'workpic': picUrl + result_pic
            }
        })
    }
    console.log(result)
    return result
}