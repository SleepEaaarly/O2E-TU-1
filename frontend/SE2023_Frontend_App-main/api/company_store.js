import axios from '@/config/requestConfig.js';

import {
    picUrl
} from './common.js'


//获取 专家-搜索
export const getCompanyList = async (paras) => {
    console.log("getCompanyList OK.")
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    let encode_text = encodeURIComponent(paras.key_word)
    let ret = await axios.get('search/enterprise?key_word=' + encode_text,
        paras,
        headers)
	let result = ret.data
    if (result && result.length) {
        result = result.map((item) => {
            return {
                "uid": item.user_id,
                "id": item.enterprise_id,
                "logoPath": picUrl + item.userpic, //picUrl + item.userpic,
                "area": item.field,
                'authorLogoPath': '', //picUrl + item.authorLogoPath,
                'title': item.name,
                'intro': item.instruction,
				"address": item.address
            }
        })
    }
    console.log(result)
    return result
}