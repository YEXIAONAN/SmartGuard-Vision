<script setup>
import { ElMessage } from 'element-plus'
import { computed, onMounted, reactive, ref } from 'vue'
import PanelCard from '../../components/common/PanelCard.vue'
import DashboardAlertList from '../../components/dashboard/DashboardAlertList.vue'
import DashboardChartPanel from '../../components/dashboard/DashboardChartPanel.vue'
import DashboardDeviceStatus from '../../components/dashboard/DashboardDeviceStatus.vue'
import DashboardMonitor from '../../components/dashboard/DashboardMonitor.vue'
import DashboardStats from '../../components/dashboard/DashboardStats.vue'
import { dashboardApi } from '../../services/api'
import { useAuthStore } from '../../stores/auth'
import { useDashboardStore } from '../../stores/dashboard'
import {
  createAlertTrendOption,
  createAreaRiskOption,
  createParkingRecognitionOption,
  createRiskLevelOption,
  createRiskTrendOption,
} from './chart-options'

const dashboardStore = useDashboardStore()
const authStore = useAuthStore()

const handlingDialogVisible = ref(false)
const handlingTarget = ref(null)
const actionLogsLoading = ref(false)
const actionLogs = ref([])
const handlingFormRef = ref(null)
const handlingForm = reactive({
  status: 'processing',
  handledBy: '',
  handlingNote: '',
})

const formRules = {
  handledBy: [
    { required: true, message: '处理人不能为空', trigger: 'blur' },
    { min: 2, max: 32, message: '处理人长度需在 2-32 个字符之间', trigger: 'blur' },
  ],
  handlingNote: [
    { required: true, message: '处理备注不能为空', trigger: 'blur' },
    { min: 5, max: 300, message: '处理备注长度需在 5-300 个字符之间', trigger: 'blur' },
  ],
}

const riskTrendOption = computed(() => createRiskTrendOption(dashboardStore.riskTrend))
const eventDistributionOption = computed(() =>
  createParkingRecognitionOption(dashboardStore.eventDistribution),
)
const riskLevelOption = computed(() => createRiskLevelOption(dashboardStore.riskLevel))
const areaRiskOption = computed(() => createAreaRiskOption(dashboardStore.areaRisk))
const alertTrendOption = computed(() => createAlertTrendOption(dashboardStore.alertTrend))
const currentAlert = computed(() => dashboardStore.alerts[0] || null)
const riskTagClass = (levelKey) =>
  `sg-status-tag-risk-${['high', 'medium', 'low'].includes(levelKey) ? levelKey : 'low'}`
const stateTagClass = (statusKey) =>
  `sg-status-tag-state-${['pending', 'processing', 'resolved'].includes(statusKey) ? statusKey : 'pending'}`

const loadActionLogs = async (alertId) => {
  actionLogsLoading.value = true
  actionLogs.value = []
  try {
    const logs = await dashboardApi.getAlertActions(alertId)
    actionLogs.value = logs
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '处置审计日志加载失败')
  } finally {
    actionLogsLoading.value = false
  }
}

const openHandlingDialog = async ({ alert, nextStatus }) => {
  if (!authStore.canHandleAlerts) return

  handlingTarget.value = alert
  handlingForm.status = nextStatus
  handlingForm.handledBy = alert.handledBy || ''
  handlingForm.handlingNote = alert.handlingNote || ''
  handlingDialogVisible.value = true
  await loadActionLogs(alert.id)
}

const closeHandlingDialog = () => {
  handlingDialogVisible.value = false
  handlingTarget.value = null
  handlingForm.status = 'processing'
  handlingForm.handledBy = ''
  handlingForm.handlingNote = ''
  actionLogs.value = []
  handlingFormRef.value?.clearValidate?.()
}

const submitAlertHandling = async () => {
  if (!handlingTarget.value || !handlingFormRef.value) return

  const valid = await handlingFormRef.value.validate().catch(() => false)
  if (!valid) return

  const success = await dashboardStore.updateAlertStatus(handlingTarget.value.id, {
    status: handlingForm.status,
    handled_by: handlingForm.handledBy,
    handling_note: handlingForm.handlingNote,
  })
  if (!success) return

  ElMessage.success(handlingForm.status === 'processing' ? '告警已转入处理中' : '告警已标记为已处理')
  closeHandlingDialog()
}

