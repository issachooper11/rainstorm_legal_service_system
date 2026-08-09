<template>
  <div class="market-container">
    <!-- 1. 顶部搜索与操作卡片 -->
    <el-card class="filter-card" shadow="never" style="margin-bottom: 20px;">
      <el-form :model="queryParams" class="search-form">
        <!-- 第一行输入框：地区、名称、法代 -->
        <div class="form-row">
          <el-form-item label="地区" class="form-item-custom">
            <el-input v-model="queryParams.region" placeholder="请输入地区" clearable @clear="handleQuery"/>
          </el-form-item>
          <el-form-item label="名称" class="form-item-custom">
            <el-input v-model="queryParams.enterprise_name" placeholder="请输入企业名称" clearable
                      @clear="handleQuery"/>
          </el-form-item>
          <el-form-item label="法代" class="form-item-custom">
            <el-input v-model="queryParams.legal_representative" placeholder="请输入法定代表人" clearable
                      @clear="handleQuery"/>
          </el-form-item>
        </div>

        <!-- 第二行输入框：电话、邮箱、类别 -->
        <div class="form-row" style="margin-top: 12px;">
          <el-form-item label="电话" class="form-item-custom">
            <el-input v-model="queryParams.contact_info" placeholder="请输入联系方式" clearable @clear="handleQuery"/>
          </el-form-item>
          <el-form-item label="邮箱" class="form-item-custom">
            <el-input v-model="queryParams.email" placeholder="请输入邮箱" clearable @clear="handleQuery"/>
          </el-form-item>
          <el-form-item label="类别" class="form-item-custom">
            <el-select v-model="queryParams.enterprise_category" placeholder="全部类别" clearable style="width: 100%;"
                       @change="handleQuery">
              <el-option label="科技" :value="1"/>
              <el-option label="商服" :value="2"/>
              <el-option label="合同" :value="3"/>
              <el-option label="劳动" :value="4"/>
              <el-option label="综合" :value="5"/>
            </el-select>
          </el-form-item>
        </div>

        <!-- 第三行：按钮操作区（整体右对齐，等间距） -->
        <div class="form-row action-row">
          <div class="action-right">
            <!-- 开启多选时显示的批量操作按钮 -->
            <template v-if="isMultiSelect">
              <el-button type="danger" plain @click="handleBatchDelete">
                <el-icon>
                  <Delete/>
                </el-icon>
                <span>批量删除</span>
              </el-button>
              <el-button type="warning" plain @click="handleBatchEmail">
                <el-icon>
                  <Message/>
                </el-icon>
                <span>批量发送邮件</span>
              </el-button>
              <el-button type="success" plain @click="handleBatchSms">
                <el-icon>
                  <Iphone/>
                </el-icon>
                <span>批量发送短信</span>
              </el-button>
              <!-- 批量按钮与基础按钮之间的分割线 -->
              <el-divider direction="vertical" class="action-divider"/>
            </template>

            <!-- 查询与重置 -->
            <el-button type="primary" @click="handleQuery">
              <el-icon>
                <Search/>
              </el-icon>
              <span>查询</span>
            </el-button>
            <el-button @click="resetQuery">
              <el-icon>
                <Refresh/>
              </el-icon>
              <span>重置</span>
            </el-button>

            <!-- 分割线 -->
            <el-divider direction="vertical" class="action-divider"/>

            <!-- 上传 Excel 图标按钮 -->
            <el-tooltip content="一键导入 Excel" placement="top">
              <el-upload
                  action="#"
                  :http-request="handleUploadExcel"
                  :show-file-list="false"
                  accept=".xlsx, .xls"
                  class="inline-upload"
              >
                <el-button type="success" circle>
                  <el-icon>
                    <Upload/>
                  </el-icon>
                </el-button>
              </el-upload>
            </el-tooltip>

            <!-- 多选模式开关 -->
            <el-tooltip :content="isMultiSelect ? '关闭多选模式' : '开启多选模式'" placement="top">
              <el-button
                  :type="isMultiSelect ? 'primary' : 'default'"
                  circle
                  @click="toggleMultiSelect"
              >
                <el-icon><Select/></el-icon>
              </el-button>
            </el-tooltip>

            <!-- 操作列显隐开关 -->
            <el-tooltip :content="showOperationCol ? '隐藏操作列' : '显示操作列'" placement="top">
              <el-button
                  :type="showOperationCol ? 'primary' : 'default'"
                  circle
                  @click="showOperationCol = !showOperationCol"
              >
                <el-icon>
                  <Operation/>
                </el-icon>
              </el-button>
            </el-tooltip>
          </div>
        </div>
      </el-form>
    </el-card>

    <!-- 2. 数据表格区域 -->
    <el-card shadow="never">
      <el-table
          :data="tableData"
          style="width: 100%"
          v-loading="loading"
          @sort-change="handleSortChange"
          @selection-change="handleSelectionChange"
          border
      >
        <!-- 多选列 -->
        <el-table-column
            v-if="isMultiSelect"
            type="selection"
            width="55"
            align="center"
            header-align="center"
        />

        <el-table-column type="index" label="序号" min-width="60" align="center" header-align="center"/>

        <!-- 企业类别列 -->
        <el-table-column prop="enterprise_category" label="类别" width="auto" align="center" header-align="center">
          <template #default="{ row }">
            <el-tag :type="getCategoryType(row.enterprise_category)">
              {{ getCategoryText(row.enterprise_category) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="region" label="地区" width="60" align="center" header-align="center"/>
        <el-table-column prop="enterprise_name" label="企业名称" min-width="250" show-overflow-tooltip align="center"
                         header-align="center"/>
        <el-table-column prop="legal_representative" label="法定代表人" width="100" align="center"
                         header-align="center"/>

        <!-- 联系方式列（多行展示） -->
        <el-table-column prop="contact_info" label="联系方式" min-width="120" align="center" header-align="center">
          <template #default="scope">
            <div v-for="(item, index) in formatContacts(scope.row.contact_info)" :key="index">
              {{ item }}
            </div>
          </template>
        </el-table-column>

        <!-- 邮箱列（多行展示） -->
        <el-table-column prop="email" label="邮箱" min-width="180" align="center" header-align="center">
          <template #default="scope">
            <div v-for="(item, index) in formatContacts(scope.row.email)" :key="index">
              {{ item }}
            </div>
          </template>
        </el-table-column>

        <!-- 成立日期排序 -->
        <el-table-column prop="establishment_date" label="成立日期" width="110" sortable="custom" align="center"
                         header-align="center"/>

        <!-- 注册资本排序 -->
        <el-table-column prop="registered_capital" label="注册资本" width="140" sortable="custom" align="center"
                         header-align="center">
          <template #default="{ row }">
            <span>{{ row.registered_capital ? row.registered_capital + ' 万元' : '暂无' }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="enterprise_type" label="企业类型" min-width="150" align="center" show-overflow-tooltip
                         header-align="center"/>
        <el-table-column prop="registered_address" label="注册地址" min-width="200" show-overflow-tooltip
                         header-align="center"/>

        <!-- 操作列 -->
        <el-table-column
            v-if="showOperationCol"
            label="操作"
            width="100"
            fixed="right"
            align="center"
            header-align="center"
        >
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleOpenTrace(row)">
              记录
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 3. 分页组件 -->
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

    <!-- 4. 跟进记录侧边抽屉 (Drawer) -->
    <el-drawer
        v-model="traceDrawerVisible"
        :title="`跟进记录 - ${currentEnterprise.enterprise_name || ''}`"
        size="500px"
        direction="rtl"
    >
      <!-- 上半部分：写跟进表单 -->
      <div class="trace-form-box" style="margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #ebeef5;">
        <h4 style="margin-bottom: 10px; color: #303133;">添加新跟进</h4>
        <el-form :model="traceForm" label-width="80px">
          <el-form-item label="跟进方式">
            <el-select v-model="traceForm.trace_type" placeholder="请选择跟进方式" style="width: 100%;">
              <el-option label="邮件" :value="1"/>
              <el-option label="电话" :value="2"/>
              <el-option label="微信" :value="3"/>
              <el-option label="线下" :value="4"/>
            </el-select>
          </el-form-item>
          <el-form-item label="跟进内容">
            <el-input
                v-model="traceForm.content"
                type="textarea"
                :rows="3"
                placeholder="请输入本次沟通详情、客户反馈等..."
            />
          </el-form-item>
          <el-form-item style="margin-bottom: 0; text-align: right;">
            <el-button type="primary" :loading="traceSubmitting" @click="submitTrace">提交跟进</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 下半部分：历史跟进时间轴 -->
      <div class="trace-timeline-box">
        <h4 style="margin-bottom: 15px; color: #303133;">历史跟进轨迹</h4>
        <div v-if="traceList.length === 0" style="color: #909399; text-align: center; padding: 20px 0;">
          暂无跟进记录
        </div>

        <div v-else class="timeline-scroll-container">
          <el-timeline>
            <el-timeline-item
                v-for="item in traceList"
                :key="item.id"
                :timestamp="formatDate(item.created_at)"
                placement="top"
            >
              <el-card shadow="hover" style="margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                  <el-tag size="small" :type="getTraceTypeTag(item.trace_type)">
                    {{ getTraceTypeText(item.trace_type) }}
                  </el-tag>
                  <span style="font-size: 12px; color: #909399;">跟进人：{{ item.creator_name }}</span>
                </div>
                <p style="margin: 5px 0 0 0; white-space: pre-wrap; word-break: break-all; font-size: 14px; color: #606266;">
                  {{ item.content }}
                </p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Upload, Operation, Select, Search, Refresh, Delete, Message, Iphone} from '@element-plus/icons-vue'
import {getMarketListApi, importMarketExcelApi} from "../../api/market.js"
import {getEnterpriseTracesApi, createEnterpriseTraceApi} from "../../api/trace.js"

// 时间格式化函数
const formatDate = (isoString) => {
  if (!isoString) return ''
  return isoString.replace('T', ' ').split('.')[0]
}

// 表格状态
const loading = ref(false)
const tableData = ref([])
const total = ref(0)

// 功能开关与多选
const showOperationCol = ref(true)
const isMultiSelect = ref(false)
const selectedRows = ref([])

const handleSelectionChange = (val) => {
  selectedRows.value = val
}

const toggleMultiSelect = () => {
  isMultiSelect.value = !isMultiSelect.value
  if (!isMultiSelect.value) {
    selectedRows.value = [] // 关闭多选模式时清空已选
  }
}

// --- 批量处理占位方法 ---
const handleBatchDelete = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请先勾选需要批量删除的项')
    return
  }
  ElMessageBox.confirm(`确认要删除已选中的 ${selectedRows.value.length} 项数据吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    console.log('待删除的项：', selectedRows.value)
    ElMessage.info('已触发批量删除，请在此处接入 API')
  }).catch(() => {
  })
}

const handleBatchEmail = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请先勾选需要发送邮件的项')
    return
  }
  console.log('待发送邮件的项：', selectedRows.value)
  ElMessage.info(`已选择 ${selectedRows.value.length} 项，请在此处接入批量发送邮件 API`)
}

const handleBatchSms = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请先勾选需要发送短信的项')
    return
  }
  console.log('待发送短信的项：', selectedRows.value)
  ElMessage.info(`已选择 ${selectedRows.value.length} 项，请在此处接入批量发送短信 API`)
}

// 抽屉状态
const traceDrawerVisible = ref(false)
const currentEnterprise = ref({})
const traceList = ref([])
const traceSubmitting = ref(false)
const traceForm = reactive({
  trace_type: 2,
  content: ''
})

// 查询参数
const queryParams = reactive({
  region: '',
  enterprise_name: '',
  legal_representative: '',
  contact_info: '',
  email: '',
  enterprise_category: undefined,
  sort_field: '',
  sort_order: 'asc',
  page: 1,
  page_size: 10
})

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

const handleQuery = () => {
  queryParams.page = 1
  fetchTableData()
}

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

const handleSortChange = ({prop, order}) => {
  if (!order) {
    queryParams.sort_field = ''
    queryParams.sort_order = 'asc'
  } else {
    queryParams.sort_field = prop
    queryParams.sort_order = order === 'ascending' ? 'asc' : 'desc'
  }
  fetchTableData()
}

const handleSizeChange = (val) => {
  queryParams.page_size = val
  fetchTableData()
}

const handleCurrentChange = (val) => {
  queryParams.page = val
  fetchTableData()
}

const handleOpenTrace = async (row) => {
  currentEnterprise.value = row
  traceForm.content = ''
  traceForm.trace_type = 2
  traceDrawerVisible.value = true
  await fetchTraces(row.id)
}

const fetchTraces = async (enterpriseId) => {
  try {
    const res = await getEnterpriseTracesApi(enterpriseId)
    if (res) {
      traceList.value = res
    }
  } catch (error) {
    console.error('获取跟进记录失败', error)
    ElMessage.error('获取跟进记录失败')
  }
}

const submitTrace = async () => {
  if (!traceForm.content.trim()) {
    ElMessage.warning('请输入跟进详细内容')
    return
  }
  traceSubmitting.value = true
  try {
    await createEnterpriseTraceApi(currentEnterprise.value.id, {
      trace_type: traceForm.trace_type,
      content: traceForm.content
    })
    ElMessage.success('跟进记录添加成功')
    traceForm.content = ''
    await fetchTraces(currentEnterprise.value.id)
  } catch (error) {
    console.error('添加跟进失败', error)
    ElMessage.error('添加失败')
  } finally {
    traceSubmitting.value = false
  }
}

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
      fetchTableData()
    }
  } catch (error) {
    console.error('导入失败', error)
    ElMessage.error('Excel 导入失败，请检查文件内容或格式')
  }
}

const getCategoryType = (category) => {
  const map = {1: 'success', 2: 'warning', 3: 'primary', 4: 'danger', 5: 'info'}
  return map[category] || 'info'
}

const getCategoryText = (category) => {
  const map = {1: '科技', 2: '商服', 3: '合同', 4: '劳动', 5: '综合'}
  return map[category] || '未知'
}

const getTraceTypeTag = (type) => {
  const map = {1: 'info', 2: 'success', 3: 'warning', 4: 'danger'}
  return map[type] || ''
}

const getTraceTypeText = (type) => {
  const map = {1: '邮件', 2: '电话', 3: '微信', 4: '线下'}
  return map[type] || '未知'
}

const formatContacts = (contactStr) => {
  if (!contactStr) return []
  return contactStr.split(/[,，\s]+/)
}

onMounted(() => {
  fetchTableData()
})
</script>

<style scoped>
/* 整个 Form 容器 */
.search-form {
  width: 100%;
}

/* 每一行输入框容器：3 列平分，间距 16px */
.form-row {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
}

/* 第三行操作栏专用样式：靠右对齐 */
.action-row {
  margin-top: 16px;
  justify-content: flex-end;
}

/* 统一控制每个输入框/下拉框同宽与对齐 */
.form-item-custom {
  flex: 1;
  margin: 0 !important;
}

.form-item-custom :deep(.el-form-item__content) {
  width: 100%;
}

.form-item-custom :deep(.el-input),
.form-item-custom :deep(.el-select) {
  width: 100% !important;
}

/* 按钮组：靠右排布、统一 12px 间距 */
.action-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-right .el-button {
  margin: 0 !important; /* 清除默认外边距 */
}

.action-divider {
  margin: 0 4px;
  height: 18px;
}

.inline-upload {
  display: inline-flex;
  align-items: center;
}

/* 抽屉滚动条 */
.timeline-scroll-container {
  max-height: 50vh;
  overflow-y: auto;
  padding-right: 8px;
}

.timeline-scroll-container::-webkit-scrollbar {
  width: 6px;
}

.timeline-scroll-container::-webkit-scrollbar-thumb {
  background-color: #dcdfe6;
  border-radius: 3px;
}

.timeline-scroll-container::-webkit-scrollbar-thumb:hover {
  background-color: #c0c4cc;
}
</style>