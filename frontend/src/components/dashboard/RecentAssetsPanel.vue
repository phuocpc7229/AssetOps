<template>
  <section class="recent-assets-panel">
    <header>
      <div>
        <p>Recent Assets</p>
        <h2>Recently Updated Inventory</h2>
      </div>
      <RouterLink :to="{ name: 'assets' }">
        View All
      </RouterLink>
    </header>

    <DashboardAssetTable
      v-if="assets.length"
      :assets="assets"
    />
    <div
      v-else
      class="recent-assets-panel__empty"
    >
      No asset activity yet.
    </div>

    <footer>
      <span>Showing {{ assets.length }} recent assets</span>
      <RouterLink :to="{ name: 'asset-new' }">
        Add Asset
      </RouterLink>
    </footer>
  </section>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'

import DashboardAssetTable from '@/components/dashboard/DashboardAssetTable.vue'
import type { DashboardAsset } from '@/services/dashboard'

defineProps<{
  assets: DashboardAsset[]
}>()
</script>

<style scoped>
.recent-assets-panel {
  overflow: hidden;
  border: 1px solid rgba(30, 155, 255, 0.34);
  border-radius: 12px;
  background:
    linear-gradient(145deg, rgba(13, 33, 56, 0.82), rgba(3, 10, 24, 0.95)),
    var(--assetops-panel);
  box-shadow:
    var(--assetops-glow),
    inset 0 0 42px rgba(18, 107, 255, 0.06);
}

.recent-assets-panel header,
.recent-assets-panel footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 20px;
}

.recent-assets-panel header {
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
}

.recent-assets-panel footer {
  border-top: 1px solid rgba(142, 168, 203, 0.16);
}

.recent-assets-panel p {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.recent-assets-panel h2 {
  margin: 0;
  color: var(--assetops-text);
  font-size: 20px;
}

.recent-assets-panel a {
  border: 1px solid rgba(30, 155, 255, 0.32);
  border-radius: 8px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
  padding: 9px 12px;
  font-size: 13px;
  font-weight: 800;
}

.recent-assets-panel footer span,
.recent-assets-panel__empty {
  color: var(--assetops-muted);
  font-size: 13px;
  font-weight: 700;
}

.recent-assets-panel__empty {
  display: grid;
  min-height: 220px;
  place-items: center;
}
</style>
