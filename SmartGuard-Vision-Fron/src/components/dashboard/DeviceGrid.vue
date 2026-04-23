<script setup lang="ts">
import type { Device } from '@/types/dashboard'

defineProps<{
  devices: Device[]
  selectedDeviceId: string | null
}>()

const statusMap = {
  online: '在线',
  offline: '离线',
  warning: '告警',
}
</script>

<template>
  <div class="device-grid">
    <article
      v-for="item in devices"
      :key="item.id"
      class="device-card"
      :class="[item.status, { active: selectedDeviceId === item.id }]"
    >
      <header class="card-head">
        <h4>{{ item.name }}</h4>
        <el-tag
          :type="item.status === 'online' ? 'success' : item.status === 'offline' ? 'info' : 'danger'"
          effect="light"
          size="small"
        >
          {{ statusMap[item.status] }}
        </el-tag>
      </header>
      <p class="location">{{ item.location }}</p>
      <div class="metrics">
        <span>温度 {{ item.temperature.toFixed(1) }}℃</span>
        <span>烟雾 {{ item.smoke.toFixed(1) }}ppm</span>
      </div>
      <div class="metrics">
        <span>电池 {{ item.batteryStatus }}%</span>
        <span>{{ item.deviceCode }}</span>
      </div>
    </article>
  </div>
</template>

<style scoped lang="scss">
.device-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.device-card {
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.55);
  padding: 10px;
  transition: all 0.2s ease;
  &.active {
    border-color: rgba(0, 122, 255, 0.6);
    box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.2);
  }
  &.warning {
    background: rgba(255, 245, 243, 0.82);
  }
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  h4 {
    margin: 0;
    font-size: 14px;
    color: #1d1d1f;
  }
}

.location {
  margin: 6px 0 8px;
  font-size: 12px;
  color: #6e6e73;
}

.metrics {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #3a3a3c;
  & + .metrics {
    margin-top: 4px;
  }
}

@media (max-width: 1366px) {
  .device-grid {
    grid-template-columns: 1fr;
  }
}
</style>
