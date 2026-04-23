<script setup>
import { ElMessage } from 'element-plus'
import { onMounted, reactive, ref } from 'vue'
import PanelCard from '../../components/common/PanelCard.vue'
import { auditApi } from '../../services/api'

const loading = ref(false)
const logs = ref([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})
const filters = reactive({
  username: '',
  action: '',
})

const fetchLogs = async () => {
  loading.value = true
  try {
    const data = await auditApi.getAuditLogs({
      page: pagination.page,
      page_size: pagination.pageSize,
      username: filters.username || undefined,
      action: filters.action || undefined,
    })
    logs.value = data.items
    pagination.total = data.total
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '审计日志加载失败')
  } finally {
    loading.value = false
  }
}

const onPageChanged = (nextPage) => {
  pagination.page = nextPage
  void fetchLogs()
}

const onPageSizeChanged = (nextSize) => {
  pagination.pageSize = nextSize
  pagination.page = 1
  void fetchLogs()
}

onMounted(fetchLogs)
</script>

<template>
  <div class="page-container">
    <PanelCard title="审计中心" extra="关键操作全量留痕">
      <div class="toolbar">
        <el-input v-model="filters.username" clearable placeholder="用户名" />
        <el-input v-model="filters.action" clearable placeholder="动作类型（如 auth.login）" />
        <el-button type="primary" @click="fetchLogs">查询</el-button>
      </div>

      <el-table v-loading="loading" :data="logs" border>
        <el-table-column prop="created_at" label="时间" min-width="170" />
        <el-table-column prop="username" label="用户" min-width="120" />
        <el-table-column prop="role" label="角色" min-width="100" />
        <el-table-column prop="action" label="动作" min-width="180" />
        <el-table-column prop="target_type" label="对象类型" min-width="120" />
        <el-table-column prop="target_id" label="对象ID" min-width="120" />
        <el-table-column prop="detail" label="详情" min-width="260" show-overflow-tooltip />
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
    </PanelCard>
  </div>
</template>

<style scoped>
.toolbar {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 12px;
  margin-bottom: 12px;
}

.pager-wrap {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 992px) {
  .toolbar {
    grid-template-columns: 1fr;
  }
}
</style>
