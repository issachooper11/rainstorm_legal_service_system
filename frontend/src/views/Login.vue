<template>
  <div class="login-container">
    <!-- 背景极简纯净弥散光晕 -->
    <div class="bg-glow glow-blue"></div>
    <div class="bg-glow glow-red"></div>

    <el-card class="login-card" shadow="never">
      <!-- 头部：律所 VI 品牌视觉标识 -->
      <div class="login-header">
        <!-- SVG Logo 纯蓝纯红 -->
        <div class="logo-wrapper">
          <svg class="logo-svg" viewBox="0 0 200 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="logo-grad-blue" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#2563eb"/>
                <stop offset="100%" stop-color="#1d4ed8"/>
              </linearGradient>
              <linearGradient id="logo-grad-red" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ef4444"/>
                <stop offset="100%" stop-color="#dc2626"/>
              </linearGradient>
            </defs>
            <!-- 纯蓝 M 形左侧与折线 -->
            <path d="M 30,70 Q 55,20 85,55 T 130,20" stroke="url(#logo-grad-blue)" stroke-width="12"
                  stroke-linecap="round" stroke-linejoin="round"/>
            <!-- 纯红 V 形右侧折线 -->
            <path d="M 125,25 Q 145,80 170,30" stroke="url(#logo-grad-red)" stroke-width="12" stroke-linecap="round"
                  stroke-linejoin="round"/>
          </svg>
        </div>

        <h1 class="brand-title">北京觅理律师事务所</h1>
        <p class="brand-subtitle">BEIJING MILLY LAW FIRM</p>

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
/* 1. 纯白主体背景 + 纯蓝纯红极弱光晕 */
.login-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #ffffff; /* 主色：纯白 */
  background-image: radial-gradient(#e2e8f0 0.8px, transparent 0.8px); /* 极细白灰色点阵纹理 */
  background-size: 24px 24px;
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
}

/* 极简红蓝柔和光晕 */
.bg-glow {
  position: absolute;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.1;
  pointer-events: none;
}

.glow-blue {
  top: -150px;
  left: -100px;
  background: #1d4ed8; /* 深纯蓝 */
}

.glow-red {
  bottom: -150px;
  right: -100px;
  background: #dc2626; /* 纯红 */
}

/* 2. 纯白清爽高质感卡片 */
.login-card {
  position: relative;
  width: 100%;
  max-width: 410px;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.08),
  0 1px 3px rgba(0, 0, 0, 0.02);
  padding: 36px 28px 24px 28px;
  transition: all 0.3s ease;
}

/* 3. Header 品牌区域 */
.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo-wrapper {
  width: 100px;
  height: 50px;
  margin: 0 auto 14px auto;
}

.logo-svg {
  width: 100%;
  height: 100%;
}

.brand-title {
  font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: 1.5px;
  margin: 0;
}

.brand-subtitle {
  font-family: "Arial", sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  letter-spacing: 1.5px;
  margin: 6px 0 0 0;
}

/* 系统 Label 胶囊小标签 (纯蓝+纯红) */
.system-tag {
  display: inline-flex;
  align-items: center;
  background-color: #eff6ff; /* 浅纯蓝衬底 */
  border: 1px solid #bfdbfe;
  padding: 4px 14px;
  border-radius: 50px;
  margin-top: 18px;
}

.tag-dot {
  width: 7px;
  height: 7px;
  background-color: #dc2626; /* 纯红 */
  border-radius: 50%;
  margin-right: 8px;
  box-shadow: 0 0 6px rgba(220, 38, 38, 0.5);
}

.tag-text {
  font-size: 12px;
  font-weight: 700;
  color: #1d4ed8; /* 纯深蓝 */
  letter-spacing: 1px;
}

/* 4. 输入框改造 */
.login-form {
  margin-top: 10px;
}

:deep(.el-form-item) {
  margin-bottom: 22px;
}

:deep(.el-input__wrapper) {
  border-radius: 12px !important;
  background-color: #ffffff;
  box-shadow: 0 0 0 1px #cbd5e1 inset !important;
  padding: 6px 16px;
  transition: all 0.25s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1.5px #2563eb inset !important;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px #1d4ed8 inset, 0 0 10px rgba(29, 78, 216, 0.15) !important;
}

.input-icon {
  font-size: 18px;
  color: #64748b;
}

/* 5. 💡 浓郁纯深蓝为主调的微红渐变按钮 */
.btn-item {
  margin-top: 30px;
  margin-bottom: 12px;
}

.submit-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 6px;
  border-radius: 12px !important;
  /* 💡 核心调整：1d4ed8(纯深蓝 0%) -> 2563eb(纯宝蓝 75%) -> dc2626(纯红 100%) */
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%, #dc2626 100%) !important;
  color: #ffffff !important;
  border: none !important;
  box-shadow: 0 8px 20px -4px rgba(29, 78, 216, 0.45);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.submit-btn:hover {
  /* 悬停时加深纯蓝饱和度 */
  background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 60%, #b91c1c 100%) !important;
  box-shadow: 0 12px 24px -4px rgba(29, 78, 216, 0.55);
  transform: translateY(-2px);
}

.submit-btn:active {
  transform: translateY(1px);
  box-shadow: 0 4px 12px -2px rgba(29, 78, 216, 0.3);
}

/* 6. 底部 Footer */
.login-footer {
  text-align: center;
  margin-top: 24px;
  font-size: 12px;
  color: #94a3b8;
  letter-spacing: 0.5px;
}

/* 自动填充样式兼容 */
:deep(input:-webkit-autofill) {
  -webkit-box-shadow: 0 0 0 1000px #ffffff inset !important;
  -webkit-text-fill-color: #0f172a !important;
}
</style>