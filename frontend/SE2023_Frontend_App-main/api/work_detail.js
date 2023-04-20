import axios from '@/config/requestConfig.js';
import time from '../common/time.js';
import {
    picUrl
} from './common.js'
export const getWork = async (id) => {
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
	// console.log("Get work before call " + id)
    let item = await axios.get("result/getinfo/" + id, {}, headers)
    let result = {
		"workName": item.title,
		"expert_name": item.expert_name,
		"expert_title": item.expert_title,
		"work_abstract": item.abstract,
		"expert_organization": item.expert_organization,
		"expert_logoPath": picUrl + item.expert_logo,
		"work_id": id,
		"expert_id": item.relate_expert_id,
		"user_id": item.uid,
		"work_pic": picUrl + item.result_pic ,
		"expert_mail": item.expert_email,
		"work_period": item.period,
		"work_field": item.field
	}
    return result
}