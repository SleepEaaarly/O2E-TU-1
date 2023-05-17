import {
  login,
  register,
  getUserInfo,
  getMessage,
  getContentByMsgId,
  hasRead,
  removeReaded,
  restoreTrash,
  getUnreadCount
} from '@/api/user'
import { setToken, getToken, setRefreshToken, getRefreshToken } from '@/libs/util'

export default {
  state: {
    userName: '',
    userIsSponsor: false,
    userId: '',
    userEmail: '',
    userInstitution: '',
    userTotalFan: 0,
    userTotalLike: 0,
    userTotalPost: 0,
    userpic: '',
    token: getToken(),
    refresh_token: getRefreshToken(),
    access: '',
    hasGetInfo: false,
    unreadCount: 0,
    messageUnreadList: [],
    messageReadedList: [],
    messageTrashList: [],
    messageContentStore: {}
  },
  mutations: {
    setAvatar (state, userpic) {
      state.userpic = 'http://116.63.14.146:8000/api/' + userpic
    },
    setUserName (state, name) {
      state.userName = name
    },
    setUserProfile (state, params) {
      console.log("enter set User Profile")
      console.log(params)
      console.log(params.username)
      console.log(params.nickname)
      state.userName = params.username
      console.log("Now we can get the userName in state.user.userName 2")
      console.log(state.userName)
      state.userId = params.id
      console.log("Now we can get the userId in state.user.userId 2")
      console.log(state.userId)
      state.userEmail = params.email
      console.log("Now we can get the userEmail in state.user.userEmail 2")
      console.log(state.userEmail)
      // state.user.userInstitution = params.institution===null ? "" : params.institution
      state.userTotalFan = params.total_fan
      console.log("Now we can get the userTotalFan in state.user.userEmail 2")
      console.log(state.userTotalFan)
      state.userTotalLike = params.total_like
      console.log("Now we can get the userTotalLike in state.user.userEmail 2")
      console.log(state.userTotalLike)
      state.userTotalPost = params.total_post
      console.log("Now we can get the userTotalPost in state.user.userEmail 2")
      console.log(state.userTotalPost)
      // state.user.userIsSponsor = params.is_sponsor 不存在这个字段
      state.userpic = 'http://116.63.14.146:8000/api/' + params.userpic
      console.log("Now we can get the userPic in state.user.userId 2")
      console.log(state.userpic)
    },
    setAccess (state, access) {
      state.access = access
    },
    setToken (state, token) {
      state.token = token
      setToken(token)
    },
    setRefreshToken (state, token) {
      state.refresh_token = token
      setRefreshToken(token)
    },
    setHasGetInfo (state, status) {
      state.hasGetInfo = status
    },
    setMessageCount (state, count) {
      state.unreadCount = count
    },
    setMessageUnreadList (state, list) {
      state.messageUnreadList = list
    },
    setMessageReadedList (state, list) {
      state.messageReadedList = list
    },
    setMessageTrashList (state, list) {
      state.messageTrashList = list
    },
    updateMessageContentStore (state, { msg_id, content }) {
      state.messageContentStore[msg_id] = content
    },
    moveMsg (state, { from, to, msg_id }) {
      const index = state[from].findIndex(_ => _.msg_id === msg_id)
      const msgItem = state[from].splice(index, 1)[0]
      msgItem.loading = false
      state[to].unshift(msgItem)
    }
  },
  getters: {
    messageUnreadCount: state => state.messageUnreadList.length,
    messageReadedCount: state => state.messageReadedList.length,
    messageTrashCount: state => state.messageTrashList.length
  },
  actions: {
    // 注册
    handleRegister ({ commit }, { userName, password, email }) {
      userName = userName.trim()
      return new Promise((resolve, reject) => {
        register('post', {
          username: userName,
          password: password,
          email: email
        }).then(res => {
          resolve()
        }).catch(err => {
          reject(err)
        })
      })
    },
    // 登录
    handleLogin ({ commit }, { userName, password }) {
      userName = userName.trim()
      return new Promise((resolve, reject) => {
        login('post', {
          username: userName,
          password: password
        }).then(res => {
          const data = res.data
          console.log(data)
          console.log(res)
          commit('setToken', data.access_token)
          console.log("set Token complete")
          commit('setRefreshToken', data.refresh_token)
          console.log("set refresh token complete")
          getUserInfo(data.userInfo.id).then(res => {
            commit('setUserProfile', res.data)
          }).catch(error => {
            console.log("ERROR!!!")
            this.$Modal.error(getErrModalOptions(error))
          })
          resolve()
        }).catch(err => {
          reject(err)
        })
      })
    },
    // 退出登录
    handleLogOut ({ state, commit }) {
      return new Promise((resolve, reject) => {
        // logout(state.token).then(() => {
        //   commit('setToken', '')
        //   commit('setAccess', [])
        //   resolve()
        // }).catch(err => {
        //   reject(err)
        // })
        // 如果你的退出登录无需请求接口，则可以直接使用下面三行代码而无需使用logout调用接口
        commit('setToken', '')
        commit('setRefreshToken', '')
        setToken('') // 清除 cookie 缓存
        setRefreshToken('')
        // commit('setAccess', [])
        resolve()
      })
    },
    // 此方法用来获取未读消息条数，接口只返回数值，不返回消息列表
    getUnreadMessageCount ({ state, commit }) {
      getUnreadCount().then(res => {
        console.log(res)
        commit('setMessageCount', res.data.num)
      })
    },
    // 获取消息列表，其中包含未读、已读、回收站三个列表
    getMessageList ({ state, commit }) {
      return new Promise((resolve, reject) => {
        getMessage().then(res => {
          const { unread, readed, trash } = res.data
          commit('setMessageUnreadList', unread.sort((a, b) => new Date(b.create_time) - new Date(a.create_time)))
          commit('setMessageReadedList', readed.map(_ => {
            _.loading = false
            return _
          }).sort((a, b) => new Date(b.create_time) - new Date(a.create_time)))
          commit('setMessageTrashList', trash.map(_ => {
            _.loading = false
            return _
          }).sort((a, b) => new Date(b.create_time) - new Date(a.create_time)))
          resolve()
        }).catch(error => {
          console.log(error)
          reject(error)
        })
      })
    },
    // 根据当前点击的消息的id获取内容
    getContentByMsgId ({ state, commit }, { msg_id }) {
      return new Promise((resolve, reject) => {
        let contentItem = state.messageContentStore[msg_id]
        if (contentItem) {
          resolve(contentItem)
        } else {
          getContentByMsgId(msg_id).then(res => {
            const content = res.data
            commit('updateMessageContentStore', { msg_id, content })
            resolve(content)
          })
        }
      })
    },
    // 把一个未读消息标记为已读
    hasRead ({ state, commit }, { msg_id }) {
      return new Promise((resolve, reject) => {
        hasRead(msg_id).then(() => {
          commit('moveMsg', {
            from: 'messageUnreadList',
            to: 'messageReadedList',
            msg_id
          })
          commit('setMessageCount', state.unreadCount - 1)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    // 删除一个已读消息到回收站
    removeReaded ({ commit }, { msg_id }) {
      return new Promise((resolve, reject) => {
        removeReaded(msg_id).then(() => {
          commit('moveMsg', {
            from: 'messageReadedList',
            to: 'messageTrashList',
            msg_id
          })
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    // 还原一个已删除消息到已读消息
    restoreTrash ({ commit }, { msg_id }) {
      return new Promise((resolve, reject) => {
        restoreTrash(msg_id).then(() => {
          commit('moveMsg', {
            from: 'messageTrashList',
            to: 'messageReadedList',
            msg_id
          })
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    }
  }
}
