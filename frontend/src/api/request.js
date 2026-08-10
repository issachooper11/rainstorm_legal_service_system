import axios from 'axios'
import {ElMessage} from 'element-plus'
// 创建统一的 axios 实例
const service = axios.create({
    baseURL: '', // 后端基础地址，以后换线上环境只需改这里
    timeout: 5000,
})

// 请求拦截器：每次发送请求前，自动带上本地的 token（如果有的话）
service.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// 响应拦截器：统一处理后端返回的错误信息
service.interceptors.response.use(
    (response) => {
        return response.data
    },
    (error) => {
        const message = error.response?.data?.detail || '网络请求失败，请稍后重试'
        ElMessage.error(message)
        return Promise.reject(error)
    }
)

export default service