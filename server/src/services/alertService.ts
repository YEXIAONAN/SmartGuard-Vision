import { appendTimeline, alerts, alertTimelineMap } from '../models/mockData.js'
import type { Alert, AlertDetail, AlertLevel, AlertStatus } from '../types/index.js'

interface AlertQuery {
  status?: AlertStatus
  level?: AlertLevel
  keyword?: string
}

export const listAlerts = (query: AlertQuery = {}): Alert[] => {
  const { status, level, keyword } = query
  const keywordLower = keyword?.trim().toLowerCase()

  return alerts
    .filter((item) => (!status ? true : item.status === status))
    .filter((item) => (!level ? true : item.level === level))
    .filter((item) => {
      if (!keywordLower) return true
      return (
        item.title.toLowerCase().includes(keywordLower) ||
        item.alertCode.toLowerCase().includes(keywordLower) ||
        item.location.toLowerCase().includes(keywordLower)
      )
    })
    .sort((a, b) => (a.createdAt < b.createdAt ? 1 : -1))
}

export const getAlertDetailById = (id: string): AlertDetail | null => {
  const alert = alerts.find((item) => item.id === id)
  if (!alert) return null
  return {
    ...alert,
    timeline: alertTimelineMap[id] || [],
  }
}

export const updateAlertStatusById = (
  id: string,
  status: AlertStatus,
  remark = '',
  operator = '系统管理员',
): AlertDetail | null => {
  const target = alerts.find((item) => item.id === id)
  if (!target) return null

  target.status = status
  target.updatedAt = new Date().toISOString()
  target.handler = operator
  target.handleRemark = remark || target.handleRemark || (status === 'resolved' ? '已完成处置' : '处理中')

  appendTimeline(id, status, target.handleRemark, operator)

  return getAlertDetailById(id)
}
