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
}

:deep(.el-card__header) {
  padding: 16px 18px 10px;
  border-bottom: none;
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.panel-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--sg-text-main);
}

.panel-extra {
  font-size: 12px;
  color: var(--sg-text-muted);
}
</style>
