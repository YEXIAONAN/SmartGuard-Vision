<script setup>
import { ElMessage } from 'element-plus'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useClock } from '../composables/useClock'
import { authApi } from '../services/api'
import { useAuthStore } from '../stores/auth'
import { useDashboardStore } from '../stores/dashboard'

const route = useRoute()
const router = useRouter()
const dashboardStore = useDashboardStore()
const authStore = useAuthStore()
const { currentTime } = useClock()

const navItems = [
  { path: '/', label: '首页总览' },
  { path: '/vision-history', label: '视频历史' },
  { path: '/sensor-history', label: '传感历史' },
  { path: '/rules', label: '规则中心', roles: ['admin', 'operator'] },
  { path: '/audit', label: '审计中心', roles: ['admin'] },
]

const roleLabelMap = {
  admin: '管理员',
  operator: '值班员',
  viewer: '只读用户',
}

const roleLabel = computed(() => roleLabelMap[authStore.role] || authStore.role || '--')
const visibleNavItems = computed(() =>
  navItems.filter((item) => !item.roles || item.roles.includes(authStore.role)),
)
const isSystemOk = computed(() => dashboardStore.systemStatus.includes('正常'))
const showExtraMeta = ref(false)

const isTabActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

const headerRefreshInterval = 60000
let timerId = null

const logout = async () => {
  try {
    await authApi.logout({ refresh_token: authStore.refreshToken || null })
  } catch {
    // 忽略登出接口异常，保证本地会话能清理。
  }
  authStore.clearSession()
  dashboardStore.stopAutoRefresh()
  await router.replace('/login')
  ElMessage.success('已退出登录')
}

onMounted(async () => {
  try {
    const me = await authApi.getMe()
    authStore.setSession({
      token: authStore.token,
      refreshToken: authStore.refreshToken,
      user: me,
    })
  } catch {
    await logout()
    return
  }

  if (!dashboardStore.initialized) {
    void dashboardStore.fetchDashboard()
  }

  timerId = window.setInterval(() => {
    void dashboardStore.fetchDashboard({ silent: true })
  }, headerRefreshInterval)
})

onBeforeUnmount(() => {
  if (timerId) {
    window.clearInterval(timerId)
    timerId = null
  }
})
</script>

<template>
  <div class="app-shell">
    <header class="top-console">
      <section class="glass-nav">
        <div class="console-main-row">
          <div class="console-brand">
            <span class="brand-logo">智</span>
            <div class="brand-text">
              <div class="brand-title">智感护航</div>
            </div>
          </div>

          <div class="console-right">
            <div class="console-status">
              <div class="status-card">
                <span class="status-label">系统状态</span>
                <span class="status-value">
                  <span class="state-dot" :class="{ 'state-dot-ok': isSystemOk, 'state-dot-danger': !isSystemOk }"></span>
                  {{ dashboardStore.systemStatus || '--' }}
                </span>
              </div>
              <div class="status-card">
                <span class="status-label">在线设备</span>
                <span class="status-value status-number">{{ dashboardStore.onlineSummary || '--' }}</span>
              </div>
            </div>

            <div class="console-user">
            <div class="user-card">
              <span class="user-avatar">管</span>
              <div class="user-meta">
                <span class="user-name">{{ authStore.displayName }}</span>
                <el-tag type="info" effect="plain" size="small">{{ roleLabel }}</el-tag>
              </div>
            </div>
            <el-button class="ghost-btn" @click="showExtraMeta = !showExtraMeta">
              {{ showExtraMeta ? '收起信息' : '展开信息' }}
            </el-button>
            <el-button class="ghost-btn ghost-btn-danger" @click="logout">退出登录</el-button>
          </div>
          </div>
        </div>

        <el-collapse-transition>
          <div v-show="showExtraMeta" class="console-extra-row">
            <div class="status-card">
              <span class="status-label">当前时间</span>
              <span class="status-value">{{ currentTime }}</span>
            </div>
            <div class="status-card">
              <span class="status-label">最后更新时间</span>
              <span class="status-value">{{ dashboardStore.generatedAt || '--' }}</span>
            </div>
          </div>
        </el-collapse-transition>

        <nav class="console-tabs">
          <router-link
            v-for="item in visibleNavItems"
            :key="item.path"
            :to="item.path"
            class="console-tab"
            :class="{ 'console-tab-active': isTabActive(item.path) }"
          >
            {{ item.label }}
          </router-link>
        </nav>
      </section>
    </header>

    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.top-console {
  position: sticky;
  top: 0;
  z-index: 40;
  padding: 12px 24px 8px;
}

