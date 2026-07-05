<template>
  <section class="asset-form-page">
    <div class="asset-form-page__panel">
      <header>
        <div>
          <p>Asset Management</p>
          <h2>{{ isEditMode ? 'Edit Asset' : 'Add Asset' }}</h2>
        </div>
        <RouterLink :to="{ name: 'assets' }">
          Back to Assets
        </RouterLink>
      </header>

      <div
        v-if="isLoading"
        class="asset-form-page__state"
      >
        Loading asset...
      </div>
      <AssetForm
        v-else
        :asset="asset"
        :error="error"
        :is-submitting="isSubmitting"
        :asset-types="assetTypes"
        :vendors="vendors"
        :sites="sites"
        :locations="locations"
        :submit-label="isEditMode ? 'Update Asset' : 'Create Asset'"
        @cancel="router.push({ name: 'assets' })"
        @submit="saveAsset"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import AssetForm from '@/components/assets/AssetForm.vue'
import { useAuthStore } from '@/stores/auth'
import { createAsset, fetchAsset, updateAsset, type Asset, type AssetPayload } from '@/services/assets'
import { fetchMasterData, type MasterDataRecord } from '@/services/masterData'
import { fetchAllPages } from '@/services/pagination'
import { fetchSites, type Site } from '@/services/sites'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const asset = ref<Asset | null>(null)
const error = ref<string | null>(null)
const isLoading = ref(false)
const isSubmitting = ref(false)
const assetTypes = ref<MasterDataRecord[]>([])
const vendors = ref<MasterDataRecord[]>([])
const sites = ref<Site[]>([])
const locations = ref<MasterDataRecord[]>([])

const assetId = computed(() => Number(route.params.id))
const isEditMode = computed(() => route.name === 'asset-edit')

const loadAsset = async () => {
  if (!authStore.accessToken) {
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const token = authStore.accessToken
    const [assetTypeRecords, vendorRecords, siteRecords, locationRecords] = await Promise.all([
      fetchAllPages((params) => fetchMasterData('asset-types', params, token), { ordering: 'code' }),
      fetchAllPages((params) => fetchMasterData('vendors', params, token), { ordering: 'code' }),
      fetchAllPages((params) => fetchSites(params, token), { ordering: 'code' }),
      fetchAllPages((params) => fetchMasterData('locations', params, token), { ordering: 'code' }),
    ])
    assetTypes.value = assetTypeRecords
    vendors.value = vendorRecords
    sites.value = siteRecords
    locations.value = locationRecords

    if (isEditMode.value) {
      asset.value = await fetchAsset(assetId.value, token)
    }
  } catch (loadError) {
    error.value = loadError instanceof Error ? loadError.message : 'Unable to load asset form.'
  } finally {
    isLoading.value = false
  }
}

const saveAsset = async (payload: AssetPayload) => {
  if (!authStore.accessToken) {
    return
  }

  isSubmitting.value = true
  error.value = null

  try {
    if (isEditMode.value) {
      await updateAsset(assetId.value, payload, authStore.accessToken)
    } else {
      await createAsset(payload, authStore.accessToken)
    }

    router.push({ name: 'assets' })
  } catch (saveError) {
    error.value = saveError instanceof Error ? saveError.message : 'Unable to save asset.'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(loadAsset)
</script>

<style scoped>
.asset-form-page {
  padding: 0 32px 34px;
}

.asset-form-page__panel {
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

.asset-form-page header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 24px;
}

.asset-form-page header p {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.asset-form-page header h2 {
  margin: 0;
  color: var(--assetops-text);
  font-size: 21px;
}

.asset-form-page header a {
  border: 1px solid rgba(30, 155, 255, 0.32);
  border-radius: 8px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
  padding: 10px 14px;
  font-weight: 700;
}

.asset-form-page__state {
  display: grid;
  min-height: 240px;
  place-items: center;
  color: var(--assetops-muted);
  font-weight: 700;
}

@media (max-width: 720px) {
  .asset-form-page {
    padding: 0 18px 24px;
  }

  .asset-form-page header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
