import axios from '@/config/requestConfig.js';

import {
    picUrl
} from './common.js'


//获取 专家-搜索
export const getWorkRec = async (paras) => {
    console.log("getWorkList OK.")
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
	//path->ai/resultRec/expert/int
	//path->ai/resultRec/enterprise/int
	var ret
	console.log(paras.type)
	if(paras.type==4){
		ret = await axios.get('ai/resultRec/expert/' + paras.id,
		    {},
		    headers)
	}else{
		ret = await axios.get('ai/resultRec/enterprise/' + paras.id,
		    {},
		    headers)
	}

    let result = ret.data
    if (result && result.length) {
        result = result.map((item) => {
            return {
                "result_id": item.result_id,
                "expert_id": item.expert_id,
                "userpic": picUrl + item.expert_icon, //picUrl + item.userpic,
                "field": item.field,
                'author': item.scholars,
                'title': item.title,
                'abstract': item.abstract,
                'date': item.pyear + "",
                'period': item.period,
                'content': item.content,
                'state': item.state,
				'work_logo': item.picture,
                'workpic': picUrl + file
            }
        })
    }
	console.log('ret result is')
    console.log(result)
    return result
}