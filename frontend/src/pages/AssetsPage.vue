<template>
  <section class="assets-page">
    <div class="assets-page__panel">
      <header class="assets-page__header">
        <div>
          <p>Asset Management</p>
          <h2>Assets</h2>
        </div>
        <RouterLink
          class="assets-page__add"
          :to="{ name: 'asset-new' }"
        >
          Add Asset
        </RouterLink>
      </header>

      <form
        class="assets-page__filters"
        @submit.prevent="applyFilters"
      >
        <label class="assets-page__search">
          <span>Search</span>
          <input
            v-model.trim="draftFilters.search"
            placeholder="Asset tag, name, hostname, serial or IP"
          >
        </label>

        <label>
          <span>Status</span>
          <SearchableSelect
            v-model="draftFilters.status"
            :options="statusFilterOptions"
            placeholder="Default Active View"
            search-placeholder="Search statuses"
            clearable
          />
        </label>

        <label>
          <span>Criticality</span>
          <SearchableSelect
            v-model="draftFilters.criticality"
            :options="criticalityFilterOptions"
            placeholder="All"
            search-placeholder="Search criticality"
            clearable
          />
        </label>

        <label>
          <span>Type</span>
          <input v-model.trim="draftFilters.asset_type">
        </label>

        <label>
          <span>Vendor</span>
          <input v-model.trim="draftFilters.vendor">
        </label>

        <label>
          <span>Site</span>
          <SearchableSelect
            v-model="draftFilters.site"
            :options="siteFilterOptions"
            placeholder="All"
            search-placeholder="Search sites"
            clearable
          />
        </label>

        <label class="assets-page__checkbox">
          <input
            v-model="draftFilters.include_archived"
            type="checkbox"
          >
          <span>Include archived</span>
        </label>

        <div class="assets-page__filter-actions">
          <button
            type="button"
            @click="resetFilters"
          >
            Reset
          </button>
          <button type="submit">
            Apply
          </button>
        </div>
      </form>

      <div
        v-if="isLoading"
        class="assets-page__state"
      >
        Loading assets...
      </div>
      <div
        v-else-if="error"
        class="assets-page__state assets-page__state--error"
      >
        {{ error }}
      </div>
      <div
        v-else-if="assets.length === 0"
        class="assets-page__state"
      >
        No assets match the current filters.
      </div>
      <AssetTable
        v-else
        :assets="assets"
        @archive="requestArchive"
        @ping="runPingTest"
      />

      <div
        v-if="pingResult"
        class="assets-page__ping-result"
        :class="{ 'assets-page__ping-result--success': pingResult.success }"
      >
        <strong>{{ pingResult.assetTag }}</strong>
        <span>{{ pingResult.message }}</span>
        <span v-if="pingResult.latency_ms !== null">{{ pingResult.latency_ms }} ms</span>
      </div>

      <footer class="assets-page__footer">
        <span>{{ resultSummary }}</span>
        <div class="assets-page__pagination">
          <button
            type="button"
            :disabled="params.page <= 1"
            @click="goToPage(params.page - 1)"
          >
            Previous
          </button>
          <span>Page {{ params.page }} of {{ totalPages }}</span>
          <button
            type="button"
            :disabled="params.page >= totalPages"
            @click="goToPage(params.page + 1)"
          >
            Next
          </button>
        </div>
      </footer>
    </div>

    <div
      v-if="assetPendingArchive"
      class="assets-page__modal"
      role="dialog"
      aria-modal="true"
    >
      <section>
        <h3>Archive Asset</h3>
        <p>
          Archive {{ assetPendingArchive.asset_tag }}? It will be hidden from the default list but can be shown with
          archived assets included.
        </p>
        <div>
          <button
            type="button"
            @click="assetPendingArchive = null"
          >
            Cancel
          </button>
          <button
            type="button"
            :disabled="isArchiving"
            @click="confirmArchive"
          >
            {{ isArchiving ? 'Archiving...' : 'Archive' }}
          </button>
        </div>
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

import AssetTable from '@/components/assets/AssetTable.vue'
import SearchableSelect from '@/components/ui/SearchableSelect.vue'
import { useAuthStore } from '@/stores/auth'
import {
  archiveAsset,
  fetchAssets,
  pingAsset,
  type Asset,
  type AssetListParams,
  type AssetPingResponse,
} from '@/services/assets'
import { fetchSites, type Site } from '@/services/sites'

const authStore = useAuthStore()
const route = useRoute()

const assets = ref<Asset[]>([])
const isLoading = ref(false)
const isArchiving = ref(false)
const error = ref<string | null>(null)
const totalCount = ref(0)
const totalPages = ref(1)
const assetPendingArchive = ref<Asset | null>(null)
const sites = ref<Site[]>([])
const pingResult = ref<(AssetPingResponse & { assetTag: string }) | null>(null)

