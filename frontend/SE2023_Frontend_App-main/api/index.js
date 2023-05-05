import axios from '@/config/requestConfig.js';
import time from '../common/time.js';

// import {
// 	picUrl
// } from './common.js'

//获取 首页-热榜
export const getTopicList = async () => {
	let picUrl = "http://116.63.14.146:8000/api"
	console.log("getTopicList OK.")
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.get('recommend', {}, headers)
	let index = 0
	
	if(result && result.length){
		result = result.map((item)=>{
			index = index + 1
			return{
				"createTime": time.gettime.gettime(item.created_at),
				"content": item.title,
				"id": item.id,
				"userpic": picUrl + item.userpic,
				"username": item.created_by.username,
				"index": index,
			}
		})
	}
	console.log(result)
	return result
}

//获取 首页-推荐
export const getRecommendList = async () => {
	console.log("getRecommendList OK.")
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.get('Interpretation/popup',{},headers)
	if(result && result.length){
		result = result.map((item)=>{
			return{
				"created_at": time.gettime.gettime(item.created_at),
				"content": item.content,
				"title":item.title,
				"isguanzhu":item.isguanzhu,
				"is_like":item.is_like,
				"is_favor":item.is_favor,
				"commentNum": item.commentNum,
				"like_num": item.like_num,
				"favor_num": item.favor_num,
				"id":item.id,
				"userpic": picUrl+item.userpic,
				"username" : item.created_by.username,
				"uid":item.uid,
				"tags":item.tags
			}
		})
	}
	return result
}
