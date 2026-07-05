<template>
  <div class="asset-table">
    <table>
      <thead>
        <tr>
          <th>Asset Tag</th>
          <th>Name</th>
          <th>Hostname</th>
          <th>Type</th>
          <th>Vendor</th>
          <th>Site</th>
          <th>Status</th>
          <th>Criticality</th>
          <th>Warranty</th>
          <th>Actions</th>
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
          <td>{{ asset.hostname || '-' }}</td>
          <td>{{ asset.asset_type.name }}</td>
          <td>{{ asset.vendor?.name || '-' }}</td>
          <td>{{ formatSite(asset) }}</td>
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
          <td :class="{ 'asset-table__expired': isWarrantyExpired(asset.warranty_expires_on) }">
            {{ formatDate(asset.warranty_expires_on) }}
          </td>
          <td>
            <div class="asset-table__actions">
              <RouterLink :to="{ name: 'asset-edit', params: { id: asset.id } }">
                Edit
              </RouterLink>
              <button
                v-if="asset.ip_address"
                type="button"
                class="asset-table__ping"
                @click="$emit('ping', asset)"
              >
                Ping
              </button>
              <button
                type="button"
                @click="$emit('archive', asset)"
              >
                Archive
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'

import AssetStatusPill from '@/components/assets/AssetStatusPill.vue'
import type { Asset } from '@/services/assets'

defineProps<{
  assets: Asset[]
}>()

defineEmits<{
  archive: [asset: Asset]
  ping: [asset: Asset]
}>()

const formatSite = (asset: Asset) => {
  if (!asset.site) {
    return '-'
  }

  return `${asset.site.code} - ${asset.site.name}`
}

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

const isWarrantyExpired = (value: string | null) => {
  if (!value) {
    return false
  }

  return new Date(`${value}T23:59:59`) < new Date()
}
</script>

<style scoped>
.asset-table {
  width: 100%;
  overflow-x: auto;
}

.asset-table table {
  width: 100%;
  min-width: 1120px;
  border-collapse: collapse;
}

.asset-table th,
.asset-table td {
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  padding: 14px 16px;
  text-align: left;
  vertical-align: middle;
}

.asset-table th {
  color: var(--assetops-muted);
  background: rgba(10, 26, 45, 0.8);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.asset-table td {
  color: var(--assetops-muted-strong);
  font-size: 14px;
}

.asset-table a {
  color: var(--assetops-cyan);
  font-weight: 700;
}

.asset-table__actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.asset-table__actions button {
  border: 0;
  color: #ff951a;
  background: transparent;
  cursor: pointer;
  font-weight: 700;
}

.asset-table__actions .asset-table__ping {
  color: var(--assetops-cyan);
}

.asset-table__expired {
  color: #ff4d5e !important;
  font-weight: 700;
}
</style>
