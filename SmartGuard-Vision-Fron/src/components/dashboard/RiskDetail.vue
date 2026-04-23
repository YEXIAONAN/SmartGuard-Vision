<script setup lang="ts">
import { computed } from 'vue'
import type { AlertDetail, AlertStatus } from '@/types/dashboard'
import AppEmpty from '@/components/common/AppEmpty.vue'

const props = defineProps<{
  detail: AlertDetail | null
  loading: boolean
}>()

const emit = defineEmits<{
  updateStatus: [status: AlertStatus]
}>()

const canStart = computed(() => props.detail?.status === 'pending')
const canResolve = computed(() => props.detail?.status !== 'resolved')

const statusLabelMap: Record<AlertStatus, string> = {
  pending: '未处理',
  processing: '处理中',
  resolved: '已完成',
}
</script>

<template>
  <div v-loading="loading" class="risk-detail">
    <template v-if="detail">
      <div class="base-info">
        <div class="row"><span>告警编码</span><strong>{{ detail.alertCode }}</strong></div>
        <div class="row"><span>告警标题</span><strong>{{ detail.title }}</strong></div>
        <div class="row"><span>告警位置</span><strong>{{ detail.location }}</strong></div>
        <div class="row"><span>风险等级</span><el-tag :type="detail.level === 'high' ? 'danger' : detail.level === 'medium' ? 'warning' : 'success'">{{ detail.level }}</el-tag></div>
        <div class="row"><span>处理状态</span><el-tag :type="detail.status === 'pending' ? 'danger' : detail.status === 'processing' ? 'warning' : 'success'">{{ statusLabelMap[detail.status] }}</el-tag></div>
        <div class="row"><span>风险描述</span><strong class="desc">{{ detail.description }}</strong></div>
      </div>

      <div class="action-bar">
        <el-button type="warning" :disabled="!canStart" @click="emit('updateStatus', 'processing')">开始处理</el-button>
        <el-button type="success" :disabled="!canResolve" @click="emit('updateStatus', 'resolved')">标记完成</el-button>
      </div>

      <el-timeline class="timeline">
        <el-timeline-item v-for="item in detail.timeline" :key="item.id" :timestamp="item.createdAt">
          <div class="timeline-title">{{ statusLabelMap[item.status] }} · {{ item.operator }}</div>
          <div class="timeline-remark">{{ item.remark }}</div>
        </el-timeline-item>
      </el-timeline>
    </template>
    <AppEmpty v-else description="请选择告警查看风险详情" />
  </div>
</template>

<style scoped lang="scss">
.risk-detail {
  min-height: 420px;
}

.base-info {
  display: grid;
  gap: 8px;
}

.row {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 8px;
  align-items: center;
  span {
    font-size: 12px;
    color: #6e6e73;
  }
  strong {
    font-size: 13px;
    color: #1d1d1f;
    line-height: 1.5;
    &.desc {
      font-weight: 500;
    }
  }
}

.action-bar {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

.timeline {
  margin-top: 12px;
}

.timeline-title {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
}

.timeline-remark {
  margin-top: 4px;
  font-size: 12px;
  color: #6e6e73;
}
</style>
