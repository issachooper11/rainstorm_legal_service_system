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
            <el-tag :type="getRoleTagType(row.role)" size="medium" effect="plain">
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
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="medium">
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

        <!-- 头像上传（支持本地预览与删除） -->
        <!--        <el-form-item label="员工头像">-->
        <!--          <div class="avatar-upload-wrapper">-->
        <!--            <el-upload-->
        <!--                class="avatar-uploader"-->
        <!--                :show-file-list="false"-->
        <!--                :http-request="customUploadAvatar"-->
        <!--                :before-upload="beforeAvatarUpload"-->
        <!--            >-->
        <!--              <div v-if="form.avatar" class="avatar-preview-box" @mouseenter="showOverlay = true"-->
        <!--                   @mouseleave="showOverlay = false">-->
        <!--                <img :src="form.avatar" class="uploaded-avatar"/>-->
        <!--                &lt;!&ndash; 悬浮操作层：预览或删除 &ndash;&gt;-->
        <!--                <div v-if="showOverlay" class="avatar-overlay" @click.stop>-->
        <!--                  <el-icon @click="handlePreview">-->
        <!--                    <ZoomIn/>-->
        <!--                  </el-icon>-->
        <!--                  <el-icon @click="handleRemoveAvatar">-->
        <!--                    <Delete/>-->
        <!--                  </el-icon>-->
        <!--                </div>-->
        <!--              </div>-->
        <!--              <el-icon v-else class="avatar-uploader-icon">-->
        <!--                <Plus/>-->
        <!--              </el-icon>-->
        <!--            </el-upload>-->
        <!--            <div class="upload-tip">支持 JPG/PNG/WEBP 格式，大小不超过 2MB</div>-->
        <!--          </div>-->
        <!--        </el-form-item>-->

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
import {createUserApi, fetchUserListApi} from "../../api/user.js";


const userList = ref([])
const loading = ref(false)
const currentUserRole = ref(3)

const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)

// 头像交互控制
const showOverlay = ref(false)
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
  avatar: '', // 对应数据库字段，存储图片链接或Base64
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

// 自定义本地图片转 Base64 预览（或对接你的文件上传接口）
const customUploadAvatar = (options) => {
  const file = options.file
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onload = (e) => {
    form.avatar = e.target.result // 赋值后直接在表单中实时预览
    ElMessage.success('头像加载成功')
  }
}

// 头像上传前校验
const beforeAvatarUpload = (file) => {
  const isImage = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/webp'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('上传头像图片只能是 JPG/PNG/WEBP 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('上传头像图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 预览大图
const handlePreview = () => {
  previewVisible.value = true
}

// 删除已选头像
const handleRemoveAvatar = () => {
  form.avatar = ''
  showOverlay.value = false
  ElMessage.info('已移除头像')
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
          avatar: form.avatar, // 对应数据库字段提交
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
  const map = {1: ' 主任', 2: '高级合伙人', 3: '专职律师', 4: '律师助理', 5: '行政主管'}
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

.user-name-box {
  display: flex;
  flex-direction: row;
}

.real-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.username {
  font-size: 12px;
  color: #94a3b8;
}

/* 头像上传与预览删除交互样式 */
.avatar-upload-wrapper {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.avatar-uploader :deep(.el-upload) {
  border: 1px dashed #d9d9d9;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader :deep(.el-upload):hover {
  border-color: var(--el-color-primary);
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 80px;
  height: 80px;
  text-align: center;
  line-height: 80px;
}

.avatar-preview-box {
  position: relative;
  width: 80px;
  height: 80px;
}

.uploaded-avatar {
  width: 80px;
  height: 80px;
  display: block;
  object-fit: cover;
  border-radius: 8px;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  color: #fff;
  font-size: 18px;
  border-radius: 8px;
}

.avatar-overlay .el-icon {
  cursor: pointer;
  transition: transform 0.2s;
}

.avatar-overlay .el-icon:hover {
  transform: scale(1.2);
  color: var(--el-color-primary-light-3);
}

.upload-tip {
  font-size: 12px;
  color: #94a3b8;
}

:deep(.custom-dialog) {
  border-radius: 12px;
  overflow: hidden;
}

/* 让表格里的角色标签宽度统一，且文字居中 */
.team-info-container :deep(.el-tag) {
  width: 90px; /* 你可以根据实际视觉效果调整这个数值，比如 85px 或 90px */
  justify-content: center; /* 让 Element Plus 标签内部的文字水平居中 */
}
</style>