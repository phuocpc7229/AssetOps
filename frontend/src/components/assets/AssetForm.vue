<template>
  <form
    class="asset-form"
    @submit.prevent="submit"
  >
    <div class="asset-form__grid">
      <label>
        <span>Asset Tag</span>
        <input
          v-model.trim="form.asset_tag"
          required
        >
      </label>

      <label>
        <span>Name</span>
        <input
          v-model.trim="form.name"
          required
        >
      </label>

      <label>
        <span>Hostname</span>
        <input v-model.trim="form.hostname">
      </label>

      <label>
        <span>Asset Type</span>
        <div class="asset-form__lookup">
          <input
            v-model.trim="assetTypeSearch"
            placeholder="Search asset types"
          >
          <select
            v-model="form.asset_type_id"
            required
          >
            <option
              disabled
              :value="null"
            >
              Select asset type
            </option>
            <option
              v-for="assetType in filteredAssetTypes"
              :key="assetType.id"
              :value="assetType.id"
            >
              {{ assetType.code }} - {{ assetType.name }}
            </option>
          </select>
        </div>
      </label>

      <label>
        <span>Vendor</span>
        <div class="asset-form__lookup">
          <input
            v-model.trim="vendorSearch"
            placeholder="Search vendors"
          >
          <select v-model="form.vendor_id">
            <option :value="null">No Vendor</option>
            <option
              v-for="vendor in filteredVendors"
              :key="vendor.id"
              :value="vendor.id"
            >
              {{ vendor.code }} - {{ vendor.name }}
            </option>
          </select>
        </div>
      </label>

      <label>
        <span>Model</span>
        <input v-model.trim="form.model">
      </label>

      <label>
        <span>Serial Number</span>
        <input v-model.trim="form.serial_number">
      </label>

      <label>
        <span>IP Address</span>
        <input v-model.trim="form.ip_address">
      </label>

      <label>
        <span>MAC Address</span>
        <input v-model.trim="form.mac_address">
      </label>

      <label>
        <span>Site</span>
        <select v-model="form.site_id">
          <option :value="null">No Site</option>
          <option
            v-for="site in sites"
            :key="site.id"
            :value="site.id"
          >
            {{ site.code }} - {{ site.name }}
          </option>
        </select>
      </label>

      <label>
        <span>Location</span>
        <div class="asset-form__lookup">
          <input
            v-model.trim="locationSearch"
            placeholder="Search locations"
          >
          <select v-model="form.location_id">
            <option :value="null">No Location</option>
            <option
              v-for="location in filteredLocations"
              :key="location.id"
              :value="location.id"
            >
              {{ location.code }} - {{ location.name }}
            </option>
          </select>
        </div>
      </label>

      <label>
        <span>Status</span>
        <select v-model="form.status">
          <option value="active">Active</option>
          <option value="in_maintenance">In Maintenance</option>
          <option value="archived">Archived</option>
        </select>
      </label>

      <label>
        <span>Criticality</span>
        <select v-model="form.criticality">
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
      </label>

      <label>
        <span>Warranty Starts On</span>
        <input
          v-model="form.warranty_starts_on"
          type="date"
        >
      </label>

      <label>
        <span>Warranty Expires On</span>
        <input
          v-model="form.warranty_expires_on"
          type="date"
        >
      </label>

      <label>
        <span>Purchase Date</span>
        <input
          v-model="form.purchase_date"
          type="date"
        >
      </label>
    </div>

    <label class="asset-form__notes">
      <span>Notes</span>
      <textarea
        v-model.trim="form.notes"
        rows="5"
      />
    </label>

    <p
      v-if="error"
      class="asset-form__error"
    >
      {{ error }}
    </p>

    <div class="asset-form__actions">
      <button
        type="button"
        class="asset-form__secondary"
        @click="$emit('cancel')"
      >
        Cancel
      </button>
      <button
        type="submit"
        class="asset-form__primary"
        :disabled="isSubmitting"
      >
        {{ isSubmitting ? 'Saving...' : submitLabel }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'

import type { Asset, AssetPayload } from '@/services/assets'
import type { MasterDataRecord } from '@/services/masterData'
import type { Site } from '@/services/sites'

const props = withDefaults(
  defineProps<{
    asset?: Asset | null
    error?: string | null
    isSubmitting?: boolean
    submitLabel?: string
    sites?: Site[]
    assetTypes?: MasterDataRecord[]
    vendors?: MasterDataRecord[]
    locations?: MasterDataRecord[]
  }>(),
  {
    asset: null,
    error: null,
    isSubmitting: false,
    submitLabel: 'Save Asset',
    sites: () => [],
    assetTypes: () => [],
    vendors: () => [],
    locations: () => [],
  },
)

const emit = defineEmits<{
  cancel: []
  submit: [payload: AssetPayload]
}>()

const emptyForm = (): AssetPayload => ({
  asset_tag: '',
  name: '',
  hostname: '',
  asset_type_id: null,
  vendor_id: null,
  model: '',
  serial_number: '',
  ip_address: null,
  mac_address: '',
  site_id: null,
  location_id: null,
  status: 'active',
  criticality: 'medium',
  warranty_starts_on: null,
  warranty_expires_on: null,
  purchase_date: null,
  notes: '',
})

const form = reactive<AssetPayload>(emptyForm())
const assetTypeSearch = ref('')
const vendorSearch = ref('')
const locationSearch = ref('')

const applyAsset = (asset: Asset | null) => {
  Object.assign(form, emptyForm())
  if (asset) {
    Object.assign(form, {
      asset_tag: asset.asset_tag,
      name: asset.name,
      hostname: asset.hostname,
      model: asset.model,
      serial_number: asset.serial_number,
      ip_address: asset.ip_address,
      mac_address: asset.mac_address,
      status: asset.status,
      criticality: asset.criticality,
      warranty_starts_on: asset.warranty_starts_on,
      warranty_expires_on: asset.warranty_expires_on,
      purchase_date: asset.purchase_date,
      notes: asset.notes,
    })
  }
  form.asset_type_id = asset?.asset_type?.id ?? null
  form.vendor_id = asset?.vendor?.id ?? null
  form.site_id = asset?.site?.id ?? null
  form.location_id = asset?.location?.id ?? null
}

watch(
  () => props.asset,
  (asset) => applyAsset(asset),
  { immediate: true },
)

const normalizePayload = (): AssetPayload => ({
  ...form,
  ip_address: form.ip_address || null,
  warranty_starts_on: form.warranty_starts_on || null,
  warranty_expires_on: form.warranty_expires_on || null,
  purchase_date: form.purchase_date || null,
})

const filterRecords = (records: MasterDataRecord[], search: string) => {
  const normalizedSearch = search.trim().toLowerCase()
  if (!normalizedSearch) {
    return records
  }

  return records.filter((record) =>
    `${record.code} ${record.name}`.toLowerCase().includes(normalizedSearch),
  )
}

const filteredAssetTypes = computed(() => filterRecords(props.assetTypes, assetTypeSearch.value))
const filteredVendors = computed(() => filterRecords(props.vendors, vendorSearch.value))
const filteredLocations = computed(() => filterRecords(props.locations, locationSearch.value))

const submit = () => {
  emit('submit', normalizePayload())
}
</script>

<style scoped>
.asset-form {
  display: grid;
  gap: 22px;
}

.asset-form__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.asset-form label {
  display: grid;
  gap: 8px;
}

.asset-form span {
  color: var(--assetops-text);
  font-size: 13px;
  font-weight: 700;
}

.asset-form input,
.asset-form select,
.asset-form textarea {
  width: 100%;
  border: 1px solid var(--assetops-border-muted);
  border-radius: 8px;
  color: var(--assetops-text);
  background: linear-gradient(145deg, rgba(13, 33, 56, 0.74), rgba(6, 15, 30, 0.9));
  padding: 12px 14px;
  outline: 0;
}

.asset-form textarea {
  resize: vertical;
}

.asset-form__lookup {
  display: grid;
  gap: 8px;
}

.asset-form input:focus,
.asset-form select:focus,
.asset-form textarea:focus {
  border-color: var(--assetops-cyan);
  box-shadow: 0 0 16px rgba(0, 216, 255, 0.18);
}

.asset-form__notes {
  grid-column: 1 / -1;
}

.asset-form__error {
  margin: 0;
  border: 1px solid rgba(255, 77, 94, 0.38);
  border-radius: 8px;
  color: #ffb9c0;
  background: rgba(255, 77, 94, 0.1);
  padding: 12px 14px;
}

.asset-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.asset-form__primary,
.asset-form__secondary {
  min-height: 44px;
  border-radius: 8px;
  padding: 0 18px;
  cursor: pointer;
  font-weight: 700;
}

.asset-form__primary {
  border: 1px solid rgba(36, 212, 255, 0.62);
  color: #ffffff;
  background: linear-gradient(110deg, #058cff, #123de8);
  box-shadow: 0 0 22px rgba(0, 132, 255, 0.28);
}

.asset-form__primary:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.asset-form__secondary {
  border: 1px solid rgba(30, 155, 255, 0.32);
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
}

@media (max-width: 760px) {
  .asset-form__grid {
    grid-template-columns: 1fr;
  }
}
</style>
