import {createRouter, createWebHistory} from 'vue-router'
import {ElMessage} from 'element-plus'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import TeamInfo from '../views/team/TeamInfo.vue'
import MarketInfo from '../views/market/MarketInfo.vue'

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
        redirect: '/dashboard/case-management',
        children: [
            {
                path: '/dashboard/team-info',
                name: 'TeamInfo',
                component: TeamInfo,
                meta: {title: '团队信息', roles: ['partner']}
            },
            {
                path: '/dashboard/market-info',
                name: 'MarketInfo',
                component: MarketInfo,
                meta: {title: '市场信息', roles: ['partner']}
            },
            {
                path: '/dashboard/case-management',
                name: 'CaseManagement',
                component: () => import('../views/case/CaseManagement.vue'),
                meta: {title: '案件管理', roles: ['lawyer', 'partner']}
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

// 全局前置守卫
router.beforeEach((to) => {
    const token = localStorage.getItem('token')

    if (to.meta.requiresAuth && !token) {
        return '/login'
    }

    if (to.meta.roles) {
        const role = getUserRole()

        if (!to.meta.roles.includes(role)) {
            // 安全触发提示
            try {
                ElMessage.error('权限不足：您的账号无权访问该模块')
            } catch (err) {
                console.error(err)
            }

            if (role === 'lawyer') {
                return '/dashboard/case-management'
            } else {
                return '/login'
            }
        }
    }

    return true
})

// 注册路由错误处理器，防止未捕获的导航异常崩溃
router.onError((error) => {
    console.error('路由导航错误:', error)
})

export default router