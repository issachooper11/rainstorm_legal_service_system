<template>
  <div class="dashboard-container">
    <!-- 极简纯净背景光晕 -->
    <div class="bg-glow glow-blue"></div>
    <div class="bg-glow glow-red"></div>

    <!-- 左侧工具栏 -->
    <aside :class="['sidebar', { 'sidebar-collapsed': isCollapsed }]">
      <!-- 顶部 Logo 区域 -->
      <div class="sidebar-header" @click="router.push('/dashboard/team-info')">
        <div class="logo-icon">M</div>
        <div class="logo-text" v-show="!isCollapsed">
          <div class="title-cn">北京觅理律师事务所</div>
          <div class="title-en">BEIJING MILLY LAW FIRM</div>
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
          active-text-color="#1d4ed8"
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
            <span>市场信息</span>
          </el-menu-item>
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
            <span>案件管理</span>
          </el-menu-item>
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
      <!-- 固定的顶部导航条 -->
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

      <!-- 💡 可平滑独立滚动的信息卡片区域 -->
      <main class="main-view" ref="scrollTarget">
        <div class="view-card">
          <router-view/>
        </div>

        <!-- 💡 右下角浮动控制按钮组（包含回到顶部和一键到底部） -->
        <div class="scroll-actions-group">
          <!-- 回到顶部按钮 -->
          <el-backtop
              target=".main-view"
              :visibility-height="100"
          >
            <div class="action-btn-inner" title="回到顶部">
              <el-icon>
                <CaretTop/>
              </el-icon>
            </div>
          </el-backtop>

          <!-- 一键到底部按钮 -->
          <div class="action-btn-bottom" @click="scrollToBottom" title="一键到底部">
            <div class="action-btn-inner">
              <el-icon>
                <CaretBottom/>
              </el-icon>
            </div>
          </div>
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
import {
  User,
  TrendCharts,
  FolderOpened,
  ArrowLeft,
  ArrowRight,
  SwitchButton,
  CaretTop,
  CaretBottom,
  Tickets
} from '@element-plus/icons-vue'
import ConfirmDialog from "../components/ConfirmDialog.vue";

const router = useRouter()
const route = useRoute()

// 视图容器 Ref
const scrollTarget = ref(null)

// 控制退出弹窗显示
const showLogoutDialog = ref(false)

const isCollapsed = ref(false)
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

// 💡 一键滚动到底部方法
const scrollToBottom = () => {
  if (scrollTarget.value) {
    scrollTarget.value.scrollTo({
      top: scrollTarget.value.scrollHeight,
      behavior: 'smooth'
    })
  }
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
/* ================= 1. 全局布局与白底红蓝氛围 ================= */
.dashboard-container {
  position: relative;
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: #ffffff; /* 纯白主底色 */
  background-image: radial-gradient(#e2e8f0 0.8px, transparent 0.8px); /* 极细白灰色点阵纹理 */
  background-size: 24px 24px;
  overflow: hidden;
  box-sizing: border-box;
}

/* 柔和红蓝弥散光晕 */
.bg-glow {
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  filter: blur(140px);
  opacity: 0.08;
  pointer-events: none;
}

.glow-blue {
  top: -200px;
  left: 10%;
  background: #1d4ed8;
}

.glow-red {
  bottom: -200px;
  right: 10%;
  background: #dc2626;
}

/* ================= 2. 左侧 Sidebar 侧边栏 ================= */
.sidebar {
  position: relative;
  width: 240px;
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  margin: 12px 0 12px 12px;
  box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.05);
  display: flex;
  flex-direction: column;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 10;
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
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
}

.sidebar-header:hover {
  background-color: #f8fafc;
}

.sidebar-collapsed .sidebar-header {
  padding: 0;
}

/* LOGO 图标更换为纯蓝纯红极彩渐变 */
.logo-icon {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%, #dc2626 100%);
  color: #ffffff;
  font-weight: 800;
  font-size: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3);
}

.logo-text {
  margin-left: 12px;
  white-space: nowrap;
}

.title-cn {
  font-size: 14px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: 0.5px;
}

.title-en {
  font-size: 8px;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 1px;
}

/* ================= 3. 菜单栏 ================= */
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
  background-color: #eff6ff !important;
  color: #1d4ed8 !important;
}

:deep(.el-menu-item.is-active) {
  background: #eff6ff !important;
  color: #1d4ed8 !important;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(29, 78, 216, 0.08);
  border-right: none !important;
}

