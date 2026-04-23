import { alerts, devices } from '../models/mockData.js'
import type { AlertLevel, ChartData, OverviewStats, SystemStatus } from '../types/index.js'

const randomDelta = () => Math.floor(Math.random() * 3) - 1

const normalizeCount = (value: number) => Math.max(0, value)

const getTodayCount = () => {
  const today = new Date().toISOString().slice(0, 10)
  return alerts.filter((item) => item.createdAt.startsWith(today)).length
}

export const getOverviewStats = (): OverviewStats => {
  const onlineDevices = devices.filter((item) => item.status !== 'offline').length
  const totalDevices = devices.length
  const todayAlerts = getTodayCount()
  const highRiskAlerts = alerts.filter((item) => item.level === 'high' && item.status !== 'resolved').length
  const chargingPoints = devices.filter((item) => item.location.includes('充电')).length
  const temperatureAnomalies = devices.filter((item) => item.temperature >= 50 || item.smoke >= 10).length
  const slaTimeouts = alerts.filter((item) => item.status === 'pending').length
  const processingAlerts = alerts.filter((item) => item.status === 'processing')
  const avgHandleMinutes = processingAlerts.length ? 9 : 6

  return {
    onlineDevices,
    totalDevices,
    todayAlerts,
    highRiskAlerts,
    chargingPoints,
    temperatureAnomalies,
    slaTimeouts,
    avgHandleMinutes,
  }
}

export const getChartData = (): ChartData => {
  const trend24h = Array.from({ length: 24 }).map((_, index) => ({
    time: `${String(index).padStart(2, '0')}:00`,
    value: normalizeCount(4 + Math.floor(Math.sin(index / 2) * 2) + randomDelta()),
  }))

  const online = devices.filter((item) => item.status === 'online').length
  const offline = devices.filter((item) => item.status === 'offline').length
  const warning = devices.filter((item) => item.status === 'warning').length

  const levelCount = (level: AlertLevel) => alerts.filter((item) => item.level === level).length

  return {
    trend24h,
    deviceDistribution: [
      { name: '在线', value: online },
      { name: '离线', value: offline },
      { name: '告警', value: warning },
    ],
    riskDistribution: [
      { level: 'low', value: levelCount('low') },
      { level: 'medium', value: levelCount('medium') },
      { level: 'high', value: levelCount('high') },
    ],
  }
}

export const getDeviceList = () => devices

export const getSystemStatus = (): SystemStatus => {
  const overview = getOverviewStats()
  const onlineRate = overview.totalDevices ? Math.round((overview.onlineDevices / overview.totalDevices) * 100) : 0
  const hasHighRiskPending = alerts.some((item) => item.level === 'high' && item.status === 'pending')

  return {
    systemStatus: hasHighRiskPending ? 'degraded' : 'running',
    onlineRate,
    onlineDevices: overview.onlineDevices,
    totalDevices: overview.totalDevices,
    lastUpdatedAt: new Date().toISOString(),
    currentUser: {
      id: 'u-admin',
      name: '系统管理员',
      role: 'admin',
    },
  }
}
