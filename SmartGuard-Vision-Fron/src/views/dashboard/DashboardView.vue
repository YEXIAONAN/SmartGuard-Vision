<script setup>
import { computed } from 'vue'
import PanelCard from '../../components/common/PanelCard.vue'
import DashboardAlertList from '../../components/dashboard/DashboardAlertList.vue'
import DashboardChartPanel from '../../components/dashboard/DashboardChartPanel.vue'
import DashboardDeviceStatus from '../../components/dashboard/DashboardDeviceStatus.vue'
import DashboardHeader from '../../components/dashboard/DashboardHeader.vue'
import DashboardMonitor from '../../components/dashboard/DashboardMonitor.vue'
import DashboardStats from '../../components/dashboard/DashboardStats.vue'
import { useClock } from '../../composables/useClock'
import { useDashboardStore } from '../../stores/dashboard'
import {
  createAlertTrendOption,
  createAreaRiskOption,
  createParkingRecognitionOption,
  createRiskLevelOption,
  createRiskTrendOption,
} from './chart-options'

const dashboardStore = useDashboardStore()
const { currentTime } = useClock()

const riskTrendOption = computed(() => createRiskTrendOption(dashboardStore.riskTrend))
const parkingRecognitionOption = computed(() =>
  createParkingRecognitionOption(dashboardStore.parkingRecognition),
)
const riskLevelOption = computed(() => createRiskLevelOption(dashboardStore.riskLevel))
const areaRiskOption = computed(() => createAreaRiskOption(dashboardStore.areaRisk))
const alertTrendOption = computed(() => createAlertTrendOption(dashboardStore.alertTrend))
</script>

<template>
  <div class="page-container dashboard-page">
    <PanelCard body-padding="18px 22px">
      <DashboardHeader
        :project-name="dashboardStore.project.name"
        :subtitle="dashboardStore.project.subtitle"
        :current-time="currentTime"
        :system-status="dashboardStore.systemStatus"
        :online-summary="dashboardStore.onlineSummary"
      />
    </PanelCard>

    <DashboardStats :stats="dashboardStore.stats" />

    <el-row :gutter="16" class="content-row">
      <el-col :xs="24" :lg="6">
        <div class="stack-column">
          <DashboardChartPanel
            title="风险趋势图"
            extra="按时段统计"
            :option="riskTrendOption"
            :height="250"
          />
          <DashboardChartPanel
            title="停放规范识别统计"
            extra="今日累计"
            :option="parkingRecognitionOption"
            :height="250"
          />
        </div>
      </el-col>

      <el-col :xs="24" :lg="12">
        <PanelCard :title="dashboardStore.monitor.title" :extra="dashboardStore.monitor.channel">
          <DashboardMonitor :monitor="dashboardStore.monitor" />
        </PanelCard>
      </el-col>

      <el-col :xs="24" :lg="6">
        <div class="stack-column">
          <PanelCard title="实时告警列表" extra="最新 5 条">
            <DashboardAlertList :alerts="dashboardStore.alerts" />
          </PanelCard>
          <PanelCard title="设备在线状态" extra="实时巡检">
            <DashboardDeviceStatus :devices="dashboardStore.deviceStatusList" />
          </PanelCard>
          <DashboardChartPanel
            title="风险等级分布"
            extra="当前点位"
            :option="riskLevelOption"
            :height="220"
          />
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="analysis-row">
      <el-col :xs="24" :lg="12">
        <DashboardChartPanel
          title="区域风险热力分布"
          extra="重点区域排序"
          :option="areaRiskOption"
          :height="300"
        />
      </el-col>
      <el-col :xs="24" :lg="12">
        <DashboardChartPanel
          title="近7日告警趋势分析"
          extra="总量与高风险事件"
          :option="alertTrendOption"
          :height="300"
        />
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.content-row,
.analysis-row {
  margin-top: 16px;
}
</style>
