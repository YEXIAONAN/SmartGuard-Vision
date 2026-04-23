export type DeviceStatus = 'online' | 'offline' | 'warning'
export type AlertLevel = 'low' | 'medium' | 'high'
export type AlertStatus = 'pending' | 'processing' | 'resolved'

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export interface Device {
  id: string
  deviceCode: string
  name: string
  location: string
  type: string
  status: DeviceStatus
  temperature: number
  smoke: number
  batteryStatus: number
  lastReportTime: string
  hasAlert: boolean
}

export interface Alert {
  id: string
  alertCode: string
  title: string
  deviceId: string
  location: string
  level: AlertLevel
  status: AlertStatus
  description: string
  createdAt: string
  updatedAt: string
  handler?: string
  handleRemark?: string
}

export interface AlertTimelineItem {
  id: string
  status: AlertStatus
  operator: string
  remark: string
  createdAt: string
}

export interface AlertDetail extends Alert {
  timeline: AlertTimelineItem[]
}

export interface OverviewStats {
  onlineDevices: number
  totalDevices: number
  todayAlerts: number
  highRiskAlerts: number
  chargingPoints: number
  temperatureAnomalies: number
  slaTimeouts: number
  avgHandleMinutes: number
}

export interface ChartData {
  trend24h: Array<{ time: string; value: number }>
  deviceDistribution: Array<{ name: string; value: number }>
  riskDistribution: Array<{ level: AlertLevel; value: number }>
}

export interface SystemStatus {
  systemStatus: 'running' | 'degraded' | 'down'
  onlineRate: number
  onlineDevices: number
  totalDevices: number
  lastUpdatedAt: string
  currentUser: {
    id: string
    name: string
    role: string
  }
}
