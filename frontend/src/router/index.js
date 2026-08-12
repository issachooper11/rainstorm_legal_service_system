import {createRouter, createWebHistory} from 'vue-router'
import {ElMessage} from 'element-plus'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import TeamInfo from '../views/team/TeamInfo.vue'
import MarketInfo from '../views/market/MarketInfo.vue'

// 定义数字角色常量
const Role = {
    CHAIRMAN: 1,  // 董事长
    PARTNER: 2,   // 合伙人
    LAWYER: 3,    // 律师
    ASSISTANT: 4, // 助理
    ADMINI: 5     // 管理员
}

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: {requiresAuth: true},
        // 动态默认重定向：根据角色决定一登录跳到哪个默认页面
        redirect: (to) => {
            const role = Number(getUserRole())
            if (role === Role.ADMINI) {
                return '/dashboard/team-info' // 5 只能看团队信息
            } else if (role === Role.LAWYER || role === Role.ASSISTANT) {
                return '/dashboard/case-management' // 3, 4 只能看案件管理
            }
            return '/dashboard/market-info' // 1, 2 默认进案件管理
        },
        children: [
            {
                path: '/dashboard/team-info',
                name: 'TeamInfo',
                component: TeamInfo,
                // 团队信息：1(董事长)、2(合伙人)、5(管理员)可看
                meta: {title: '团队信息', roles: [Role.CHAIRMAN, Role.PARTNER, Role.ADMINI]}
            },
            {
                path: '/dashboard/market-info',
                name: 'MarketInfo',
                component: MarketInfo,
                // 市场信息：只有 1(董事长) 可看
                meta: {title: '市场信息', roles: [Role.CHAIRMAN]}
            },
            {
                path: '/dashboard/case-management',
                name: 'CaseManagement',
                component: () => import('../views/case/CaseManagement.vue'),
                // 案件管理：1(董事长)、2(合伙人)、3(律师)、4(助理)可看（管理员5不能看）
                meta: {title: '案件管理', roles: [Role.CHAIRMAN, Role.PARTNER, Role.LAWYER, Role.ASSISTANT]}
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 解析 JWT Token 获取用户角色的辅助函数
function getUserRole() {
    const token = localStorage.getItem('token')
    if (!token) return null
    try {
        const base64Url = token.split('.')[1]
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
        }).join(''))
        return JSON.parse(jsonPayload).role
    } catch (e) {
        return null
    }
}

// 防连击弹窗锁
let isShowingMessage = false

router.beforeEach((to) => {
    const token = localStorage.getItem('token')

    if (to.meta.requiresAuth && !token) {
        return '/login'
    }

    if (to.meta.roles) {
        const role = Number(getUserRole())
        console.log('当前登录用户数字角色:', role)

        if (!to.meta.roles.includes(role)) {
            if (!isShowingMessage) {
                isShowingMessage = true
                try {
                    ElMessage.error('权限不足：您的账号无权访问该模块')
                } catch (err) {
                    console.error(err)
                }
                setTimeout(() => {
                    isShowingMessage = false
                }, 1000)
            }

            // 严格的越权拦截重定向：
            if (role === Role.ADMINI) {
                return '/dashboard/team-info' // 5 强制拉回团队信息
            } else if (role === Role.LAWYER || role === Role.ASSISTANT) {
                return '/dashboard/case-management' // 3, 4 强制拉回案件管理
            } else if (role === Role.PARTNER) {
                return '/dashboard/team-info' // 2 合伙人无权看市场时，踢回团队信息
            } else {
                return '/login'
            }
        }
    }

    return true
})

router.onError((error) => {
    console.error('路由导航错误:', error)
})

export default router