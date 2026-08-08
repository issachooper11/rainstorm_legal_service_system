<template>
  <div class="login-container">
    <el-card class="login-card" shadow="never">
      <!-- 头部：律所品牌视觉标识 -->
      <div class="login-header">
        <div class="brand-title">北京觅理律师事务所</div>
        <div class="brand-subtitle">BEIJING MILLY LAW FIRM</div>
        <div class="system-tag">
          <span class="tag-red"></span>
          <span class="tag-text">综合管理系统</span>
        </div>
      </div>

      <!-- 登录表单 -->
      <el-form :model="loginForm" class="login-form">
        <el-form-item>
          <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              clearable
              size="large"
          >
            <template #prefix>
              <el-icon>
                <User/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              show-password
              size="large"
              @keyup.enter="handleLogin"
          >
            <template #prefix>
              <el-icon>
                <Lock/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item class="btn-item">
          <el-button type="primary" class="submit-btn" size="large" @click="handleLogin">
            登 录
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 底部版权 -->
      <div class="login-footer">
        <span>Rainstorm Legal Service System</span>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import {reactive} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {User, Lock} from '@element-plus/icons-vue'
import {loginApi} from '../api/auth'

const router = useRouter()
const loginForm = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  try {
    const res = await loginApi({
      username: loginForm.username,
      password: loginForm.password
    })

    localStorage.setItem('token', res.access_token)

    ElMessage.success('登录成功，欢迎回来！')
    router.push('/dashboard')
  } catch (error) {
    // 错误已由拦截器统一提示
  }
}
</script>

<style scoped>
/* 全局设计规范：亮白基底、统一圆角、蓝红辅助 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f8fafc;
  padding: 16px; /* 兼容手机端边距 */
  box-sizing: border-box;
}

/* 响应式卡片：PC端精致大气，手机端自适应撑满 */
.login-card {
  width: 100%;
  max-width: 420px;
  border-radius: 16px; /* 统一全局标准圆角 */
  border: 1px solid #e2e8f0;
  background-color: #ffffff;
  box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05);
  padding: 24px 16px;
}

/* 品牌头部区 */
.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.brand-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: 0.5px;
}

.brand-subtitle {
  font-size: 10px;
  color: #94a3b8;
  letter-spacing: 2.5px;
  margin-top: 4px;
  text-transform: uppercase;
}

/* 蓝红点缀的系统标题样式（后续页面小标题可参考此规范） */
.system-tag {
  display: inline-flex;
  align-items: center;
  background-color: #f0f9ff;
  border: 1px solid #bae6fd;
  padding: 4px 14px;
  border-radius: 20px;
  margin-top: 16px;
}

.tag-red {
  width: 6px;
  height: 6px;
  background-color: #dc2626; /* 律所经典红点缀 */
  border-radius: 50%;
  margin-right: 6px;
}

.tag-text {
  font-size: 13px;
  font-weight: 600;
  color: #0284c7; /* 清爽专业蓝 */
  letter-spacing: 0.5px;
}

/* 表单与圆角输入框规范 */
.login-form {
  margin-top: 10px;
}

:deep(.el-input__wrapper) {
  border-radius: 10px; /* 统一输入框圆角 */
  background-color: #f8fafc;
  box-shadow: 0 0 0 1px #cbd5e1 inset;
  padding: 4px 12px;
  transition: all 0.2s;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #0284c7 inset;
}

:deep(.el-input__wrapper.is-focus) {
  background-color: #ffffff;
  box-shadow: 0 0 0 1px #0284c7 inset !important;
}

/* 按钮规范：专业蓝，圆角与高度统一 */
.btn-item {
  margin-top: 24px;
  margin-bottom: 10px;
}

.submit-btn {
  width: 100%;
  height: 46px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 4px;
  border-radius: 10px; /* 统一按钮圆角 */
  background-color: #0284c7;
  border: none;
  transition: background-color 0.2s;
}

.submit-btn:hover {
  background-color: #0369a1;
}

/* 底部版权 */
.login-footer {
  text-align: center;
  margin-top: 24px;
  font-size: 11px;
  color: #cbd5e1;
  letter-spacing: 0.5px;
}

/* 覆盖浏览器自动填充账号密码时的背景色和文字颜色 */
:deep(input:-webkit-autofill),
:deep(input:-webkit-autofill:hover),
:deep(input:-webkit-autofill:focus),
:deep(input:-webkit-autofill:active) {
  -webkit-box-shadow: 0 0 0 1000px #ffffff inset !important; /* 把背景色强制设为白色 (#ffffff) 或你输入框原本的背景色 */
  -webkit-text-fill-color: #1e293b !important; /* 强制文字颜色保持正常 */
  transition: background-color 5000s ease-in-out 0s; /* 延缓背景色过渡，防止闪烁 */
}
</style>