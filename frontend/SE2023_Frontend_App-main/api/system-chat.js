import axios from '@/config/requestConfig.js';
import time from '../common/time.js'
import {
	picUrl
} from './common.js'

export const showSystemMessage = async (uId, show) => {
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    // axios.setLoading(false)
    await axios.post('system_chat/show', {
        uId: uId,
        show: show
    }, headers)
    
    // axios.setLoading(false)
}

export const getBasicAISystemQuestionAns = async (question) => {
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    axios.setLoading(false)
    let output = await axios.post("system_chat_basic_question", {
        input: question
    })
    axios.setLoading(true)
    return output
}

export const getAdvanceAISystemQuestionAns = async (question) => {
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    axios.setLoading(false)
    let output = await axios.post("system_chat_advance_question", {
        input: question
    })
    axios.setLoading(true)
    return output
}

export const pushSystemMessage = async (data) => {  // 将一个msg送入数据库保存起来
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    axios.setLoading(false);
    let result = await axios.post("system_chat/push", data, headers)
    axios.setLoading(true);
    return result
}

export const createSystemChat = async (data) => {   // 创建一个客服聊天窗口，没有时创建
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }

    let result = await axios.post('system_chat/create', data, headers)
    console.log(result)
    return result
}

export const getSystemChat = async (userInfo) => {  // 得到uid对应的客服聊天窗口
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    let item = null
    // for test
    console.log("get system chat test")
    console.log(userInfo)
    console.log("sdf")
    item = await axios.get('system_chat/get', {
        "uId": userInfo.id
    }, headers)
    console.log(item)
    /*
    let result = {}
    if (item) {
        // let fid = ...
        let sendTime = time.gettime.gettime(new Date())
        let message = ''
        let msgList = item.message_list || []
        result = {
            // id
            // fid:
            // fromId
            // toId
            afterTime: + new Date(item.afterTime),
            userpic: item.from_user_id == userInfo.id? picUrl + item.to_user_pic: picUrl + item.from_user_pic,
            username: item.from_user_id == userInfo.id? item.to_user: item.from_user,
            time: sendTime,
            name: item.from_user_id == userInfo.id ? item.to_user: item.from_user,
            message: message,
            noreadnum: 0,
            messages: msgList
        }
    }
    */
    
    // for test
    // let result = {
    //     messages: [],
    //     noreadnum: 0,
    // }
    // end for test
    
    return item
}

export const readSystemChatMsg = async (uId) => { // 将聊天窗口中的消息都标记为已读
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    axios.setLoading(true);
    await axios.post('system_chat/read', {
        uId: uId
    }, headers)
    axios.setLoading(false);
}

export const createSocketForSystemChat = async (uid) => {   // 创建一个socket
    // let socket = await axios.websocket('POST', "msg/" + uid)
    let socket = await axios.websocket('POST', "system_msg/" + uid)
    return socket
}