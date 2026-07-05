<template>
  <section class="master-data-page">
    <div class="master-data-page__panel">
      <header class="master-data-page__header">
        <div>
          <p>Master Data</p>
          <h2>{{ config.title }}</h2>
        </div>
        <button
          type="button"
          @click="startCreate"
        >
          Add {{ config.singular }}
        </button>
      </header>

      <form
        class="master-data-page__filters"
        @submit.prevent="loadRecords"
      >
        <label>
          <span>Search</span>
          <input
            v-model.trim="search"
            placeholder="Code, name or description"
          >
        </label>
        <button type="submit">
          Search
        </button>
      </form>

      <div
        v-if="isLoading"
        class="master-data-page__state"
      >
        Loading {{ config.title.toLowerCase() }}...
      </div>
      <div
        v-else-if="error"
        class="master-data-page__state master-data-page__state--error"
      >
        {{ error }}
      </div>
      <div
        v-else-if="records.length === 0"
        class="master-data-page__state"
      >
        No {{ config.title.toLowerCase() }} found.
      </div>
      <table
        v-else
        class="master-data-page__table"
      >
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Description</th>
            <th>Updated</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="record in records"
            :key="record.id"
          >
            <td>{{ record.code }}</td>
            <td>{{ record.name }}</td>
            <td>{{ record.description || '-' }}</td>
            <td>{{ formatDate(record.updated_at) }}</td>
            <td>
              <div class="master-data-page__actions">
                <button
                  type="button"
                  @click="startEdit(record)"
                >
                  Edit
                </button>
                <button
                  type="button"
                  @click="deleteSelectedRecord(record)"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <footer class="master-data-page__footer">
        <span>{{ count }} records</span>
      </footer>
    </div>

    <Transition name="assetops-modal">
      <div
        v-if="isFormOpen"
        class="master-data-page__modal"
        role="dialog"
        aria-modal="true"
      >
        <form @submit.prevent="saveRecord">
          <h3>{{ editingRecord ? `Edit ${config.singular}` : `Add ${config.singular}` }}</h3>
          <label v-if="editingRecord">
            <span>Code</span>
            <input
              v-model.trim="form.code"
              readonly
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
            <span>Description</span>
            <textarea
              v-model.trim="form.description"
              rows="4"
            />
          </label>
          <p v-if="formError">
            {{ formError }}
          </p>
          <div>
            <button
              type="button"
              @click="closeForm"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isSaving"
            >
              {{ isSaving ? 'Saving...' : `Save ${config.singular}` }}
            </button>
          </div>
        </form>
      </div>
    </Transition>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import {
  createMasterData,
  deleteMasterData,
  fetchMasterData,
  updateMasterData,
  type MasterDataKind,
  type MasterDataPayload,
  type MasterDataRecord,
} from '@/services/masterData'
import { useAuthStore } from '@/stores/auth'

type PageConfig = {
  kind: MasterDataKind
  title: string
  singular: string
}

const configs: Record<string, PageConfig> = {
  'asset-types': { kind: 'asset-types', title: 'Asset Types', singular: 'Asset Type' },
  vendors: { kind: 'vendors', title: 'Vendors', singular: 'Vendor' },
  'device-types': { kind: 'device-types', title: 'Device Types', singular: 'Device Type' },
  locations: { kind: 'locations', title: 'Locations', singular: 'Location' },
}

const route = useRoute()
const authStore = useAuthStore()
const records = ref<MasterDataRecord[]>([])
const count = ref(0)
const search = ref('')
const error = ref<string | null>(null)
const formError = ref<string | null>(null)
const isLoading = ref(false)
const isSaving = ref(false)
const isFormOpen = ref(false)
const editingRecord = ref<MasterDataRecord | null>(null)

const config = computed(() => configs[String(route.params.kind)] ?? configs['asset-types'])

const emptyForm = (): MasterDataPayload => ({
  code: '',
  name: '',
  description: '',
})

const form = reactive<MasterDataPayload>(emptyForm())

const loadRecords = async () => {
  if (!authStore.accessToken) {
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const response = await fetchMasterData(
      config.value.kind,
      {
        search: search.value,
        ordering: 'code',
        page_size: 100,
      },
      authStore.accessToken,
    )
    records.value = response.results
    count.value = response.count
  } catch (loadError) {
    error.value = loadError instanceof Error ? loadError.message : `Unable to load ${config.value.title}.`
  } finally {
    isLoading.value = false
  }
}

const startCreate = () => {
  editingRecord.value = null
  Object.assign(form, emptyForm())
  formError.value = null
  isFormOpen.value = true
}

const startEdit = (record: MasterDataRecord) => {
  editingRecord.value = record
  Object.assign(form, {
    code: record.code,
    name: record.name,
    description: record.description,
  })
  formError.value = null
  isFormOpen.value = true
}

const closeForm = () => {
  isFormOpen.value = false
  editingRecord.value = null
  formError.value = null
}

const saveRecord = async () => {
  if (!authStore.accessToken) {
    return
  }

  isSaving.value = true
  formError.value = null

  try {
    const payload: MasterDataPayload = {
      name: form.name,
      description: form.description,
    }

    if (editingRecord.value) {
      payload.code = form.code
      await updateMasterData(config.value.kind, editingRecord.value.id, payload, authStore.accessToken)
    } else {
      await createMasterData(config.value.kind, payload, authStore.accessToken)
    }

    closeForm()
    await loadRecords()
  } catch (saveError) {
    formError.value = saveError instanceof Error ? saveError.message : `Unable to save ${config.value.singular}.`
  } finally {
    isSaving.value = false
  }
}

