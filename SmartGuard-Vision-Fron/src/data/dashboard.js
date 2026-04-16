export const dashboardMock = {
  project: {
    name: '智感护航',
    subtitle: '面向停充场景的多模态安全感知平台',
  },
  systemStatus: '运行正常',
  onlineSummary: '248 / 256',
  stats: [
    { title: '接入设备数', value: '256', unit: '台', note: '摄像机、烟感、温感、充电终端' },
    { title: '今日告警数', value: '18', unit: '起', note: '较昨日下降 12.5%' },
    { title: '高风险事件数', value: '3', unit: '起', note: '均已进入复核处置流程' },
    { title: '在线监测点位数', value: '42', unit: '处', note: '覆盖教学区、宿舍区、车棚区' },
  ],
  alerts: [
    { time: '15:18:32', level: '高风险', place: 'A区充电棚 03', detail: '检测到飞线充电行为，已推送值守人员。' },
    { time: '14:56:07', level: '中风险', place: '学生宿舍北侧', detail: '车辆停放越线，占用消防通道边界。' },
    { time: '13:42:15', level: '一般', place: '综合实训楼西侧', detail: '识别到头盔悬挂充电插座，建议现场复查。' },
    { time: '11:08:51', level: '高风险', place: '地下停放点 02', detail: '电池拆卸充电，伴随温升异常。' },
    { time: '09:26:44', level: '中风险', place: '后勤服务区', detail: '充电结束未及时拔除设备，停放密度偏高。' },
  ],
  devices: [
    { name: '视频监测设备', online: 118, total: 126 },
    { name: '烟雾感知设备', online: 52, total: 54 },
    { name: '温度感知设备', online: 36, total: 38 },
    { name: '充电终端设备', online: 42, total: 42 },
  ],
  monitor: {
    title: '实时监测主面板',
    channel: '监测通道 01',
    pointCode: 'JC-ED-03',
    captureStatus: '稳定',
    screenLabel: '实时监测画面',
    overlays: [
      { text: '飞线充电', className: 'overlay-main' },
      { text: '越线停放', className: 'overlay-secondary' },
    ],
    tags: ['飞线充电', '温升关注', '越线停放', '人工复核中'],
    recognitionList: [
      { label: '当前点位', value: '教学楼东侧集中停放区' },
      { label: '识别状态', value: '持续监测中' },
      { label: '停放秩序', value: '存在 2 处越线停放' },
      { label: '充电行为', value: '识别到 1 起飞线充电' },
      { label: '环境状态', value: '烟感正常，局部温度偏高' },
      { label: '处置建议', value: '现场巡查并断开异常充电线路' },
    ],
  },
  riskTrend: {
    labels: ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'],
    values: [3, 5, 4, 8, 6, 7, 5],
  },
  parkingRecognition: {
    labels: ['规范停放', '越线停放', '占道停放', '密集停放'],
    values: [168, 22, 8, 13],
    colors: ['#4c8bf5', '#7aa9ff', '#f3b24d', '#f08c6a'],
  },
  riskLevel: [
    { name: '高风险', value: 3, color: '#e35d5d' },
    { name: '中风险', value: 7, color: '#f2a93b' },
    { name: '一般风险', value: 12, color: '#4c8bf5' },
    { name: '低风险', value: 20, color: '#9dc2ff' },
  ],
  areaRisk: [
    { name: '宿舍充电棚', value: 92, color: '#d85c5c' },
    { name: '教学楼东侧', value: 76, color: '#eb8b56' },
    { name: '食堂北通道', value: 64, color: '#f3b24d' },
    { name: '实训中心南侧', value: 48, color: '#72a6ff' },
    { name: '地下停放点', value: 36, color: '#4c8bf5' },
  ],
  alertTrend: {
    labels: ['04-10', '04-11', '04-12', '04-13', '04-14', '04-15', '04-16'],
    total: [11, 15, 9, 13, 16, 14, 18],
    highRisk: [2, 3, 1, 2, 4, 2, 3],
  },
}
