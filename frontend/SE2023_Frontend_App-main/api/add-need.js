import axios from '@/config/requestConfig.js';



export const addneed = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.post('need', data, headers)
	return result
}

export const saveneed = async (data) => {
	let result = addneed(data)
	return result
}