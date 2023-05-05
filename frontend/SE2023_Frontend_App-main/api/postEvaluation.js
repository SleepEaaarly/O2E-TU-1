import axios from '../config/requestConfig.js'
import{ picUrl, } from '@/api/common.js'

// 提交评价
export const postEvaluation = async data => {
	console.log('postEvaluation')
	let result = await axios.post('order/rate', { 'formData':data })
	return result
}

// 订单id => 评价
export const orderToEvaluation = async data => {
	console.log('orderToEvaluation')
	let result = await axios.get('order/'+data+'/rate')
	return result
}

// 用户id => 评价
export const idToEvaluation = async data => {
	console.log('idToEvaluation')
	let result = await axios.get('user/'+data+'/rate')
	if(result && result.code){
		console.log(result)
	}else{
		let x=0
		let l = result.data.length
		for(x = 0;x<l;x++){
			result.data[x].expert.expert_icon = picUrl+result.data[x].expert.expert_icon
			result.data[x].enterprise.enterprise_icon = picUrl+result.data[x].enterprise.enterprise_icon
		}
	}
	
	return result
}