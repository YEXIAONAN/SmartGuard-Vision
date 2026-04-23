<script setup lang="ts">
defineProps<{
  title: string
  value: string | number
  subtitle: string
  type?: 'normal' | 'warning' | 'danger'
}>()
</script>

<template>
  <div class="stat-card" :class="type || 'normal'">
    <div class="title">{{ title }}</div>
    <div class="value">{{ value }}</div>
    <div class="subtitle">{{ subtitle }}</div>
  </div>
</template>

<style scoped lang="scss">
.stat-card {
  border-radius: 16px;
  padding: 12px 14px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.58);
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
  backdrop-filter: blur(16px);
  transition: all 0.2s ease;
  &:hover {
    transform: translateY(-2px);
  }
}

.title {
  font-size: 12px;
  color: #6e6e73;
}

.value {
  margin-top: 8px;
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 0.2px;
  color: #007aff;
}

.subtitle {
  margin-top: 8px;
  font-size: 12px;
  color: #6e6e73;
  border-top: 1px dashed rgba(197, 211, 229, 0.8);
  padding-top: 8px;
}

.warning .value {
  color: #ff9f0a;
}

.danger .value {
  color: #ff3b30;
}
</style>
