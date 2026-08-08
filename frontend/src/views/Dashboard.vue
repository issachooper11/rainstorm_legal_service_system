<template>
  <div class="dashboard-container">
    <!-- 左侧工具栏 -->
    <aside :class="['sidebar', { 'sidebar-collapsed': isCollapsed }]">
      <!-- 顶部 Logo 区域 -->
      <div class="sidebar-header" @click="router.push('/dashboard/team-info')">
        <div class="logo-icon">M</div>
        <div class="logo-text" v-show="!isCollapsed">
          <div class="title-cn">北京觅理律师事务所</div>
          <div class="title-en">MILICY LAW FIRM</div>
        </div>
      </div>

      <!-- 中间菜单栏 -->
      <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical"
          :collapse="isCollapsed"
          :router="true"
          background-color="#ffffff"
          text-color="#1e293b"
          active-text-color="#0284c7"
      >
        <!-- 团队管理 -->
        <el-sub-menu index="team" v-if="[1, 2, 5].includes(userInfo.role)">
          <template #title>
            <el-icon>
              <User/>
            </el-icon>
            <span>团队管理</span>
          </template>
          <el-menu-item index="/dashboard/team-info">团队信息</el-menu-item>
        </el-sub-menu>

        <!-- 市场管理 -->
        <el-sub-menu index="market" v-if="userInfo.role === 1">
          <template #title>
            <el-icon>
              <TrendCharts/>
            </el-icon>
            <span>市场管理</span>
          </template>
          <el-menu-item index="/dashboard/market-info">市场信息</el-menu-item>
        </el-sub-menu>

        <!-- 案件管理 -->
        <el-sub-menu index="case" v-if="[1, 2, 3, 4].includes(userInfo.role)">
          <template #title>
            <el-icon>
              <FolderOpened/>
            </el-icon>
            <span>业务中心</span>
          </template>
          <el-menu-item index="/dashboard/case-management">案件管理</el-menu-item>
        </el-sub-menu>
      </el-menu>

      <!-- 底部：用户信息与退出登录按钮 -->
      <div class="sidebar-footer">
        <div class="user-info-box" v-show="!isCollapsed">
          <div class="user-avatar">{{ userInfo.username.charAt(0).toUpperCase() }}</div>
          <div class="user-detail">
            <span class="username">{{ userInfo.username }}</span>
            <span class="user-role">{{ getRoleText(userInfo.role) }}</span>
          </div>
        </div>
        <el-button
            type="danger"
            plain
            size="small"
            class="logout-btn"
            @click="showLogoutDialog = true"
            :title="isCollapsed ? '退出登录' : ''"
        >
          <el-icon>
            <SwitchButton/>
          </el-icon>
          <span v-show="!isCollapsed" style="margin-left: 4px;">退出</span>
        </el-button>
      </div>

      <!-- 侧边栏折叠竖直箭头按钮 -->
      <div class="collapse-btn" @click="toggleSidebar" :title="isCollapsed ? '展开菜单' : '收起菜单'">
        <el-icon>
          <component :is="isCollapsed ? 'ArrowRight' : 'ArrowLeft'"/>
        </el-icon>
      </div>
    </aside>

    <!-- 右侧主体内容区域 -->
    <div class="main-content">
      <header class="top-navbar">
        <div class="nav-left">
          <span class="current-position">当前模块：{{ currentModuleName }}</span>
        </div>
        <div class="nav-right">
          <span class="welcome-text">欢迎您，{{ userInfo.username }} ({{ getRoleText(userInfo.role) }})</span>
        </div>
      </header>

      <main class="main-view">
        <router-view/>
      </main>
    </div>

    <!-- 引用公共退出确认弹窗组件 -->
    <ConfirmDialog
        v-model:visible="showLogoutDialog"
        title="安全提示"
        message="确定要退出当前账号登录吗？"
        confirm-text="确认退出"
        confirm-button-type="danger"
        @confirm="handleLogout"
        @cancel="showLogoutDialog = false"
    />
  </div>
</template>

<script setup>
import {computed, reactive, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {User, TrendCharts, FolderOpened, ArrowLeft, ArrowRight, SwitchButton} from '@element-plus/icons-vue'
import ConfirmDialog from "../components/ConfirmDialog.vue";
// 引入公共弹窗组件


const router = useRouter()
const route = useRoute()

// 控制退出弹窗显示
const showLogoutDialog = ref(false)

const isCollapsed = ref(false)
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

const userInfo = reactive({
  username: 'Admin',
  role: 3
})

try {
  const token = localStorage.getItem('token')
  if (token) {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    }).join(''))
    const parsed = JSON.parse(jsonPayload)
    userInfo.username = parsed.sub || '用户'
    userInfo.role = Number(parsed.role) || 3
  }
} catch (e) {
  console.error('解析Token失败', e)
}

const currentModuleName = computed(() => route.meta.title || '工作台')
const activeMenu = computed(() => route.path)

// 执行真正的退出登录逻辑
const handleLogout = () => {
  showLogoutDialog.value = false
  localStorage.removeItem('token')
  ElMessage.success('已安全退出登录')
  router.push('/login')
}

const getRoleText = (roleNum) => {
  const map = {
    1: '主任',
    2: '高级合伙人',
    3: '专职律师',
    4: '律师助理',
    5: '行政主管'
  }
  return map[roleNum] || '未知角色'
}
</script>

<style scoped>
/* 保持你原本的样式不变 */
.dashboard-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: #f8fafc;
  overflow: hidden;
  box-sizing: border-box;
}

.sidebar {
  position: relative;
  width: 240px;
  background-color: #ffffff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  z-index: 10;
}

.sidebar-collapsed {
  width: 64px;
}

.sidebar-header {
  height: 70px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background-color: #0284c7;
  color: #ffffff;
  font-weight: 700;
  font-size: 18px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.logo-text {
  margin-left: 12px;
  white-space: nowrap;
}

.title-cn {
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
}

.title-en {
  font-size: 9px;
  color: #94a3b8;
  letter-spacing: 1px;
}

.el-menu-vertical {
  border-right: none;
  flex: 1;
}

:deep(.el-sub-menu__title), :deep(.el-menu-item) {
  font-size: 14px;
}

:deep(.el-menu-item.is-active) {
  background-color: #f0f9ff !important;
  font-weight: 600;
  border-right: 3px solid #0284c7;
}

.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid #f1f5f9;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.user-info-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
}

.user-avatar {
  width: 32px;
  height: 32px;
  background-color: #0f2c59;
  color: #ffffff;
  font-weight: 600;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.user-detail {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.username {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 11px;
  color: #0284c7;
}

.logout-btn {
  width: 100%;
  border-radius: 6px;
}

.collapse-btn {
  position: absolute;
  top: 50%;
  right: -12px;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #64748b;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  z-index: 20;
  transition: all 0.2s;
}

.collapse-btn:hover {
  background-color: #0284c7;
  color: #ffffff;
  border-color: #0284c7;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-navbar {
  height: 70px;
  background-color: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.current-position {
  font-size: 15px;
  font-weight: 600;
  color: #334155;
}

.welcome-text {
  font-size: 13px;
  color: #64748b;
}

.main-view {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}
</style>