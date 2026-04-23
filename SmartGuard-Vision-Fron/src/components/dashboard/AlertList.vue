<script setup lang="ts">
import type { Alert } from '@/types/dashboard'
import AppEmpty from '@/components/common/AppEmpty.vue'

const props = defineProps<{
  alerts: Alert[]
  selectedAlertId: string | null
}>()

const emit = defineEmits<{
  select: [alertId: string]
}>()

const levelTypeMap = {
  low: 'success',
  medium: 'warning',
  high: 'danger',
} as const

const statusTypeMap = {
  pending: 'danger',
  processing: 'warning',
  resolved: 'success',
} as const

const statusLabelMap = {
  pending: '未处理',
  processing: '处理中',
  resolved: '已完成',
} as const
</script>

<template>
  <div class="alert-list">
    <template v-if="props.alerts.length">
      <article
        v-for="item in props.alerts"
        :key="item.id"
        class="alert-item"
        :class="{ active: item.id === props.selectedAlertId }"
        @click="emit('select', item.id)"
      >
        <header>
          <strong>{{ item.title }}</strong>
          <span class="time">{{ item.createdAt }}</span>
        </header>
        <div class="meta">{{ item.location }}</div>
        <div class="tag-row">
          <el-tag size="small" :type="levelTypeMap[item.level]">{{ item.level }}</el-tag>
          <el-tag size="small" effect="plain" :type="statusTypeMap[item.status]">
            {{ statusLabelMap[item.status] }}
          </el-tag>
        </div>
      </article>
    </template>
    <AppEmpty v-else description="暂无告警记录" />
  </div>
</template>

<style scoped lang="scss">
.alert-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 420px;
  overflow: auto;
  padding-right: 4px;
}

.alert-item {
  padding: 10px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.55);
  cursor: pointer;
  transition: all 0.2s ease;
  &:hover {
    transform: translateY(-1px);
    background: rgba(255, 255, 255, 0.74);
  }
  &.active {
    border-color: rgba(0, 122, 255, 0.55);
    box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.16);
    background: rgba(235, 245, 255, 0.82);
  }
  header {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    strong {
      font-size: 14px;
      color: #1d1d1f;
    }
    .time {
      font-size: 12px;
      color: #6e6e73;
      white-space: nowrap;
    }
  }
}

.meta {
  margin-top: 6px;
  font-size: 12px;
  color: #6e6e73;
}

.tag-row {
  margin-top: 8px;
  display: flex;
  gap: 6px;
}
</style>
