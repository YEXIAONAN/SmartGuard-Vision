<script setup>
defineProps({
  stats: {
    type: Array,
    default: () => [],
  },
})

const toneClassMap = {
  neutral: 'stat-tone-neutral',
  warning: 'stat-tone-warning',
  danger: 'stat-tone-danger',
}
</script>

<template>
  <div class="stats-block">
    <div
      v-for="item in stats"
      :key="item.title"
      class="stat-card"
      :class="[item.size === 'key' ? 'stat-card-key' : 'stat-card-normal', toneClassMap[item.tone] || 'stat-tone-neutral']"
    >
      <div class="stat-title">{{ item.title }}</div>
      <div class="stat-value-wrap">
        <span class="stat-value">{{ item.value }}</span>
        <span class="stat-unit">{{ item.unit }}</span>
      </div>
      <div class="stat-note">{{ item.note }}</div>
    </div>
  </div>
</template>

<style scoped>
.stats-block {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 10px;
}

.stat-card {
  min-height: 126px;
  padding: 12px 14px;
  border: 1px solid var(--sg-border);
  border-radius: 16px;
  background: var(--sg-bg-card);
  box-shadow: var(--sg-shadow-soft);
  backdrop-filter: var(--sg-blur-xl);
  -webkit-backdrop-filter: var(--sg-blur-xl);
  transition: all 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.68);
}

.stat-card-key {
  grid-column: span 2;
  border-color: rgba(255, 255, 255, 0.6);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.72) 0%, rgba(238, 246, 255, 0.72) 100%);
}

.stat-card-normal {
  grid-column: span 1;
}

.stat-title {
  font-size: 13px;
  font-weight: 600;
  color: #3a3a3c;
}

.stat-value-wrap {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-top: 10px;
}

.stat-value {
  font-size: 32px;
  line-height: 1;
  font-weight: 700;
}

.stat-unit {
  font-size: 12px;
  color: var(--sg-text-muted);
}

.stat-note {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed rgba(196, 212, 229, 0.8);
  font-size: 12px;
  line-height: 1.6;
  color: var(--sg-text-secondary);
}

.stat-tone-neutral .stat-value {
  color: #007aff;
}

.stat-tone-warning .stat-value {
  color: #ff9f0a;
}

.stat-tone-danger .stat-value {
  color: #ff3b30;
}

@media (max-width: 1366px) {
  .stat-card-key {
    grid-column: span 1;
  }
}

@media (max-width: 992px) {
  .stats-block {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  }
}
</style>
