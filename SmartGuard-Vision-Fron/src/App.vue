<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import * as echarts from 'echarts'

const currentTime = ref('')

const statCards = [
  { title: '接入设备数', value: '256', unit: '台', note: '摄像机、烟感、温感、充电终端' },
  { title: '今日告警数', value: '18', unit: '起', note: '较昨日下降 12.5%' },
  { title: '高风险事件数', value: '3', unit: '起', note: '均已进入复核处置流程' },
  { title: '在线监测点位数', value: '42', unit: '处', note: '覆盖教学区、宿舍区、车棚区' },
]

const alertList = [
  { time: '15:18:32', level: '高风险', place: 'A区充电棚 03', detail: '检测到飞线充电行为，已推送值守人员。' },
  { time: '14:56:07', level: '中风险', place: '学生宿舍北侧', detail: '车辆停放越线，占用消防通道边界。' },
  { time: '13:42:15', level: '一般', place: '综合实训楼西侧', detail: '识别到头盔悬挂充电插座，建议现场复查。' },
  { time: '11:08:51', level: '高风险', place: '地下停放点 02', detail: '电池拆卸充电，伴随温升异常。' },
  { time: '09:26:44', level: '中风险', place: '后勤服务区', detail: '充电结束未及时拔除设备，停放密度偏高。' },
]

const deviceStatusList = [
  { name: '视频监测设备', online: 118, total: 126 },
  { name: '烟雾感知设备', online: 52, total: 54 },
  { name: '温度感知设备', online: 36, total: 38 },
  { name: '充电终端设备', online: 42, total: 42 },
]

const recognitionList = [
  { label: '当前点位', value: '教学楼东侧集中停放区' },
  { label: '识别状态', value: '持续监测中' },
  { label: '停放秩序', value: '存在 2 处越线停放' },
  { label: '充电行为', value: '识别到 1 起飞线充电' },
  { label: '环境状态', value: '烟感正常，局部温度偏高' },
  { label: '处置建议', value: '现场巡查并断开异常充电线路' },
]

const riskTrendRef = ref(null)
const parkingChartRef = ref(null)
const riskLevelChartRef = ref(null)
const heatChartRef = ref(null)
const alertTrendChartRef = ref(null)

let timeTimer = null
const chartInstances = []

const updateCurrentTime = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const date = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  currentTime.value = `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`
}

const initChart = (chartRef, option) => {
  if (!chartRef.value) return

  const instance = echarts.init(chartRef.value)
  instance.setOption(option)
  chartInstances.push(instance)
}

