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

// 2. 获取市场信息列表（支持多条件查询、分页、排序）
export const getMarketListApi = (params) => {
    return request({
        url: '/api/v1/market/list',
        method: 'get',
        params // params 包含：region, enterprise_name, legal_representative, contact_info, email, enterprise_category, sort_field, sort_order, page, page_size
    })
}