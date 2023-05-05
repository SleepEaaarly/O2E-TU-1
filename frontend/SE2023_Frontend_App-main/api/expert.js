import axios from '@/config/requestConfig.js'
import time from '../common/time.js'

import { picUrl } from './common.js'

//清洗result函数的格式
function purifyPapers(item){
	let purified_result = {
		type: 0,	// 0=论文，1=专利，2=项目
		strType: '论文',
		title: item.title,		//标题
		scholars: item.scholars,	//所有作者
		pyear: String(item.pyear),		//发表年限
		cites: '引用次数：' + item.cites,	//引用次数
	}
	if(purified_result.pyear === 'undefined' || purified_result.pyear === null || purified_result.pyear === ''){
		purified_result.pyear = '未知年份'
	}
	return purified_result
}

function purifyPatents(item){
	let purified_result = {
		type: 1,	// 0=论文，1=专利，2=项目
		strType: '专利',
		title: item.title,		//标题
		scholars: item.scholars,	//所有作者
		pyear: String(item.pyear),		//发表年限
		description: '详情介绍: ' + item.url,
	}
	if(purified_result.pyear === 'undefined' || purified_result.pyear === null || purified_result.pyear === ''){
		purified_result.pyear = '未知年份'
	}
	return purified_result
}

function purifyProjects(item){
	let purified_result = {
		type: 2,	// 0=论文，1=专利，2=项目
		strType: '项目',
		title: item.title,		//题目
		scholars: item.scholars,	//所有作者
		pyear: item.startYead + '-' + item.endYear,		//发表年限
		description: '详情介绍: ' + item.url,
	}
	if(item.endYear === null){
		purified_result.pyear = item.startYead + '-' + '至今'
	}
	if(purified_result.pyear === 'undefined' || purified_result.pyear === null){
		purified_result.pyear = '未知年份'
	}
	let str = ""
	if(item.typeFirst !== null){
		str = str.concat(item.typeFirst)	//项目级别
		if(item.typeSecond !== null){
			str = str.concat(", " + item.typeSecond)
			if(item.typeThird !== null){
				str = str.concat(", " + item.typeThird)
			}
		}
		purified_result.description = str.concat("。" + purified_result.description)
	}
	
	return purified_result
}

export const getExpertInfo = async(uid, type) => {
	// type为papers、patents、projects三类
	console.log('getExpertInfo')
	let headers = { 'Authorization':'Bearer ' + uni.getStorageSync('token') }
	
	// console.log(uid)
	
	let result = await axios.get('expert/' + uid, { 'tab':type, }, headers)
	
	result = result.data
	
	// console.log(result)
	
	//清洗数据格式
	if(result && result.length){
		result = result.map(item=>{
			switch(type){
				case 'papers':
					return purifyPapers(item)
				case 'patents':
					return purifyPatents(item)
				case 'projects':
					return purifyProjects(item)
			}
			
		})
	}
	
	
	return result
}