const buildCharts = () => {
  chartInstances.forEach((item) => item.dispose())
  chartInstances.length = 0

  initChart(riskTrendRef, {
    tooltip: { trigger: 'axis' },
    grid: { left: 28, right: 18, top: 28, bottom: 24 },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'],
      axisLine: { lineStyle: { color: '#c7d3e3' } },
      axisLabel: { color: '#5b6b7f' },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#e7eef6' } },
      axisLabel: { color: '#5b6b7f' },
    },
    series: [
      {
        data: [3, 5, 4, 8, 6, 7, 5],
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: { width: 3, color: '#2f6bff' },
        itemStyle: { color: '#2f6bff' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(47, 107, 255, 0.24)' },
            { offset: 1, color: 'rgba(47, 107, 255, 0.03)' },
          ]),
        },
      },
    ],
  })

  initChart(parkingChartRef, {
    tooltip: { trigger: 'axis' },
    grid: { left: 18, right: 18, top: 20, bottom: 24, containLabel: true },
    xAxis: {
      type: 'category',
      data: ['规范停放', '越线停放', '占道停放', '密集停放'],
      axisLine: { lineStyle: { color: '#c7d3e3' } },
      axisLabel: { color: '#5b6b7f' },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#e7eef6' } },
      axisLabel: { color: '#5b6b7f' },
    },
    series: [
      {
        data: [168, 22, 8, 13],
        type: 'bar',
        barWidth: 26,
        itemStyle: {
          borderRadius: [6, 6, 0, 0],
          color: ({ dataIndex }) => ['#4c8bf5', '#7aa9ff', '#f3b24d', '#f08c6a'][dataIndex],
        },
      },
    ],
  })

  initChart(riskLevelChartRef, {
    tooltip: { trigger: 'item' },
    legend: {
      bottom: 0,
      itemWidth: 10,
      itemHeight: 10,
      textStyle: { color: '#5b6b7f' },
    },
    series: [
      {
        type: 'pie',
        radius: ['48%', '68%'],
        center: ['50%', '42%'],
        label: { color: '#5b6b7f', formatter: '{b}\n{d}%' },
        labelLine: { length: 12, length2: 8 },
        data: [
          { value: 3, name: '高风险', itemStyle: { color: '#e35d5d' } },
          { value: 7, name: '中风险', itemStyle: { color: '#f2a93b' } },
          { value: 12, name: '一般风险', itemStyle: { color: '#4c8bf5' } },
          { value: 20, name: '低风险', itemStyle: { color: '#9dc2ff' } },
        ],
      },
    ],
  })

  initChart(heatChartRef, {
    tooltip: { trigger: 'axis' },
    grid: { left: 18, right: 24, top: 20, bottom: 24, containLabel: true },
    xAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#e7eef6' } },
      axisLabel: { color: '#5b6b7f' },
    },
    yAxis: {
      type: 'category',
      data: ['宿舍充电棚', '教学楼东侧', '食堂北通道', '实训中心南侧', '地下停放点'],
      axisLabel: { color: '#5b6b7f' },
      axisLine: { show: false },
      axisTick: { show: false },
    },
    series: [
      {
        type: 'bar',
        barWidth: 18,
        data: [
          { value: 92, itemStyle: { color: '#d85c5c' } },
          { value: 76, itemStyle: { color: '#eb8b56' } },
          { value: 64, itemStyle: { color: '#f3b24d' } },
          { value: 48, itemStyle: { color: '#72a6ff' } },
          { value: 36, itemStyle: { color: '#4c8bf5' } },
        ],
        label: {
          show: true,
          position: 'right',
          color: '#3b4a5c',
        },
      },
    ],
  })

  initChart(alertTrendChartRef, {
    tooltip: { trigger: 'axis' },
    legend: {
      right: 0,
      textStyle: { color: '#5b6b7f' },
    },
    grid: { left: 18, right: 18, top: 30, bottom: 24, containLabel: true },
    xAxis: {
      type: 'category',
      data: ['04-10', '04-11', '04-12', '04-13', '04-14', '04-15', '04-16'],
      axisLine: { lineStyle: { color: '#c7d3e3' } },
      axisLabel: { color: '#5b6b7f' },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#e7eef6' } },
      axisLabel: { color: '#5b6b7f' },
    },
    series: [
      {
        name: '告警总量',
        type: 'bar',
        barWidth: 18,
        data: [11, 15, 9, 13, 16, 14, 18],
        itemStyle: { color: '#8fb7ff', borderRadius: [6, 6, 0, 0] },
      },
      {
        name: '高风险事件',
        type: 'line',
        smooth: true,
        data: [2, 3, 1, 2, 4, 2, 3],
        symbol: 'circle',
        symbolSize: 7,
        lineStyle: { width: 3, color: '#e35d5d' },
        itemStyle: { color: '#e35d5d' },
      },
    ],
  })
}

const handleResize = () => {
  chartInstances.forEach((item) => item.resize())
}

onMounted(async () => {
  updateCurrentTime()
  timeTimer = window.setInterval(updateCurrentTime, 1000)

  await nextTick()
  buildCharts()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  if (timeTimer) {
    window.clearInterval(timeTimer)
  }

  window.removeEventListener('resize', handleResize)
  chartInstances.forEach((item) => item.dispose())
})
</script>

