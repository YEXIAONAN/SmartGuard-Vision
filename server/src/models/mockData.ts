import { v4 as uuid } from 'uuid'
import type { Alert, AlertDetail, AlertStatus, Device } from '../types/index.js'

const now = new Date()

const toTime = (offsetMinutes: number) => new Date(now.getTime() - offsetMinutes * 60 * 1000).toISOString()

export const devices: Device[] = [
  {
    id: 'dev-1',
    deviceCode: 'SEN-001',
    name: '宿舍区温烟传感器',
    location: '学生宿舍北侧充电棚',
    type: 'sensor',
    status: 'warning',
    temperature: 56.2,
    smoke: 12.1,
    batteryStatus: 86,
    lastReportTime: toTime(2),
    hasAlert: true,
  },
  {
    id: 'dev-2',
    deviceCode: 'CAM-018',
    name: '教学楼东侧摄像头',
    location: '教学楼东侧集中停放区',
    type: 'camera',
    status: 'online',
    temperature: 34.5,
    smoke: 4.3,
    batteryStatus: 100,
    lastReportTime: toTime(1),
    hasAlert: true,
  },
  {
    id: 'dev-3',
    deviceCode: 'SEN-014',
    name: '地下车库烟感',
    location: '地下车库 B2',
    type: 'sensor',
    status: 'online',
    temperature: 28.2,
    smoke: 3.5,
    batteryStatus: 72,
    lastReportTime: toTime(1),
    hasAlert: false,
  },
  {
    id: 'dev-4',
    deviceCode: 'GAT-006',
    name: '园区网关设备',
    location: '园区西门机房',
    type: 'gateway',
    status: 'offline',
    temperature: 0,
    smoke: 0,
    batteryStatus: 0,
    lastReportTime: toTime(90),
    hasAlert: false,
  },
  {
    id: 'dev-5',
    deviceCode: 'CAM-022',
    name: '宿舍区南侧摄像头',
    location: '宿舍南区停车棚',
    type: 'camera',
    status: 'online',
    temperature: 31.5,
    smoke: 5.5,
    batteryStatus: 100,
    lastReportTime: toTime(2),
    hasAlert: true,
  },
]

export const alerts: Alert[] = [
  {
    id: 'alt-1',
    alertCode: 'ALT-20260423-001',
    title: '宿舍区温烟异常',
    deviceId: 'dev-1',
    location: '学生宿舍北侧充电棚',
    level: 'high',
    status: 'pending',
    description: '温度持续超过 55℃ 且烟雾值持续上升',
    createdAt: toTime(5),
    updatedAt: toTime(5),
    handler: '',
    handleRemark: '',
  },
  {
    id: 'alt-2',
    alertCode: 'ALT-20260423-002',
    title: '飞线充电行为识别',
    deviceId: 'dev-2',
    location: '教学楼东侧集中停放区',
    level: 'medium',
    status: 'processing',
    description: '视觉识别到飞线充电行为，需尽快处置',
    createdAt: toTime(18),
    updatedAt: toTime(12),
    handler: '巡检员A',
    handleRemark: '已通知物业前往现场',
  },
  {
    id: 'alt-3',
    alertCode: 'ALT-20260423-003',
    title: '网关掉线预警',
    deviceId: 'dev-4',
    location: '园区西门机房',
    level: 'high',
    status: 'pending',
    description: '网关离线超过 30 分钟，设备数据无法上报',
    createdAt: toTime(42),
    updatedAt: toTime(42),
    handler: '',
    handleRemark: '',
  },
  {
    id: 'alt-4',
    alertCode: 'ALT-20260423-004',
    title: '停放区拥挤风险',
    deviceId: 'dev-5',
    location: '宿舍南区停车棚',
    level: 'low',
    status: 'resolved',
    description: '停放区拥挤度超过阈值，已分流处理完成',
    createdAt: toTime(80),
    updatedAt: toTime(65),
    handler: '巡检员B',
    handleRemark: '已完成车辆分流，风险解除',
  },
]

const baseTimeline = (alert: Alert): AlertDetail['timeline'] => [
  {
    id: uuid(),
    status: 'pending',
    operator: '系统',
    remark: `告警触发：${alert.title}`,
    createdAt: alert.createdAt,
  },
]

export const alertTimelineMap: Record<string, AlertDetail['timeline']> = {
  'alt-1': baseTimeline(alerts[0]),
  'alt-2': [
    ...baseTimeline(alerts[1]),
    {
      id: uuid(),
      status: 'processing',
      operator: '巡检员A',
      remark: '已确认现场风险，正在处置',
      createdAt: alerts[1].updatedAt,
    },
  ],
  'alt-3': baseTimeline(alerts[2]),
  'alt-4': [
    ...baseTimeline(alerts[3]),
    {
      id: uuid(),
      status: 'processing',
      operator: '巡检员B',
      remark: '已安排值守人员疏导',
      createdAt: toTime(72),
    },
    {
      id: uuid(),
      status: 'resolved',
      operator: '巡检员B',
      remark: '风险已解除',
      createdAt: alerts[3].updatedAt,
    },
  ],
}

export const appendTimeline = (alertId: string, status: AlertStatus, remark: string, operator: string) => {
  const arr = alertTimelineMap[alertId] || []
  arr.push({
    id: uuid(),
    status,
    operator,
    remark,
    createdAt: new Date().toISOString(),
  })
  alertTimelineMap[alertId] = arr
}
