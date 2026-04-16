<script setup>
import BaseChart from '../common/BaseChart.vue'
import PanelCard from '../common/PanelCard.vue'

defineProps({
  title: {
    type: String,
    required: true,
  },
  extra: {
    type: String,
    default: '',
  },
  option: {
    type: Object,
    required: true,
  },
  height: {
    type: [Number, String],
    default: 260,
  },
})
</script>

<template>
  <PanelCard :title="title" :extra="extra">
    <BaseChart :option="option" :height="height" />
  </PanelCard>
</template>
