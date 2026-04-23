import { defineStore } from 'pinia'
import { dashboardApi } from '../services/api'
import { adaptDashboardData, createDefaultDashboardState } from './dashboard-adapter'

const REFRESH_INTERVAL_MS = 30000
let refreshTimerId = null

export const useDashboardStore = defineStore('dashboard', {
  state: () => createDefaultDashboardState(),
  getters: {
    deviceStatusList: (state) =>
      state.devices.map((item) => ({
        ...item,
        rate: item.total ? Math.round((item.online / item.total) * 100) : 0,
      })),
  },
  actions: {
    async fetchDashboard({ silent = false } = {}) {
      if (!silent) this.loading = true

      try {
        const [health, overview] = await Promise.all([dashboardApi.getHealth(), dashboardApi.getOverview()])
        this.$patch(adaptDashboardData({ health, overview }))
      } catch (error) {
        this.systemStatus = '连接异常'
        this.error = error instanceof Error ? error.message : '首页态势数据加载失败'
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async updateAlertStatus(alertId, payload) {
      this.updatingAlertId = alertId
      try {
        await dashboardApi.updateAlertStatus(alertId, payload)
        await this.fetchDashboard({ silent: true })
        return true
      } catch (error) {
        this.error = error instanceof Error ? error.message : '告警状态更新失败'
        console.error(error)
        return false
      } finally {
        this.updatingAlertId = null
      }
    },
    startAutoRefresh(interval = REFRESH_INTERVAL_MS) {
      if (refreshTimerId) return
      void this.fetchDashboard()
      refreshTimerId = window.setInterval(() => {
        void this.fetchDashboard({ silent: true })
      }, interval)
    },
    stopAutoRefresh() {
      if (!refreshTimerId) return
      window.clearInterval(refreshTimerId)
      refreshTimerId = null
    },
  },
})
