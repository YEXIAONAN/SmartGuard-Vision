<script setup>
defineProps({
  monitor: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <div class="monitor-layout">
    <div class="monitor-screen">
      <div class="screen-badge">{{ monitor.screenLabel }}</div>
      <div
        v-for="overlay in monitor.overlays"
        :key="overlay.text"
        class="screen-overlay"
        :class="overlay.className"
      >
        {{ overlay.text }}
      </div>
      <div class="screen-footer">
        <span>点位编码：{{ monitor.pointCode }}</span>
        <span>采集状态：{{ monitor.captureStatus }}</span>
      </div>
    </div>

    <div class="monitor-side">
      <div class="info-group">
        <div class="info-group-title">识别结果信息</div>
        <div v-for="item in monitor.recognitionList" :key="item.label" class="info-item">
          <span class="info-label">{{ item.label }}</span>
          <span class="info-value">{{ item.value }}</span>
        </div>
      </div>

      <div class="tag-group">
        <el-tag v-for="tag in monitor.tags" :key="tag" effect="plain">
          {{ tag }}
        </el-tag>
      </div>
    </div>
  </div>
</template>

<style scoped>
.monitor-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
  gap: 16px;
}

.monitor-screen {
  position: relative;
  min-height: 430px;
  overflow: hidden;
  border: 1px solid var(--sg-border);
  border-radius: 14px;
  background:
    linear-gradient(180deg, rgba(38, 73, 121, 0.18), rgba(19, 41, 78, 0.34)),
    linear-gradient(135deg, #c6d8f2 0%, #f1f6fc 42%, #d5e2f3 100%);
}

.monitor-screen::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(rgba(255, 255, 255, 0.18) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.18) 1px, transparent 1px);
  background-size: 36px 36px;
  opacity: 0.45;
}

.screen-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 1;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(20, 54, 104, 0.86);
  color: #fff;
  font-size: 13px;
}

.screen-overlay {
  position: absolute;
  z-index: 1;
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  color: #fff;
}

.overlay-main {
  top: 108px;
  right: 82px;
  background: rgba(215, 89, 89, 0.92);
}

.overlay-secondary {
  bottom: 104px;
  left: 74px;
  background: rgba(242, 169, 59, 0.92);
}

.screen-footer {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  padding: 14px 18px;
  background: rgba(15, 37, 68, 0.78);
  font-size: 13px;
  color: rgba(255, 255, 255, 0.92);
}

.monitor-side {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-group {
  padding: 16px;
  border: 1px solid var(--sg-border-light);
  border-radius: 12px;
  background: var(--sg-bg-soft);
}

.info-group-title {
  margin-bottom: 14px;
  font-size: 15px;
  font-weight: 600;
  color: #25405f;
}

.info-item {
  display: grid;
  grid-template-columns: 88px minmax(0, 1fr);
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed #dde7f2;
}

.info-item:last-child {
  padding-bottom: 0;
  border-bottom: none;
}

.info-label {
  font-size: 13px;
  color: var(--sg-text-secondary);
}

.info-value {
  font-size: 14px;
  line-height: 1.6;
  color: var(--sg-text-main);
}

.tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

@media (max-width: 1366px) {
  .monitor-layout {
    grid-template-columns: 1fr;
  }

  .monitor-screen {
    min-height: 360px;
  }
}

@media (max-width: 768px) {
  .monitor-screen {
    min-height: 300px;
  }

  .screen-footer {
    flex-direction: column;
    gap: 6px;
  }
}
</style>