<template>
  <div class="page-shell">
    <div class="page-backdrop"></div>

    <div class="dashboard-page">
      <el-card shadow="never" class="panel-card page-header">
        <div class="header-main">
          <div>
            <div class="project-title">智感护航</div>
            <div class="project-subtitle">面向停充场景的多模态安全感知平台</div>
          </div>

          <div class="header-metrics">
            <div class="header-metric">
              <span class="metric-label">当前时间</span>
              <span class="metric-value">{{ currentTime }}</span>
            </div>
            <div class="header-metric">
              <span class="metric-label">系统状态</span>
              <span class="metric-value">
                <span class="status-dot"></span>
                运行正常
              </span>
            </div>
            <div class="header-metric">
              <span class="metric-label">在线设备数</span>
              <span class="metric-value">248 / 256</span>
            </div>
          </div>
        </div>
      </el-card>

      <el-row :gutter="16" class="stats-row">
        <el-col v-for="item in statCards" :key="item.title" :xs="24" :sm="12" :lg="6">
          <el-card shadow="never" class="panel-card stat-card">
            <div class="panel-head">
              <span class="panel-title">{{ item.title }}</span>
            </div>
            <div class="stat-value-wrap">
              <span class="stat-value">{{ item.value }}</span>
              <span class="stat-unit">{{ item.unit }}</span>
            </div>
            <div class="stat-note">{{ item.note }}</div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="16" class="content-row">
        <el-col :xs="24" :lg="6">
          <div class="stack-column">
            <el-card shadow="never" class="panel-card">
              <template #header>
                <div class="panel-head">
                  <span class="panel-title">风险趋势图</span>
                  <span class="panel-extra">按时段统计</span>
                </div>
              </template>
              <div ref="riskTrendRef" class="chart-box chart-medium"></div>
            </el-card>

            <el-card shadow="never" class="panel-card">
              <template #header>
                <div class="panel-head">
                  <span class="panel-title">停放规范识别统计</span>
                  <span class="panel-extra">今日累计</span>
                </div>
              </template>
              <div ref="parkingChartRef" class="chart-box chart-medium"></div>
            </el-card>
          </div>
        </el-col>

        <el-col :xs="24" :lg="12">
          <el-card shadow="never" class="panel-card monitor-card">
            <template #header>
              <div class="panel-head">
                <span class="panel-title">实时监测主面板</span>
                <span class="panel-extra">监测通道 01</span>
              </div>
            </template>

            <div class="monitor-layout">
              <div class="monitor-screen">
                <div class="screen-badge">实时监测画面</div>
                <div class="screen-overlay overlay-main">飞线充电</div>
                <div class="screen-overlay overlay-secondary">越线停放</div>
                <div class="screen-footer">
                  <span>点位编码：JC-ED-03</span>
                  <span>采集状态：稳定</span>
                </div>
              </div>

              <div class="monitor-side">
                <div class="info-group">
                  <div class="info-group-title">识别结果信息</div>
                  <div v-for="item in recognitionList" :key="item.label" class="info-item">
                    <span class="info-label">{{ item.label }}</span>
                    <span class="info-value">{{ item.value }}</span>
                  </div>
                </div>

                <div class="tag-group">
                  <el-tag type="danger" effect="plain">飞线充电</el-tag>
                  <el-tag type="warning" effect="plain">温升关注</el-tag>
                  <el-tag type="primary" effect="plain">越线停放</el-tag>
                  <el-tag type="info" effect="plain">人工复核中</el-tag>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <el-col :xs="24" :lg="6">
          <div class="stack-column">
            <el-card shadow="never" class="panel-card">
              <template #header>
                <div class="panel-head">
                  <span class="panel-title">实时告警列表</span>
                  <span class="panel-extra">最新 5 条</span>
                </div>
              </template>

              <div class="alert-list">
                <div v-for="item in alertList" :key="`${item.time}-${item.place}`" class="alert-item">
                  <div class="alert-top">
                    <span class="alert-time">{{ item.time }}</span>
                    <el-tag
                      :type="
                        item.level === '高风险'
                          ? 'danger'
                          : item.level === '中风险'
                            ? 'warning'
                            : 'info'
                      "
                      size="small"
                      effect="plain"
                    >
                      {{ item.level }}
                    </el-tag>
                  </div>
                  <div class="alert-place">{{ item.place }}</div>
                  <div class="alert-detail">{{ item.detail }}</div>
                </div>
              </div>
            </el-card>

            <el-card shadow="never" class="panel-card">
              <template #header>
                <div class="panel-head">
                  <span class="panel-title">设备在线状态</span>
                  <span class="panel-extra">实时巡检</span>
                </div>
              </template>

              <div class="device-list">
                <div v-for="item in deviceStatusList" :key="item.name" class="device-item">
                  <div class="device-top">
                    <span>{{ item.name }}</span>
                    <span>{{ item.online }}/{{ item.total }}</span>
                  </div>
                  <el-progress
                    :percentage="Math.round((item.online / item.total) * 100)"
                    :stroke-width="10"
                    :show-text="false"
                    color="#2f6bff"
                  />
                </div>
              </div>
            </el-card>

            <el-card shadow="never" class="panel-card">
              <template #header>
                <div class="panel-head">
                  <span class="panel-title">风险等级分布</span>
                  <span class="panel-extra">当前点位</span>
                </div>
              </template>
              <div ref="riskLevelChartRef" class="chart-box chart-small"></div>
            </el-card>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="16" class="analysis-row">
        <el-col :xs="24" :lg="12">
          <el-card shadow="never" class="panel-card">
            <template #header>
              <div class="panel-head">
                <span class="panel-title">区域风险热力分布</span>
                <span class="panel-extra">重点区域排序</span>
              </div>
            </template>
            <div ref="heatChartRef" class="chart-box chart-large"></div>
          </el-card>
        </el-col>

        <el-col :xs="24" :lg="12">
          <el-card shadow="never" class="panel-card">
            <template #header>
              <div class="panel-head">
                <span class="panel-title">近7日告警趋势分析</span>
                <span class="panel-extra">总量与高风险事件</span>
              </div>
            </template>
            <div ref="alertTrendChartRef" class="chart-box chart-large"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<style>
