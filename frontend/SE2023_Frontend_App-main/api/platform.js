import axios from '@/config/requestConfig.js'
import time from '../common/time.js'

import { picUrl } from './common.js'

// 处理need格式
async function purifyResult(item){
	let purified_result = {
		'need_id': item.need_id,
		'address': item.address,
		'title': item.title,
		'description': item.description,
		'start_time': item.start_time,
		'end_time': item.end_time,
		'money': item.money,
		'field': item.field,
		'state': item.state,
		'emergency': item.emergency,
		'predict': item.predict,
		'real': item.real,
	}

	if(purified_result.description === 'undefined' || purified_result.description === null){
		purified_result.pyear = '暂无详情'
	}
	// 新增专家、头像url属性
	purified_result.experts = await getMatchedExperts(item.need_id)
	// console.log('清洗！！！')
	// console.log(purified_result)
	return purified_result
}

function purifyMatchedExperts(item){
	let purified_result = {
		'expert_id': item.expert_id,
		'scholar_id': item.scholar_id,
		'name': item.name,
		'pic': picUrl + item.icon_url,
	}
	
	if(purified_result.scholar_id === 'undefined' || purified_result.scholar_id === null){
		purified_result.pyear = '暂无知兔专家id'
	}
	
	// console.log(purified_result)
	return purified_result
}

// 获取全部“待解决”需求（发现页面展示）
export const getAllNeed =async () => {
	console.log('getAllNeed')
	let headers = { 'Authorization':'Bearer ' + uni.getStorageSync('token') }
	let result = await axios.get('need/all', {}, headers)
	result = result.data
	// console.log("result is:" + result)
	
	//清洗数据格式
	if(result && result.length){
		for(let x of result){
			if(x.description === 'undefined' || x.description === null){
				x.pyear = '暂无详情'
			}
			// x.experts = await getMatchedExperts(item.need_id)
			
			// let headers = { 'Authorization':'Bearer ' + uni.getStorageSync('token') }
			// let experts = await axios.get('need/'+x.need_id+'/allexperts', {}, headers)
			// experts = experts.data
			// let experts_new = [];
			// if(experts && experts.length) {
			// 	for (let i of experts) {
			// 		let expert = {
			// 			'expert_id': i.expert_id,
			// 			'scholar_id': i.scholar_id,
			// 			'name': i.name,
			// 			'pic': picUrl + i.icon_url,
			// 		}
			// 		if(expert.scholar_id === 'undefined' || expert.scholar_id === null){
			// 			expert.pyear = '暂无知兔专家id'
			// 		}
			// 		experts_new.push(expert);
			// 	}
			// }
			// x.experts = experts_new;
			for (var i = 0; i < x.experts.length; i++) {
				x.experts[i].expert_icon = picUrl + x.experts[i].expert_icon
			}
		}
		return result
		
		// result = result.map(item=>{
		// 	res =  await purifyResult(item)
		// 	return res
		// })
	}
	
	return result
}

export const getAllList =async () => {
	let headers = { 'Authorization':'Bearer ' + uni.getStorageSync('token') }
	let result = await axios.get(url = 'platform', data = {}, headers)
	
	//result 参照接口文档
	if(result&&result.length){
		result = result.data
	}
	return result
}

//获取已完成需求
export const getFinishedNeed =async data => {
	let result = await axios.get(url = 'platform', data = {}, this.data)
	
	//result 参照接口文档
	if(result&&result.length){
		result = result.data
	}
	return result
}

//获取进行中需求
export const getProcedingNeed =async data => {
	//TODO:如何传递参数进来
	let headers = { 'Authorization':'Bearer ' + uni.getStorageSync('token') }
	let result = await axios.get(url = 'platform', data = {}, headers)
	
	//result 参照接口文档
	if(result&&result.length){
		result = result.data
		// result = result.map((item)=>{
		// 	index = index + 1
		// 	return{
				
		// 	}
		// })
	}
	return result
}

//发布新需求
export const postNewNeed =async data => {
	//TODO:如何传递参数进来
	// let headers = {
	// 	"Authorization":'Bearer ' + uni.getStorageSync('token')
	// }
	let result = await axios.post(url = 'platform', data)
	
	//result 参照接口文档
	// if(result&&result.length){
	// 	result = result.data
	// 	// result = result.map((item)=>{
	// 	// 	index = index + 1
	// 	// 	return{
				
	// 	// 	}
	// 	// })
	// }
	return result
}

// 获取某个需求的全部已对接专家及头像url，传入需求id
export const getMatchedExperts =async id => {
	let headers = { 'Authorization':'Bearer ' + uni.getStorageSync('token') }
	
	let result = await axios.get('need/'+id+'/allexperts', {}, headers)
	result = result.data
	
	if(result && result.length) {
		result = result.map(item=>{
			return purifyMatchedExperts(item)
		})
	}
	// console.log(result)
	return result
}
