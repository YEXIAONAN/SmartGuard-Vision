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
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 12px;
}

.stat-card {
  padding: 14px 16px;
  border: 1px solid var(--sg-border);
  border-radius: 10px;
  background: var(--sg-bg-card);
  box-shadow: var(--sg-shadow-soft);
}

.stat-card-key {
  grid-column: span 3;
}

.stat-card-normal {
  grid-column: span 2;
}

.stat-title {
  font-size: 13px;
  font-weight: 600;
  color: #33485d;
}

.stat-value-wrap {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-top: 10px;
}

.stat-value {
  font-size: 30px;
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
  border-top: 1px dashed #dbe4ee;
  font-size: 12px;
  line-height: 1.6;
  color: var(--sg-text-secondary);
}

.stat-tone-neutral .stat-value {
  color: #2b4a74;
}

.stat-tone-warning .stat-value {
  color: #9b6b2c;
}

.stat-tone-danger .stat-value {
  color: #9f3e3e;
}

@media (max-width: 1366px) {
  .stat-card-key {
    grid-column: span 4;
  }

  .stat-card-normal {
    grid-column: span 4;
  }
}

@media (max-width: 992px) {
  .stat-card-key,
  .stat-card-normal {
    grid-column: span 6;
  }
}

@media (max-width: 640px) {
  .stat-card-key,
  .stat-card-normal {
    grid-column: span 12;
  }
}
</style>
