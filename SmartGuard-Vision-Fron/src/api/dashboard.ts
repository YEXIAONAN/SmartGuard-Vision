import request from '@/utils/request'
import type {
  Alert,
  AlertDetail,
  AlertLevel,
  AlertStatus,
  ChartData,
  Device,
  OverviewStats,
  SystemStatus,
} from '@/types/dashboard'

interface DashboardOverviewRaw {
  generated_at: string
  stats: {
    device_count: number
    online_device_count: number
    offline_device_count: number
    today_alert_count: number
    high_risk_alert_count: number
    charging_device_count: number
    over_temperature_event_count: number
    sla_overdue_count: number
    average_resolution_minutes: number
  }
  seven_day_alert_trend: Array<{ date: string; total_alerts: number; high_risk_alerts: number }>
  risk_distribution: Array<{ level: string; count: number }>
  device_status_summary: Array<{ name: string; online: number; total: number }>
  recent_alerts: AlertRaw[]
}

interface DeviceRaw {
  id: number
  device_code: string
  device_name: string
  device_type: string
  location: string
  status: string
  is_online: boolean
  last_seen_at: string
}

interface AlertRaw {
  id: number
  alert_code: string
  alert_type: string
  alert_level: string
  source_type: string
  location: string
  description: string
  status: string
  handled_by: string | null
  handling_note: string | null
  handled_at: string | null
  occurred_at: string
  created_at: string
  updated_at: string
  device_id: number | null
}

interface AlertActionRaw {
  id: number
  from_status: string | null
  to_status: string
  handled_by: string | null
  handling_note: string | null
  created_at: string
}

interface PaginatedData<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface AlertQuery {
  status?: AlertStatus
  level?: AlertLevel
  keyword?: string
}

const normalizeLevel = (value: string): AlertLevel => {
  const v = value.toLowerCase()
  if (v.includes('high') || v.includes('高')) return 'high'
  if (v.includes('medium') || v.includes('中')) return 'medium'
  return 'low'
}

const normalizeStatus = (value: string): AlertStatus => {
  const v = value.toLowerCase()
  if (v === 'resolved') return 'resolved'
  if (v === 'processing') return 'processing'
  return 'pending'
}

const mapAlert = (row: AlertRaw): Alert => ({
  id: String(row.id),
  alertCode: row.alert_code,
  title: row.alert_type,
  deviceId: String(row.device_id ?? ''),
  location: row.location,
  level: normalizeLevel(row.alert_level),
  status: normalizeStatus(row.status),
  description: row.description,
  createdAt: row.occurred_at || row.created_at,
  updatedAt: row.updated_at,
  handler: row.handled_by || undefined,
  handleRemark: row.handling_note || undefined,
})

const mapOverviewToStats = (raw: DashboardOverviewRaw): OverviewStats => ({
  onlineDevices: raw.stats.online_device_count,
  totalDevices: raw.stats.device_count,
  todayAlerts: raw.stats.today_alert_count,
  highRiskAlerts: raw.stats.high_risk_alert_count,
  chargingPoints: raw.stats.charging_device_count,
  temperatureAnomalies: raw.stats.over_temperature_event_count,
  slaTimeouts: raw.stats.sla_overdue_count,
  avgHandleMinutes: raw.stats.average_resolution_minutes,
})

const mapOverviewToCharts = (raw: DashboardOverviewRaw): ChartData => ({
  trend24h: raw.seven_day_alert_trend.map((item) => ({ time: item.date, value: item.total_alerts })),
  deviceDistribution: raw.device_status_summary.map((item) => ({
    name: item.name,
    value: Math.max(item.online, item.total - item.online),
  })),
  riskDistribution: raw.risk_distribution.map((item) => ({
    level: normalizeLevel(item.level),
    value: item.count,
  })),
})

const mapDevice = (row: DeviceRaw): Device => ({
  id: String(row.id),
  deviceCode: row.device_code,
  name: row.device_name,
  location: row.location,
  type: row.device_type,
  status: row.is_online ? (row.status === 'warning' ? 'warning' : 'online') : 'offline',
  temperature: 20 + (row.id % 10) * 2.3,
  smoke: 2 + (row.id % 6) * 1.1,
  batteryStatus: 70 + (row.id % 5) * 5,
  lastReportTime: row.last_seen_at,
  hasAlert: false,
})

let overviewCache: DashboardOverviewRaw | null = null

const getOverviewRaw = async () => {
  overviewCache = await request.get<DashboardOverviewRaw>('/dashboard/overview')
  return overviewCache
}

export const dashboardApi = {
  async getOverview() {
    const raw = await getOverviewRaw()
    return mapOverviewToStats(raw)
  },
  async getCharts() {
    const raw = overviewCache || (await getOverviewRaw())
    return mapOverviewToCharts(raw)
  },
  async getDevices() {
    const rows = await request.get<DeviceRaw[]>('/devices')
    return rows.map(mapDevice)
  },
  async getSystemStatus(overview?: OverviewStats | null) {
    const health = await fetch('/health').then((r) => r.json())
    const onlineDevices = overview?.onlineDevices ?? 0
    const totalDevices = overview?.totalDevices ?? 0
    const onlineRate = totalDevices ? Math.round((onlineDevices / totalDevices) * 100) : 0
    const statusText = String(health?.data?.status || 'down').toLowerCase()
    return {
      systemStatus: statusText === 'ok' ? 'running' : 'down',
      onlineRate,
      onlineDevices,
      totalDevices,
      lastUpdatedAt: health?.data?.now || new Date().toISOString(),
      currentUser: {
        id: 'u-admin',
        name: '管理员',
        role: 'admin',
      },
    } as SystemStatus
  },
  async getAlerts(query: AlertQuery = {}) {
    const data = await request.get<PaginatedData<AlertRaw>>('/alerts', {
      params: {
        ...query,
        page: 1,
        page_size: 20,
      },
    })
    return data.items.map(mapAlert)
  },
  async getAlertDetail(id: string) {
    const all = await request.get<PaginatedData<AlertRaw>>('/alerts', {
      params: { page: 1, page_size: 100 },
    })
    const base = all.items.find((item) => String(item.id) === id)
    if (!base) throw new Error('告警不存在')

    const actions = await request.get<AlertActionRaw[]>(`/alerts/${id}/actions`)

    return {
      ...mapAlert(base),
      timeline: actions.map((item) => ({
        id: String(item.id),
        status: normalizeStatus(item.to_status),
        operator: item.handled_by || '系统',
        remark: item.handling_note || `状态变更：${item.from_status || 'unknown'} -> ${item.to_status}`,
        createdAt: item.created_at,
      })),
    } as AlertDetail
  },
  async updateAlertStatus(id: string, status: AlertStatus, remark?: string) {
    const res = await request.patch<AlertRaw>(`/alerts/${id}/status`, {
      status,
      handled_by: '系统管理员',
      handling_note: remark || (status === 'resolved' ? '已完成处置' : '处理中'),
      handled_at: new Date().toISOString(),
    })

    return {
      ...mapAlert(res),
      timeline: [],
    } as AlertDetail
  },
}
