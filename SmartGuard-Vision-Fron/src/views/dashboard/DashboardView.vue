<script setup>
import { ElMessage } from 'element-plus'
import { computed, reactive, ref, onBeforeUnmount, onMounted } from 'vue'
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

const handlingDialogVisible = ref(false)
const handlingTarget = ref(null)
const handlingForm = reactive({
  status: 'processing',
  handledBy: '',
  handlingNote: '',
})

const riskTrendOption = computed(() => createRiskTrendOption(dashboardStore.riskTrend))
const eventDistributionOption = computed(() =>
  createParkingRecognitionOption(dashboardStore.eventDistribution),
)
const riskLevelOption = computed(() => createRiskLevelOption(dashboardStore.riskLevel))
const areaRiskOption = computed(() => createAreaRiskOption(dashboardStore.areaRisk))
const alertTrendOption = computed(() => createAlertTrendOption(dashboardStore.alertTrend))

const openHandlingDialog = ({ alert, nextStatus }) => {
  handlingTarget.value = alert
  handlingForm.status = nextStatus
  handlingForm.handledBy = alert.handledBy || ''
  handlingForm.handlingNote = alert.handlingNote || ''
  handlingDialogVisible.value = true
}

const closeHandlingDialog = () => {
  handlingDialogVisible.value = false
  handlingTarget.value = null
  handlingForm.status = 'processing'
  handlingForm.handledBy = ''
  handlingForm.handlingNote = ''
}

const submitAlertHandling = async () => {
  if (!handlingTarget.value) return
  if (!handlingForm.handledBy.trim()) {
    ElMessage.warning('请填写处理人')
    return
  }

  const success = await dashboardStore.updateAlertStatus(handlingTarget.value.id, {
    status: handlingForm.status,
    handled_by: handlingForm.handledBy,
    handling_note: handlingForm.handlingNote,
  })

  if (!success) return

  ElMessage.success(handlingForm.status === 'processing' ? '告警已转入处理中' : '告警已标记为已处理')
  closeHandlingDialog()
}

onMounted(() => {
  dashboardStore.startAutoRefresh()
})

onBeforeUnmount(() => {
  dashboardStore.stopAutoRefresh()
})
</script>

<template>
  <div
    v-loading="dashboardStore.loading && !dashboardStore.initialized"
    class="page-container dashboard-page"
    element-loading-text="正在同步大屏数据..."
  >
    <el-alert
      v-if="dashboardStore.error"
      class="sync-alert"
      title="大屏数据同步失败"
      :description="dashboardStore.error"
      type="warning"
      :closable="false"
      show-icon
    />

    <PanelCard body-padding="18px 22px">
      <DashboardHeader
        :project-name="dashboardStore.project.name"
        :subtitle="dashboardStore.project.subtitle"
        :current-time="currentTime"
        :generated-at="dashboardStore.generatedAt"
        :system-status="dashboardStore.systemStatus"
        :online-summary="dashboardStore.onlineSummary"
      />
    </PanelCard>

    <DashboardStats :stats="dashboardStore.stats" />

    <el-row :gutter="16" class="content-row">
      <el-col :xs="24" :lg="6">
        <div class="stack-column">
          <DashboardChartPanel
            title="告警趋势图"
            extra="近 7 天"
            :option="riskTrendOption"
            :height="250"
          />
          <DashboardChartPanel
            title="风险事件分布"
            extra="按事件类型统计"
            :option="eventDistributionOption"
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
          <PanelCard title="实时告警列表" extra="支持联动处置">
            <DashboardAlertList
              :alerts="dashboardStore.alerts"
              :updating-alert-id="dashboardStore.updatingAlertId"
              @handle-alert="openHandlingDialog"
            />
          </PanelCard>
          <PanelCard title="设备在线状态" extra="按设备类型统计">
            <DashboardDeviceStatus :devices="dashboardStore.deviceStatusList" />
          </PanelCard>
          <DashboardChartPanel
            title="风险等级分布"
            extra="当前告警数据"
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
          title="告警趋势分析"
          extra="总量与高风险事件"
          :option="alertTrendOption"
          :height="300"
        />
      </el-col>
    </el-row>

    <el-dialog
      v-model="handlingDialogVisible"
      :title="handlingForm.status === 'processing' ? '转入处理中' : '标记已处理'"
      width="520px"
      @closed="closeHandlingDialog"
    >
      <el-form label-width="88px">
        <el-form-item label="告警位置">
          <div>{{ handlingTarget?.place || '--' }}</div>
        </el-form-item>
        <el-form-item label="处理人" required>
          <el-input v-model="handlingForm.handledBy" placeholder="请输入处理人姓名或岗位" />
        </el-form-item>
        <el-form-item label="处理备注">
          <el-input
            v-model="handlingForm.handlingNote"
            type="textarea"
            :rows="4"
            placeholder="请输入联动处置说明、巡检结果或现场反馈"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="closeHandlingDialog">取消</el-button>
        <el-button
          type="primary"
          :loading="dashboardStore.updatingAlertId === handlingTarget?.id"
          @click="submitAlertHandling"
        >
          确认提交
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.content-row,
.analysis-row {
  margin-top: 16px;
}

.sync-alert {
  margin-bottom: 16px;
}
</style>
