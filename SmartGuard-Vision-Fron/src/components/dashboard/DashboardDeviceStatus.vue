<script setup>
defineProps({
  devices: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div v-if="devices.length" class="device-list">
    <div v-for="item in devices" :key="item.name" class="device-item">
      <div class="device-top">
        <span class="name">{{ item.name }}</span>
        <span class="summary">{{ item.online }}/{{ item.total }}</span>
      </div>
      <el-progress
        :percentage="item.rate"
        :stroke-width="8"
        :show-text="false"
        color="var(--sg-color-primary)"
      />
    </div>
  </div>
  <el-empty v-else description="暂无设备状态数据" />
</template>

<style scoped>
.device-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.device-item {
  padding: 10px 12px;
  border: 1px solid var(--sg-border);
  border-radius: 8px;
  background: #ffffff;
}

.device-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.name {
  font-size: 13px;
  color: #2f435b;
}

.summary {
  font-size: 12px;
  color: var(--sg-text-muted);
}
</style>