:deep(.el-menu--collapse .el-sub-menu__title),
:deep(.el-menu--collapse .el-menu-item) {
  justify-content: center !important;
}

:deep(.el-menu--collapse .el-sub-menu__title .el-icon),
:deep(.el-menu--collapse .el-menu-item .el-icon) {
  margin: 0 !important;
}

/* ================= 4. 底部用户信息与退出按钮 ================= */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #f1f5f9;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
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
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}

.user-avatar {
  width: 34px;
  height: 34px;
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
  color: #ffffff;
  font-weight: 700;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(29, 78, 216, 0.25);
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
  color: #1d4ed8;
  font-weight: 600;
}

.logout-btn {
  width: 100%;
  height: 38px;
  border-radius: 10px !important;
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

.collapse-btn {
  position: absolute;
  top: 50%;
  right: -13px;
  transform: translateY(-50%);
  width: 26px;
  height: 26px;
  background-color: #ffffff;
  border: 1px solid #cbd5e1;
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
  background-color: #1d4ed8;
  color: #ffffff;
  border-color: #1d4ed8;
  box-shadow: 0 4px 10px rgba(29, 78, 216, 0.3);
}

/* ================= 5. 右侧主体与独立滚动区域 ================= */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  padding: 12px 12px 12px 8px;
  gap: 12px;
  box-sizing: border-box;
}

/* 顶部 Top-Navbar (固定不动) */
.top-navbar {
  height: 60px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 4px 16px -5px rgba(15, 23, 42, 0.04);
  z-index: 5;
  flex-shrink: 0;
}

.nav-left .module-tag {
  display: inline-flex;
  align-items: center;
  background-color: #eff6ff; /* 浅纯蓝衬底 */
  padding: 5px 16px;
  border-radius: 30px;
  border: 1px solid #bfdbfe;
}

.module-dot {
  width: 7px;
  height: 7px;
  background-color: #dc2626; /* 纯红标点 */
  border-radius: 50%;
  margin-right: 10px;
  box-shadow: 0 0 6px rgba(220, 38, 38, 0.5);
}

.current-position {
  font-size: 13px;
  font-weight: 700;
  color: #1d4ed8; /* 纯深蓝 */
  letter-spacing: 0.5px;
}

.nav-right .user-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #ffffff;
  padding: 5px 8px 5px 14px;
  border-radius: 30px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}

.badge-icon {
  font-size: 14px;
  color: #1d4ed8;
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
  font-weight: 700;
  color: #1d4ed8;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  padding: 2px 10px;
  border-radius: 20px;
  letter-spacing: 0.5px;
}

/* 下方可滚动的主视图画布 */
.main-view {
  flex: 1;
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
  scroll-behavior: smooth;
  box-sizing: border-box;
}

.view-card {
  min-height: 100%;
  background-color: #ffffff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  padding: 20px;
  box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.04);
  box-sizing: border-box;
  overflow-x: hidden;
}

/* 💡 右下角浮动控制按钮组 */
.scroll-actions-group {
  position: fixed;
  right: 28px;
  bottom: 28px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 99;
}

/* 重置 Element 回到顶部按钮 */
:deep(.el-backtop) {
  position: relative !important;
  right: auto !important;
  bottom: auto !important;
  background-color: #ffffff !important;
  color: #1d4ed8 !important;
  border: 1px solid #cbd5e1 !important;
  box-shadow: 0 4px 14px rgba(29, 78, 216, 0.15) !important;
  width: 40px !important;
  height: 40px !important;
  border-radius: 50% !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

:deep(.el-backtop:hover),
.action-btn-bottom:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
  color: #ffffff !important;
  border-color: transparent !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(29, 78, 216, 0.35) !important;
}

/* 自定义一键到底部按钮 */
.action-btn-bottom {
  width: 40px;
  height: 40px;
  background-color: #ffffff;
  color: #1d4ed8;
  border: 1px solid #cbd5e1;
  border-radius: 50%;
  box-shadow: 0 4px 14px rgba(29, 78, 216, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.action-btn-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

/* 精细的内嵌滚动条 */
.main-view::-webkit-scrollbar {
  width: 6px;
  height: 0px;
}

.main-view::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 4px;
}

.main-view::-webkit-scrollbar-thumb:hover {
  background-color: #94a3b8;
}

.main-view::-webkit-scrollbar-track {
  background: transparent;
}
</style>