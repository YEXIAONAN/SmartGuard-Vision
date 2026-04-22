export const createRiskTrendOption = (payload) => ({
  animation: false,
  tooltip: { trigger: 'axis' },
  grid: { left: 28, right: 12, top: 24, bottom: 24 },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: payload.labels,
    axisLine: { lineStyle: { color: '#ccd6e3' } },
    axisLabel: { color: '#5a6d82' },
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#e9eef5' } },
    axisLabel: { color: '#5a6d82' },
  },
  series: [
    {
      data: payload.values,
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { width: 2, color: '#365f8d' },
      itemStyle: { color: '#365f8d' },
    },
  ],
})

export const createParkingRecognitionOption = (payload) => ({
  animation: false,
  tooltip: { trigger: 'axis' },
  grid: { left: 20, right: 12, top: 20, bottom: 24, containLabel: true },
  xAxis: {
    type: 'category',
    data: payload.labels,
    axisLine: { lineStyle: { color: '#ccd6e3' } },
    axisLabel: { color: '#5a6d82', interval: 0 },
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#e9eef5' } },
    axisLabel: { color: '#5a6d82' },
  },
  series: [
    {
      data: payload.values,
      type: 'bar',
      barWidth: 24,
      itemStyle: {
        color: ({ dataIndex }) => payload.colors[dataIndex],
        borderRadius: [4, 4, 0, 0],
      },
    },
  ],
})

export const createRiskLevelOption = (payload) => ({
  animation: false,
  tooltip: { trigger: 'item' },
  legend: {
    bottom: 2,
    itemWidth: 10,
    itemHeight: 10,
    textStyle: { color: '#5a6d82' },
  },
  series: [
    {
      type: 'pie',
      radius: ['46%', '66%'],
      center: ['50%', '42%'],
      label: { color: '#5a6d82', fontSize: 11 },
      labelLine: { length: 10, length2: 6 },
      data: payload.map((item) => ({
        value: item.value,
        name: item.name,
        itemStyle: { color: item.color },
      })),
    },
  ],
})

export const createAreaRiskOption = (payload) => ({
  animation: false,
  tooltip: { trigger: 'axis' },
  grid: { left: 18, right: 20, top: 20, bottom: 18, containLabel: true },
  xAxis: {
    type: 'value',
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#e9eef5' } },
    axisLabel: { color: '#5a6d82' },
  },
  yAxis: {
    type: 'category',
    data: payload.map((item) => item.name),
    axisLabel: { color: '#5a6d82' },
    axisLine: { show: false },
    axisTick: { show: false },
  },
  series: [
    {
      type: 'bar',
      barWidth: 14,
      data: payload.map((item) => ({
        value: item.value,
        itemStyle: { color: item.color, borderRadius: [0, 4, 4, 0] },
      })),
      label: { show: true, position: 'right', color: '#32465d', fontSize: 11 },
    },
  ],
})

export const createAlertTrendOption = (payload) => ({
  animation: false,
  tooltip: { trigger: 'axis' },
  legend: { right: 4, textStyle: { color: '#5a6d82' } },
  grid: { left: 20, right: 16, top: 28, bottom: 22, containLabel: true },
  xAxis: {
    type: 'category',
    data: payload.labels,
    axisLine: { lineStyle: { color: '#ccd6e3' } },
    axisLabel: { color: '#5a6d82' },
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#e9eef5' } },
    axisLabel: { color: '#5a6d82' },
  },
  series: [
    {
      name: '告警总量',
      type: 'bar',
      barWidth: 14,
      data: payload.total,
      itemStyle: { color: '#7f98b7', borderRadius: [3, 3, 0, 0] },
    },
    {
      name: '高风险事件',
      type: 'line',
      smooth: true,
      data: payload.highRisk,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { width: 2, color: '#ad5656' },
      itemStyle: { color: '#ad5656' },
    },
  ],
})
