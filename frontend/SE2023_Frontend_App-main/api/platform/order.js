import axios from '@/config/requestConfig.js'

import{ picUrl, } from '@/api/common.js'

//清洗result格式的函数
function purifyKeys(item){
	let purified_result = {
		state: item.state,
		order_id: item.order_id,						//订单id
		//state: item.state,							//订单状态
		//ctime: item.create_time,						//订单创建时间
		//etime: item.end_time,							//订单结束时间
		entp_id: item.need.enterprise_id,				//企业id
		entp_name: item.need.enterprise_name,			//企业名称
		description: item.need.enterprise_description,	//企业描述
		headpic: picUrl + item.need.enterprise_pic,		//企业头像url地址
		exp_id: item.expert_id,							//专家id
		exp_name: item.expert_name,						//专家姓名
		exp_pic: picUrl + item.expert_pic, 				//专家头像
		exp_des: item.expert_description,  				//专家描述
		title: item.need.title,							//需求名称
		time: item.end_time,							//时间
		need_id: item.need.need_id
	}
	if(purified_result.description === 'undefined' || purified_result.description === null || purified_result.description === ''){
		purified_result.description = 'Lux et veritas'
	}
	if(purified_result.time === 'undefined' || purified_result.time === null || purified_result.time === ''){
		purified_result.time = item.create_time
	}
	return purified_result
}

// 获得已经完成的订单
export const getFinishedOrder = async uid => {
	console.log('getFinishedOrder')
	let result = await axios.get('user/' + uid + '/order/finished')
	result = result.data
	
	//清洗数据格式
	if(result && result.length){
		result = result.map(item=>{
			return purifyKeys(item)
		})
	}
	//否则返回空值
	return result
}

// 获得进行中的订单
export const getCooperatingOrder = async uid => {
	console.log('getCooperatingOrder')
	let result = await axios.get('user/' + uid + '/order/cooperating')
	result = result.data
	
	//清洗数据格式
	if(result && result.length){
		result = result.map(item=>{
			return purifyKeys(item)
		})
	}
	//否则返回空值
	return result
}

// 获得待处理的订单
export const getPendingOrder = async uid => {
	console.log('getPendingOrder')
	let result = await axios.get('user/' + uid + '/order/pending')
	result = result.data
	
	//清洗数据格式
	if(result && result.length){
		result = result.map(item=>{
			return purifyKeys(item)
		})
	}
	//否则返回空值
	return result
}

// 获得全部订单
export const getAllOrder = async uid => {
	console.log('getAllOrder')
	let result = await axios.get('user/' + uid + '/order/all')
	console.log(result)
	result = result.data
	
	//清洗数据格式
	if(result && result.length){
		result = result.map(item=>{
			return purifyKeys(item)
		})
	}
	//否则返回空值
	return result
}


/****** 以下为专家操作 *****/

// 接受某订单
export const acceptOrder = async (uid,id) => {
	console.log('acceptOrder')
	let headers = { 'Authorization':'Bearer ' + uni.getStorageSync('token') }
	let result = await axios.post('user/' + uid + '/order/' + id + '/accept',{},headers)
	
	
	
	//todo 是否操作成功？
	
	

	return result
}

// 拒绝某订单
export const rejectOrder = async (uid,id) => {
	console.log('rejectOrder')
	let headers = { 'Authorization':'Bearer ' + uni.getStorageSync('token') }
	let result = await axios.post('user/' + uid + '/order/' + id + '/refuse',{},headers)		//为啥不叫reject？？好别扭
	
	return result
}

export const abandonOrder = async (uid,id) => {
	let headers = { 'Authorization':'Bearer ' + uni.getStorageSync('token') }
	let result = await axios.post('user/' + uid + '/order/' + id + '/abandon',{},headers)
	
	return result
}

export const accomplishOrder = async (uid,id) => {
	console.log('accomplishOrder')
	let headers = { 'Authorization':'Bearer ' + uni.getStorageSync('token') }
	let result = await axios.post('user/' + uid + '/order/' + id + '/finish',{},headers)
	console.log(result.error_msg)

	return result
}