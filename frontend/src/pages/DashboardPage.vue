<template>
  <section class="dashboard-page">
    <header class="dashboard-page__header">
      <div>
        <p>Admin Dashboard</p>
        <h2>Asset Operations Overview</h2>
        <span>Monitor inventory health, warranty exposure, and recent operational movement.</span>
      </div>

      <form
        class="dashboard-page__search"
        @submit.prevent="searchAssets"
      >
        <label>
          <span>Global Asset Search</span>
          <input
            v-model.trim="assetSearch"
            placeholder="Search assets, sites, vendors..."
          >
        </label>
        <button type="submit">
          Search
        </button>
      </form>
    </header>

    <DashboardState
      v-if="isLoading"
      title="Loading dashboard"
      message="Collecting asset metrics and recent activity."
    />
    <DashboardState
      v-else-if="error"
      title="Dashboard unavailable"
      :message="error"
      variant="error"
    />

    <template v-else-if="metrics">
      <DashboardKpiGrid :kpis="metrics.kpis" />

      <DashboardContentGrid>
        <template #main>
          <RecentAssetsPanel :assets="recentAssets" />
        </template>

        <template #side>
          <DonutChartCard
            title="Assets by Type"
            :chart="metrics.charts.assets_by_type"
            :view-report-to="{ name: 'assets' }"
          />
          <DonutChartCard
            title="Warranty Status"
            :chart="metrics.charts.warranty_status"
            :view-report-to="{ name: 'assets', query: { ordering: 'warranty_expires_on' } }"
          />
          <QuickActionsPanel :badges="metrics.quick_action_badges" />
          <RecentActivityPanel
            :activities="recentActivity"
            :note="activityNote"
          />
        </template>
      </DashboardContentGrid>
    </template>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import DashboardContentGrid from '@/components/dashboard/DashboardContentGrid.vue'
import DashboardKpiGrid from '@/components/dashboard/DashboardKpiGrid.vue'
import DashboardState from '@/components/dashboard/DashboardState.vue'
import DonutChartCard from '@/components/dashboard/DonutChartCard.vue'
import QuickActionsPanel from '@/components/dashboard/QuickActionsPanel.vue'
import RecentActivityPanel from '@/components/dashboard/RecentActivityPanel.vue'
import RecentAssetsPanel from '@/components/dashboard/RecentAssetsPanel.vue'
import {
  fetchDashboardMetrics,
  fetchDashboardRecentActivity,
  fetchDashboardRecentAssets,
  type DashboardActivity,
  type DashboardAsset,
  type DashboardMetrics,
} from '@/services/dashboard'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const metrics = ref<DashboardMetrics | null>(null)
const recentAssets = ref<DashboardAsset[]>([])
const recentActivity = ref<DashboardActivity[]>([])
const activityNote = ref('Recent activity is inferred from existing records until an AuditEvent table exists.')
const isLoading = ref(false)
const error = ref<string | null>(null)
const assetSearch = ref('')

const canLoadDashboard = computed(() => Boolean(authStore.accessToken))

const loadDashboard = async () => {
  if (!authStore.accessToken) {
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const [metricsResponse, assetsResponse, activityResponse] = await Promise.all([
      fetchDashboardMetrics(authStore.accessToken),
      fetchDashboardRecentAssets(authStore.accessToken, 8),
      fetchDashboardRecentActivity(authStore.accessToken, 8),
    ])

    metrics.value = metricsResponse
    recentAssets.value = assetsResponse.results
    recentActivity.value = activityResponse.results
    activityNote.value = activityResponse.note
  } catch (loadError) {
    error.value = loadError instanceof Error ? loadError.message : 'Unable to load dashboard.'
  } finally {
    isLoading.value = false
  }
}

const searchAssets = () => {
  const search = assetSearch.value.trim()
  router.push({
    name: 'assets',
    query: search ? { search } : {},
  })
}

onMounted(() => {
  if (canLoadDashboard.value) {
    void loadDashboard()
  }
})
</script>

<style scoped>
.dashboard-page {
  display: grid;
  gap: 22px;
  padding: 0 32px 34px;
}

.dashboard-page__header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(420px, 0.62fr);
  align-items: end;
  gap: 24px;
  border: 1px solid rgba(30, 155, 255, 0.34);
  border-radius: 12px;
  background:
    linear-gradient(145deg, rgba(13, 33, 56, 0.82), rgba(3, 10, 24, 0.95)),
    var(--assetops-panel);
  padding: 22px;
  box-shadow:
    var(--assetops-glow),
    inset 0 0 42px rgba(18, 107, 255, 0.06);
}

.dashboard-page__header p {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.dashboard-page__header h2 {
  margin: 0;
  color: var(--assetops-text);
  font-size: 24px;
}

.dashboard-page__header div > span {
  display: block;
  margin-top: 10px;
  color: var(--assetops-muted-strong);
  font-size: 14px;
}

.dashboard-page__search {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: end;
  gap: 12px;
}

.dashboard-page__search label {
  display: grid;
  gap: 8px;
}

.dashboard-page__search label span {
  color: var(--assetops-muted);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.dashboard-page__search input {
  min-height: 46px;
  border: 1px solid var(--assetops-border-muted);
  border-radius: 8px;
  color: var(--assetops-text);
  background: rgba(7, 21, 40, 0.8);
  padding: 0 14px;
  outline: 0;
}

.dashboard-page__search input:focus {
  border-color: var(--assetops-cyan);
  box-shadow: 0 0 16px rgba(0, 216, 255, 0.18);
}

.dashboard-page__search button {
  min-height: 46px;
  border: 1px solid rgba(36, 212, 255, 0.62);
  border-radius: 8px;
  color: #ffffff;
  background: linear-gradient(110deg, #058cff, #123de8);
  padding: 0 18px;
  cursor: pointer;
  font-weight: 800;
  box-shadow: 0 0 18px rgba(0, 132, 255, 0.24);
}

@media (max-width: 1100px) {
  .dashboard-page__header {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .dashboard-page {
    padding: 0 18px 24px;
  }

  .dashboard-page__search {
    grid-template-columns: 1fr;
  }
}
</style>
