<script setup lang="ts">
withDefaults(
  defineProps<{
    description?: string
  }>(),
  { description: '暂无数据' },
)
</script>

<template>
  <div class="app-empty">
    <el-empty :description="description" />
  </div>
</template>

<style scoped lang="scss">
.app-empty {
  padding: 8px 0;
}
</style>
