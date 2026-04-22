<script setup>
import { onMounted } from 'vue'
import PanelCard from '../../components/common/PanelCard.vue'
import { useRecordHistory } from '../../composables/useRecordHistory'
import { dashboardApi } from '../../services/api'

const history = useRecordHistory({
  listFetcher: dashboardApi.getVisionRecords,
  detailFetcher: dashboardApi.getVisionRecordDetail,
  optionsFetcher: dashboardApi.getVisionFilterOptions,
  initialFilters: {
    keyword: '',
    eventType: '',
    riskLevel: '',
  },
  requestMapper: (filters, page) => ({
    keyword: filters.keyword,
    event_type: filters.eventType,
    risk_level: filters.riskLevel,
    ...page,
  }),
  optionsMapper: (filters) => ({
    keyword: filters.keyword,
    event_type: filters.eventType,
    risk_level: filters.riskLevel,
  }),
  listErrorMessage: '视觉历史加载失败',
  detailErrorMessage: '视觉记录详情加载失败',
  optionsErrorMessage: '视觉筛选项加载失败',
})

onMounted(async () => {
  await history.reload({ syncOptions: true })
})
</script>

<template>
  <div class="page-container">
    <PanelCard title="视觉识别历史" extra="服务端分页与联动筛选">
      <div class="toolbar">
        <el-input
          v-model="history.filters.keyword"
          clearable
          placeholder="搜索设备编码、位置或事件类型"
          @change="history.onFilterChanged"
        />
        <el-select
          v-model="history.filters.eventType"
          clearable
          placeholder="事件类型"
          @change="history.onFilterChanged"
        >
          <el-option
            v-for="option in history.filterOptions.first"
            :key="option"
            :label="option"
            :value="option"
          />
        </el-select>
        <el-select
          v-model="history.filters.riskLevel"
          clearable
          placeholder="风险等级"
          @change="history.onFilterChanged"
        >
          <el-option
            v-for="option in history.filterOptions.risk"
            :key="option"
            :label="option"
            :value="option"
          />
        </el-select>
        <el-button type="primary" @click="history.reload({ syncOptions: true })">查询</el-button>
        <el-button @click="history.resetFilters">重置</el-button>
      </div>

      <el-table v-loading="history.loading" :data="history.records" border class="history-table">
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
            <el-button type="primary" link @click="history.openDetail(row.id)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pager-wrap">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :current-page="history.pagination.page"
          :page-size="history.pagination.pageSize"
          :total="history.pagination.total"
          :page-sizes="[10, 20, 50]"
          @current-change="history.onPageChanged"
          @size-change="history.onPageSizeChanged"
        />
      </div>
    </PanelCard>

    <el-drawer v-model="history.drawerVisible" title="视觉记录详情" size="40%">
      <div v-loading="history.detailLoading" class="detail-panel">
        <template v-if="history.detail">
          <div class="detail-grid">
            <div><strong>设备编码：</strong>{{ history.detail.device_code }}</div>
            <div><strong>事件类型：</strong>{{ history.detail.event_type }}</div>
            <div><strong>风险等级：</strong>{{ history.detail.risk_level }}</div>
            <div><strong>检测数量：</strong>{{ history.detail.detected_count }}</div>
            <div><strong>监测位置：</strong>{{ history.detail.location }}</div>
            <div><strong>上报时间：</strong>{{ history.detail.reported_at }}</div>
          </div>
          <div v-if="history.detail.image_url" class="image-wrap">
            <img :src="history.detail.image_url" alt="视觉识别截图" />
          </div>
          <PanelCard title="原始载荷" body-padding="16px">
            <pre class="payload-text">{{ history.payloadText }}</pre>
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

.pager-wrap {
  display: flex;
  justify-content: flex-end;
  margin-top: 14px;
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

  .pager-wrap {
    justify-content: center;
  }
}
</style>
