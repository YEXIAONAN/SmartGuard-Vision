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
        <span>{{ item.name }}</span>
        <span>{{ item.online }}/{{ item.total }}</span>
      </div>
      <el-progress
        :percentage="item.rate"
        :stroke-width="10"
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
  gap: 14px;
}

.device-item {
  padding: 12px 14px;
  border: 1px solid var(--sg-border-light);
  border-radius: 12px;
  background: var(--sg-bg-soft);
}

.device-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 13px;
  color: #33485f;
}
</style>
