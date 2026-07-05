<template>
  <svg
    class="mini-sparkline"
    viewBox="0 0 120 38"
    role="img"
    aria-label="KPI trend"
  >
    <polyline
      class="mini-sparkline__fill"
      :points="fillPoints"
    />
    <polyline
      class="mini-sparkline__line"
      :points="linePoints"
    />
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { DashboardTrendPoint } from '@/services/dashboard'

const props = defineProps<{
  points: DashboardTrendPoint[]
}>()

const linePoints = computed(() => {
  if (props.points.length === 0) {
    return '0,32 120,32'
  }

  const values = props.points.map((point) => point.value)
  const maxValue = Math.max(...values, 1)
  const xStep = props.points.length > 1 ? 120 / (props.points.length - 1) : 120

  return values
    .map((value, index) => {
      const x = Math.round(index * xStep * 100) / 100
      const y = Math.round((34 - (value / maxValue) * 28) * 100) / 100
      return `${x},${y}`
    })
    .join(' ')
})

const fillPoints = computed(() => `0,38 ${linePoints.value} 120,38`)
</script>

<style scoped>
.mini-sparkline {
  width: 100%;
  height: 42px;
  overflow: visible;
}

.mini-sparkline__fill {
  fill: rgba(0, 132, 255, 0.16);
  stroke: 0;
}

.mini-sparkline__line {
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 2.4;
  filter: drop-shadow(0 0 6px currentColor);
}
</style>
