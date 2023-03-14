//跨域代理前缀
const API_PROXY_PREFIX='/api'
const BASE_URL = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_API_BASE_URL : API_PROXY_PREFIX
// const BASE_URL = process.env.VUE_APP_API_BASE_URL
// const BASE_URL_IP = 'http://122.9.14.73:8000'
const BASE_URL_IP = 'http://127.0.0.1:8000'


module.exports = {
  LOGIN: `${BASE_URL_IP}/api/token-auth`,
  ROUTES: `${BASE_URL}/routes`,
  GOODS: `${BASE_URL}/goods`,
  GOODS_COLUMNS: `${BASE_URL}/columns`,
  PaperAll:`${BASE_URL_IP}/api/Interpretation/getall`,
  UserAll:`${BASE_URL_IP}/api/user/all`,
  ExpertAll:`${BASE_URL_IP}/api/expert/getall`,
  EnterpriseAll: `${BASE_URL_IP}/api/enterprise/getall`,
  OrderAll: `${BASE_URL_IP}/api/admin/order/getall`,
  BASE_URL_IP: BASE_URL_IP
}