:root {
  color-scheme: light;
  font-family:
    'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', 'Helvetica Neue', Arial, sans-serif;
  background: #f3f7fb;
  color: #243447;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background:
    linear-gradient(180deg, #eef5fc 0%, #f5f8fc 38%, #f2f6fb 100%);
  color: #243447;
}

#app {
  min-height: 100vh;
}

.page-shell {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.page-backdrop {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at top left, rgba(117, 164, 255, 0.14), transparent 28%),
    radial-gradient(circle at right 20%, rgba(112, 179, 255, 0.1), transparent 24%);
  pointer-events: none;
}

.dashboard-page {
  position: relative;
  z-index: 1;
  padding: 20px;
}

.panel-card {
  border: 1px solid #dbe5f0;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.96);
}

.panel-card .el-card__header {
  padding: 16px 18px 10px;
  border-bottom: none;
}

.panel-card .el-card__body {
  padding: 0 18px 18px;
}

.page-header .el-card__body {
  padding: 18px 22px;
}

.header-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.project-title {
  font-size: 30px;
  font-weight: 700;
  line-height: 1.1;
  color: #1f3e68;
  letter-spacing: 1px;
}

.project-subtitle {
  margin-top: 8px;
  font-size: 15px;
  color: #5d7188;
}

.header-metrics {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 12px;
}

.header-metric {
  min-width: 180px;
  padding: 10px 14px;
  border: 1px solid #e3ebf5;
  border-radius: 10px;
  background: #f7faff;
}

.metric-label {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  color: #6a7d92;
}

.metric-value {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #20354d;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #2fa86f;
}

.stats-row,
.content-row,
.analysis-row {
  margin-top: 16px;
}

