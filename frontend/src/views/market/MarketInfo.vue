<template>
  <div class="market-container" style="padding: 20px;">
    <!-- 1. 顶部搜索过滤表单 -->
    <el-card class="filter-card" shadow="never" style="margin-bottom: 20px;">
      <el-form :inline="true" :model="queryParams" class="demo-form-inline">
        <el-form-item label="地区">
          <el-input v-model="queryParams.region" placeholder="请输入地区" clearable @clear="handleQuery"/>
        </el-form-item>
        <el-form-item label="企业名称">
          <el-input v-model="queryParams.enterprise_name" placeholder="请输入企业名称" clearable @clear="handleQuery"/>
        </el-form-item>
        <el-form-item label="法定代表人">
          <el-input v-model="queryParams.legal_representative" placeholder="请输入法人" clearable @clear="handleQuery"/>
        </el-form-item>
        <el-form-item label="联系方式">
          <el-input v-model="queryParams.contact_info" placeholder="请输入联系方式" clearable @clear="handleQuery"/>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="queryParams.email" placeholder="请输入邮箱" clearable @clear="handleQuery"/>
        </el-form-item>
        <el-form-item label="企业类别">
          <el-select v-model="queryParams.enterprise_category" placeholder="全部类别" clearable style="width: 130px;"
                     @change="handleQuery">
            <el-option label="科技" :value="1"/>
            <el-option label="商服" :value="2"/>
            <el-option label="合同" :value="3"/>
            <el-option label="劳动" :value="4"/>
            <el-option label="综合" :value="5"/>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 2. 操作栏（一键导入） -->
    <div class="action-bar"
         style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
      <div class="left-actions">
        <el-upload
            action="#"
            :http-request="handleUploadExcel"
            :show-file-list="false"
            accept=".xlsx, .xls"
        >
          <el-button type="success">
            <el-icon style="margin-right: 4px;">
              <Upload/>
            </el-icon>
            一键导入 Excel
          </el-button>
        </el-upload>
      </div>
    </div>

    <!-- 3. 数据表格区域（带排序监听） -->
    <el-card shadow="never">
      <el-table
          :data="tableData"
          style="width: 100%"
          v-loading="loading"
          @sort-change="handleSortChange"
          border
      >
        <el-table-column type="index" label="序号" width="60" align="center"/>
        <el-table-column prop="region" label="地区" width="100"/>
        <el-table-column prop="enterprise_name" label="企业名称" min-width="180" show-overflow-tooltip/>
        <el-table-column prop="legal_representative" label="法定代表人" width="110"/>
        <el-table-column prop="contact_info" label="联系方式" width="130" show-overflow-tooltip/>
        <el-table-column prop="email" label="邮箱" width="150" show-overflow-tooltip/>

        <!-- 成立日期排序 -->
        <el-table-column prop="establishment_date" label="成立日期" width="120" sortable="custom"/>

        <!-- 注册资本排序（纯数字展示，拼接万元） -->
        <el-table-column prop="registered_capital" label="注册资本" width="130" sortable="custom">
          <template #default="{ row }">
            <span>{{ row.registered_capital ? row.registered_capital + ' 万元' : '暂无' }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="enterprise_type" label="企业类型" width="120"/>
        <el-table-column prop="registered_address" label="注册地址" min-width="180" show-overflow-tooltip/>

        <!-- 企业类别 1-5 渲染标签 -->
        <el-table-column prop="enterprise_category" label="类别" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="getCategoryType(row.enterprise_category)">
              {{ getCategoryText(row.enterprise_category) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <!-- 4. 分页组件 (支持 5/10/25/50 条) -->
      <div class="pagination-container" style="margin-top: 20px; display: flex; justify-content: flex-end;">
        <el-pagination
            v-model:current-page="queryParams.page"
            v-model:page-size="queryParams.page_size"
            :page-sizes="[5, 10, 25, 50]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue'
import {ElMessage} from 'element-plus'
import {Upload} from '@element-plus/icons-vue'
import {getMarketListApi, importMarketExcelApi} from "../../api/market.js";

// 表格加载状态
const loading = ref(false)
const tableData = ref([])
const total = ref(0)

// 查询与分页参数
const queryParams = reactive({
  region: '',
  enterprise_name: '',
  legal_representative: '',
  contact_info: '',
  email: '',
  enterprise_category: undefined,
  sort_field: '',   // 'registered_capital' 或 'establishment_date'
  sort_order: 'asc', // 'asc' 或 'desc'
  page: 1,
  page_size: 10
})

// 获取列表数据
const fetchTableData = async () => {
  loading.value = true
  try {
    const res = await getMarketListApi(queryParams)
    if (res) {
      tableData.value = res.items
      total.value = res.total
    }
  } catch (error) {
    console.error('获取市场信息失败', error)
    ElMessage.error('获取数据失败，请检查网络或后端服务')
  } finally {
    loading.value = false
  }
}

// 点击查询
const handleQuery = () => {
  queryParams.page = 1
  fetchTableData()
}

// 重置查询
const resetQuery = () => {
  queryParams.region = ''
  queryParams.enterprise_name = ''
  queryParams.legal_representative = ''
  queryParams.contact_info = ''
  queryParams.email = ''
  queryParams.enterprise_category = undefined
  queryParams.sort_field = ''
  queryParams.sort_order = 'asc'
  queryParams.page = 1
  queryParams.page_size = 10
  fetchTableData()
}

// 监听表格排序变化
const handleSortChange = ({prop, order}) => {
  if (!order) {
    queryParams.sort_field = ''
    queryParams.sort_order = 'asc'
  } else {
    queryParams.sort_field = prop // 'registered_capital' 或 'establishment_date'
    queryParams.sort_order = order === 'ascending' ? 'asc' : 'desc'
  }
  fetchTableData()
}

// 分页大小改变 (5/10/25/50)
const handleSizeChange = (val) => {
  queryParams.page_size = val
  fetchTableData()
}

// 翻页
const handleCurrentChange = (val) => {
  queryParams.page = val
  fetchTableData()
}

// 自定义 Excel 上传逻辑
const handleUploadExcel = async (options) => {
  const file = options.file
  try {
    const res = await importMarketExcelApi(file)
    if (res && res.code === 200) {
      const data = res.data
      let tipMsg = `导入完成！成功新增 ${data.success_count} 条数据。`
      if (data.skipped_count > 0) {
        tipMsg += ` 有 ${data.skipped_count} 家企业因已存在被自动过滤。`
      }
      ElMessage.success({
        message: tipMsg,
        duration: 5000
      })
      // 刷新表格
      fetchTableData()
    }
  } catch (error) {
    console.error('导入失败', error)
    ElMessage.error('Excel 导入失败，请检查文件内容或格式')
  }
}

// 辅助函数：根据企业类别数字返回标签类型
const getCategoryType = (category) => {
  const map = {
    1: 'success', // 科技 - 绿色
    2: 'warning', // 商服 - 黄色
    3: 'primary', // 合同 - 蓝色
    4: 'danger',  // 劳动 - 红色
    5: 'info'     // 综合 - 灰色
  }
  return map[category] || 'info'
}

// 辅助函数：根据企业类别数字返回文本
const getCategoryText = (category) => {
  const map = {
    1: '科技',
    2: '商服',
    3: '合同',
    4: '劳动',
    5: '综合'
  }
  return map[category] || '未知'
}

// 页面挂载时请求数据
onMounted(() => {
  fetchTableData()
})
</script>