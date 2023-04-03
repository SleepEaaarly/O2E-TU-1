import axios from '@/config/requestConfig.js';

import {
    picUrl
} from './common.js'


//获取 专家-搜索
export const getExpertList = async (searchText = '') => {
    console.log("getExpertList OK.")
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    let result = await axios.get('expert/search?key_word=' + searchText, {}, headers)
	console.log('Experts:')
	console.log(result)
    if (result && result.length) {
        result = result.map((item) => {
            return {
                "id": item.id,
                "userpic":  '', //picUrl + item.userpic,
                "tags": item.field,
                'authorLogoPath': '', //picUrl + item.authorLogoPath,
                'author': item.author,
                'title': item.title,
                'institution': item.institution,
                'intro': item.intro,
            }
        })
    }
    console.log(result)
    return result
}
