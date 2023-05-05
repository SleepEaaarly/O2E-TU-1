import axios from '@/config/requestConfig.js';

export const  editneed =async (company_id, need_id, data) => {
	console.log("company_id is:" + company_id)
	console.log("need_id is:" + need_id)
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.post('user/' + company_id + "/need/" + need_id + "/edit", data, headers)
	console.log("edit result:" + result.code + " " + result)
	return result
}