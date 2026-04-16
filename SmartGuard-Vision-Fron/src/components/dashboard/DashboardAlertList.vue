<script setup>
defineProps({
  alerts: {
    type: Array,
    default: () => [],
  },
})

const levelTypeMap = {
  高风险: 'danger',
  中风险: 'warning',
  一般: 'info',
}
</script>

<template>
  <div class="alert-list">
    <div v-for="item in alerts" :key="`${item.time}-${item.place}`" class="alert-item">
      <div class="alert-top">
        <span class="alert-time">{{ item.time }}</span>
        <el-tag :type="levelTypeMap[item.level] || 'info'" size="small" effect="plain">
          {{ item.level }}
        </el-tag>
      </div>
      <div class="alert-place">{{ item.place }}</div>
      <div class="alert-detail">{{ item.detail }}</div>
    </div>
  </div>
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
</style>
