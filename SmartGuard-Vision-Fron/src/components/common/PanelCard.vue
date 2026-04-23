<script setup>
import { computed, useSlots } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  extra: {
    type: String,
    default: '',
  },
  bodyPadding: {
    type: String,
    default: '0 18px 18px',
  },
})

const slots = useSlots()
const showHeader = computed(() => props.title || props.extra || slots.header)
</script>

<template>
  <el-card shadow="never" class="panel-card" :body-style="{ padding: bodyPadding }">
    <template v-if="showHeader" #header>
      <slot name="header">
        <div class="panel-head">
          <span class="panel-title">{{ title }}</span>
          <span v-if="extra" class="panel-extra">{{ extra }}</span>
        </div>
      </slot>
    </template>
    <slot />
  </el-card>
</template>

<style scoped>
.panel-card {
  border: 1px solid var(--sg-border);
  border-radius: var(--sg-radius-card);
  background: var(--sg-bg-card);
  box-shadow: var(--sg-shadow-soft);
  backdrop-filter: var(--sg-blur-xl);
  -webkit-backdrop-filter: var(--sg-blur-xl);
  transition: all 0.2s ease;
}

.panel-card:hover {
  transform: translateY(-1px);
  background: rgba(255, 255, 255, 0.66);
}

:deep(.el-card__header) {
  padding: 10px 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.45);
  background: rgba(255, 255, 255, 0.45);
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
}

.panel-extra {
  font-size: 11px;
  color: #6e6e73;
}
</style>
