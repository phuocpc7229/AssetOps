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
        <SearchableSelect
          v-model="form.asset_type_id"
          :options="assetTypeOptions"
          placeholder="Select asset type"
          search-placeholder="Search asset types"
          :error="fieldErrors.asset_type_id"
        />
      </label>

      <label>
        <span>Vendor</span>
        <SearchableSelect
          v-model="form.vendor_id"
          :options="vendorOptions"
          placeholder="Select vendor"
          search-placeholder="Search vendors"
          clearable
        />
      </label>

      <label>
        <span>Model</span>
        <input v-model.trim="form.model">
      </label>

      <label>
        <span>Serial Number</span>
        <input v-model.trim="form.serial_number">
      </label>

      <section class="asset-form__ip-section">
        <div class="asset-form__ip-header">
          <span>IP Addresses</span>
          <button
            type="button"
            @click="addIpRow"
          >
            Add IP Row
          </button>
        </div>
        <div
          v-for="(row, index) in ipRows"
          :key="row.key"
          class="asset-form__ip-row"
        >
          <label>
            <span>IP Address</span>
            <input
              v-model.trim="row.address"
              placeholder="Enter IP address"
            >
            <small v-if="row.error">{{ row.error }}</small>
          </label>
          <button
            type="button"
            class="asset-form__primary-toggle"
            :class="{ 'asset-form__primary-toggle--active': row.is_primary }"
            @click="setPrimaryIp(index)"
          >
            {{ row.is_primary ? 'Primary' : 'Set Primary' }}
          </button>
          <button
            type="button"
            class="asset-form__remove-ip"
            :disabled="ipRows.length === 1"
            @click="removeIpRow(index)"
          >
            Remove
          </button>
        </div>
      </section>

      <label>
        <span>MAC Address</span>
        <input v-model.trim="form.mac_address">
      </label>

      <label>
        <span>Site</span>
        <SearchableSelect
          v-model="form.site_id"
          :options="siteOptions"
          placeholder="Select site"
          search-placeholder="Search sites"
          :error="fieldErrors.site_id"
        />
      </label>

      <label>
        <span>Location</span>
        <SearchableSelect
          v-model="form.location_id"
          :options="locationOptions"
          placeholder="Select location"
          search-placeholder="Search locations"
          clearable
        />
      </label>

      <label>
        <span>Status</span>
        <SearchableSelect
          v-model="form.status"
          :options="statusOptions"
          placeholder="Select status"
          search-placeholder="Search statuses"
        />
      </label>

      <label>
        <span>Criticality</span>
        <SearchableSelect
          v-model="form.criticality"
          :options="criticalityOptions"
          placeholder="Select criticality"
          search-placeholder="Search criticality"
        />
      </label>

      <label>
        <span>Warranty Starts On</span>
        <div class="asset-form__date">
          <input
            v-model.trim="dateForm.warranty_starts_on"
            placeholder="dd/mm/yyyy"
          >
          <button
            type="button"
            aria-label="Open warranty start calendar"
            @click="openDatePicker('warranty_starts_on')"
          >
            <span aria-hidden="true" />
          </button>
          <input
            ref="warrantyStartsPicker"
            class="asset-form__native-date"
            type="date"
            min="1990-01-01"
            max="2050-12-31"
            :value="displayDateToIso(dateForm.warranty_starts_on) ?? ''"
            @input="setDateFromPicker('warranty_starts_on', $event)"
          >
        </div>
        <small v-if="fieldErrors.warranty_starts_on">{{ fieldErrors.warranty_starts_on }}</small>
      </label>

      <label>
        <span>Warranty Expires On</span>
        <div class="asset-form__date">
          <input
            v-model.trim="dateForm.warranty_expires_on"
            placeholder="dd/mm/yyyy"
          >
          <button
            type="button"
            aria-label="Open warranty expiry calendar"
            @click="openDatePicker('warranty_expires_on')"
          >
            <span aria-hidden="true" />
          </button>
          <input
            ref="warrantyExpiresPicker"
            class="asset-form__native-date"
            type="date"
            min="1990-01-01"
            max="2050-12-31"
            :value="displayDateToIso(dateForm.warranty_expires_on) ?? ''"
            @input="setDateFromPicker('warranty_expires_on', $event)"
          >
        </div>
        <small v-if="fieldErrors.warranty_expires_on">{{ fieldErrors.warranty_expires_on }}</small>
      </label>

      <label>
        <span>Purchase Date</span>
        <div class="asset-form__date">
          <input
            v-model.trim="dateForm.purchase_date"
            placeholder="dd/mm/yyyy"
          >
          <button
            type="button"
            aria-label="Open purchase date calendar"
            @click="openDatePicker('purchase_date')"
          >
            <span aria-hidden="true" />
          </button>
          <input
            ref="purchaseDatePicker"
            class="asset-form__native-date"
            type="date"
            min="1990-01-01"
            max="2050-12-31"
            :value="displayDateToIso(dateForm.purchase_date) ?? ''"
            @input="setDateFromPicker('purchase_date', $event)"
          >
        </div>
        <small v-if="fieldErrors.purchase_date">{{ fieldErrors.purchase_date }}</small>
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

