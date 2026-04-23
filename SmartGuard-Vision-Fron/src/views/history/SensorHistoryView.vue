<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import AppShell from '@/components/dashboard/AppShell.vue'
import AppCard from '@/components/common/AppCard.vue'
import { dashboardApi } from '@/services/api'

interface SensorRecord {
  id: number
  device_code: string
  location: string
  sensor_type: string
  temperature?: number
  humidity?: number
  smoke_ppm?: number
  risk_level: string
  reported_at: string
}

const loading = ref(false)
const drawerVisible = ref(false)
const detailLoading = ref(false)
const records = ref<SensorRecord[]>([])
const detail = ref<Record<string, any> | null>(null)

const filterOptions = reactive({
  sensorTypes: [] as string[],
  riskLevels: [] as string[],
})

const filters = reactive({
  keyword: '',
  sensorType: '',
  riskLevel: '',
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

const payloadText = () => JSON.stringify(detail.value?.payload || {}, null, 2)

const fetchFilterOptions = async () => {
  const data = await dashboardApi.getSensorFilterOptions({
    keyword: filters.keyword || undefined,
    sensor_type: filters.sensorType || undefined,
    risk_level: filters.riskLevel || undefined,
  })
  filterOptions.sensorTypes = data.first || []
  filterOptions.riskLevels = data.risk || []
}

const fetchRecords = async () => {
  loading.value = true
  try {
    const data = await dashboardApi.getSensorRecords({
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: filters.keyword || undefined,
      sensor_type: filters.sensorType || undefined,
      risk_level: filters.riskLevel || undefined,
    })
    records.value = data.items || []
    pagination.total = data.total || 0
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '传感历史加载失败')
    records.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

const reloadData = async () => {
  try {
    await Promise.all([fetchFilterOptions(), fetchRecords()])
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '筛选项加载失败')
  }
}

const onSearch = async () => {
  pagination.page = 1
  await reloadData()
}

const onReset = async () => {
  filters.keyword = ''
  filters.sensorType = ''
  filters.riskLevel = ''
  pagination.page = 1
  await reloadData()
}

const onPageChanged = async (page: number) => {
  pagination.page = page
  await fetchRecords()
}

const onPageSizeChanged = async (pageSize: number) => {
  pagination.pageSize = pageSize
  pagination.page = 1
  await fetchRecords()
}

const openDetail = async (recordId: number) => {
  drawerVisible.value = true
  detailLoading.value = true
  detail.value = null
  try {
    detail.value = await dashboardApi.getSensorRecordDetail(recordId)
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '记录详情加载失败')
  } finally {
    detailLoading.value = false
  }
}

onMounted(async () => {
  await reloadData()
})
</script>

<template>
  <AppShell @refresh="reloadData">
    <AppCard title="传感历史" extra="服务端分页 + 条件联动筛选">
      <div class="toolbar">
        <el-input
          v-model="filters.keyword"
          clearable
          placeholder="搜索设备编码、位置或传感器类型"
          @keyup.enter="onSearch"
        />
        <el-select v-model="filters.sensorType" clearable placeholder="传感器类型">
          <el-option
            v-for="option in filterOptions.sensorTypes"
            :key="option"
            :label="option"
            :value="option"
          />
        </el-select>
        <el-select v-model="filters.riskLevel" clearable placeholder="风险等级">
          <el-option
            v-for="option in filterOptions.riskLevels"
            :key="option"
            :label="option"
            :value="option"
          />
        </el-select>
        <el-button type="primary" @click="onSearch">查询</el-button>
        <el-button @click="onReset">重置</el-button>
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
            <el-button type="primary" link @click="openDetail(row.id)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pager-wrap">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :current-page="pagination.page"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50]"
          @current-change="onPageChanged"
          @size-change="onPageSizeChanged"
        />
      </div>
    </AppCard>

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
          <AppCard title="原始载荷">
            <pre class="payload-text">{{ payloadText() }}</pre>
          </AppCard>
        </template>
      </div>
    </el-drawer>
  </AppShell>
</template>

<style scoped lang="scss">
.toolbar {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr auto auto;
  gap: 12px;
  margin-bottom: 14px;
}

.history-table {
  width: 100%;
}

.pager-wrap {
  display: flex;
  justify-content: flex-end;
  margin-top: 14px;
}

.detail-panel {
  min-height: 260px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 16px;
  padding: 14px;
  border-radius: 14px;
  border: 1px solid rgba(226, 236, 248, 0.8);
  background: rgba(255, 255, 255, 0.6);
}

.payload-text {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  color: #1d1d1f;
}

@media (max-width: 992px) {
  .toolbar {
    grid-template-columns: 1fr;
  }

  .pager-wrap {
    justify-content: center;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
