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
          text-color="#475569"
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
          <el-menu-item index="/dashboard/team-info">
            <el-icon>
              <Tickets/>
            </el-icon>
            <span>团队信息</span>
          </el-menu-item>
        </el-sub-menu>

        <!-- 市场管理 -->
        <el-sub-menu index="market" v-if="userInfo.role === 1">
          <template #title>
            <el-icon>
              <TrendCharts/>
            </el-icon>
            <span>市场管理</span>
          </template>
          <el-menu-item index="/dashboard/market-info">
            <el-icon>
              <Tickets/>
            </el-icon>
            <span>市场信息</span></el-menu-item>
        </el-sub-menu>

        <!-- 案件管理 -->
        <el-sub-menu index="case" v-if="[1, 2, 3, 4].includes(userInfo.role)">
          <template #title>
            <el-icon>
              <FolderOpened/>
            </el-icon>
            <span>业务中心</span>
          </template>
          <el-menu-item index="/dashboard/case-management">
            <el-icon>
              <Tickets/>
            </el-icon>
            <span>案件管理</span></el-menu-item>
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
          <div class="module-tag">
            <span class="module-dot"></span>
            <span class="current-position">当前模块：{{ currentModuleName }}</span>
          </div>
        </div>
        <div class="nav-right">
          <div class="user-badge">
            <el-icon class="badge-icon">
              <User/>
            </el-icon>
            <span class="welcome-text">欢迎您，<strong>{{ userInfo.username }}</strong></span>
            <span class="role-pill">{{ getRoleText(userInfo.role) }}</span>
          </div>
        </div>
      </header>

      <!-- 核心视图容器 -->
      <main class="main-view">
        <div class="view-card">
          <router-view/>
        </div>
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
/* ================= 1. 全局与侧边栏布局 ================= */
/* 1. 修复整体外层背景色（统一为右侧的淡蓝灰底色） */
.dashboard-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: #eaf3ff; /* 💡 修改：精准匹配截图的天蓝背景 */
  overflow: hidden;
  box-sizing: border-box;
}

/* 侧边栏：调整为与右侧一致的卡片式圆角设计 */
.sidebar {
  position: relative;
  width: 240px;
  background-color: #ffffff;
  border: 1px solid rgba(186, 214, 245, 0.7); /* 💡 修改：与顶栏边框色系一致 */
  border-radius: 16px;
  margin: 12px 0 12px 12px;
  box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.03);
  display: flex;
  flex-direction: column;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 10;
  /* overflow: hidden;  💡 移除此行！允许超出定位的折叠按钮正常显示 */
  box-sizing: border-box;
}

.sidebar-collapsed {
  width: 68px;
}

.sidebar-header {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: background-color 0.2s;
  border-top-left-radius: 16px; /* 💡 新增：保证顶部跟随卡片圆角 */
  border-top-right-radius: 16px;
}

.sidebar-header:hover {
  background-color: #f8fafc;
}

.sidebar-collapsed .sidebar-header {
  padding: 0;
}

.logo-icon {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
  color: #ffffff;
  font-weight: 800;
  font-size: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 10px rgba(2, 132, 199, 0.25);
}

.logo-text {
  margin-left: 12px;
  white-space: nowrap;
}

.title-cn {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: 0.5px;
}

.title-en {
  font-size: 9px;
  color: #64748b;
  letter-spacing: 1px;
}

/* ================= 2. 菜单栏 ================= */
.el-menu-vertical {
  border-right: none;
  flex: 1;
  padding: 12px 8px;
}

.sidebar-collapsed .el-menu-vertical {
  padding: 12px 0;
}

:deep(.el-sub-menu__title), :deep(.el-menu-item) {
  font-size: 14px;
  border-radius: 12px !important;
  margin-bottom: 4px;
  height: 44px;
  line-height: 44px;
  transition: all 0.2s ease;
}

:deep(.el-menu-item:hover), :deep(.el-sub-menu__title:hover) {
  background-color: #f1f5f9 !important;
  color: #0284c7 !important;
}

:deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
  color: #0284c7 !important;
  font-weight: 700;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.08);
  border-right: none !important;
}

:deep(.el-menu--collapse .el-sub-menu__title),
:deep(.el-menu--collapse .el-menu-item) {
  justify-content: center !important;
  padding: 0 !important;
}

