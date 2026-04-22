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
      <div class="screen-head">
        <span class="screen-title">{{ monitor.screenLabel }}</span>
        <span class="screen-point">点位编码：{{ monitor.pointCode }}</span>
      </div>
      <div class="screen-canvas">
        <div v-for="overlay in monitor.overlays" :key="overlay.text" class="screen-overlay" :class="overlay.className">
          {{ overlay.text }}
        </div>
      </div>
      <div class="screen-footer">
        <span>采集状态：{{ monitor.captureStatus }}</span>
        <div class="screen-tags">
          <el-tag v-for="tag in monitor.tags" :key="tag" effect="plain" size="small">{{ tag }}</el-tag>
        </div>
      </div>
    </div>

    <div class="monitor-info">
      <div class="info-title">识别联动信息</div>
      <div v-for="item in monitor.recognitionList" :key="item.label" class="info-row">
        <span class="info-label">{{ item.label }}</span>
        <span class="info-value">{{ item.value }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.monitor-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(260px, 0.65fr);
  gap: 12px;
}

.monitor-screen {
  border: 1px solid #cfd8e4;
  border-radius: 10px;
  overflow: hidden;
  background: #0f1823;
}

.screen-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  border-bottom: 1px solid #2a3848;
  background: #132233;
}

.screen-title {
  font-size: 13px;
  font-weight: 600;
  color: #d7e5f6;
}

.screen-point {
  font-size: 12px;
  color: #9eb2c7;
}

.screen-canvas {
  position: relative;
  min-height: 320px;
  background:
    linear-gradient(180deg, rgba(22, 33, 47, 0.8), rgba(12, 18, 27, 0.9)),
    repeating-linear-gradient(0deg, rgba(62, 84, 107, 0.14), rgba(62, 84, 107, 0.14) 1px, transparent 1px, transparent 36px),
    repeating-linear-gradient(90deg, rgba(62, 84, 107, 0.14), rgba(62, 84, 107, 0.14) 1px, transparent 1px, transparent 36px);
}

.screen-overlay {
  position: absolute;
  z-index: 1;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #ffffff;
}

.overlay-main {
  top: 78px;
  right: 72px;
  background: rgba(174, 78, 78, 0.92);
}

.overlay-secondary {
  bottom: 88px;
  left: 66px;
  background: rgba(169, 123, 53, 0.92);
}

.screen-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-top: 1px solid #2a3848;
  background: #132233;
  color: #c5d6e7;
  font-size: 12px;
}

.screen-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 6px;
}

.screen-tags :deep(.el-tag) {
  color: #aec2d8;
  border-color: #35516c;
  background: rgba(36, 58, 82, 0.35);
}

.monitor-info {
  border: 1px solid var(--sg-border);
  border-radius: 10px;
  padding: 10px 12px;
  background: var(--sg-bg-soft);
}

.info-title {
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #2c425a;
}

.info-row {
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: 10px;
  padding: 9px 0;
  border-bottom: 1px dashed #d6dfeb;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 12px;
  color: var(--sg-text-muted);
}

.info-value {
  font-size: 13px;
  line-height: 1.5;
  color: var(--sg-text-main);
}

@media (max-width: 1200px) {
  .monitor-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .screen-canvas {
    min-height: 240px;
  }

  .screen-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .screen-tags {
    justify-content: flex-start;
  }
}
</style>