.glass-nav {
  padding: 12px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.34);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  backdrop-filter: var(--sg-blur-xl);
  -webkit-backdrop-filter: var(--sg-blur-xl);
}

.console-main-row {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  gap: 12px;
}

.console-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-logo {
  width: 34px;
  height: 34px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  color: #007aff;
  background: rgba(255, 255, 255, 0.62);
  border: 1px solid rgba(255, 255, 255, 0.58);
}

.brand-title {
  font-size: 24px;
  line-height: 1;
  font-weight: 700;
  letter-spacing: 0.4px;
  color: #1d1d1f;
}

.console-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
}

.console-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-card {
  min-width: 142px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 8px 10px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.45);
}

.status-label {
  font-size: 11px;
  color: #6e6e73;
}

.status-value {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 15px;
  font-weight: 600;
  color: #1d1d1f;
}

.status-number {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.4px;
}

.state-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}

.state-dot-ok {
  background: #34c759;
  box-shadow: 0 0 0 0 rgba(52, 199, 89, 0.45);
  animation: breathe 1.8s ease-out infinite;
}

.state-dot-danger {
  background: #ff3b30;
}

.console-user {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.45);
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: #007aff;
  background: rgba(0, 122, 255, 0.12);
}

.user-meta {
  display: flex;
  align-items: center;
  gap: 6px;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
}

.ghost-btn {
  margin: 0;
  padding: 8px 12px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.46);
  background: rgba(255, 255, 255, 0.5);
  color: #1d1d1f;
  transition: all 0.2s ease;
}

.ghost-btn:hover {
  background: rgba(255, 255, 255, 0.72);
  transform: translateY(-1px);
}

.ghost-btn:active {
  transform: scale(0.98);
}

.ghost-btn.ghost-btn-danger {
  color: #ff3b30;
}

.console-extra-row {
  margin-top: 8px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.console-tabs {
  margin-top: 10px;
  display: flex;
  gap: 6px;
  padding: 6px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.36);
}

.console-tab {
  padding: 8px 16px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
  color: #6e6e73;
  transition: all 0.2s ease;
}

.console-tab:hover {
  color: #1d1d1f;
  background: rgba(255, 255, 255, 0.62);
}

.console-tab:active {
  transform: scale(0.98);
}

.console-tab-active {
  color: #1d1d1f;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.84);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.82), 0 6px 14px rgba(0, 122, 255, 0.12);
}

.app-main {
  min-height: calc(100vh - 118px);
}

@keyframes breathe {
  0% {
    box-shadow: 0 0 0 0 rgba(52, 199, 89, 0.45);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(52, 199, 89, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(52, 199, 89, 0);
  }
}

@media (max-width: 1366px) {
  .top-console {
    padding: 10px 14px 8px;
  }

  .console-main-row {
    grid-template-columns: 1fr;
    align-items: start;
  }

  .console-right,
  .console-status,
  .console-user {
    justify-content: flex-start;
    flex-wrap: wrap;
  }
}

@media (max-width: 992px) {
  .brand-title {
    font-size: 21px;
  }

  .console-extra-row {
    grid-template-columns: 1fr;
  }

  .console-tabs {
    flex-wrap: wrap;
  }
}
</style>
