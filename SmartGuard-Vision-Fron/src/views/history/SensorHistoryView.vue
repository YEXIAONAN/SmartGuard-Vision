<script setup>
import { ElMessage } from 'element-plus'
import { computed, onMounted, reactive, ref } from 'vue'
import PanelCard from '../../components/common/PanelCard.vue'
import { dashboardApi } from '../../services/api'

const loading = ref(false)
const detailLoading = ref(false)
const drawerVisible = ref(false)
const records = ref([])
const detail = ref(null)
const filters = reactive({
  keyword: '',
  sensorType: '',
  riskLevel: '',
})

const payloadText = computed(() => JSON.stringify(detail.value?.payload || {}, null, 2))

const fetchRecords = async () => {
  loading.value = true
  try {
    records.value = await dashboardApi.getSensorRecords({
      keyword: filters.keyword,
      sensor_type: filters.sensorType,
      risk_level: filters.riskLevel,
      limit: 100,
    })
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '传感历史加载失败')
  } finally {
    loading.value = false
  }
}

const openDetail = async (row) => {
  drawerVisible.value = true
  detailLoading.value = true
  detail.value = null

  try {
    detail.value = await dashboardApi.getSensorRecordDetail(row.id)
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '传感记录详情加载失败')
  } finally {
    detailLoading.value = false
  }
}

const resetFilters = () => {
  filters.keyword = ''
  filters.sensorType = ''
  filters.riskLevel = ''
  void fetchRecords()
}

onMounted(() => {
  void fetchRecords()
})
</script>

<template>
  <div class="page-container">
    <PanelCard title="传感历史记录" extra="支持筛选和详情查看">
      <div class="toolbar">
        <el-input v-model="filters.keyword" clearable placeholder="搜索设备编码、位置或传感器类型" />
        <el-select v-model="filters.sensorType" clearable placeholder="传感器类型">
          <el-option label="温度传感器" value="temperature" />
          <el-option label="烟温传感器" value="smoke_temperature" />
        </el-select>
        <el-select v-model="filters.riskLevel" clearable placeholder="风险等级">
          <el-option label="高风险" value="high" />
          <el-option label="中风险" value="medium" />
          <el-option label="低风险" value="low" />
        </el-select>
        <el-button type="primary" @click="fetchRecords">查询</el-button>
        <el-button @click="resetFilters">重置</el-button>
      </div>

      <el-table v-loading="loading" :data="records" border class="history-table">
        <el-table-column prop="device_code" label="设备编码" min-width="120" />
        <el-table-column prop="location" label="监测位置" min-width="180" show-overflow-tooltip />
        <el-table-column prop="sensor_type" label="传感器类型" min-width="120" />
        <el-table-column prop="temperature" label="温度(℃)" min-width="100" />
        <el-table-column prop="humidity" label="湿度(%)" min-width="100" />
        <el-table-column prop="smoke_ppm" label="烟雾(ppm)" min-width="110" />
        <el-table-column prop="risk_level" label="风险等级" min-width="100" />
        <el-table-column prop="reported_at" label="上报时间" min-width="180" />
        <el-table-column label="操作" fixed="right" width="100">
          <template #default="{ row }">
            <el-button type="primary" link @click="openDetail(row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </PanelCard>

    <el-drawer v-model="drawerVisible" title="传感记录详情" size="40%">
      <div v-loading="detailLoading" class="detail-panel">
        <template v-if="detail">
          <div class="detail-grid">
            <div><strong>设备编码：</strong>{{ detail.device_code }}</div>
            <div><strong>传感器类型：</strong>{{ detail.sensor_type }}</div>
            <div><strong>风险等级：</strong>{{ detail.risk_level }}</div>
            <div><strong>上报时间：</strong>{{ detail.reported_at }}</div>
            <div><strong>温度：</strong>{{ detail.temperature ?? '--' }} ℃</div>
            <div><strong>湿度：</strong>{{ detail.humidity ?? '--' }} %</div>
            <div><strong>烟雾：</strong>{{ detail.smoke_ppm ?? '--' }} ppm</div>
            <div><strong>监测位置：</strong>{{ detail.location }}</div>
          </div>
          <PanelCard title="原始载荷" body-padding="16px">
            <pre class="payload-text">{{ payloadText }}</pre>
          </PanelCard>
        </template>
      </div>
    </el-drawer>
  </div>
</template>

<style scoped>
.toolbar {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr auto auto;
  gap: 12px;
  margin-bottom: 16px;
}

.history-table {
  width: 100%;
}

.detail-panel {
  min-height: 240px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 16px;
  padding: 14px;
  border: 1px solid var(--sg-border-light);
  border-radius: 12px;
  background: var(--sg-bg-soft);
}

.payload-text {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  color: var(--sg-text-main);
}

@media (max-width: 992px) {
  .toolbar {
    grid-template-columns: 1fr;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
