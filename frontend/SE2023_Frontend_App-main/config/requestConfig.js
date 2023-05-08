import request from "./request";

// let baseUrl=process.env.NODE_ENV === 'development'?"http://127.0.0.1:8000/api/":"http://127.0.0.1:8000/api/";
// let socketBaseUrl=process.env.NODE_ENV === 'development'?"ws://127.0.0.1:8000/api/":"ws://127.0.0.1:8000/api/";

let baseUrl=process.env.NODE_ENV === 'development'?"http://116.63.14.146:8000/api/":"http://116.63.14.146:8000/api/";
let socketBaseUrl=process.env.NODE_ENV === 'development'?"ws://116.63.14.146:8000/api/":"ws://116.63.14.146:8000/api/";
//可以new多个request来支持多个域名请求
//let picUrl = "http://127.0.0.1:8000/api/"	统一管理，也许可替代api/common.js
let picUrl = "http://116.63.14.146:8000/api/"	//统一管理，也许可替代api/common.js


let $http = new request({
	//接口请求地址
	baseUrl: baseUrl,
	//服务器本地上传文件地址
	fileUrl: baseUrl,
	websocket: socketBaseUrl,
	//设置请求头（如果使用报错跨域问题，可能是content-type请求类型和后台那边设置的不一致）
	headers: {
		'content-type': 'application/json;charset=UTF-8'
	},
	// {
	// 	"content-type":"application/x-www-form-urlencoded"
	// }
	
})
export default $http;