const emptyFilters = () => ({
  search: '',
  status: null as string | null,
  criticality: null as string | null,
  asset_type: '',
  vendor: '',
  site: null as number | null,
  include_archived: false,
})

const readQueryString = (value: unknown) => (typeof value === 'string' ? value : '')
const readNullableQueryString = (value: unknown) => {
  const queryValue = readQueryString(value)
  return queryValue || null
}
const readQueryNumber = (value: unknown) => {
  const queryValue = readQueryString(value)
  return queryValue && !Number.isNaN(Number(queryValue)) ? Number(queryValue) : null
}
const initialFilters = () => ({
  search: readQueryString(route.query.search),
  status: readNullableQueryString(route.query.status),
  criticality: readNullableQueryString(route.query.criticality),
  asset_type: readQueryString(route.query.asset_type),
  vendor: readQueryString(route.query.vendor),
  site: readQueryNumber(route.query.site),
  include_archived: route.query.include_archived === 'true',
})

const initialOrdering = () =>
  readQueryString(route.query.ordering) ||
  (readQueryString(route.query.warranty) === 'expiring' ? 'warranty_expires_on' : 'asset_tag')

const draftFilters = reactive(initialFilters())
const params = reactive<AssetListParams>({
  ...initialFilters(),
  ordering: initialOrdering(),
  page: 1,
  page_size: 10,
})

const resultSummary = computed(() => {
  if (totalCount.value === 0) {
    return '0 assets'
  }

  const start = (Number(params.page) - 1) * Number(params.page_size) + 1
  const end = Math.min(start + assets.value.length - 1, totalCount.value)
  return `${start}-${end} of ${totalCount.value} assets`
})

const statusFilterOptions = [
  { id: 'active', label: 'Active' },
  { id: 'in_maintenance', label: 'In Maintenance' },
  { id: 'archived', label: 'Archived' },
]

const criticalityFilterOptions = [
  { id: 'low', label: 'Low' },
  { id: 'medium', label: 'Medium' },
  { id: 'high', label: 'High' },
  { id: 'critical', label: 'Critical' },
]

const siteFilterOptions = computed(() =>
  sites.value.map((site) => ({
    id: site.id,
    label: site.name,
    detail: site.code,
  })),
)

const loadAssets = async () => {
  if (!authStore.accessToken) {
    return
  }

  isLoading.value = true
  error.value = null

  try {
    if (sites.value.length === 0) {
      const sitesResponse = await fetchSites({ ordering: 'code', page_size: 100 }, authStore.accessToken)
      sites.value = sitesResponse.results
    }

    const response = await fetchAssets(params, authStore.accessToken)
    assets.value = response.results
    totalCount.value = response.count
    totalPages.value = Math.max(response.total_pages, 1)
    params.page = response.page
    params.page_size = response.page_size
  } catch (loadError) {
    error.value = loadError instanceof Error ? loadError.message : 'Unable to load assets.'
  } finally {
    isLoading.value = false
  }
}

const applyRouteQueryFilters = () => {
  const filters = initialFilters()
  Object.assign(draftFilters, filters)
  Object.assign(params, filters, {
    ordering: initialOrdering(),
    page: 1,
    page_size: params.page_size || 10,
  })
}

const runPingTest = async (asset: Asset) => {
  if (!authStore.accessToken) {
    return
  }

  const availableIpAddresses = asset.ip_addresses?.map((ipAddress) => ipAddress.address).filter(Boolean) ?? []
  const selectedIpAddress =
    availableIpAddresses.length > 1
      ? globalThis.prompt(`Select IP to ping:\n${availableIpAddresses.join('\n')}`, asset.ip_address ?? availableIpAddresses[0])
      : asset.ip_address

  if (!selectedIpAddress) {
    return
  }

  error.value = null
  pingResult.value = {
    success: false,
    assetTag: asset.asset_tag,
    ip_address: selectedIpAddress,
    latency_ms: null,
    message: 'Running ping test...',
  }

  try {
    const response = await pingAsset(asset.id, authStore.accessToken, selectedIpAddress)
    pingResult.value = {
      ...response,
      assetTag: asset.asset_tag,
    }
  } catch (pingError) {
    pingResult.value = {
      success: false,
      assetTag: asset.asset_tag,
      ip_address: asset.ip_address ?? '',
      latency_ms: null,
      message: pingError instanceof Error ? pingError.message : 'Ping test failed.',
    }
  }
}

const applyFilters = () => {
  Object.assign(params, draftFilters, { page: 1 })
  loadAssets()
}

const resetFilters = () => {
  Object.assign(draftFilters, emptyFilters())
  Object.assign(params, emptyFilters(), { ordering: 'asset_tag', page: 1, page_size: 10 })
  loadAssets()
}

const goToPage = (page: number) => {
  params.page = page
  loadAssets()
}

