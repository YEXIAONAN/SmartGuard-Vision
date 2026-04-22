<script setup>
import { computed, onBeforeUnmount, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useClock } from '../composables/useClock'
import { useDashboardStore } from '../stores/dashboard'

const route = useRoute()
const dashboardStore = useDashboardStore()
const { currentTime } = useClock()

const navItems = [
  { path: '/', label: '首页总览' },
  { path: '/vision-history', label: '视觉历史' },
  { path: '/sensor-history', label: '传感历史' },
]

const activePath = computed(() => route.path)
const systemStateClass = computed(() =>
  dashboardStore.systemStatus.includes('正常') ? 'state-ok' : 'state-danger',
)

const headerRefreshInterval = 60000
let timerId = null

onMounted(() => {
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
      <div class="console-brand">
        <div class="brand-title">智感护航</div>
        <div class="brand-subtitle">停充场景多模态安全感知与联动处置平台</div>
      </div>

      <div class="console-meta">
        <div class="meta-item">
          <span class="meta-label">当前时间</span>
          <span class="meta-value">{{ currentTime }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">最后更新时间</span>
          <span class="meta-value">{{ dashboardStore.generatedAt || '--' }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">系统状态</span>
          <span class="meta-value">
            <span class="state-dot" :class="systemStateClass"></span>
            {{ dashboardStore.systemStatus }}
          </span>
        </div>
        <div class="meta-item">
          <span class="meta-label">在线设备</span>
          <span class="meta-value">{{ dashboardStore.onlineSummary }}</span>
        </div>
      </div>

      <nav class="console-tabs">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="console-tab"
          :class="{ 'console-tab-active': activePath === item.path }"
        >
          {{ item.label }}
        </router-link>
      </nav>
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
  z-index: 30;
  display: grid;
  grid-template-columns: 1.15fr 1fr auto;
  gap: 16px;
  align-items: center;
  padding: 10px 20px;
  background: #f3f6fa;
  border-bottom: 1px solid #d9e1eb;
}

.brand-title {
  font-size: 21px;
  line-height: 1;
  font-weight: 700;
  color: #1f2f42;
}

.brand-subtitle {
  margin-top: 6px;
  font-size: 12px;
  color: var(--sg-text-secondary);
}

.console-meta {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
}

.meta-item {
  padding: 7px 10px;
  background: #ffffff;
  border: 1px solid var(--sg-border-light);
  border-radius: 8px;
}

.meta-label {
  display: block;
  font-size: 11px;
  color: var(--sg-text-muted);
}

.meta-value {
  margin-top: 3px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #243244;
}

.state-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.state-ok {
  background: var(--sg-color-success);
}

.state-danger {
  background: var(--sg-color-danger);
}

.console-tabs {
  display: flex;
  align-items: center;
  border: 1px solid #d1dbe7;
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
}

.console-tab {
  padding: 10px 16px;
  font-size: 13px;
  font-weight: 600;
  color: #526377;
  border-right: 1px solid #e2e9f2;
  background: #ffffff;
}

.console-tab:last-child {
  border-right: none;
}

.console-tab-active {
  color: #1f3a59;
  background: #e9f0f8;
}

.app-main {
  min-height: calc(100vh - 80px);
}

@media (max-width: 1366px) {
  .top-console {
    grid-template-columns: 1fr;
    align-items: stretch;
  }

  .console-tabs {
    width: fit-content;
  }
}

@media (max-width: 992px) {
  .top-console {
    padding: 10px 14px;
  }

  .console-meta {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .console-tabs {
    width: 100%;
  }

  .console-tab {
    flex: 1;
    text-align: center;
  }
}
</style>