const deleteSelectedRecord = async (record: MasterDataRecord) => {
  if (!authStore.accessToken || !globalThis.confirm(`Delete ${config.value.singular} ${record.code}?`)) {
    return
  }

  try {
    await deleteMasterData(config.value.kind, record.id, authStore.accessToken)
    await loadRecords()
  } catch (deleteError) {
    error.value = deleteError instanceof Error ? deleteError.message : `Unable to delete ${config.value.singular}.`
  }
}

const formatDate = (value: string) =>
  new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
  }).format(new Date(value))

watch(
  () => route.params.kind,
  () => {
    closeForm()
    search.value = ''
    void loadRecords()
  },
)

onMounted(loadRecords)
</script>

<style scoped>
.master-data-page {
  padding: 0 32px 34px;
}

.master-data-page__panel {
  overflow: hidden;
  border: 1px solid rgba(30, 155, 255, 0.34);
  border-radius: 12px;
  background:
    linear-gradient(145deg, rgba(13, 33, 56, 0.82), rgba(3, 10, 24, 0.95)),
    var(--assetops-panel);
  box-shadow:
    var(--assetops-glow),
    inset 0 0 42px rgba(18, 107, 255, 0.06);
  transition:
    border-color var(--assetops-motion-standard) var(--assetops-ease-standard),
    box-shadow var(--assetops-motion-standard) var(--assetops-ease-standard);
}

.master-data-page__panel:hover {
  border-color: rgba(0, 216, 255, 0.42);
}

.master-data-page__header,
.master-data-page__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 20px 22px;
}

.master-data-page__header {
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
}

.master-data-page__header p {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.master-data-page__header h2,
.master-data-page__modal h3 {
  margin: 0;
  color: var(--assetops-text);
}

.master-data-page__header button,
.master-data-page__filters button,
.master-data-page__modal button:last-child {
  border: 1px solid rgba(36, 212, 255, 0.62);
  border-radius: 8px;
  color: #ffffff;
  background: linear-gradient(110deg, #058cff, #123de8);
  padding: 11px 16px;
  font-weight: 800;
  box-shadow: 0 0 18px rgba(0, 132, 255, 0.24);
}

.master-data-page__filters {
  display: grid;
  grid-template-columns: minmax(240px, 1fr) auto;
  gap: 14px;
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  padding: 18px 22px;
}

.master-data-page label {
  display: grid;
  gap: 7px;
}

.master-data-page span {
  color: var(--assetops-muted);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.master-data-page input,
.master-data-page textarea {
  border: 1px solid var(--assetops-border-muted);
  border-radius: 8px;
  color: var(--assetops-text);
  background: rgba(7, 21, 40, 0.8);
  padding: 12px;
  outline: 0;
}

.master-data-page input:focus,
.master-data-page textarea:focus {
  border-color: var(--assetops-cyan);
  box-shadow: 0 0 16px rgba(0, 216, 255, 0.18);
}

.master-data-page__table {
  width: 100%;
  border-collapse: collapse;
}

.master-data-page__table th,
.master-data-page__table td {
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  padding: 14px 16px;
  text-align: left;
}

.master-data-page__table th {
  color: var(--assetops-muted);
  background: rgba(10, 26, 45, 0.8);
  font-size: 12px;
  text-transform: uppercase;
}

.master-data-page__table td {
  color: var(--assetops-muted-strong);
  font-size: 14px;
}

.master-data-page__table tbody tr {
  transition:
    background var(--assetops-motion-standard) var(--assetops-ease-standard),
    box-shadow var(--assetops-motion-standard) var(--assetops-ease-standard);
}

.master-data-page__table tbody tr:hover {
  background: rgba(10, 132, 255, 0.07);
  box-shadow: inset 2px 0 0 rgba(0, 216, 255, 0.52);
}

.master-data-page__actions {
  display: flex;
  gap: 10px;
}

.master-data-page__actions button,
.master-data-page__modal button:first-child {
  border: 1px solid rgba(30, 155, 255, 0.32);
  border-radius: 8px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
  padding: 9px 12px;
  cursor: pointer;
  font-weight: 700;
}

.master-data-page button:not(:disabled):hover,
.master-data-page button:not(:disabled):focus-visible {
  border-color: var(--assetops-cyan);
  box-shadow: 0 0 18px rgba(0, 132, 255, 0.18);
  outline: 0;
}

.master-data-page__state {
  display: grid;
  min-height: 240px;
  place-items: center;
  color: var(--assetops-muted);
  font-weight: 700;
}

.master-data-page__state--error,
.master-data-page__modal p {
  color: #ffb9c0;
}

.master-data-page__footer {
  color: var(--assetops-muted);
  font-size: 13px;
}

.master-data-page__modal {
  position: fixed;
  z-index: 20;
  inset: 0;
  display: grid;
  place-items: center;
  background: rgba(2, 7, 19, 0.78);
}

.master-data-page__modal form {
  display: grid;
  width: min(520px, calc(100vw - 32px));
  gap: 16px;
  border: 1px solid var(--assetops-border);
  border-radius: 12px;
  background: var(--assetops-panel-strong);
  padding: 24px;
  box-shadow: var(--assetops-strong-glow);
}

.master-data-page__modal div {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (prefers-reduced-motion: reduce) {
  .master-data-page__panel,
  .master-data-page__table tbody tr {
    transition: none;
  }
}

@media (max-width: 720px) {
  .master-data-page {
    padding: 0 18px 24px;
  }

  .master-data-page__filters,
  .master-data-page__header {
    grid-template-columns: 1fr;
  }
}
</style>
