import axios from '@/config/requestConfig.js';

import {
    picUrl
} from './common.js'


export const getExpertList = async (paras) => {
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    encode_text = encodeURIComponent(paras.key_word)
    let ret = await axios.get('search/expert?key_word=' + encode_text,
        paras,
        headers)
	let result = ret.data
    if (result && result.length) {
        result = result.map((item) => {
            return {
                "uid": item.user_id,
                "id": item.expert_id,
                "userpic": picUrl + item.userpic, //picUrl + item.userpic,
                "tags": item.field,
                'authorLogoPath': '', //picUrl + item.authorLogoPath,
                'author': item.name,
                'title': item.title,
                'institution': item.organization,
                'intro': item.self_profile,
            }
        })
    }
    return result
}


export const getExpertByID = async (uid) => {
    console.log('getExpertByID')
    let headers = { 'Authorization': 'Bearer ' + uni.getStorageSync('token') }

    // console.log(uid)

    let result = await axios.get('expert/' + uid, headers)

    result = result.data

    return result
}