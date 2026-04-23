export interface NavTab {
  key: string
  label: string
  path: string
}

export const DASHBOARD_TABS: NavTab[] = [
  { key: 'overview', label: '首页总览', path: '/' },
  { key: 'vision-history', label: '视频历史', path: '/vision-history' },
  { key: 'sensor-history', label: '传感历史', path: '/sensor-history' },
  { key: 'rules', label: '规则中心', path: '/rules' },
  { key: 'audit', label: '审计中心', path: '/audit' },
]
