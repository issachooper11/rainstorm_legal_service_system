import request from "./request.js";

// 1. 一键导入 Excel 接口
export const importMarketExcelApi = (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return request({
        url: '/api/v1/market/import',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

// 2. 获取市场信息列表（支持多条件查询、分页、排序、意向/签约筛选）
export const getMarketListApi = (params) => {
    return request({
        url: '/api/v1/market/list',
        method: 'get',
        params // params 包含：region, enterprise_name, legal_representative, contact_info, email, enterprise_category, is_intention, is_signed, sort_field, sort_order, page, page_size
    })
}

// 3. 修改/更新企业信息接口
export const updateMarketApi = (enterpriseId, data) => {
    return request({
        url: `/api/v1/market/${enterpriseId}`,
        method: 'put',
        data
    })
}

// 4. 删除单个企业信息接口
export const deleteMarketApi = (enterpriseId) => {
    return request({
        url: `/api/v1/market/${enterpriseId}`,
        method: 'delete'
    })
}

// 5.单个邮件发送接口
export function sendMarketEmailApi(data) {
    return request({
        url: '/api/v1/market/email/send', // 对应 /api/v1/market/email/send
        method: 'post',
        data
    })
}