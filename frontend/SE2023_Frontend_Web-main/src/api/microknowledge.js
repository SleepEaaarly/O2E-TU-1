import { getRequest } from './utils'

export const createEvidence = (method, params) => {
  const url = '/api/micro-evidence'
  return getRequest(url, method, params)
}

export const createConjecture = (method, params) => {
  const url = '/api/micro-conjecture'
  return getRequest(url, method, params)
}

export const getEvidencePage = (method, params) => {
  const url = '//page/' + params.pindx
  return getRequest(url, method, params)
}

export const getConjecturePage = (method, params) => {
  const url = '/api/micro-conjecture/page/' + params.pindx
  return getRequest(url, method, params)
}

export const getKnowledgePage = (method, params) => {
  const url = `/api/micro-knowledge/page/${params.pindx}`
  return getRequest(url, method, params)
}

export const favorMicroKnowledge = (method, id, type) => {
  // type 取值为 "favor" or "unfavor"
  const url = `/api/micro-knowledge/${id}/${type}`
  return getRequest(url, method)
}

export const likeMicroKnowledge = (method, id) => {
  const url = `/api/micro-knowledge/${id}/like`
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

export const getMicroknowledgeComments = (method, params) => {
  const url = '/api/comment'
  return getRequest(url, method, params)
}

export const microKnowledgeIdReq = (id, type, method, params) => {
  // type 0: evidence 1: conjecture
  const typeUrl = type === 0 ? 'micro-evidence' : 'micro-conjecture'
  const url = `/api/${typeUrl}/${id}`
  return getRequest(url, method, params)
}

export const recommend = (params) => {
  const url = 'api/recommend'
  return getRequest(url, 'get', params)
}

export const verifyMicroKnowledge = (id, method, params) => {
  const url = `/api/micro-knowledge/${id}/judge`
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
