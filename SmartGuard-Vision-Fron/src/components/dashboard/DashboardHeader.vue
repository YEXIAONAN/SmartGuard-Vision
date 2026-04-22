<script setup>
defineProps({
  projectName: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    required: true,
  },
  currentTime: {
    type: String,
    required: true,
  },
  generatedAt: {
    type: String,
    required: true,
  },
  systemStatus: {
    type: String,
    required: true,
  },
  onlineSummary: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="page-header">
    <div>
      <div class="project-title">{{ projectName }}</div>
      <div class="project-subtitle">{{ subtitle }}</div>
    </div>

    <div class="header-metrics">
      <div class="header-metric">
        <span class="metric-label">当前时间</span>
        <span class="metric-value">{{ currentTime }}</span>
      </div>
      <div class="header-metric">
        <span class="metric-label">数据更新时间</span>
        <span class="metric-value">{{ generatedAt }}</span>
      </div>
      <div class="header-metric">
        <span class="metric-label">系统状态</span>
        <span class="metric-value">
          <span class="status-dot"></span>
          {{ systemStatus }}
        </span>
      </div>
      <div class="header-metric">
        <span class="metric-label">在线设备数</span>
        <span class="metric-value">{{ onlineSummary }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.project-title {
  font-size: 30px;
  line-height: 1.1;
  font-weight: 700;
  color: #1f3e68;
  letter-spacing: 1px;
}

.project-subtitle {
  margin-top: 8px;
  font-size: 15px;
  color: var(--sg-text-secondary);
}

.header-metrics {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 12px;
}

.header-metric {
  min-width: 190px;
  padding: 10px 14px;
  border: 1px solid var(--sg-border-light);
  border-radius: 10px;
  background: #f7faff;
}

.metric-label {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  color: var(--sg-text-muted);
}

.metric-value {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #20354d;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--sg-color-success);
}

@media (max-width: 992px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-metrics {
    width: 100%;
    justify-content: flex-start;
  }

  .header-metric {
    min-width: calc(50% - 6px);
  }
}

@media (max-width: 768px) {
  .project-title {
    font-size: 24px;
  }

  .project-subtitle {
    font-size: 14px;
    line-height: 1.6;
  }

  .header-metric {
    min-width: 100%;
  }
}
</style>
