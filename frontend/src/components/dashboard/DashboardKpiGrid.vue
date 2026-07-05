<template>
  <section
    class="dashboard-kpi-grid"
    aria-label="Asset KPI summary"
  >
    <DashboardKpiCard
      v-for="kpi in kpis"
      :key="kpi.key"
      :kpi="kpi"
    />
  </section>
</template>

<script setup lang="ts">
import DashboardKpiCard from '@/components/dashboard/DashboardKpiCard.vue'
import type { DashboardKpi } from '@/services/dashboard'

defineProps<{
  kpis: DashboardKpi[]
}>()
</script>

<style scoped>
.dashboard-kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 18px;
}

@media (max-width: 1480px) {
  .dashboard-kpi-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .dashboard-kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 620px) {
  .dashboard-kpi-grid {
    grid-template-columns: 1fr;
  }
}
</style>
