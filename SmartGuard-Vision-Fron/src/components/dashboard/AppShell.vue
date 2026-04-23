<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import HeaderStatus from '@/components/dashboard/HeaderStatus.vue'
import { DASHBOARD_TABS } from '@/constants/navigation'
import { useDashboardStore } from '@/stores/dashboard'
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits<{
  refresh: []
}>()

const route = useRoute()
const router = useRouter()
const dashboardStore = useDashboardStore()
const authStore = useAuthStore()

const activeTabKey = computed(() => {
  const matched = DASHBOARD_TABS.find((tab) => tab.path === route.path)
  return matched?.key || 'overview'
})

const handleChangeTab = async (tabKey: string) => {
  const matched = DASHBOARD_TABS.find((tab) => tab.key === tabKey)
  if (!matched || matched.path === route.path) return
  await router.push(matched.path)
}

const handleRefresh = async () => {
  try {
    await dashboardStore.fetchOverview()
    await dashboardStore.fetchSystemStatus()
  } catch (error) {
    dashboardStore.setError(error)
  }
  emit('refresh')
}

const handleLogout = async () => {
  authStore.clearSession()
  dashboardStore.stopPolling()
  ElMessage.success('已退出登录')
  await router.replace('/login')
}

onMounted(async () => {
  if (!dashboardStore.systemStatus) {
    try {
      await dashboardStore.fetchOverview()
      await dashboardStore.fetchSystemStatus()
    } catch (error) {
      dashboardStore.setError(error)
    }
  }
})
</script>

<template>
  <div class="app-shell">
    <HeaderStatus
      :system-status="dashboardStore.systemStatus"
      :tabs="DASHBOARD_TABS"
      :active-tab-key="activeTabKey"
      @change-tab="handleChangeTab"
      @refresh="handleRefresh"
      @logout="handleLogout"
    />
    <slot />
  </div>
</template>

<style scoped lang="scss">
.app-shell {
  min-height: 100vh;
  padding: 12px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (max-width: 992px) {
  .app-shell {
    padding: 10px 12px 14px;
  }
}
</style>
