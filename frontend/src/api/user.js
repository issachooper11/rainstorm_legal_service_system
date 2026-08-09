// 引入你项目中已经封装好的通用请求工具（根据你的实际路径调整，比如 '@/utils/request' 或 '@/api/axios'）


import request from "./request.js";

/**
 * 获取所有用户列表
 */
export const fetchUserListApi = () => {
    return request({
        url: '/api/v1/users/',
        method: 'get'
    })
}

/**
 * 创建新用户
 * @param {Object} userData
 */
export const createUserApi = (userData) => {
    return request({
        url: '/api/v1/users/',
        method: 'post',
        data: userData
    })
}