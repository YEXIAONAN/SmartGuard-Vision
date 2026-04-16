import * as echarts from 'echarts'

export const createRiskTrendOption = (payload) => ({
  tooltip: { trigger: 'axis' },
  grid: { left: 28, right: 18, top: 28, bottom: 24 },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: payload.labels,
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
      data: payload.values,
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

export const createParkingRecognitionOption = (payload) => ({
  tooltip: { trigger: 'axis' },
  grid: { left: 18, right: 18, top: 20, bottom: 24, containLabel: true },
  xAxis: {
    type: 'category',
    data: payload.labels,
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
      data: payload.values,
      type: 'bar',
      barWidth: 26,
      itemStyle: {
        borderRadius: [6, 6, 0, 0],
        color: ({ dataIndex }) => payload.colors[dataIndex],
      },
    },
  ],
})

export const createRiskLevelOption = (payload) => ({
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
      data: payload.map((item) => ({
        value: item.value,
        name: item.name,
        itemStyle: { color: item.color },
      })),
    },
  ],
})

export const createAreaRiskOption = (payload) => ({
  tooltip: { trigger: 'axis' },
  grid: { left: 18, right: 24, top: 20, bottom: 24, containLabel: true },
  xAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: '#e7eef6' } },
    axisLabel: { color: '#5b6b7f' },
  },
  yAxis: {
    type: 'category',
    data: payload.map((item) => item.name),
    axisLabel: { color: '#5b6b7f' },
    axisLine: { show: false },
    axisTick: { show: false },
  },
  series: [
    {
      type: 'bar',
      barWidth: 18,
      data: payload.map((item) => ({
        value: item.value,
        itemStyle: { color: item.color },
      })),
      label: {
        show: true,
        position: 'right',
        color: '#3b4a5c',
      },
    },
  ],
})

export const createAlertTrendOption = (payload) => ({
  tooltip: { trigger: 'axis' },
  legend: {
    right: 0,
    textStyle: { color: '#5b6b7f' },
  },
  grid: { left: 18, right: 18, top: 30, bottom: 24, containLabel: true },
  xAxis: {
    type: 'category',
    data: payload.labels,
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
      data: payload.total,
      itemStyle: { color: '#8fb7ff', borderRadius: [6, 6, 0, 0] },
    },
    {
      name: '高风险事件',
      type: 'line',
      smooth: true,
      data: payload.highRisk,
      symbol: 'circle',
      symbolSize: 7,
      lineStyle: { width: 3, color: '#e35d5d' },
      itemStyle: { color: '#e35d5d' },
    },
  ],
})