import SearchableSelect from '@/components/ui/SearchableSelect.vue'
import type { Asset, AssetIPAddress, AssetPayload } from '@/services/assets'
import { displayDateToIso, isoToDisplayDate } from '@/services/dates'
import type { MasterDataRecord } from '@/services/masterData'
import type { Site } from '@/services/sites'

type SearchableSelectOption = {
  id: number | string
  label: string
  detail?: string
}

type IpRow = {
  key: number
  address: string
  is_primary: boolean
  error: string | null
}

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
  ip_addresses: [],
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
const ipRows = ref<IpRow[]>([])
let nextIpRowKey = 1
const dateForm = reactive({
  warranty_starts_on: '',
  warranty_expires_on: '',
  purchase_date: '',
})
const fieldErrors = reactive<Record<string, string | null>>({
  asset_type_id: null,
  site_id: null,
  warranty_starts_on: null,
  warranty_expires_on: null,
  purchase_date: null,
})
const warrantyStartsPicker = ref<{ showPicker?: () => void; click: () => void } | null>(null)
const warrantyExpiresPicker = ref<{ showPicker?: () => void; click: () => void } | null>(null)
const purchaseDatePicker = ref<{ showPicker?: () => void; click: () => void } | null>(null)
const minDate = '1990-01-01'
const maxDate = '2050-12-31'

const toOption = (record: MasterDataRecord): SearchableSelectOption => ({
  id: record.id,
  label: record.name,
  detail: record.code,
})

const assetTypeOptions = computed(() => props.assetTypes.map(toOption))
const vendorOptions = computed(() => props.vendors.map(toOption))
const locationOptions = computed(() => props.locations.map(toOption))
const statusOptions: SearchableSelectOption[] = [
  { id: 'active', label: 'Active' },
  { id: 'in_maintenance', label: 'In Maintenance' },
  { id: 'archived', label: 'Archived' },
]
const criticalityOptions: SearchableSelectOption[] = [
  { id: 'low', label: 'Low' },
  { id: 'medium', label: 'Medium' },
  { id: 'high', label: 'High' },
  { id: 'critical', label: 'Critical' },
]
const siteOptions = computed(() =>
  props.sites.map((site) => ({
    id: site.id,
    label: site.name,
    detail: site.code,
  })),
)

const createIpRow = (ipAddress?: Partial<AssetIPAddress>): IpRow => ({
  key: nextIpRowKey,
  address: ipAddress?.address ?? '',
  is_primary: Boolean(ipAddress?.is_primary),
  error: null,
})

const resetIpRows = (ipAddresses: AssetIPAddress[] = []) => {
  nextIpRowKey = 1
  const rows = ipAddresses
    .filter((ipAddress) => ipAddress.address)
    .map((ipAddress) => {
      const row = createIpRow(ipAddress)
      nextIpRowKey += 1
      return row
    })

  if (rows.length === 0) {
    rows.push(createIpRow({ is_primary: true }))
    nextIpRowKey += 1
  }

  if (rows.every((row) => !row.is_primary)) {
    rows[0].is_primary = true
  }

  ipRows.value = rows
}

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
      ip_addresses: asset.ip_addresses ?? [],
      mac_address: asset.mac_address,
      status: asset.status,
      criticality: asset.criticality,
      notes: asset.notes,
    })
  }
  form.asset_type_id = asset?.asset_type?.id ?? null
  form.vendor_id = asset?.vendor?.id ?? null
  form.site_id = asset?.site?.id ?? null
  form.location_id = asset?.location?.id ?? null
  dateForm.warranty_starts_on = isoToDisplayDate(asset?.warranty_starts_on ?? null)
  dateForm.warranty_expires_on = isoToDisplayDate(asset?.warranty_expires_on ?? null)
  dateForm.purchase_date = isoToDisplayDate(asset?.purchase_date ?? null)
  resetIpRows(asset?.ip_addresses?.length ? asset.ip_addresses : asset?.ip_address ? [{ address: asset.ip_address, is_primary: true }] : [])
}

