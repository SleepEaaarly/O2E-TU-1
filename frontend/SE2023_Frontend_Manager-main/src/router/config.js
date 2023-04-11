import TabsView from '@/layouts/tabs/TabsView'
import BlankView from '@/layouts/BlankView'
import PageView from '@/layouts/PageView'

// 路由配置
const options = {
    routes: [
        {
            path: '/login',
            name: '登录页',
            component: () => import('@/pages/login')
        },
        {
            path: '*',
            name: '404',
            component: () => import('@/pages/exception/404'),
        },
        {
            path: '/403',
            name: '403',
            component: () => import('@/pages/exception/403'),
        },
        {
            path: '/',
            name: '首页',
            component: TabsView,
            redirect: '/login',
            children: [
                {
                    path: 'dashboard',
                    name: '主面板',
                    meta: {
                        icon: 'dashboard',
                    },
                    component: () => import('@/pages/dashboard/analysis'),BlankView,


                    
                },
				
                {
                    path: 'user',
                    name: '用户管理',
                    meta: {
                        icon: 'form',
                        page: {
                            cacheAble: false
                        }
                    },
                    component: PageView,
                    children: [
                        {
                            path: 'list',
                            name: '用户列表',
                            component: () => import('@/pages/form/advance/UserForm'),
                        },

                        {
                            path: 'ExpertCertificate',
                            name: '专家认证审核',
                            component: () => import('../pages/expert-certificate/ExpertList')
                        },

                        {
                            path: 'EnterpriseCertificate',
                            name: '企业认证审核',
                            component: () => import('../pages/enterprise-certificate/EnterpriseList')
                        },

                        {
                            path: 'chengguoCertificate',
                            name: '成果审核',
                            component: () => import('@/pages/chengguo-certificate/ChengguoList'),
                        }
                        
                    ]
                }, {
                    path: 'interpretation',
                    name: '解读管理',
                    meta: {
                        icon: 'profile'
                    },
                    component: PageView,
                    children: [
                        {
                            path: 'list',
                            name: '解读列表',
                            component: () => import('@/pages/list/search/ArticleList'),
                        },

                    ]
                },
                {
                    path: 'NeedOrder',
                    name: "需求订单管理",
                    meta: {
                        icon: 'shopping-cart'
                    },
                    component: PageView,
                    children: [
                        {
                            path: 'NeedForm',
                            name: "需求订单列表",
                            component: () => import('../pages/need-order/NeedForm')
                        }
                    ]
                },
                {
                    path: 'feedback',
                    name: '用户反馈',
                    meta: {
                        icon: 'table',
                    },
                    component: PageView,
                    children: [
                        {
                            path: 'FeedbackList',
                            name: '用户反馈列表',
                            component: () => import('../pages/feedback/feedbackList')
                        }
                    ]
                },
                {
                    path: 'system-chat',
                    name: 'AI/人工客服回复',
                    meta: {
                        icon: 'table',
                    },
                    component: PageView,
                    children: [
                        {
                            path: 'SystemChatList',
                            name: '客服回复列表',
                            component: () => import('../pages/system-chat/systemChatList'),
                        }
                    ]
                },
            ]
        },
    ]
}


export default options
