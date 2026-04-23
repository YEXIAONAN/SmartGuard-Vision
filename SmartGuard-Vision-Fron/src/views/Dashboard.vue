<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted } from 'vue'
import type { EChartsOption } from 'echarts'
import { ElMessage } from 'element-plus'
import { useDashboardStore } from '@/stores/dashboard'
import AppShell from '@/components/dashboard/AppShell.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppLoading from '@/components/common/AppLoading.vue'
import AppEmpty from '@/components/common/AppEmpty.vue'
import StatCard from '@/components/dashboard/StatCard.vue'
import TrendChart from '@/components/dashboard/TrendChart.vue'
import DeviceGrid from '@/components/dashboard/DeviceGrid.vue'
import RiskDetail from '@/components/dashboard/RiskDetail.vue'
import AlertList from '@/components/dashboard/AlertList.vue'
import type { AlertStatus } from '@/types/dashboard'

const dashboardStore = useDashboardStore()

const statCards = computed(() => {
  const stats = dashboardStore.overviewStats
  if (!stats) return []
  return [
    { title: '在线设备', value: `${stats.onlineDevices} / ${stats.totalDevices}`, subtitle: '实时在线数量', type: 'normal' },
    { title: '今日告警', value: stats.todayAlerts, subtitle: '今日新增告警', type: 'warning' },
    { title: '高风险事件', value: stats.highRiskAlerts, subtitle: '需优先处置', type: 'danger' },
    { title: '充电监测点位', value: stats.chargingPoints, subtitle: '重点区域监测', type: 'normal' },
    { title: '温升异常', value: stats.temperatureAnomalies, subtitle: '温度/烟雾异常', type: 'warning' },
    { title: 'SLA 超时', value: stats.slaTimeouts, subtitle: '处置超时任务', type: 'danger' },
    { title: '平均处置时长', value: `${stats.avgHandleMinutes} 分钟`, subtitle: '当前处置效率', type: 'normal' },
  ]
})

const trendOption = computed<EChartsOption>(() => {
  const points = dashboardStore.chartData?.trend24h || []
  return {
    grid: { top: 24, right: 20, left: 36, bottom: 30 },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: points.map((item) => item.time),
      axisLine: { lineStyle: { color: '#b7c7dd' } },
      axisLabel: { color: '#6e6e73' },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: 'rgba(182, 199, 220, 0.38)' } },
      axisLabel: { color: '#6e6e73' },
    },
    series: [
      {
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: { color: '#007aff', width: 3 },
        itemStyle: { color: '#007aff' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(0, 122, 255, 0.32)' },
              { offset: 1, color: 'rgba(0, 122, 255, 0.03)' },
            ],
          },
        },
        data: points.map((item) => item.value),
      },
    ],
  }
})

const devicePieOption = computed<EChartsOption>(() => ({
  tooltip: { trigger: 'item' },
  legend: { bottom: 0, textStyle: { color: '#6e6e73' } },
  series: [
    {
      type: 'pie',
      radius: ['42%', '72%'],
      avoidLabelOverlap: false,
      label: { color: '#6e6e73' },
      data: dashboardStore.chartData?.deviceDistribution || [],
      itemStyle: {
        borderRadius: 8,
        borderWidth: 4,
        borderColor: '#f4f7fd',
      },
    },
  ],
}))

const riskBarOption = computed<EChartsOption>(() => ({
  tooltip: { trigger: 'axis' },
  xAxis: {
    type: 'category',
    data: (dashboardStore.chartData?.riskDistribution || []).map((item) => item.level),
    axisLabel: { color: '#6e6e73' },
  },
  yAxis: {
    type: 'value',
    axisLabel: { color: '#6e6e73' },
    splitLine: { lineStyle: { color: 'rgba(182, 199, 220, 0.38)' } },
  },
  series: [
    {
      type: 'bar',
      barWidth: 36,
      itemStyle: {
        borderRadius: [8, 8, 0, 0],
        color: (params: { dataIndex: number }) => ['#34c759', '#ff9f0a', '#ff3b30'][params.dataIndex] || '#007aff',
      },
      data: (dashboardStore.chartData?.riskDistribution || []).map((item) => item.value),
    },
  ],
}))

const handleAlertStatusUpdate = async (status: AlertStatus) => {
  try {
    await dashboardStore.updateSelectedAlertStatus(status)
    ElMessage.success(status === 'processing' ? '已转为处理中' : '已标记为完成')
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '更新失败')
  }
}

onMounted(async () => {
  await dashboardStore.initialize()
  dashboardStore.startPolling(10000)
})

onBeforeUnmount(() => {
  dashboardStore.stopPolling()
})
</script>

<template>
  <AppShell @refresh="dashboardStore.refreshCore">
    <el-alert
      v-if="dashboardStore.error"
      class="error-alert"
      :title="dashboardStore.error"
      type="error"
      show-icon
      :closable="false"
    />

    <template v-if="dashboardStore.loading && !dashboardStore.overviewStats">
      <AppCard title="数据加载中">
        <AppLoading />
      </AppCard>
    </template>

    <template v-else>
      <section class="stats-grid">
        <StatCard
          v-for="item in statCards"
          :key="item.title"
          :title="item.title"
          :value="item.value"
          :subtitle="item.subtitle"
          :type="item.type as 'normal' | 'warning' | 'danger'"
        />
      </section>

      <section class="chart-grid">
        <AppCard title="最近24小时告警趋势" extra="实时更新">
          <TrendChart :option="trendOption" :height="280" />
        </AppCard>
        <AppCard title="设备状态分布" extra="在线 / 离线 / 告警">
          <TrendChart :option="devicePieOption" :height="280" />
        </AppCard>
        <AppCard title="风险等级分布" extra="低 / 中 / 高">
          <TrendChart :option="riskBarOption" :height="280" />
        </AppCard>
      </section>

      <section class="content-grid">
        <AppCard title="设备监控网格" extra="按状态高亮">
          <template v-if="dashboardStore.devices.length">
            <DeviceGrid :devices="dashboardStore.devices" :selected-device-id="dashboardStore.selectedDeviceId" />
          </template>
          <AppEmpty v-else description="暂无设备信息" />
        </AppCard>

        <AppCard title="当前风险详情" extra="支持处置流转">
          <RiskDetail
            :detail="dashboardStore.riskDetail"
            :loading="dashboardStore.detailLoading"
            @update-status="handleAlertStatusUpdate"
          />
        </AppCard>
      </section>

      <section class="alert-section">
        <AppCard title="实时告警列表" extra="点击联动右侧详情与设备高亮">
          <AlertList
            :alerts="dashboardStore.alerts"
            :selected-alert-id="dashboardStore.selectedAlert?.id || null"
            @select="dashboardStore.selectAlertById"
          />
        </AppCard>
      </section>
    </template>
  </AppShell>
</template>

<style scoped lang="scss">
.error-alert {
  border-radius: 12px;
}

.stats-grid {
  display: grid;
  gap: 10px;
  grid-template-columns: repeat(7, minmax(0, 1fr));
}

.chart-grid {
  display: grid;
  gap: 10px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.content-grid {
  display: grid;
  gap: 10px;
  grid-template-columns: minmax(0, 1.25fr) minmax(380px, 1fr);
  align-items: start;
}

.alert-section {
  display: grid;
}

@media (max-width: 1820px) {
  .stats-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 1400px) {
  .chart-grid {
    grid-template-columns: 1fr;
  }
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 992px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
