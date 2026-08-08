import request from './request'

/**
 * 用户登录接口
 * @param {Object} data 包含 username 和 password 的对象
 */
export function loginApi(data) {
    // FastAPI 的 OAuth2 密码登录要求必须是 x-www-form-urlencoded 格式
    const params = new URLSearchParams()
    params.append('username', data.username)
    params.append('password', data.password)

    return request({
        url: '/api/v1/auth/login',
        method: 'post',
        data: params,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
}