<template>
  <div class="team-info-container">
    <!-- 顶部操作栏 -->
    <div class="page-header">
      <div class="header-title">
        <h2>团队成员管理</h2>
        <p class="sub-title">查看和管理律所所有员工账号与详细资料</p>
      </div>
      <!-- 主任(1)、高级合伙人(2)、行政主管(5) 显示新增用户按钮 -->
      <el-button
          type="primary"
          v-if="[1, 2, 5].includes(currentUserRole)"
          @click="openCreateDialog"
      >
        <el-icon style="margin-right: 4px;">
          <Plus/>
        </el-icon>
        新增团队成员
      </el-button>
    </div>

    <!-- 用户数据表格 -->
    <el-card class="table-card" shadow="never">
      <el-table :data="userList" v-loading="loading" style="width: 100%" stripe>
        <!-- 头像与基本信息 -->
        <el-table-column label="用户名" min-width="auto" header-align="center" align="center">
          <template #default="{ row }">
            <div class="user-cell">
              <el-avatar :size="36" :src="row.avatar" class="user-avatar">
                {{ row.real_name ? row.real_name.charAt(0) : row.username.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username">{{ row.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="真实姓名" min-width="auto" header-align="center" align="center">
          <template #default="{ row }">
            <span>{{ row.real_name || '未填姓名' }}</span>
          </template>
        </el-table-column>
        <!-- 角色标签 -->
        <el-table-column prop="role" label="级别" width="auto" header-align="center" align="center">
          <template #default="{ row }">
            <el-tag :type="getRoleTagType(row.role)" size="default" effect="plain">
              {{ getRoleText(row.role) }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- 电话 -->
        <el-table-column prop="phone" label="联系电话" min-width="auto" header-align="center" align="center">
          <template #default="{ row }">
            <span>{{ row.phone || '暂无电话' }}</span>
          </template>
        </el-table-column>

        <!-- 邮箱 -->
        <el-table-column prop="email" label="电子邮箱" min-width="auto" header-align="center" align="center">
          <template #default="{ row }">
            <span>{{ row.email || '暂无邮箱' }}</span>
          </template>
        </el-table-column>

        <!-- 状态 -->
        <el-table-column prop="is_active" label="账号状态" width="auto" header-align="center" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="default">
              {{ row.is_active ? '正常' : '已禁用' }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- 创建时间 -->
        <el-table-column prop="created_at" label="加入时间" min-width="auto" header-align="center" align="center">
          <template #default="{ row }">
            <span>{{ formatDate(row.created_at) }}</span>
          </template>
        </el-table-column>

        <!-- 最后一列：操作选项 -->
        <el-table-column label="操作" width="120" header-align="center" align="center">
          <template #default="{ row }">
            <el-button
                type="danger"
                size="small"
                link
                v-if="row.is_active"
                @click="openStatusDialog(row, 'freeze')"
            >
              冻结
            </el-button>
            <el-button
                type="success"
                size="small"
                link
                v-else
                @click="openStatusDialog(row, 'unfreeze')"
            >
              解冻
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增用户弹窗表单 -->
    <el-dialog
        v-model="dialogVisible"
        title="新增团队成员"
        width="550px"
        align-center
        class="custom-dialog"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" status-icon>
        <!-- 登录账号 -->
        <el-form-item label="登录账号" prop="username">
          <el-input
              v-model="form.username"
              autocomplete="off"
              placeholder="请输入英文或拼音登录账号"
              clearable
          />
        </el-form-item>

        <!-- 初始密码 -->
        <el-form-item label="初始密码" prop="password">
          <el-input
              v-model="form.password"
              type="password"
              autocomplete="new-password"
              placeholder="请输入初始密码"
              show-password
              clearable
          />
        </el-form-item>

        <!-- 确认密码 -->
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
              v-model="form.confirmPassword"
              type="password"
              autocomplete="new-password"
              placeholder="请再次输入密码"
              show-password
              clearable
          />
        </el-form-item>

        <!-- 真实姓名（必填） -->
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="form.real_name" placeholder="请输入真实姓名" clearable/>
        </el-form-item>

        <!-- 职位角色 -->
        <el-form-item label="职位角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色职位" style="width: 100%;">
            <el-option label="主任" :value="1"/>
            <el-option label="高级合伙人" :value="2"/>
            <el-option label="专职律师" :value="3"/>
            <el-option label="律师助理" :value="4"/>
            <el-option label="行政主管" :value="5"/>
          </el-select>
        </el-form-item>

        <!-- 联系电话（必填） -->
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号码" clearable/>
        </el-form-item>

        <!-- 电子邮箱 -->
        <el-form-item label="电子邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入常用电子邮箱（可选）" clearable/>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitting" @click="submitForm">确定创建</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 公共确认提示框组件：用于冻结与解冻操作 -->
    <ConfirmDialog
        v-model:visible="showStatusDialog"
        title="安全提示"
        :message="statusMessage"
        :confirm-text="actionType === 'freeze' ? '确认冻结' : '确认解冻'"
        :confirm-button-type="actionType === 'freeze' ? 'danger' : 'primary'"
        @confirm="handleConfirmStatus"
        @cancel="showStatusDialog = false"
    />

    <!-- 头像大图预览弹窗 -->
    <el-image-viewer
        v-if="previewVisible"
        :url-list="[form.avatar]"
        @close="previewVisible = false"
    />
  </div>
</template>

<script setup>
import {ref, reactive, onMounted, nextTick} from 'vue'
import {ElMessage} from 'element-plus'
import {Plus, ZoomIn, Delete} from '@element-plus/icons-vue'
import {createUserApi, fetchUserListApi, updateUserStatusApi} from "../../api/user.js";
import ConfirmDialog from "../../components/ConfirmDialog.vue";
// 假设你的公共组件放在这个路径，请根据实际情况调整引用


const userList = ref([])
const loading = ref(false)
const currentUserRole = ref(3)

const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)

// 状态修改弹窗控制
const showStatusDialog = ref(false)
const statusMessage = ref('')
const currentActionRow = ref(null)
const actionType = ref('freeze') // 'freeze' 冻结 或 'unfreeze' 解冻
// 头像交互控制
const previewVisible = ref(false)

// 新增表单数据对象
const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  real_name: '',
  role: 3,
  phone: '',
  email: '',
  avatar: '',
  is_active: true
})

// 密码二次确认校验
const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入的密码不一致！'))
  } else {
    callback()
  }
}

