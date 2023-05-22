import Vue from 'vue'
import Vuex from 'vuex'
import time from '../common/time.js'

import {
	createSocket,
	readChatMsg
} from '@/api/paper.js'

import {
	readSystemChatMsg,

} from '@/api/system-chat.js'

Vue.use(Vuex)
Vuex.createLogger()
/**
	userInfo: 用户信息
	chatList: 聊天列表
	msgPage:1,	消息的索引
	msgIndex:-1, 聊天界面索引
	currentChat: 当前聊天信息
	selTitle: 发布动态选择的标题
 */
const store = new Vuex.Store({
	state: {
		userInfo: {},
		chatList: [],
		isPaper: false,
		msgPage: 1,
		msgIndex: -1,
		currentChat: [],
		selTitle: {},
		category: {},
		socket: undefined,
		$is_open_socket: false,
		isPlatformSwitchOn: true,	//是否设置导航栏显示“平台”
		system_chat: {
			// afterTime: 0, 	基本都是Nan，但是chatlist排序的函数中都是用的aftertime来排序的（如何排序）
			// fid: 0,			fid似乎和toId相同，都是对方的id
			// fromId: 0,		fromId 是本人id
			// id: 0,			98可能是表示这个聊天的id，对应数据库中core_chatroom的id
			// message: 0,		表示消息列表中展示的消息是什么
			messages: [],	//这是一个数组，表示chat中的所有消息
			// name: 0,			对应的是企业名称
			noreadnum: 0,	//我觉得是表示未读消息的提醒
			// time: 0,			表示显示出来的聊天框的时间
			// toId: 0,			对方的id
			// type: 0,			基本都是undefined
			// username: 0,		对方姓名
			// userpic: 0,		对方头像
		},
		inSystemChat: false,
	},
	getters: {
		currentChatMsgs(state) {
			if (state.msgIndex == -1) {
				return []
			}
			let len = state.chatList[state.msgIndex].messages ? state.chatList[state.msgIndex].messages.length : 0
			if (len > 20) {
				return state.chatList[state.msgIndex].messages.slice(Math.max(0, len - 20 * state.msgPage), len)
			}
			return state.chatList[state.msgIndex].messages || []
		},
		currentSystemChatMsgs(state, msgPage=1) {
			let len = state.system_chat.messages ? state.system_chat.messages.length : 0
			if (len > 20) {
				return state.system_chat.messages.slice(Math.max(0, len - 20 * msgPage), len)
			}
			return state.system_chat.messages || []
		}
	},
	mutations: {
		addCategory(state, obj) {
			state.category = obj
		},
		delCategory(state, ) {
			state.category = {}
		},
		addselTitle(state, obj) {
			state.selTitle = obj
		},
		delSelTitle(state, index) {
			state.selTitle = {}
		},
		resetSelTitle(state) {
			state.selTitle = {}
		},
		setIndex(state, msgIndex) {
			state.msgIndex = msgIndex
		},
		setMsgPage(state, msgPage) {
			if (msgPage) {
				state.msgPage = msgPage
			} else {
				state.msgPage++
			}

		},
		setUserInfo(state, userInfo) {
			state.userInfo = userInfo

		},
		setChatList(state, chatList) {
			state.chatList = chatList

		},
		setSystemChat(state, system_chat) {
			state.system_chat = system_chat
		},
		delChatList(state, index) { // 删除chatList中指定下标的聊天
			state.chatList.splice(index, 1)

		},
		addChatList(state, chat) {
			state.chatList.unshift(chat)
		},
		updateMsg(state, index) {
			state.chatList[state.msgIndex].noreadnum = 0
		},
		updateSystemMsg(state){
			state.system_chat.noreadnum = 0
		},
		addChatMessage(state, obj) {
			state.chatList[state.msgIndex].message = obj.message	
			let len = state.chatList[state.msgIndex].messages.length
			if(len == 0) {
				obj.gstime=time.gettime.getChatTime(obj.gstime,0)
			} else {
				obj.gstime=time.gettime.getChatTime(obj.gstime,state.chatList[state.msgIndex].messages[len-1].created_at)
			}
			state.chatList[state.msgIndex].time = obj.time
			state.chatList[state.msgIndex].afterTime = + new Date(obj.sendTime)
			state.chatList[state.msgIndex].messages.push(obj)
		},
		addSystemChatMessage(state, obj) {
			state.system_chat.message = obj.message
			console.log(state.system_chat.messages)
			let len = state.system_chat.messages.length
			if (len == 0) {
				obj.gstime = time.gettime.getChatTime(obj.gstime, 0)
			} else {
				obj.gstime = time.gettime.getChatTime(obj.gstime, state.system_chat.messages[len - 1].created_at)
			}
			state.system_chat.time = obj.time
			state.system_chat.afterTime = + new Date(obj.sendTime)
			state.system_chat.messages.push(obj)
		},
		sortChatList(state) {
			state.chatList.sort((a, b) => {
				return b.afterTime - a.afterTime
			})
		},
		addNoreadMessage(state, index) {
			state.chatList[index].noreadnum = state.chatList[index].noreadnum + 1
		},
		addSystemNoReadMessage(state) {
			state.system_chat.noreadnum = state.system_chat.noreadnum + 1
		},
		addSocket(state, soc) {
			state.socket = soc
		}
	},

	actions: {
		addChatListMessage(state, data) {
			console.log(888888)
		},
		async setSocketV({state, commit}, uid) {
			if (!state.$is_open_socket) {
				let socket = await createSocket(uid)
				socket.onOpen(res => {
					console.log('WebSocket连接正常打开中...vuex！')
					state.$is_open_socket = true
					if (state.$is_open_socket) {
						socket.onMessage(async res => {
							if (res.data === '连接成功') {
								console.log('连接成功')
								return
							}
							console.log('收到消息并追加')
							let data = {}
							try {
								data = JSON.parse(res.data)
								let flag = false
								if (Array.isArray(state.chatList)) {
									state.chatList.forEach((item, index) => {
										if (item.id == data.cId) {
											if (state.msgIndex == index) {
												flag = true
												state.chatList[index].noreadnum = 0
												data.status = true
												readChatMsg([data.id])
											} else {
												state.chatList[index].noreadnum = state.chatList[index].noreadnum + 1
											}
											state.chatList[index].message = data.message
											state.chatList[index].time = time.gettime.gettime(data.sendTime)
											state.chatList[index].afterTime = +new Date(data.sendTime)
											let o = {
												id: data.id,
												isme: data.fromId == state.userInfo.id,
												uid: data.fromId == state.userInfo.id ? data.toId : data.fromId,
												userpic: data.fromId == state.userInfo.id ? state.userInfo.authorUrl : item.userpic,
												type: 'text',
												message: data.message,
												time: time.gettime.gettime(data.sendTime),
												gstime: time.gettime.getChatTime(data.sendTime),
												status: data.status,
											}
											state.chatList[index].messages.push(o)
										}
									})
								}
							} catch (e) {
								console.log(e)
							}

						})
					}
				})
				// 这里仅是事件监听【如果socket关闭了会执行】
				socket.onClose(() => {
					state.$is_open_socket = false
					console.log('已经被关闭了')
				})
				socket.onError(e => {
					console.log('失败了')
					state.$is_open_socket = false
					console.log(e)
				})
				commit('addSocket', socket)
			}
		},
		async setSocketVForSystem({state, commit}, uid) {
			if (!state.$is_open_socket) {
				let socket = await createSocket(uid)
				socket.onOpen(res => {
					console.log('WebSOcket 连接正常打开中...vuex!')
					state.$is_open_socket = true
					if (state.$is_open_socket) {
						socket.onMessage(async res => {
							if (res.data === '连接成功') {
								console.log('连接成功')
								return
							}
							console.log('收到消息并追加')
							let data = {}
							try {
								data = JSON.parse(res.data)
								let flag = false
								if (state.system_chat.id == data.cId) {
									if (state.inSystemChat) {	// 如果页面是当前聊天
										flag = true
										state.system_chat.noreadnum = 0
										data.status = true
										readChatMsg([data.id])
									} else {	// 如果页面不是当前聊天
										state.system_chat.noreadnum = state.system_chat.noreadnum + 1
									}
									state.chatList[index].message = data.message
									state.chatList[index].time = time.gettime.gettime(data.sendTime)
									state.chatList[index].afterTime = +new Date(data.sendTime)
									let o = {
										id: data.id,
										isme: data.fromId == state.userInfo.id,
										uid: data.fromId == state.userInfo.id ? data.toId : data.fromId,
										userpic: data.fromId == state.userInfo.id ? state.userInfo.authorUrl : item.userpic,
										type: 'text',
										message: data.message,
										time: time.gettime.gettime(data.sendTime),
										gstime: time.gettime.getChatTime(data.sendTime),
										status: data.status,
									}
									state.chatList[index].messages.push(o)
								}
							} catch (e) {
								console.log(e)
							}
						})
					}
				})
				socket.onClose(() => {
					state.$is_open_socket = false
					console.log('已经被关闭了')
				})
				socket.onError(e => {
					console.log('失败了')
					state.$is_open_socket = false
					console.log(e)
				})
				commit('addSocket', socket)
			}
		}
	}


})


export default store
