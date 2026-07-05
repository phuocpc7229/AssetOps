<template>
  <div class="dashboard-asset-table">
    <table>
      <thead>
        <tr>
          <th>Asset Tag</th>
          <th>Name</th>
          <th>Primary IP</th>
          <th>Type</th>
          <th>Vendor</th>
          <th>Site</th>
          <th>Status</th>
          <th>Criticality</th>
          <th>Warranty</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="asset in assets"
          :key="asset.id"
        >
          <td>
            <RouterLink :to="{ name: 'asset-edit', params: { id: asset.id } }">
              {{ asset.asset_tag }}
            </RouterLink>
          </td>
          <td>{{ asset.name }}</td>
          <td>
            <span>{{ asset.primary_ip || '-' }}</span>
            <small v-if="asset.ip_count > 1">+{{ asset.ip_count - 1 }}</small>
          </td>
          <td>{{ asset.asset_type.name }}</td>
          <td>{{ asset.vendor?.name || '-' }}</td>
          <td>{{ asset.site ? `${asset.site.code} - ${asset.site.name}` : '-' }}</td>
          <td>
            <AssetStatusPill
              :value="asset.status"
              type="status"
            />
          </td>
          <td>
            <AssetStatusPill
              :value="asset.criticality"
              type="criticality"
            />
          </td>
          <td :class="`dashboard-asset-table__warranty dashboard-asset-table__warranty--${asset.warranty_state}`">
            {{ formatDate(asset.warranty_expires_on) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'

import AssetStatusPill from '@/components/assets/AssetStatusPill.vue'
import type { DashboardAsset } from '@/services/dashboard'

defineProps<{
  assets: DashboardAsset[]
}>()

const formatDate = (value: string | null) => {
  if (!value) {
    return '-'
  }

  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
  }).format(new Date(`${value}T00:00:00`))
}
</script>

<style scoped>
.dashboard-asset-table {
  width: 100%;
  overflow-x: auto;
}

.dashboard-asset-table table {
  width: 100%;
  min-width: 980px;
  border-collapse: collapse;
}

.dashboard-asset-table th,
.dashboard-asset-table td {
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  padding: 13px 16px;
  text-align: left;
  vertical-align: middle;
}

.dashboard-asset-table th {
  color: var(--assetops-muted);
  background: rgba(10, 26, 45, 0.8);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.dashboard-asset-table td {
  color: var(--assetops-muted-strong);
  font-size: 14px;
}

.dashboard-asset-table a {
  color: var(--assetops-cyan);
  font-weight: 800;
}

.dashboard-asset-table small {
  display: inline-grid;
  min-width: 24px;
  margin-left: 8px;
  place-items: center;
  border: 1px solid rgba(0, 216, 255, 0.3);
  border-radius: 5px;
  color: var(--assetops-cyan);
  font-size: 11px;
  font-weight: 800;
}

.dashboard-asset-table__warranty {
  font-weight: 700;
}

.dashboard-asset-table__warranty--valid {
  color: var(--assetops-muted-strong);
}

.dashboard-asset-table__warranty--expiring {
  color: #ff951a;
}

.dashboard-asset-table__warranty--expired {
  color: #ff4d5e;
}

.dashboard-asset-table__warranty--unknown {
  color: var(--assetops-muted);
}
</style>
