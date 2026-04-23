<script setup lang="ts">
import type { SystemStatus } from '@/types/dashboard'
import type { NavTab } from '@/constants/navigation'

const props = defineProps<{
  systemStatus: SystemStatus | null
  tabs: NavTab[]
  activeTabKey: string
}>()

const emit = defineEmits<{
  changeTab: [tabKey: string]
  refresh: []
  logout: []
}>()

const statusLabelMap: Record<SystemStatus['systemStatus'], string> = {
  running: '运行正常',
  degraded: '服务降级',
  down: '服务异常',
}

const statusType = (status: SystemStatus['systemStatus'] | undefined) => {
  if (status === 'running') return 'success'
  if (status === 'degraded') return 'warning'
  return 'danger'
}
</script>

<template>
  <header class="header-status">
    <div class="header-main">
      <div class="brand">
        <span class="brand-logo">智</span>
        <div>
          <h1>智能护航</h1>
          <p>智能巡检与风险联动处置平台</p>
        </div>
      </div>

      <div class="status-group">
        <div class="status-pill">
          <span class="label">系统状态</span>
          <span class="value">
            <span :class="['dot', `dot-${statusType(props.systemStatus?.systemStatus)}`]"></span>
            {{ props.systemStatus ? statusLabelMap[props.systemStatus.systemStatus] : '--' }}
          </span>
        </div>
        <div class="status-pill">
          <span class="label">在线设备</span>
          <span class="value number">
            {{ props.systemStatus?.onlineDevices || 0 }} / {{ props.systemStatus?.totalDevices || 0 }}
          </span>
        </div>
        <div class="status-pill">
          <span class="label">在线率</span>
          <span class="value number">{{ props.systemStatus?.onlineRate ?? 0 }}%</span>
        </div>
      </div>

      <div class="user-actions">
        <div class="user">
          <span class="avatar">管</span>
          <div class="meta">
            <strong>{{ props.systemStatus?.currentUser?.name || '管理员' }}</strong>
            <el-tag type="info" effect="plain" size="small">{{ props.systemStatus?.currentUser?.role || 'admin' }}</el-tag>
          </div>
        </div>
        <el-button class="ghost-btn" @click="emit('refresh')">刷新数据</el-button>
        <el-button class="danger-btn" @click="emit('logout')">退出登录</el-button>
      </div>
    </div>

    <nav class="tab-nav">
      <button
        v-for="tab in props.tabs"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: tab.key === props.activeTabKey }"
        @click="emit('changeTab', tab.key)"
      >
        {{ tab.label }}
      </button>
    </nav>
  </header>
</template>

<style scoped lang="scss">
.header-status {
  border-radius: 24px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.56);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(20px);
}

.header-main {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 12px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  h1 {
    margin: 0;
    font-size: 34px;
    line-height: 1;
    color: #1d1d1f;
  }
  p {
    margin: 4px 0 0;
    font-size: 12px;
    color: #6e6e73;
  }
}

.brand-logo {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #007aff;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.72);
}

.status-group {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.status-pill {
  min-width: 130px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 10px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.58);
  border: 1px solid rgba(255, 255, 255, 0.44);
}

.label {
  font-size: 11px;
  color: #6e6e73;
}

.value {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 20px;
  font-weight: 700;
  color: #1d1d1f;
  &.number {
    letter-spacing: 0.3px;
  }
}

.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  &.dot-success {
    background: #34c759;
    box-shadow: 0 0 0 0 rgba(52, 199, 89, 0.52);
    animation: breathe 1.8s ease-out infinite;
  }
  &.dot-warning {
    background: #ff9f0a;
  }
  &.dot-danger {
    background: #ff3b30;
  }
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.58);
  border: 1px solid rgba(255, 255, 255, 0.46);
}

.avatar {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #007aff;
  font-weight: 700;
  background: rgba(0, 122, 255, 0.14);
}

.meta {
  display: flex;
  align-items: center;
  gap: 6px;
  strong {
    font-size: 14px;
    color: #1d1d1f;
  }
}

.ghost-btn {
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.46);
}

.danger-btn {
  border-radius: 12px;
}

.tab-nav {
  margin-top: 12px;
  display: flex;
  gap: 6px;
  padding: 6px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.44);
  border: 1px solid rgba(255, 255, 255, 0.4);
}

.tab-btn {
  border: none;
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 13px;
  color: #6e6e73;
  background: transparent;
  transition: all 0.2s ease;
  &:hover {
    color: #1d1d1f;
    background: rgba(255, 255, 255, 0.68);
  }
  &.active {
    color: #1d1d1f;
    font-weight: 700;
    background: rgba(255, 255, 255, 0.84);
    box-shadow: 0 6px 14px rgba(0, 122, 255, 0.12);
  }
}

@keyframes breathe {
  0% {
    box-shadow: 0 0 0 0 rgba(52, 199, 89, 0.52);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(52, 199, 89, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(52, 199, 89, 0);
  }
}

@media (max-width: 1400px) {
  .header-main {
    grid-template-columns: 1fr;
    justify-items: start;
  }

  .status-group,
  .user-actions {
    flex-wrap: wrap;
    justify-content: flex-start;
  }
}
</style>