// 表单校验规则
const rules = reactive({
  username: [{required: true, message: '请输入登录账号', trigger: 'blur'}],
  password: [{required: true, message: '请输入初始密码', trigger: 'blur'}],
  confirmPassword: [{required: true, validator: validatePass2, trigger: 'blur'}],
  real_name: [{required: true, message: '请输入员工真实姓名', trigger: 'blur'}],
  phone: [
    {required: true, message: '请输入手机号码', trigger: 'blur'},
    {pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码格式', trigger: 'blur'}
  ],
  role: [{required: true, message: '请选择职位角色', trigger: 'change'}]
})

// 打开确认弹窗
const openStatusDialog = (row, type) => {
  currentActionRow.value = row
  actionType.value = type
  if (type === 'freeze') {
    statusMessage.value = `确定要冻结用户 "${row.real_name || row.username}" 吗？冻结后该账号将无法登录。`
  } else {
    statusMessage.value = `确定要解冻用户 "${row.real_name || row.username}" 吗？解冻后该账号恢复正常登录。`
  }
  showStatusDialog.value = true
}

// 确认执行状态修改
const handleConfirmStatus = async () => {
  if (!currentActionRow.value) return
  const targetRow = currentActionRow.value
  const newStatus = actionType.value === 'unfreeze' // 解冻变 true，冻结变 false

  try {
    // 调用后端更新状态接口
    const res = await updateUserStatusApi(targetRow.id, newStatus)

    if (res && res.code === 200) {
      // 更新本地状态
      targetRow.is_active = newStatus
      ElMessage.success(actionType.value === 'freeze' ? '已成功冻结该账号' : '已成功解冻该账号')
    } else {
      ElMessage.error(res?.detail || '操作失败')
    }
  } catch (error) {
    console.error('状态更新请求异常', error)
    ElMessage.error('网络异常，操作失败')
  } finally {
    showStatusDialog.value = false
    currentActionRow.value = null
  }
}

// 解析当前用户的角色
const parseCurrentUserRole = () => {
  try {
    const token = localStorage.getItem('token')
    if (token) {
      const base64Url = token.split('.')[1]
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
      }).join(''))
      currentUserRole.value = Number(JSON.parse(jsonPayload).role) || 3
    }
  } catch (e) {
    console.error('解析Token角色失败', e)
  }
}

