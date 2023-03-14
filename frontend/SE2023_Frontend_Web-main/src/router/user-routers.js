import Main from '@/components/main'

export default {
  path: '/user',
  name: 'user',
  component: Main,
  meta: {
    title: '用户相关',
    hideInMenu: true
  },
  children: [
    {
      path: 'user-info/:id',
      name: 'user_info',
      meta: {
        title: '个人主页',
        icon: 'ios-person'
      },
      component: () => import('@/view/user/user-info')
    }
  ]
}
