import { defineStore } from 'pinia'
import { dashboardApi, type AlertQuery } from '@/api/dashboard'
import type { Alert, AlertDetail, AlertStatus, ChartData, Device, OverviewStats, SystemStatus } from '@/types/dashboard'

interface DashboardState {
  overviewStats: OverviewStats | null
  devices: Device[]
  alerts: Alert[]
  selectedAlert: Alert | null
  riskDetail: AlertDetail | null
  chartData: ChartData | null
  systemStatus: SystemStatus | null
  loading: boolean
  detailLoading: boolean
  error: string
  pollTimer: number | null
  alertQuery: AlertQuery
}

export const useDashboardStore = defineStore('dashboard-ts', {
  state: (): DashboardState => ({
    overviewStats: null,
    devices: [],
    alerts: [],
    selectedAlert: null,
    riskDetail: null,
    chartData: null,
    systemStatus: null,
    loading: false,
    detailLoading: false,
    error: '',
    pollTimer: null,
    alertQuery: {},
  }),
  getters: {
    selectedDeviceId(state): string | null {
      return state.riskDetail?.deviceId || state.selectedAlert?.deviceId || null
    },
  },
  actions: {
    setError(error: unknown) {
      this.error = error instanceof Error ? error.message : '数据加载失败'
    },
    clearError() {
      this.error = ''
    },
    async fetchOverview() {
      this.overviewStats = await dashboardApi.getOverview()
    },
    async fetchCharts() {
      this.chartData = await dashboardApi.getCharts()
    },
    async fetchDevices() {
      this.devices = await dashboardApi.getDevices()
    },
    async fetchSystemStatus() {
      this.systemStatus = await dashboardApi.getSystemStatus(this.overviewStats)
    },
    async fetchAlerts(query: AlertQuery = this.alertQuery) {
      this.alertQuery = { ...query }
      this.alerts = await dashboardApi.getAlerts(this.alertQuery)
      if (this.selectedAlert) {
        const existed = this.alerts.find((item) => item.id === this.selectedAlert?.id)
        if (existed) {
          this.selectedAlert = existed
        }
      }
      if (!this.selectedAlert && this.alerts.length > 0) {
        this.selectedAlert = this.alerts[0]
      }
    },
    async fetchAlertDetail(alertId: string) {
      this.detailLoading = true
      try {
        this.riskDetail = await dashboardApi.getAlertDetail(alertId)
      } finally {
        this.detailLoading = false
      }
    },
    async selectAlertById(alertId: string) {
      const found = this.alerts.find((item) => item.id === alertId)
      this.selectedAlert = found || null
      await this.fetchAlertDetail(alertId)
    },
    async updateSelectedAlertStatus(status: AlertStatus, remark?: string) {
      if (!this.selectedAlert) return
      await dashboardApi.updateAlertStatus(this.selectedAlert.id, status, remark)
      await Promise.all([this.fetchOverview(), this.fetchAlerts(this.alertQuery), this.fetchSystemStatus()])
      await this.fetchAlertDetail(this.selectedAlert.id)
    },
    async initialize() {
      this.loading = true
      this.clearError()
      try {
        await this.fetchOverview()
        await Promise.all([this.fetchCharts(), this.fetchDevices(), this.fetchAlerts(), this.fetchSystemStatus()])
        if (this.selectedAlert) {
          await this.fetchAlertDetail(this.selectedAlert.id)
        }
      } catch (error) {
        this.setError(error)
      } finally {
        this.loading = false
      }
    },
    async refreshCore() {
      try {
        await this.fetchOverview()
        await Promise.all([this.fetchAlerts(this.alertQuery), this.fetchSystemStatus()])
        if (this.selectedAlert) {
          await this.fetchAlertDetail(this.selectedAlert.id)
        }
      } catch (error) {
        this.setError(error)
      }
    },
    startPolling(intervalMs = 10000) {
      this.stopPolling()
      this.pollTimer = window.setInterval(() => {
        void this.refreshCore()
      }, intervalMs)
    },
    stopPolling() {
      if (this.pollTimer) {
        window.clearInterval(this.pollTimer)
        this.pollTimer = null
      }
    },
  },
})
