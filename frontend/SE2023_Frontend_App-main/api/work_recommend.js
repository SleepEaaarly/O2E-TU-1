import axios from '@/config/requestConfig.js';

import {
    picUrl
} from './common.js'


//获取 专家-搜索
export const getWorkRec = async (paras) => {
    // console.log("getWorkList OK.")
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
	//path->ai/resultRec/expert/int
	//path->ai/resultRec/enterprise/int
	var ret
	var result
	// console.log(paras.type)
	if(paras.type==4){
		ret = await axios.get('ai/resultRec/expert/' + paras.id + '/' + paras.shuffle,
		    {},
		    headers)
		result = ret.results
	}else if(paras.type==5){
		ret = await axios.get('ai/resultRec/enterprise/' + paras.id + '/' + paras.shuffle,
		    {},
		    headers)
		result = ret.results
	}else{
		result = []
	}
	// console.log(result)
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