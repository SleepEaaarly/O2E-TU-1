import Mock from 'mockjs'
import { tokenAuth } from './token'
// 配置Ajax请求延时，可用来测试网络延迟大时项目中一些效果
Mock.setup({
  timeout: 1000
})

// token 相关
Mock.mock(/\/api\/token-auth/, tokenAuth)
export default Mock
