import axios from '@/libs/api.request'
import { getRequest } from './utils'

export const login = (method, params) => {
  const url = '/api/token-auth'
  return getRequest(url, method, params)
}

export const refreshTokenReq = (refreshToken) => {
  const url = '/api/token-refresh'
  const headers = refreshToken ? { Authorization: 'Bearer ' + refreshToken } : {}
  return axios.request({
    url,
    method: 'get',
    headers
  })
}

export const modifyPassword = (params) => {
  const url = '/api/user/change-password'
  return getRequest(url, 'post', params)
}

export const modifyEmail = (params) => {
  const url = '/api/user/change-email'
  return getRequest(url, 'post', params)
}

export const modifyOrg= (params) => {
  const url = '/api/user/organization'
  return getRequest(url, 'post', params)
}

export const sendForgetPassEmail = (method, params) => {
  const url = '/api/user/forget-password'
  return getRequest(url, method, params)
}

export const sendForgetPassForm = (method, params) => {
  const url = '/api/user/forget-password'
  return getRequest(url, method, params)
}

export const sendRegiserEmail = (method, params) => {
  const url = '/api/user/create'
  return getRequest(url, method, params)
}

export const register = (method, params) => {
  const url = '/api/user/create'
  return getRequest(url, method, params)
}

export const follow = (userId) => {
  const url = `/api/user/${userId}/follow`
  return getRequest(url, 'post')
}

export const unfollow = (userId) => {
  const url = `/api/user/${userId}/unfollow`
  return getRequest(url, 'post')
}

export const followerList = (id, params) => {
  const url = `/api/follower/${id}`
  return getRequest(url, 'get', params)
}

export const fanList = (id, params) => {
  const url = `/api/fan/${id}`
  return getRequest(url, 'get', params)
}

export const myKnowledge = (id, params) => {
  const url = `/api/post/${id}`
  return getRequest(url, 'get', params)
}

export const myInterpretation = (id, params) => {
  const url = `/api/Interpretation/${id}`
  return getRequest(url, 'get', params)
}

export const getUserInfo = (id) => {
  const url = '/api/user/profile'
  if (id) {
    return getRequest(url, 'get', { user_id: id })
  } else {
    return getRequest(url, 'get')
  }
}

export const recentKnowledge = (params) => {
  const url = `/api/recent/page/${params.pindex}`
  return getRequest(url, 'get', params)
}

export const uploadAvatar = (params) => {
  const url = `/api/user/icon`
  return getRequest(url, 'put', params)
}

export const getIcon = (params) => {
  const url = `/api/user/icon`
  return getRequest(url, 'get', params)
}

export const getUnreadCount = () => {
  const url = '/api/notification'
  return getRequest(url, 'get', { only_unread: true })
}

export const getMessages = (params) => {
  const url = `/api/notification/page/${params.pindex}`
  return getRequest(url, 'get', params)
}

export const getMessage = () => {
  const url = `/api/notification/page/${params.pindex}`
  return getRequest(url, 'get', params)
}

export const getContentByMsgId = msg_id => {
  return axios.request({
    url: 'message/content',
    method: 'get',
    params: {
      msg_id
    }
  })
}

export const hasRead = msg_id => {
  return axios.request({
    url: 'message/has_read',
    method: 'post',
    data: {
      msg_id
    }
  })
}

export const removeReaded = msg_id => {
  return axios.request({
    url: 'message/remove_readed',
    method: 'post',
    data: {
      msg_id
    }
  })
}

export const restoreTrash = msg_id => {
  return axios.request({
    url: 'message/restore',
    method: 'post',
    data: {
      msg_id
    }
  })
}
