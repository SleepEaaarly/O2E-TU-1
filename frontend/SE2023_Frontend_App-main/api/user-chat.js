import axios from '@/config/requestConfig.js';
import time from '../common/time.js'
import {
	picUrl
} from './common.js'

export const  getContact = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	//console.log(data)
	let result = await axios.get("need/get_contact",data,headers)
	//console.log("getContact "+result.error_msg)
	return result
}

export const  getOrder = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	//console.log(data)
	let result = await axios.get("order/get",data,headers)
	//console.log("getOrder "+result.order_id)
	return result
}

export const createOrder = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	
	console.log(data)
	let result = await axios.post("order",data,headers)
	console.log("createOrder "+result.error_msg)
	return result
}
/*
export const acceptOrder = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	
	//console.log(data)
	let result = await axios.post("order",data,headers)
	//console.log("createOrder "+result.error_msg)
	return result
}

export const refuseOrder = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	
	//console.log(data)
	let result = await axios.post("order",data,headers)
	//console.log("createOrder "+result.error_msg)
	return result
}
*/
export const pushMessage = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	axios.setLoading(false);
	
	let result = await axios.post("chat/push",data,headers)
	axios.setLoading(true);
	return result
}

export const createChat = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.post('chat/create',data,headers)
	return result
}


export const getChat = async (id,userInfo) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let item = await axios.get('chat/'+id,{},headers)
	let result= {}
	if (item) {
			let fid = userInfo.id == item.from_user_id ? item.to_user_id : item.from_user_id
			let sendTime = time.gettime.gettime(new Date())
			let message = ''
			let msgList = item.message_list
			result = {
				id: item.chatroom_id,
				fid: fid,
				fromId: item.from_user_id,
				toId: item.to_user_id,
				afterTime: +new Date(item.afterTime),
				userpic: item.from_user_id==userInfo.id?picUrl+item.to_user_pic:picUrl+item.from_user_pic,
				username: item.from_user_id==userInfo.id?item.to_user_name:item.from_user_name,
				time: sendTime,
				name: item.from_user_id==userInfo.id?item.to_user:item.from_user,
				message: message,
				noreadnum: 0,
				messages: msgList
			}
	}
	return result
}