.stat-card .el-card__body {
  padding: 18px;
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.panel-title {
  font-size: 16px;
  font-weight: 600;
  color: #243447;
}

.panel-extra {
  font-size: 12px;
  color: #6c8096;
}

.stat-value-wrap {
  display: flex;
  align-items: flex-end;
  margin-top: 18px;
  gap: 8px;
}

.stat-value {
  font-size: 34px;
  line-height: 1;
  font-weight: 700;
  color: #2458bf;
}

.stat-unit {
  margin-bottom: 4px;
  font-size: 14px;
  color: #69809a;
}

.stat-note {
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid #e8eef5;
  font-size: 13px;
  line-height: 1.6;
  color: #61758b;
}

.stack-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chart-box {
  width: 100%;
}

.chart-small {
  height: 220px;
}

.chart-medium {
  height: 250px;
}

.chart-large {
  height: 300px;
}

.monitor-card .el-card__body {
  padding: 0 18px 18px;
}

.monitor-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
  gap: 16px;
}

.monitor-screen {
  position: relative;
  min-height: 430px;
  border-radius: 14px;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgba(38, 73, 121, 0.18), rgba(19, 41, 78, 0.34)),
    linear-gradient(135deg, #c6d8f2 0%, #f1f6fc 42%, #d5e2f3 100%);
  border: 1px solid #d7e2ef;
}

.monitor-screen::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(rgba(255, 255, 255, 0.18) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.18) 1px, transparent 1px);
  background-size: 36px 36px;
  opacity: 0.45;
}

.screen-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 1;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(20, 54, 104, 0.86);
  color: #fff;
  font-size: 13px;
}

.screen-overlay {
  position: absolute;
  z-index: 1;
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  color: #fff;
}

.overlay-main {
  top: 108px;
  right: 82px;
  background: rgba(215, 89, 89, 0.92);
}

.overlay-secondary {
  bottom: 104px;
  left: 74px;
  background: rgba(242, 169, 59, 0.92);
}

.screen-footer {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  padding: 14px 18px;
  background: rgba(15, 37, 68, 0.78);
  font-size: 13px;
  color: rgba(255, 255, 255, 0.92);
}

.monitor-side {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-group {
  padding: 16px;
  border: 1px solid #e2ebf5;
  border-radius: 12px;
  background: #f8fbff;
}

.info-group-title {
  margin-bottom: 14px;
  font-size: 15px;
  font-weight: 600;
  color: #25405f;
}

.info-item {
  display: grid;
  grid-template-columns: 84px minmax(0, 1fr);
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed #dde7f2;
}

.info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.info-label {
  color: #60768f;
  font-size: 13px;
}

.info-value {
  color: #243447;
  font-size: 14px;
  line-height: 1.6;
}

.tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 2px 0;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alert-item {
  padding: 12px 14px;
  border: 1px solid #e4ebf3;
  border-radius: 12px;
  background: #f9fbfe;
}

.alert-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.alert-time {
  font-size: 12px;
  color: #6e8298;
}

.alert-place {
  margin-top: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #22364f;
}

.alert-detail {
  margin-top: 6px;
  font-size: 13px;
  line-height: 1.6;
  color: #5f7389;
}

.device-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.device-item {
  padding: 12px 14px;
  border-radius: 12px;
  background: #f8fbff;
  border: 1px solid #e4ebf3;
}

.device-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 13px;
  color: #33485f;
}

@media (max-width: 1366px) {
  .project-title {
    font-size: 26px;
  }

  .monitor-layout {
    grid-template-columns: 1fr;
  }

  .monitor-screen {
    min-height: 360px;
  }
}

@media (max-width: 992px) {
  .dashboard-page {
    padding: 14px;
  }

  .header-main {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-metrics {
    width: 100%;
    justify-content: flex-start;
  }

  .header-metric {
    min-width: calc(50% - 6px);
  }
}

@media (max-width: 768px) {
  .header-metric {
    min-width: 100%;
  }

  .project-title {
    font-size: 24px;
  }

  .project-subtitle {
    font-size: 14px;
    line-height: 1.6;
  }

  .chart-medium,
  .chart-large,
  .chart-small {
    height: 240px;
  }

  .monitor-screen {
    min-height: 300px;
  }

  .screen-footer {
    flex-direction: column;
    gap: 6px;
  }
}
</style>
