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
  eventType: '',
  riskLevel: '',
})

const payloadText = computed(() => JSON.stringify(detail.value?.payload || {}, null, 2))

const fetchRecords = async () => {
  loading.value = true
  try {
    records.value = await dashboardApi.getVisionRecords({
      keyword: filters.keyword,
      event_type: filters.eventType,
      risk_level: filters.riskLevel,
      limit: 100,
    })
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '视觉历史加载失败')
  } finally {
    loading.value = false
  }
}

const openDetail = async (row) => {
  drawerVisible.value = true
  detailLoading.value = true
  detail.value = null

  try {
    detail.value = await dashboardApi.getVisionRecordDetail(row.id)
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '视觉记录详情加载失败')
  } finally {
    detailLoading.value = false
  }
}

const resetFilters = () => {
  filters.keyword = ''
  filters.eventType = ''
  filters.riskLevel = ''
  void fetchRecords()
}

onMounted(() => {
  void fetchRecords()
})
</script>

<template>
  <div class="page-container">
    <PanelCard title="视觉识别历史" extra="支持筛选和详情查看">
      <div class="toolbar">
        <el-input v-model="filters.keyword" clearable placeholder="搜索设备编码、位置或事件类型" />
        <el-select v-model="filters.eventType" clearable placeholder="事件类型">
          <el-option label="飞线充电" value="飞线充电" />
          <el-option label="越线停放" value="越线停放" />
          <el-option label="明火" value="明火" />
          <el-option label="电池拆卸充电" value="电池拆卸充电" />
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
        <el-table-column prop="event_type" label="识别事件" min-width="120" />
        <el-table-column prop="risk_level" label="风险等级" min-width="100" />
        <el-table-column prop="confidence" label="置信度" min-width="90">
          <template #default="{ row }">{{ row.confidence ?? '--' }}</template>
        </el-table-column>
        <el-table-column prop="detected_count" label="检测数量" min-width="90" />
        <el-table-column prop="reported_at" label="上报时间" min-width="180" />
        <el-table-column label="操作" fixed="right" width="100">
          <template #default="{ row }">
            <el-button type="primary" link @click="openDetail(row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </PanelCard>

    <el-drawer v-model="drawerVisible" title="视觉记录详情" size="40%">
      <div v-loading="detailLoading" class="detail-panel">
        <template v-if="detail">
          <div class="detail-grid">
            <div><strong>设备编码：</strong>{{ detail.device_code }}</div>
            <div><strong>事件类型：</strong>{{ detail.event_type }}</div>
            <div><strong>风险等级：</strong>{{ detail.risk_level }}</div>
            <div><strong>检测数量：</strong>{{ detail.detected_count }}</div>
            <div><strong>监测位置：</strong>{{ detail.location }}</div>
            <div><strong>上报时间：</strong>{{ detail.reported_at }}</div>
          </div>
          <div v-if="detail.image_url" class="image-wrap">
            <img :src="detail.image_url" alt="视觉识别截图" />
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

.image-wrap {
  margin-bottom: 16px;
  overflow: hidden;
  border-radius: 12px;
}

.image-wrap img {
  width: 100%;
  display: block;
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
