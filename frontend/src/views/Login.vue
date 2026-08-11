<template>
  <div class="login-container">
    <!-- 背景动态/弥散装饰光晕 -->
    <div class="bg-glow glow-blue"></div>
    <div class="bg-glow glow-red"></div>

    <el-card class="login-card" shadow="never">
      <!-- 头部：律所 VI 品牌视觉标识（根据 Logo 参考图还原） -->
      <div class="login-header">
        <!-- CSS 还原 Logo 艺术线图 -->
        <div class="logo-wrapper">
          <svg class="logo-svg" viewBox="0 0 200 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="logo-grad-blue" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#38bdf8"/>
                <stop offset="100%" stop-color="#0284c7"/>
              </linearGradient>
              <linearGradient id="logo-grad-red" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#7c3aed"/>
                <stop offset="100%" stop-color="#dc2626"/>
              </linearGradient>
            </defs>
            <!-- 蓝色 M 形左侧与折线 -->
            <path d="M 30,70 Q 55,20 85,55 T 130,20" stroke="url(#logo-grad-blue)" stroke-width="12"
                  stroke-linecap="round" stroke-linejoin="round"/>
            <!-- 红色 V 形右侧折线 -->
            <path d="M 125,25 Q 145,80 170,30" stroke="url(#logo-grad-red)" stroke-width="12" stroke-linecap="round"
                  stroke-linejoin="round"/>
          </svg>
        </div>

        <h1 class="brand-title">北京觅理律师事务所</h1>
        <p class="brand-subtitle">Beijing Milly Law Firm</p>

        <div class="system-tag">
          <span class="tag-dot"></span>
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
              <el-icon class="input-icon">
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
              <el-icon class="input-icon">
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
        <span>Rainstorm Legal Service System &copy; 2026</span>
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
/* 1. 容器与高级背景光辉效果 */
.login-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: radial-gradient(circle at 50% 0%, #f8fafc 0%, #e2e8f0 100%);
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
}

/* 弥散光斑氛围感 */
.bg-glow {
  position: absolute;
  width: 420px;
  height: 420px;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.25;
  pointer-events: none;
}

.glow-blue {
  top: -120px;
  left: 25%;
  background: #0284c7;
}

.glow-red {
  bottom: -120px;
  right: 25%;
  background: #dc2626;
}

/* 2. 悬浮圆润高质感卡片 */
.login-card {
  position: relative;
  width: 100%;
  max-width: 420px;
  border-radius: 24px; /* 润滑大圆角 */
  border: 1px solid rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 40px -15px rgba(2, 132, 199, 0.08),
  0 0 15px rgba(255, 255, 255, 0.8) inset;
  padding: 32px 24px 20px 24px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* 3. Logo & 律所品牌 Header */
.login-header {
  text-align: center;
  margin-bottom: 28px;
}

.logo-wrapper {
  width: 100px;
  height: 50px;
  margin: 0 auto 12px auto;
}

.logo-svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 4px 8px rgba(2, 132, 199, 0.2));
}

.brand-title {
  font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", serif;
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: 1.5px;
  margin: 0;
}

.brand-subtitle {
  font-family: "Times New Roman", Times, Georgia, serif;
  font-size: 12px;
  color: #64748b;
  letter-spacing: 1px;
  margin: 4px 0 0 0;
}

/* 系统 Label 胶囊小标签 */
.system-tag {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 1px solid #bae6fd;
  padding: 5px 16px;
  border-radius: 50px; /* 胶囊全圆角 */
  margin-top: 18px;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.06);
}

.tag-dot {
  width: 7px;
  height: 7px;
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
  border-radius: 50%;
  margin-right: 8px;
  box-shadow: 0 0 6px rgba(220, 38, 38, 0.4);
}

.tag-text {
  font-size: 12px;
  font-weight: 600;
  color: #0369a1;
  letter-spacing: 1px;
}

/* 4. 输入框圆润化改造 */
.login-form {
  margin-top: 16px;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-input__wrapper) {
  border-radius: 14px !important; /* 完全圆润输入框 */
  background-color: #f8fafc;
  box-shadow: 0 0 0 1px #e2e8f0 inset !important;
  padding: 6px 16px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.el-input__wrapper:hover) {
  background-color: #ffffff;
  box-shadow: 0 0 0 1.5px #38bdf8 inset !important;
}

:deep(.el-input__wrapper.is-focus) {
  background-color: #ffffff;
  box-shadow: 0 0 0 2px #0284c7 inset, 0 0 12px rgba(2, 132, 199, 0.15) !important;
}

.input-icon {
  font-size: 18px;
  color: #94a3b8;
}

/* 5. 浅蓝色微渐变圆润按钮（Logo 同款色彩） */
.btn-item {
  margin-top: 28px;
  margin-bottom: 12px;
}

.submit-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 6px;
  border-radius: 14px !important; /* 14px 润滑圆角 */
  /* 💡 替换为 Logo 同款的明亮天空蓝渐变 */
  background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
  color: #ffffff;
  border: none;
  box-shadow: 0 8px 20px -4px rgba(2, 132, 199, 0.4);
  transition: all 0.25s ease;
}

.submit-btn:hover {
  /* 悬停时略微提亮 */
  background: linear-gradient(135deg, #7dd3fc 0%, #0369a1 100%);
  box-shadow: 0 12px 24px -4px rgba(2, 132, 199, 0.55);
  transform: translateY(-1px);
}

.submit-btn:active {
  transform: translateY(1px);
  box-shadow: 0 4px 12px -2px rgba(2, 132, 199, 0.3);
}

/* 6. 底部 Footer */
.login-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 11px;
  color: #94a3b8;
  letter-spacing: 0.5px;
}

/* 自动填充样式兼容 */
:deep(input:-webkit-autofill) {
  -webkit-box-shadow: 0 0 0 1000px #ffffff inset !important;
  -webkit-text-fill-color: #0f172a !important;
}
</style>