:deep(.el-menu--collapse .el-sub-menu__title .el-icon),
:deep(.el-menu--collapse .el-menu-item .el-icon) {
  margin: 0 !important;
}

/* ================= 3. 底部用户信息与退出按钮 ================= */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #f1f5f9;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-bottom-left-radius: 16px; /* 💡 新增：保证底部跟随卡片圆角 */
  border-bottom-right-radius: 16px;
}

.sidebar-collapsed .sidebar-footer {
  padding: 16px 0;
  align-items: center;
}

.user-info-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background-color: #f8fafc;
  border-radius: 14px;
}

.user-avatar {
  width: 34px;
  height: 34px;
  background: linear-gradient(135deg, #0284c7 0%, #0f2c59 100%);
  color: #ffffff;
  font-weight: 700;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.2);
}

.user-detail {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.username {
  font-size: 13px;
  font-weight: 700;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 11px;
  color: #0284c7;
  font-weight: 500;
}

.logout-btn {
  width: 100%;
  height: 38px;
  border-radius: 12px !important;
  background: #fef2f2 !important;
  border: 1px solid #fecaca !important;
  color: #dc2626 !important;
  font-weight: 600;
  transition: all 0.25s ease !important;
}

.sidebar-collapsed .logout-btn {
  width: 38px;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logout-btn:hover {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
  color: #ffffff !important;
  border-color: transparent !important;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3) !important;
}

.logout-btn:active {
  transform: scale(0.98);
}

/* 侧边栏展开/收起按钮 */
.collapse-btn {
  position: absolute;
  top: 50%;
  right: -13px;
  transform: translateY(-50%);
  width: 26px;
  height: 26px;
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #64748b;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
  z-index: 20;
  transition: all 0.25s ease;
}

.collapse-btn:hover {
  background-color: #0284c7;
  color: #ffffff;
  border-color: #0284c7;
  box-shadow: 0 4px 10px rgba(2, 132, 199, 0.3);
}

/* ================= 4. 右侧主体内容区域（无底层多余滚动条） ================= */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto; /* 纵向滚动放最外层 */
  overflow-x: hidden; /* 💡 取消/隐藏右部分下边的横向滚动条 */
  background-color: #eaf3ff;
  padding: 12px 12px 12px 8px;
  gap: 12px;
  box-sizing: border-box;
}

/* 顶部 Top-Navbar */
.top-navbar {
  height: 60px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(186, 214, 245, 0.6); /* 💡 修改：使用天蓝调柔和边框 */
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 4px 16px -5px rgba(2, 132, 199, 0.05); /* 💡 修改：微调为蓝色调阴影 */
  z-index: 5;
  flex-shrink: 0;
}

.nav-left .module-tag {
  display: inline-flex;
  align-items: center;
  background-color: #ffffff;
  padding: 6px 16px;
  border-radius: 30px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
}

.module-dot {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
  border-radius: 50%;
  margin-right: 10px;
  box-shadow: 0 0 8px rgba(2, 132, 199, 0.4);
}

.current-position {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: 0.5px;
}

.nav-right .user-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  padding: 5px 8px 5px 14px;
  border-radius: 30px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

.badge-icon {
  font-size: 14px;
  color: #0284c7;
}

.welcome-text {
  font-size: 13px;
  color: #475569;
}

.welcome-text strong {
  color: #0f172a;
  font-weight: 700;
}

.role-pill {
  font-size: 11px;
  font-weight: 600;
  color: #0369a1;
  background: #e0f2fe;
  padding: 3px 10px;
  border-radius: 20px;
  letter-spacing: 0.5px;
}

/* 主视图与卡片区域 */
.main-view {
  flex: 1;
  padding: 0;
  overflow: visible;
  box-sizing: border-box;
}

.view-card {
  min-height: 100%;
  background-color: #ffffff;
  border-radius: 16px;
  border: 1px solid rgba(186, 214, 245, 0.7); /* 💡 修改：匹配天蓝边框 */
  padding: 20px;
  box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.03);
  box-sizing: border-box;
  overflow-x: hidden; /* 💡 避免卡片内容溢出产生底部横向滑动条 */
}

/* 精致自定义滚动条 */
.main-content::-webkit-scrollbar {
  width: 6px;
  height: 0px; /* 💡 隐藏横向滚动条 */
}

.main-content::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-track {
  background: transparent;
}
</style>