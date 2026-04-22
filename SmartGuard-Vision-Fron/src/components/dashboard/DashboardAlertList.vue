<script setup>
defineProps({
  alerts: {
    type: Array,
    default: () => [],
  },
  updatingAlertId: {
    type: Number,
    default: null,
  },
})

const emit = defineEmits(['handle-alert'])

const levelTypeMap = {
  high: 'danger',
  medium: 'warning',
  low: 'info',
  other: 'info',
}

const statusTypeMap = {
  pending: 'danger',
  processing: 'warning',
  resolved: 'success',
}

const openHandlingDialog = (alert, nextStatus) => {
  emit('handle-alert', { alert, nextStatus })
}
</script>

<template>
  <div v-if="alerts.length" class="alert-list">
    <div v-for="item in alerts" :key="item.id || `${item.time}-${item.place}`" class="alert-item">
      <div class="alert-top">
        <span class="alert-time">{{ item.time }}</span>
        <div class="alert-tags">
          <el-tag :type="levelTypeMap[item.levelKey] || 'info'" size="small" effect="plain">
            {{ item.level }}
          </el-tag>
          <el-tag :type="statusTypeMap[item.rawStatus] || 'info'" size="small" effect="light">
            {{ item.status }}
          </el-tag>
        </div>
      </div>
      <div class="alert-place">{{ item.place }}</div>
      <div class="alert-detail">{{ item.detail }}</div>
      <div v-if="item.handledBy || item.handledAt || item.handlingNote" class="alert-meta">
        <span v-if="item.handledBy">处理人：{{ item.handledBy }}</span>
        <span v-if="item.handledAt">处置时间：{{ item.handledAt }}</span>
        <span v-if="item.handlingNote">备注：{{ item.handlingNote }}</span>
      </div>
      <div v-if="item.rawStatus !== 'resolved'" class="alert-actions">
        <el-button
          v-if="item.rawStatus === 'pending'"
          size="small"
          type="warning"
          plain
          :loading="updatingAlertId === item.id"
          @click="openHandlingDialog(item, 'processing')"
        >
          转处理中
        </el-button>
        <el-button
          size="small"
          type="success"
          plain
          :loading="updatingAlertId === item.id"
          @click="openHandlingDialog(item, 'resolved')"
        >
          标记已处理
        </el-button>
      </div>
    </div>
  </div>
  <el-empty v-else description="暂无告警数据" />
</template>

<style scoped>
.alert-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alert-item {
  padding: 12px 14px;
  border: 1px solid var(--sg-border-light);
  border-radius: 12px;
  background: #f9fbfe;
}

.alert-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.alert-time {
  font-size: 12px;
  color: var(--sg-text-muted);
}

.alert-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.alert-place {
  margin-top: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #22364f;
}

.alert-detail {
  margin-top: 6px;
  font-size: 13px;
  line-height: 1.6;
  color: var(--sg-text-secondary);
}

.alert-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #dde7f2;
  font-size: 12px;
  color: var(--sg-text-secondary);
}

.alert-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 12px;
}
</style>
