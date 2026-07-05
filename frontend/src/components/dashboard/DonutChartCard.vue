<template>
  <section class="donut-chart-card">
    <header>
      <h2>{{ title }}</h2>
      <RouterLink :to="viewReportTo">
        View Report
      </RouterLink>
    </header>

    <div class="donut-chart-card__body">
      <div
        class="donut-chart-card__donut"
        :style="{ background: donutBackground }"
      >
        <div>
          <strong>{{ formattedTotal }}</strong>
          <span>Total</span>
        </div>
      </div>

      <div class="donut-chart-card__legend">
        <div
          v-for="segment in chart.segments"
          :key="segment.key"
        >
          <span :style="{ background: segment.color }" />
          <p>{{ segment.label }}</p>
          <strong>{{ segment.percent }}% ({{ segment.value }})</strong>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, type RouteLocationRaw } from 'vue-router'

import type { DashboardDonutChart } from '@/services/dashboard'

const props = defineProps<{
  title: string
  chart: DashboardDonutChart
  viewReportTo: RouteLocationRaw
}>()

const formattedTotal = computed(() => new Intl.NumberFormat('en-US').format(props.chart.total))
const donutBackground = computed(() => {
  if (props.chart.segments.length === 0) {
    return 'conic-gradient(rgba(142, 168, 203, 0.22) 0% 100%)'
  }

  let offset = 0
  const stops = props.chart.segments.map((segment) => {
    const start = offset
    offset += segment.percent
    return `${segment.color} ${start}% ${offset}%`
  })

  return `conic-gradient(${stops.join(', ')})`
})
</script>

<style scoped>
.donut-chart-card {
  border: 1px solid rgba(30, 155, 255, 0.34);
  border-radius: 12px;
  background:
    linear-gradient(145deg, rgba(13, 33, 56, 0.82), rgba(3, 10, 24, 0.95)),
    var(--assetops-panel);
  padding: 18px;
  box-shadow:
    var(--assetops-glow),
    inset 0 0 42px rgba(18, 107, 255, 0.06);
  transition:
    border-color var(--assetops-motion-standard) var(--assetops-ease-standard),
    box-shadow var(--assetops-motion-standard) var(--assetops-ease-standard),
    transform var(--assetops-motion-standard) var(--assetops-ease-standard);
}

.donut-chart-card:hover {
  border-color: rgba(0, 216, 255, 0.48);
  box-shadow:
    0 0 34px rgba(0, 184, 255, 0.24),
    inset 0 0 42px rgba(18, 107, 255, 0.07);
  transform: translateY(-1px);
}

.donut-chart-card header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 18px;
}

.donut-chart-card h2 {
  margin: 0;
  color: var(--assetops-text);
  font-size: 20px;
}

.donut-chart-card a {
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
}

.donut-chart-card a:hover,
.donut-chart-card a:focus-visible {
  color: #ffffff;
  outline: 0;
}

.donut-chart-card__body {
  display: grid;
  grid-template-columns: 168px minmax(0, 1fr);
  align-items: center;
  gap: 18px;
}

.donut-chart-card__donut {
  display: grid;
  width: 168px;
  height: 168px;
  place-items: center;
  border-radius: 50%;
  box-shadow: 0 0 22px rgba(0, 132, 255, 0.2);
}

.donut-chart-card__donut > div {
  display: grid;
  width: 92px;
  height: 92px;
  place-items: center;
  border: 1px solid rgba(30, 155, 255, 0.28);
  border-radius: 50%;
  background: rgba(4, 11, 24, 0.96);
}

.donut-chart-card__donut strong {
  align-self: end;
  color: var(--assetops-text);
  font-size: 22px;
  line-height: 1;
}

.donut-chart-card__donut span {
  align-self: start;
  color: var(--assetops-muted);
  font-size: 12px;
}

.donut-chart-card__legend {
  display: grid;
  gap: 10px;
}

.donut-chart-card__legend div {
  display: grid;
  grid-template-columns: 10px minmax(0, 1fr) auto;
  align-items: center;
  gap: 9px;
}

.donut-chart-card__legend span {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  box-shadow: 0 0 8px currentColor;
}

.donut-chart-card__legend p,
.donut-chart-card__legend strong {
  margin: 0;
  font-size: 12px;
}

.donut-chart-card__legend p {
  overflow: hidden;
  color: var(--assetops-muted-strong);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.donut-chart-card__legend strong {
  color: var(--assetops-text);
  font-weight: 700;
}

@media (max-width: 520px) {
  .donut-chart-card__body {
    grid-template-columns: 1fr;
    justify-items: center;
  }

  .donut-chart-card__legend {
    width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .donut-chart-card {
    transition: none;
  }

  .donut-chart-card:hover {
    transform: none;
  }
}
</style>
