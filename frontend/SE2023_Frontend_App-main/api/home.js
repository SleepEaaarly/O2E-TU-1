import axios from '@/config/requestConfig.js';
export const  getUserProfile =async (uId) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let data = await axios.post('user/profile',{
		user_id: uId
	},headers)
	return data
}

// export const  giveLike = async (data) => {
// 	let result = await axios.post('topic/active',data);
// 	return result
// }