watch(
  () => props.asset,
  (asset) => applyAsset(asset),
  { immediate: true },
)

const clearFieldErrors = () => {
  Object.keys(fieldErrors).forEach((key) => {
    fieldErrors[key] = null
  })
}

const datePickers = {
  warranty_starts_on: warrantyStartsPicker,
  warranty_expires_on: warrantyExpiresPicker,
  purchase_date: purchaseDatePicker,
}

const openDatePicker = (field: keyof typeof datePickers) => {
  const picker = datePickers[field].value
  if (!picker) {
    return
  }

  if (picker.showPicker) {
    picker.showPicker()
    return
  }

  picker.click()
}

const setDateFromPicker = (field: keyof typeof dateForm, event: { target: unknown }) => {
  const target = event.target as { value?: string } | null
  dateForm[field] = isoToDisplayDate(target?.value ?? null)
}

const addIpRow = () => {
  ipRows.value.push(createIpRow())
  nextIpRowKey += 1
}

const removeIpRow = (index: number) => {
  const removedPrimary = ipRows.value[index]?.is_primary
  ipRows.value.splice(index, 1)

  if (ipRows.value.length === 0) {
    resetIpRows()
    return
  }

  if (removedPrimary && ipRows.value.every((row) => !row.is_primary)) {
    ipRows.value[0].is_primary = true
  }
}

const setPrimaryIp = (index: number) => {
  ipRows.value.forEach((row, rowIndex) => {
    row.is_primary = rowIndex === index
  })
}

const isValidIpAddress = (value: string) => {
  const ipv4Parts = value.split('.')
  if (
    ipv4Parts.length === 4 &&
    ipv4Parts.every((part) => /^\d+$/.test(part) && Number(part) >= 0 && Number(part) <= 255)
  ) {
    return true
  }

  return value.includes(':') && /^[0-9A-Fa-f:]+$/.test(value)
}

const parseDateField = (field: keyof typeof dateForm, label: string) => {
  if (!dateForm[field]) {
    return null
  }

  const value = displayDateToIso(dateForm[field])
  if (!value) {
    fieldErrors[field] = `${label} must use dd/mm/yyyy.`
    return null
  }

  if (value < minDate || value > maxDate) {
    fieldErrors[field] = `${label} must be between 01/01/1990 and 31/12/2050.`
  }

  return value
}

const normalizeIpRows = () => {
  const seenAddresses = new Set<string>()
  const rows = ipRows.value
    .map((row) => {
      row.error = null
      return {
        row,
        address: row.address.trim(),
      }
    })
    .filter(({ address }) => address)

  rows.forEach(({ row, address }) => {
    if (!isValidIpAddress(address)) {
      row.error = 'Enter a valid IP address.'
      return
    }

    if (seenAddresses.has(address)) {
      row.error = 'Duplicate IP addresses are not allowed.'
      return
    }

    seenAddresses.add(address)
  })

  if (rows.some(({ row }) => row.error)) {
    return null
  }

  if (rows.length === 0) {
    return []
  }

  if (rows.every(({ row }) => !row.is_primary)) {
    rows[0].row.is_primary = true
  }

  return rows.map(({ row, address }) => ({
    address,
    is_primary: row.is_primary,
  }))
}

