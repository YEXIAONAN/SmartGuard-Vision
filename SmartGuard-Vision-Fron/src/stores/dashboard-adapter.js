const RISK_COLORS = {
  high: '#e35d5d',
  medium: '#f2a93b',
  low: '#4c8bf5',
  other: '#9dc2ff',
}

const EVENT_COLORS = ['#4c8bf5', '#7aa9ff', '#f3b24d', '#f08c6a', '#d96e6e', '#8a8ff0']
const AREA_COLORS = ['#d85c5c', '#eb8b56', '#f3b24d', '#72a6ff', '#4c8bf5', '#7f95ff']

export const createDefaultDashboardState = () => ({
  project: {
    name: '智感护航',
    subtitle: '面向停充场景的多模态安全感知平台',
  },
  systemStatus: '连接中',
  onlineSummary: '0 / 0',
  stats: [],
  alerts: [],
  devices: [],
  monitor: {
    title: '实时监测面板',
    channel: '等待设备接入',
    pointCode: '--',
    captureStatus: '未接入',
    screenLabel: '暂无实时事件',
    overlays: [],
    tags: [],
    recognitionList: [
      { label: '监测点位', value: '--' },
      { label: '风险等级', value: '--' },
      { label: '处置状态', value: '--' },
      { label: '停放识别', value: '--' },
      { label: '充电状态', value: '--' },
      { label: '温度/烟雾', value: '--' },
      { label: '最近上报', value: '--' },
    ],
  },
  riskTrend: {
    labels: [],
    values: [],
  },
  eventDistribution: {
    labels: [],
    values: [],
    colors: EVENT_COLORS,
  },
  riskLevel: [],
  areaRisk: [],
  alertTrend: {
    labels: [],
    total: [],
    highRisk: [],
  },
  generatedAt: '',
  loading: false,
  initialized: false,
  updatingAlertId: null,
  error: '',
})

const formatDateTime = (value) => {
  if (!value) return '--'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '--'

  return date.toLocaleString('zh-CN', {
    hour12: false,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

const formatTime = (value) => {
  if (!value) return '--'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '--'

  return date.toLocaleTimeString('zh-CN', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

const normalizeRiskLevel = (value) => {
  const level = String(value || '').trim().toLowerCase()
  if (level.includes('high') || level.includes('高')) return 'high'
  if (level.includes('medium') || level.includes('中')) return 'medium'
  if (level.includes('low') || level.includes('低')) return 'low'
  return 'other'
}

const formatRiskLevel = (value) => {
  switch (normalizeRiskLevel(value)) {
    case 'high':
      return '高风险'
    case 'medium':
      return '中风险'
    case 'low':
      return '低风险'
    default:
      return value || '未知'
  }
}

const formatAlertStatus = (value) => {
  const status = String(value || '').trim().toLowerCase()
  if (status === 'pending') return '待处理'
  if (status === 'processing') return '处理中'
  if (status === 'resolved') return '已处理'
  return value || '--'
}

const buildStats = (stats) => [
  {
    title: '接入设备数',
    value: String(stats.device_count ?? 0),
    unit: '台',
    note: `在线 ${stats.online_device_count ?? 0} 台，离线 ${stats.offline_device_count ?? 0} 台`,
  },
  {
    title: '今日告警数',
    value: String(stats.today_alert_count ?? 0),
    unit: '条',
    note: `累计告警 ${stats.alert_count ?? 0} 条`,
  },
  {
    title: '高风险事件',
    value: String(stats.high_risk_alert_count ?? 0),
    unit: '条',
    note: '视觉识别与传感异常联动触发',
  },
  {
    title: '充电监测点位',
    value: String(stats.charging_device_count ?? 0),
    unit: '处',
    note: `异常充电事件 ${stats.abnormal_charging_event_count ?? 0} 条`,
  },
  {
    title: '温升异常数',
    value: String(stats.over_temperature_event_count ?? 0),
    unit: '条',
    note: '重点关注高温和烟雾联动预警',
  },
  {
    title: '感知记录数',
    value: String((stats.vision_record_count ?? 0) + (stats.sensor_record_count ?? 0)),
    unit: '条',
    note: `视觉 ${stats.vision_record_count ?? 0} 条，传感 ${stats.sensor_record_count ?? 0} 条`,
  },
]

export const adaptDashboardData = ({ health, overview }) => ({
  project: {
    name: overview.project_name || '智感护航',
    subtitle: '面向停充场景的多模态安全感知平台',
  },
  systemStatus: health?.status === 'ok' ? '运行正常' : '连接异常',
  onlineSummary: `${overview.stats.online_device_count ?? 0} / ${overview.stats.device_count ?? 0}`,
  stats: buildStats(overview.stats),
  alerts: (overview.recent_alerts || []).map((item) => ({
    id: item.id,
    rawStatus: item.status,
    time: formatTime(item.occurred_at),
    level: formatRiskLevel(item.alert_level),
    levelKey: normalizeRiskLevel(item.alert_level),
    place: item.location,
    detail: item.description,
    status: formatAlertStatus(item.status),
    handledBy: item.handled_by || '',
    handlingNote: item.handling_note || '',
    handledAt: item.handled_at ? formatDateTime(item.handled_at) : '',
  })),
  devices: overview.device_status_summary || [],
  monitor: {
    title: overview.monitor_snapshot?.title || '实时监测面板',
    channel: overview.monitor_snapshot?.channel || '等待设备接入',
    pointCode: overview.monitor_snapshot?.point_code || '--',
    captureStatus: overview.monitor_snapshot?.capture_status || '--',
    screenLabel: overview.monitor_snapshot?.screen_label || '暂无实时事件',
    overlays: (overview.monitor_snapshot?.tags || []).slice(0, 2).map((text, index) => ({
      text,
      className: index === 0 ? 'overlay-main' : 'overlay-secondary',
    })),
    tags: overview.monitor_snapshot?.tags || [],
    recognitionList: overview.monitor_snapshot?.recognition_items || [],
  },
  riskTrend: {
    labels: overview.seven_day_alert_trend.map((item) => item.date),
    values: overview.seven_day_alert_trend.map((item) => item.total_alerts),
  },
  eventDistribution: {
    labels: overview.event_distribution.map((item) => item.name),
    values: overview.event_distribution.map((item) => item.count),
    colors: EVENT_COLORS,
  },
  riskLevel: overview.risk_distribution.map((item) => ({
    name: formatRiskLevel(item.level),
    value: item.count,
    color: RISK_COLORS[normalizeRiskLevel(item.level)] || RISK_COLORS.other,
  })),
  areaRisk: overview.area_risk_ranking.map((item, index) => ({
    name: item.name,
    value: item.count,
    color: AREA_COLORS[index % AREA_COLORS.length],
  })),
  alertTrend: {
    labels: overview.seven_day_alert_trend.map((item) => item.date),
    total: overview.seven_day_alert_trend.map((item) => item.total_alerts),
    highRisk: overview.seven_day_alert_trend.map((item) => item.high_risk_alerts),
  },
  generatedAt: formatDateTime(overview.generated_at),
  error: '',
  initialized: true,
})
