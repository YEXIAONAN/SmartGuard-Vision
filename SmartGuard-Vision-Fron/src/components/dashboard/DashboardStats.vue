<script setup>
defineProps({
  stats: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <el-row :gutter="16" class="stats-row">
    <el-col v-for="item in stats" :key="item.title" :xs="24" :sm="12" :lg="6">
      <div class="stat-card">
        <div class="stat-title">{{ item.title }}</div>
        <div class="stat-value-wrap">
          <span class="stat-value">{{ item.value }}</span>
          <span class="stat-unit">{{ item.unit }}</span>
        </div>
        <div class="stat-note">{{ item.note }}</div>
      </div>
    </el-col>
  </el-row>
</template>

<style scoped>
.stats-row {
  margin-top: 16px;
}

.stat-card {
  height: 100%;
  padding: 18px;
  border: 1px solid var(--sg-border);
  border-radius: var(--sg-radius-card);
  background: var(--sg-bg-card);
  box-shadow: var(--sg-shadow-soft);
}

.stat-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--sg-text-main);
}

.stat-value-wrap {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  margin-top: 18px;
}

.stat-value {
  font-size: 34px;
  line-height: 1;
  font-weight: 700;
  color: #2458bf;
}

.stat-unit {
  margin-bottom: 4px;
  font-size: 14px;
  color: var(--sg-text-muted);
}

.stat-note {
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid #e8eef5;
  font-size: 13px;
  line-height: 1.6;
  color: var(--sg-text-secondary);
}
</style>