const runSlaScan = async () => {
  try {
    const result = await dashboardApi.scanAlertSla()
    ElMessage.success(`SLA扫描完成，自动升级 ${result.escalated_count} 条告警`)
    await dashboardStore.fetchDashboard({ silent: true })
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : 'SLA 扫描失败')
  }
}

const downloadAlertsCsv = async () => {
  try {
    const blob = await dashboardApi.exportAlertsCsv()
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = 'alerts.csv'
    document.body.appendChild(anchor)
    anchor.click()
    anchor.remove()
    URL.revokeObjectURL(url)
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '导出失败')
  }
}

onMounted(() => {
  if (!dashboardStore.initialized) {
    void dashboardStore.fetchDashboard()
  }
})
</script>

<template>
  <div
    v-loading="dashboardStore.loading && !dashboardStore.initialized"
    class="page-container dashboard-page"
    element-loading-text="正在同步平台态势数据..."
  >
    <el-alert
      v-if="dashboardStore.error"
      class="sync-alert"
      title="态势数据同步失败"
      :description="dashboardStore.error"
      type="warning"
      :closable="false"
      show-icon
    />

    <section class="dashboard-layer">
      <div class="ops-bar">
        <el-button link type="primary" @click="downloadAlertsCsv">导出告警 CSV</el-button>
        <el-button v-if="authStore.canHandleAlerts" size="small" @click="runSlaScan">执行 SLA 扫描</el-button>
      </div>
      <DashboardStats :stats="dashboardStore.stats" />
    </section>

    <section class="dashboard-layer risk-center">
      <div class="risk-main">
        <PanelCard
          :title="dashboardStore.monitor.title || '实时风险联动画面'"
          :extra="dashboardStore.monitor.channel || '实时识别通道'"
        >
          <DashboardMonitor :monitor="dashboardStore.monitor" />
        </PanelCard>
      </div>

      <div class="risk-side">
        <PanelCard title="当前风险详情" extra="联动处置状态">
          <div v-if="currentAlert" class="risk-detail">
            <div class="risk-detail-row">
              <span class="risk-label">告警时间</span>
              <span class="risk-value">{{ currentAlert.time }}</span>
            </div>
            <div class="risk-detail-row">
              <span class="risk-label">监测点位</span>
              <span class="risk-value">{{ currentAlert.place }}</span>
            </div>
            <div class="risk-detail-row">
              <span class="risk-label">风险等级</span>
              <span class="sg-status-tag" :class="riskTagClass(currentAlert.levelKey)">
                {{ currentAlert.level }}
              </span>
            </div>
            <div class="risk-detail-row">
              <span class="risk-label">处理状态</span>
              <span class="sg-status-tag" :class="stateTagClass(currentAlert.rawStatus)">
                {{ currentAlert.status }}
              </span>
            </div>
            <div class="risk-detail-row">
              <span class="risk-label">风险描述</span>
              <span class="risk-value">{{ currentAlert.detail }}</span>
            </div>
            <div class="risk-detail-row">
              <span class="risk-label">处理人</span>
              <span class="risk-value">{{ currentAlert.handledBy || '--' }}</span>
            </div>
            <div class="risk-detail-row">
              <span class="risk-label">处置时间</span>
              <span class="risk-value">{{ currentAlert.handledAt || '--' }}</span>
            </div>
            <div class="risk-detail-row">
              <span class="risk-label">处理备注</span>
              <span class="risk-value">{{ currentAlert.handlingNote || '--' }}</span>
            </div>
          </div>
          <el-empty v-else description="暂无实时风险事件" />
        </PanelCard>

        <PanelCard title="实时告警列表" extra="支持联动处置">
          <DashboardAlertList
            :alerts="dashboardStore.alerts"
            :updating-alert-id="dashboardStore.updatingAlertId"
            :can-handle="authStore.canHandleAlerts"
            @handle-alert="openHandlingDialog"
          />
        </PanelCard>
      </div>
    </section>

    <section class="dashboard-layer trend-center">
      <div class="trend-main">
        <el-row :gutter="14">
          <el-col :xs="24" :xl="12">
            <DashboardChartPanel
              title="近 7 日告警走势"
              extra="总量变化"
              :option="riskTrendOption"
              :height="270"
            />
          </el-col>
          <el-col :xs="24" :xl="12">
            <DashboardChartPanel
              title="风险等级分布"
              extra="当前告警组成"
              :option="riskLevelOption"
              :height="270"
            />
          </el-col>
        </el-row>

        <el-row :gutter="14" class="trend-row">
          <el-col :xs="24" :xl="12">
            <DashboardChartPanel
              title="区域风险热力排行"
              extra="重点区域排查"
              :option="areaRiskOption"
              :height="286"
            />
          </el-col>
          <el-col :xs="24" :xl="12">
            <DashboardChartPanel
              title="告警总量与高风险对比"
              extra="辅助研判"
              :option="alertTrendOption"
              :height="286"
            />
          </el-col>
        </el-row>
      </div>

      <div class="trend-side">
        <DashboardChartPanel
          title="感知事件分类统计"
          extra="识别来源分布"
          :option="eventDistributionOption"
          :height="260"
        />
        <PanelCard title="设备在线状态" extra="按设备类型统计">
          <DashboardDeviceStatus :devices="dashboardStore.deviceStatusList" />
        </PanelCard>
      </div>
    </section>

    <el-dialog
      v-model="handlingDialogVisible"
      :title="handlingForm.status === 'processing' ? '转入处理中' : '标记为已处理'"
      width="620px"
      @closed="closeHandlingDialog"
    >
      <el-form ref="handlingFormRef" :model="handlingForm" :rules="formRules" label-width="88px">
        <el-form-item label="告警位置">
          <div>{{ handlingTarget?.place || '--' }}</div>
        </el-form-item>
        <el-form-item label="处理人" prop="handledBy">
          <el-input v-model="handlingForm.handledBy" placeholder="请输入处理人姓名或岗位" />
        </el-form-item>
        <el-form-item label="处理备注" prop="handlingNote">
          <el-input
            v-model="handlingForm.handlingNote"
            type="textarea"
            :rows="4"
            placeholder="请输入联动处置说明、巡检结果或现场反馈"
          />
        </el-form-item>
      </el-form>

      <div class="audit-log-block">
        <div class="audit-log-title">操作审计列表</div>
        <el-skeleton v-if="actionLogsLoading" :rows="3" animated />
        <el-empty v-else-if="!actionLogs.length" description="暂无审计记录" />
        <el-timeline v-else>
          <el-timeline-item
            v-for="log in actionLogs"
            :key="log.id"
            :timestamp="log.created_at"
            placement="top"
          >
            <div class="audit-log-item">
              <div>状态：{{ log.from_status || '--' }} -> {{ log.to_status || '--' }}</div>
              <div>处理人：{{ log.handled_by || '--' }}</div>
              <div>备注：{{ log.handling_note || '--' }}</div>
            </div>
          </el-timeline-item>
        </el-timeline>
      </div>

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
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sync-alert {
  margin-bottom: 0;
}

.ops-bar {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
}

.risk-center {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(420px, 1fr);
  gap: 12px;
  align-items: start;
}

.risk-side {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.risk-detail {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.risk-detail-row {
  display: grid;
  grid-template-columns: 70px 1fr;
  gap: 8px;
  align-items: start;
}

.risk-label {
  font-size: 12px;
  color: var(--sg-text-muted);
}

.risk-value {
  font-size: 13px;
  line-height: 1.5;
  color: var(--sg-text-main);
}

.trend-center {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(360px, 1fr);
  gap: 12px;
}

.trend-row {
  margin-top: 12px;
}

.trend-side {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.audit-log-block {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e7edf5;
}

.audit-log-title {
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--sg-text-main);
}

.audit-log-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  color: var(--sg-text-secondary);
}

@media (min-width: 1800px) {
  .risk-center,
  .trend-center {
    grid-template-columns: minmax(0, 1.45fr) minmax(460px, 1fr);
  }
}

@media (max-width: 1400px) {
  .risk-center,
  .trend-center {
    grid-template-columns: 1fr;
  }
}
</style>
