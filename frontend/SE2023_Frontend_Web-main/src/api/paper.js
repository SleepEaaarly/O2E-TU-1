import { getRequest } from './utils'

export const createPaper = (method, params) => {
  const url = '/api/Interpretation'
  return getRequest(url, method, params)
}

export const InterpretationIdReq = (id, type, method, params) => {
  const typeUrl = 'Interpretation'
  const url = `/api/${typeUrl}/${id}`
  return getRequest(url, method, params)
}

export const favorInterpretationList = (params) => {
  const url = `/api/favorites/page/${params.pindex}`
  return getRequest(url, 'get', params)
}

export const download = (id,params) => {
  let a = document.createElement('a')
  a.href =`/api/download/Interpretation/${id}`
  a.setAttribute('params',params)
  a.click(); 
}

export const likeInterpretation = (method, id, like) => {
  // type 取值为 "favor" or "unfavor"
  const url = `/api/Interpretation/${id}/like`
  return getRequest(url, method)
}

export const getInterpretationComments = (method, params) => {
  const url = '/api/comment'
  return getRequest(url, method, params)
}

export const collectInterpretation = (method, id, like) => {
  const url = `/api/Interpretation/${id}/${like}`
  return getRequest(url, method)
}
export const addComment = (method, params) => {
  const url = '/api/comment/create'
  return getRequest(url, method, params)
}

export const deleteComment = (method, params) => {
  const url = '/api/comment/delete'
  return getRequest(url, method, params)
}

export const recommend = (params) => {
  const url = '/api/recommend'
  return getRequest(url, 'get', params)
}

export const getInterpretationPage = (method, params) => {
  const url = '/api/Interpretation/page/' + params.pid
  return getRequest(url, method, params)
}
export const getPaperPage = (method, params) => {
  const url = '/api/Paper/page/' + params.pindx
  return getRequest(url, method, params)
}

export const getUserPage = (method, params) => {
  const url = '/api/user/search/' + params.page
  return getRequest(url, method, params)
}

export const getTags = (method, params) => {
  const url = `/api/tags/page/${params.pindx}`
  return getRequest(url, method, params)
}

export const favorKnowledgeList = (params) => {
  const url = `/api/favorites/page/${params.pindex}`
  return getRequest(url, 'get', params)
}
