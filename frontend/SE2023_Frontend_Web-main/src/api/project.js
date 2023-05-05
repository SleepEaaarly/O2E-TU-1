import { getRequest } from './utils'

export const createProject = (params) => {
  const url = `/api/project/create`
  return getRequest(url, 'post', params)
}

export const modifyProject = (params) => {
  const url = `/api/project/${params.id}`
  return getRequest(url, 'post', params)
}

export const deleteProject = (params) => {
  const url = `/api/project/${params.id}`
  return getRequest(url, 'delete', params)
}

export const queryProject = (params) => {
  const url = `/api/project/${params.id}`
  return getRequest(url, 'get', params)
}

export const queryProjects = (params) => {
  const url = `/api/project`
  return getRequest(url, 'get', params)
}

export const createDiscussion = (params) => {
  const url = `/api/topic/create`
  return getRequest(url, 'post', params)
}

export const deleteDiscussion = (params) => {
  const url = `/api/topic/${params.id}`
  return getRequest(url, 'delete', params)
}

export const queryDiscussion = (params) => {
  const url = `/api/discussion`
  return getRequest(url, 'get', params)
}

export const queryDiscussions = (params) => {
  const url = `/api/topic`
  return getRequest(url, 'get', params)
}

export const createDiscussionComment = (params) => {
  const url = `/api/discussion/create`
  return getRequest(url, 'post', params)
}

export const deleteDiscussionComment = (method, params) => {
  const url = `/api/discussion/delete`
  return getRequest(url, method, params)
}