const requestArchive = (asset: Asset) => {
  assetPendingArchive.value = asset
}

const confirmArchive = async () => {
  if (!authStore.accessToken || !assetPendingArchive.value) {
    return
  }

  isArchiving.value = true
  error.value = null

  try {
    await archiveAsset(assetPendingArchive.value.id, authStore.accessToken)
    assetPendingArchive.value = null
    await loadAssets()
  } catch (archiveError) {
    error.value = archiveError instanceof Error ? archiveError.message : 'Unable to archive asset.'
  } finally {
    isArchiving.value = false
  }
}

onMounted(loadAssets)

watch(
  () => route.query,
  () => {
    applyRouteQueryFilters()
    void loadAssets()
  },
)
</script>

<style scoped>
.assets-page {
  padding: 0 32px 34px;
}

.assets-page__panel {
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

.assets-page__header,
.assets-page__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 20px 22px;
}

.assets-page__ping-result {
  display: flex;
  align-items: center;
  gap: 12px;
  border-top: 1px solid rgba(142, 168, 203, 0.16);
  color: #ffb9c0;
  background: rgba(255, 77, 94, 0.1);
  padding: 14px 22px;
  font-size: 13px;
}

.assets-page__ping-result--success {
  color: #adffe0;
  background: rgba(0, 212, 138, 0.1);
}

.assets-page__header {
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
}

.assets-page__header p {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.assets-page__header h2 {
  margin: 0;
  color: var(--assetops-text);
  font-size: 21px;
}

.assets-page__add,
.assets-page__filter-actions button:last-child,
.assets-page__modal button:last-child {
  border: 1px solid rgba(36, 212, 255, 0.62);
  border-radius: 8px;
  color: #ffffff;
  background: linear-gradient(110deg, #058cff, #123de8);
  padding: 11px 16px;
  font-weight: 800;
  box-shadow: 0 0 18px rgba(0, 132, 255, 0.24);
}

.assets-page__filters {
  display: grid;
  grid-template-columns: minmax(240px, 2fr) repeat(5, minmax(120px, 1fr));
  gap: 14px;
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  padding: 18px 22px;
}

.assets-page__filters label {
  display: grid;
  gap: 7px;
}

.assets-page__filters span {
  color: var(--assetops-muted);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.assets-page__filters input {
  min-height: 42px;
  border: 1px solid var(--assetops-border-muted);
  border-radius: 8px;
  color: var(--assetops-text);
  background: rgba(7, 21, 40, 0.8);
  padding: 0 12px;
  outline: 0;
}

.assets-page__checkbox {
  display: flex !important;
  align-items: center;
  align-self: end;
  flex-direction: row;
  min-height: 42px;
}

.assets-page__checkbox input {
  width: 16px;
  min-height: 16px;
}

.assets-page__filter-actions {
  display: flex;
  align-items: end;
  justify-content: flex-end;
  gap: 10px;
}

.assets-page__filter-actions button,
.assets-page__pagination button,
.assets-page__modal button {
  border: 1px solid rgba(30, 155, 255, 0.32);
  border-radius: 8px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
  padding: 10px 14px;
  cursor: pointer;
  font-weight: 700;
}

.assets-page__filter-actions button:disabled,
.assets-page__pagination button:disabled,
.assets-page__modal button:disabled {
  cursor: not-allowed;
  opacity: 0.54;
}

.assets-page__state {
  display: grid;
  min-height: 240px;
  place-items: center;
  color: var(--assetops-muted);
  font-weight: 700;
}

.assets-page__state--error {
  color: #ffb9c0;
}

.assets-page__footer {
  border-top: 1px solid rgba(142, 168, 203, 0.16);
  color: var(--assetops-muted);
  font-size: 13px;
}

.assets-page__pagination {
  display: flex;
  align-items: center;
  gap: 12px;
}

.assets-page__modal {
  position: fixed;
  z-index: 20;
  inset: 0;
  display: grid;
  place-items: center;
  background: rgba(2, 7, 19, 0.78);
}

.assets-page__modal section {
  width: min(460px, calc(100vw - 32px));
  border: 1px solid var(--assetops-border);
  border-radius: 12px;
  background: var(--assetops-panel-strong);
  padding: 24px;
  box-shadow: var(--assetops-strong-glow);
}

.assets-page__modal h3 {
  margin: 0 0 10px;
}

.assets-page__modal p {
  margin: 0 0 22px;
  color: var(--assetops-muted-strong);
}

.assets-page__modal div {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 1200px) {
  .assets-page__filters {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .assets-page {
    padding: 0 18px 24px;
  }

  .assets-page__header,
  .assets-page__footer {
    align-items: flex-start;
    flex-direction: column;
  }

  .assets-page__filters {
    grid-template-columns: 1fr;
  }
}
</style>
