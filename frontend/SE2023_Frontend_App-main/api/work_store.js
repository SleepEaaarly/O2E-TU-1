import axios from '@/config/requestConfig.js';

import {
    picUrl
} from './common.js'


//获取 专家-搜索
export const getWorkList = async (paras) => {
    // console.log("getWorkList OK.")
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    encode_text = encodeURIComponent(paras.key_word)
    let ret = await axios.get('search/result?key_word=' + encode_text,
        paras,
        headers)
    let result = ret.data
    if (result && result.length) {
        result = result.map((item) => {
            return {
                "result_id": item.result_id,
                "expert_id": item.expert_id,
                "authorLogoPath": picUrl + item.expert_icon, //picUrl + item.userpic,
                "field": item.field,
                'author': item.scholars,
                'title': item.title,
                'abstract': item.abstract,
                'date': item.pyear + "",
                'period': item.period,
                'content': item.content,
                'state': item.state,
				"workLogoPath": picUrl + item.result_pic
                // 'workpic': picUrl + file
            }
        })
    }
	// console.log('ret result is')
 //    console.log(result)
    return result
}