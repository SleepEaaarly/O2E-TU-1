import axios from '@/libs/api.request'

export const getRequest = (url, method, params) => {
  const options = { url, method }
  if (typeof params !== 'undefined') {
    if (method === 'get') {
      options.params = params
    } else {
      options.data = params
    }
  }
  return axios.request(options)
}