// 获取用户列表
const fetchUserList = async () => {
  loading.value = true
  try {
    const res = await fetchUserListApi()
    if (res && res.code === 200) {
      userList.value = res.data
    } else {
      ElMessage.error(res?.detail || '获取用户列表失败')
    }
  } catch (error) {
    console.error('请求网络错误:', error)
  } finally {
    loading.value = false
  }
}

// 打开新增弹窗
const openCreateDialog = () => {
  dialogVisible.value = true
  nextTick(() => {
    if (formRef.value) {
      formRef.value.resetFields()
    }
    form.username = ''
    form.password = ''
    form.confirmPassword = ''
    form.real_name = ''
    form.role = 3
    form.phone = ''
    form.email = ''
    form.avatar = ''
    form.is_active = true
  })
}

// 提交新增用户
const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const submitData = {
          username: form.username,
          password: form.password,
          real_name: form.real_name,
          role: form.role,
          phone: form.phone,
          email: form.email,
          avatar: form.avatar,
          is_active: form.is_active
        }

        const res = await createUserApi(submitData)
        if (res && res.code === 200) {
          ElMessage.success('用户创建成功！')
          dialogVisible.value = false
          fetchUserList()
        } else {
          ElMessage.error(res?.detail || res?.message || '创建失败')
        }
      } catch (error) {
        console.error('创建用户请求异常:', error)
      } finally {
        submitting.value = false
      }
    }
  })
}

// 职位角色文本映射
const getRoleText = (role) => {
  const map = {1: '主任', 2: '高级合伙人', 3: '专职律师', 4: '律师助理', 5: '行政主管'}
  return map[role] || '未知'
}

// 角色标签颜色
const getRoleTagType = (role) => {
  const map = {1: 'danger', 2: 'warning', 3: 'primary', 4: 'info', 5: 'success'}
  return map[role] || ''
}

// 格式化时间显示
const formatDate = (dateStr) => {
  if (!dateStr) return '无'
  const d = new Date(dateStr)
  return d.toLocaleDateString() + ' ' + d.toTimeString().substring(0, 5)
}

onMounted(() => {
  parseCurrentUserRole()
  fetchUserList()
})
</script>

<style scoped>
.team-info-container {
  padding: 4px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-title h2 {
  font-size: 20px;
  color: #1e293b;
  margin: 0 0 4px 0;
}

.sub-title {
  font-size: 13px;
  color: #64748b;
  margin: 0;
}

.table-card {
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  background-color: #0284c7;
  color: #ffffff;
  font-weight: 600;
  flex-shrink: 0;
}

.username {
  font-size: 12px;
  color: #94a3b8;
}

:deep(.custom-dialog) {
  border-radius: 12px;
  overflow: hidden;
}

.team-info-container :deep(.el-tag) {
  width: 90px;
  justify-content: center;
}
</style>