import axios from '@/config/requestConfig.js';
import time from '../common/time.js';

import {
	picUrl
} from './common.js'

export const getNeedDetail = async(id) => {
	console.log("id is" + id)
	console.log("getNeedDetail")
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	
	let result = await axios.get('need/'+ id, {}, headers)
	// console.log("result is:" + result)
	// if (result && result.data && result.data.order && result.data.order.length) {
	// 	// for(let x of result.data.order){
	// 	for (var i = 0; i < result.data.order.length; i++) {
	// 			result.data.order[i].expert_icon = picUrl + result.data.order[i].expert_icon
	// 		}
	// 	// }
	// }
	
	if (result && result.order && result.order.length) {

		for (var i = 0; i < result.order.length; i++) {
				result.order[i].expert_icon = picUrl + result.order[i].expert_icon
			}

	}
	return result
}
export const createContact = async(data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.post("need/contact", data, headers)
	console.log(result.error_msg)
	return result
}