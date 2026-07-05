<template>
  <article
    class="dashboard-kpi-card"
    :class="`dashboard-kpi-card--${kpi.tone}`"
  >
    <div class="dashboard-kpi-card__top">
      <span class="dashboard-kpi-card__icon">{{ icon }}</span>
      <div>
        <p>{{ kpi.label }}</p>
        <strong>{{ formattedValue }}</strong>
      </div>
    </div>
    <span>{{ kpi.helper }}</span>
    <MiniSparkline :points="kpi.trend" />
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import MiniSparkline from '@/components/dashboard/MiniSparkline.vue'
import type { DashboardKpi, DashboardKpiKey } from '@/services/dashboard'

const props = defineProps<{
  kpi: DashboardKpi
}>()

const icons: Record<DashboardKpiKey, string> = {
  total_assets: 'TA',
  active_assets: 'AC',
  maintenance_assets: 'MT',
  expiring_warranty: 'WR',
  online_assets: 'ON',
}

const icon = computed(() => icons[props.kpi.key] ?? 'AS')
const formattedValue = computed(() => new Intl.NumberFormat('en-US').format(props.kpi.value))
</script>

<style scoped>
.dashboard-kpi-card {
  display: grid;
  min-height: 178px;
  align-content: space-between;
  gap: 10px;
  border: 1px solid rgba(30, 155, 255, 0.36);
  border-radius: 10px;
  background:
    linear-gradient(145deg, rgba(13, 33, 56, 0.74), rgba(4, 11, 24, 0.94)),
    var(--assetops-panel);
  padding: 18px;
  color: var(--assetops-cyan);
  box-shadow:
    0 0 24px rgba(0, 132, 255, 0.14),
    inset 0 0 36px rgba(18, 107, 255, 0.05);
}

.dashboard-kpi-card__top {
  display: flex;
  align-items: center;
  gap: 14px;
}

.dashboard-kpi-card__icon {
  display: inline-grid;
  width: 56px;
  height: 56px;
  flex: 0 0 auto;
  place-items: center;
  border: 1px solid currentColor;
  border-radius: 50%;
  background: rgba(10, 132, 255, 0.16);
  font-size: 13px;
  font-weight: 900;
  box-shadow: 0 0 20px rgba(0, 132, 255, 0.26);
}

.dashboard-kpi-card p {
  margin: 0 0 6px;
  color: var(--assetops-muted-strong);
  font-size: 14px;
  font-weight: 700;
}

.dashboard-kpi-card strong {
  display: block;
  color: var(--assetops-text);
  font-size: 30px;
  line-height: 1;
}

.dashboard-kpi-card > span {
  color: var(--assetops-muted);
  font-size: 13px;
}

.dashboard-kpi-card--green {
  color: #00d48a;
}

.dashboard-kpi-card--orange {
  color: #ff951a;
}

.dashboard-kpi-card--red {
  color: #ff4d5e;
}

.dashboard-kpi-card--muted {
  color: var(--assetops-muted);
}
</style>
