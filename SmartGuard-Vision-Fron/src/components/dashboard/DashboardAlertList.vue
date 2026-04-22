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

const riskClassMap = {
  high: 'sg-status-tag-risk-high',
  medium: 'sg-status-tag-risk-medium',
  low: 'sg-status-tag-risk-low',
  other: 'sg-status-tag-risk-low',
}

const statusClassMap = {
  pending: 'sg-status-tag-state-pending',
  processing: 'sg-status-tag-state-processing',
  resolved: 'sg-status-tag-state-resolved',
}

const openHandlingDialog = (alert, nextStatus) => {
  emit('handle-alert', { alert, nextStatus })
}
</script>

<template>
  <div class="alert-box">
    <div v-if="alerts.length" class="alert-list">
      <article v-for="item in alerts" :key="item.id || `${item.time}-${item.place}`" class="alert-item">
        <header class="alert-head">
          <span class="alert-time">{{ item.time }}</span>
          <div class="alert-tags">
            <span class="sg-status-tag" :class="riskClassMap[item.levelKey]">{{ item.level }}</span>
            <span class="sg-status-tag" :class="statusClassMap[item.rawStatus]">{{ item.status }}</span>
          </div>
        </header>

        <div class="alert-row">
          <span class="label">监测点位</span>
          <span class="value">{{ item.place }}</span>
        </div>
        <div class="alert-row">
          <span class="label">告警说明</span>
          <span class="value">{{ item.detail }}</span>
        </div>
        <div v-if="item.handledBy || item.handledAt || item.handlingNote" class="alert-row">
          <span class="label">处置记录</span>
          <span class="value">
            <template v-if="item.handledBy">处理人：{{ item.handledBy }}；</template>
            <template v-if="item.handledAt">时间：{{ item.handledAt }}；</template>
            <template v-if="item.handlingNote">备注：{{ item.handlingNote }}</template>
          </span>
        </div>

        <footer v-if="item.rawStatus !== 'resolved'" class="alert-actions">
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
        </footer>
      </article>
    </div>
    <el-empty v-else description="暂无实时告警" />
  </div>
</template>

<style scoped>
.alert-box {
  max-height: 630px;
  overflow: auto;
  padding-right: 4px;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.alert-item {
  padding: 10px 12px;
  border: 1px solid var(--sg-border);
  border-radius: 8px;
  background: #ffffff;
}

.alert-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.alert-time {
  font-size: 12px;
  color: var(--sg-text-muted);
}

.alert-tags {
  display: flex;
  gap: 6px;
}

.alert-row {
  margin-top: 6px;
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 8px;
}

.label {
  font-size: 12px;
  color: var(--sg-text-muted);
}

.value {
  font-size: 13px;
  line-height: 1.45;
  color: var(--sg-text-main);
}

.alert-actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
