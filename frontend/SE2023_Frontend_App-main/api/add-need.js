import axios from '@/config/requestConfig.js';



export const addneed = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	// axios.setLoading(true)
	uni.showLoading({
		title: '需求同时生成报告中，请稍等'
	});
	let result = await axios.post('need', data, headers)
	uni.hideLoading()
	return result
}

export const saveneed = async (data) => {
	let result = addneed(data)
	return result
}