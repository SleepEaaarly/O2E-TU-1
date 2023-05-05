import axios from '@/config/requestConfig.js'

export const submitForm = async data => {
	console.log('submitForm')
	console.log(data)
	let result = await axios.post('user/feedback', data)
	return result
}

export const getReplied = async (id) => {
	console.log('getReplied')
	let result = await axios.get('user/'+id+'/feedback/replied')
	if(result.errCode){
		console.log(result.errMsg)
	}
	return result
}

export const getUnreplied = async (id) => {
	console.log('getUnreplied')
	let result = await axios.get('user/'+id+'/feedback/unreplied')
	if(result.errCode){
		console.log(result.errMsg)
	}
	return result
}