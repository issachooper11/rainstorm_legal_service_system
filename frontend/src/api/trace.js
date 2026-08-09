import request from "./request.js";

// 获取某企业的跟进记录列表
export function getEnterpriseTracesApi(enterpriseId) {
    return request({
        url: `/api/v1/trace/${enterpriseId}/traces`,
        method: 'get'
    })
}

// 新增一条跟进记录
export function createEnterpriseTraceApi(enterpriseId, data) {
    return request({
        url: `/api/v1/trace/${enterpriseId}/traces`,
        method: 'post',
        data
    })
}