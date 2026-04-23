<script setup lang="ts">
defineProps<{
  title?: string
  extra?: string
}>()
</script>

<template>
  <section class="app-card">
    <header v-if="title || extra" class="app-card-header">
      <h3 class="app-card-title">{{ title }}</h3>
      <span v-if="extra" class="app-card-extra">{{ extra }}</span>
    </header>
    <div class="app-card-body">
      <slot />
    </div>
  </section>
</template>

<style scoped lang="scss">
.app-card {
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.42);
  background: rgba(255, 255, 255, 0.58);
  box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(20px);
}

.app-card-header {
  padding: 12px 14px 10px;
  border-bottom: 1px solid rgba(226, 236, 248, 0.76);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.app-card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: #1d1d1f;
}

.app-card-extra {
  font-size: 12px;
  color: #6e6e73;
}

.app-card-body {
  padding: 14px;
}
</style>