const normalizePayload = (): AssetPayload | null => {
  clearFieldErrors()

  if (!form.asset_type_id) {
    fieldErrors.asset_type_id = 'Select an asset type.'
  }

  if (!form.site_id) {
    fieldErrors.site_id = 'Select a site.'
  }

  const warrantyStartsOn = parseDateField('warranty_starts_on', 'Warranty start date')
  const warrantyExpiresOn = parseDateField('warranty_expires_on', 'Warranty expiry date')
  const purchaseDate = parseDateField('purchase_date', 'Purchase date')
  const normalizedIpRows = normalizeIpRows()

  if (warrantyStartsOn && warrantyExpiresOn && warrantyExpiresOn < warrantyStartsOn) {
    fieldErrors.warranty_expires_on = 'Warranty expiry cannot be before warranty start.'
  }

  if (purchaseDate && purchaseDate > new Date().toISOString().slice(0, 10)) {
    fieldErrors.purchase_date = 'Purchase date cannot be in the future.'
  }

  if (Object.values(fieldErrors).some(Boolean) || normalizedIpRows === null) {
    return null
  }

  const primaryIpAddress = normalizedIpRows.find((row) => row.is_primary)?.address ?? normalizedIpRows[0]?.address ?? null

  return {
    ...form,
    ip_address: primaryIpAddress,
    ip_addresses: normalizedIpRows,
    warranty_starts_on: warrantyStartsOn,
    warranty_expires_on: warrantyExpiresOn,
    purchase_date: purchaseDate,
  }
}

const submit = () => {
  const payload = normalizePayload()
  if (payload) {
    emit('submit', payload)
  }
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

.asset-form small {
  color: #ffb9c0;
  font-size: 12px;
  font-weight: 700;
}

.asset-form input,
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

.asset-form input:focus,
.asset-form textarea:focus {
  border-color: var(--assetops-cyan);
  box-shadow: 0 0 16px rgba(0, 216, 255, 0.18);
}

.asset-form__date {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 44px;
  gap: 8px;
}

.asset-form__ip-section {
  display: grid;
  grid-column: 1 / -1;
  gap: 14px;
  border: 1px solid rgba(30, 155, 255, 0.22);
  border-radius: 10px;
  background: rgba(7, 21, 40, 0.34);
  padding: 16px;
}

.asset-form__ip-header,
.asset-form__ip-row {
  display: grid;
  align-items: end;
  gap: 12px;
}

.asset-form__ip-header {
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
}

.asset-form__ip-row {
  grid-template-columns: minmax(260px, 1fr) 132px 104px;
  border-top: 1px solid rgba(142, 168, 203, 0.12);
  padding-top: 12px;
}

.asset-form__ip-row input::placeholder {
  color: rgba(154, 178, 212, 0.58);
}

.asset-form__ip-header button,
.asset-form__primary-toggle,
.asset-form__remove-ip {
  min-height: 45px;
  border: 1px solid rgba(30, 155, 255, 0.32);
  border-radius: 8px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
  padding: 0 12px;
  cursor: pointer;
  font-weight: 700;
  white-space: nowrap;
}

.asset-form__primary-toggle--active {
  border-color: rgba(36, 212, 255, 0.62);
  color: #ffffff;
  background: linear-gradient(110deg, #058cff, #123de8);
  box-shadow: 0 0 18px rgba(0, 132, 255, 0.24);
}

.asset-form__remove-ip {
  color: #ffb9c0;
}

.asset-form__remove-ip:disabled {
  cursor: not-allowed;
  opacity: 0.54;
}

.asset-form__date button {
  position: relative;
  display: grid;
  min-height: 45px;
  place-items: center;
  border: 1px solid var(--assetops-border-muted);
  border-radius: 8px;
  background: rgba(7, 21, 40, 0.72);
  cursor: pointer;
}

.asset-form__date button:focus {
  border-color: var(--assetops-cyan);
  box-shadow: 0 0 16px rgba(0, 216, 255, 0.18);
  outline: 0;
}

.asset-form__date button span {
  position: relative;
  width: 18px;
  height: 18px;
  border: 2px solid var(--assetops-cyan);
  border-radius: 4px;
}

.asset-form__date button span::before,
.asset-form__date button span::after {
  position: absolute;
  left: 2px;
  right: 2px;
  content: "";
}

.asset-form__date button span::before {
  top: 4px;
  border-top: 2px solid var(--assetops-cyan);
}

.asset-form__date button span::after {
  top: -5px;
  height: 4px;
  border: 2px solid var(--assetops-cyan);
  border-width: 0 2px;
}

.asset-form__native-date {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 1px !important;
  height: 1px;
  opacity: 0;
  pointer-events: none;
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

  .asset-form__ip-row {
    grid-template-columns: 1fr;
  }
}
</style>
