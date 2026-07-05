<template>
  <section class="sites-page">
    <div class="sites-page__panel">
      <header class="sites-page__header">
        <div>
          <p>Site Management</p>
          <h2>Sites</h2>
        </div>
        <button
          type="button"
          :disabled="isActionPending"
          @click="startCreate"
        >
          Add Site
        </button>
      </header>

      <form
        class="sites-page__filters"
        @submit.prevent="loadSites"
      >
        <label>
          <span>Search</span>
          <input
            v-model.trim="search"
            placeholder="Code, name or address"
            :disabled="isLoading"
          >
        </label>
        <button
          type="submit"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Searching...' : 'Search' }}
        </button>
      </form>

      <p
        v-if="successMessage"
        class="sites-page__feedback sites-page__feedback--success"
      >
        {{ successMessage }}
      </p>
      <p
        v-if="error"
        class="sites-page__feedback sites-page__feedback--error"
      >
        {{ error }}
      </p>

      <div
        v-if="isLoading"
        class="sites-page__state"
      >
        Loading sites...
      </div>
      <div
        v-else-if="listError"
        class="sites-page__state sites-page__state--error"
      >
        {{ listError }}
      </div>
      <div
        v-else-if="sites.length === 0"
        class="sites-page__state"
      >
        No sites found.
      </div>
      <table
        v-else
        class="sites-page__table"
      >
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Address</th>
            <th>Updated</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="site in sites"
            :key="site.id"
          >
            <td>{{ site.code }}</td>
            <td>{{ site.name }}</td>
            <td>{{ site.address || '-' }}</td>
            <td>{{ formatDate(site.updated_at) }}</td>
            <td>
              <div class="sites-page__actions">
                <button
                  type="button"
                  :disabled="isActionPending"
                  @click="startEdit(site)"
                >
                  Edit
                </button>
                <button
                  type="button"
                  :disabled="isActionPending"
                  @click="confirmDelete(site)"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <footer class="sites-page__footer">
        <span>{{ count }} sites</span>
      </footer>
    </div>

    <Transition name="assetops-modal">
      <div
        v-if="isFormOpen"
        class="sites-page__modal"
        role="dialog"
        aria-modal="true"
      >
        <form @submit.prevent="saveSite">
          <h3>{{ editingSite ? 'Edit Site' : 'Add Site' }}</h3>
          <label
            v-if="editingSite"
            :class="{ 'sites-page__field--invalid': fieldErrors.code }"
          >
            <span>Code</span>
            <input
              ref="codeInput"
              v-model.trim="form.code"
              readonly
              :disabled="isSaving"
            >
            <small v-if="fieldErrors.code">{{ fieldErrors.code }}</small>
          </label>
          <label :class="{ 'sites-page__field--invalid': fieldErrors.name }">
            <span>Name</span>
            <input
              ref="nameInput"
              v-model.trim="form.name"
              required
              :disabled="isSaving"
            >
            <small v-if="fieldErrors.name">{{ fieldErrors.name }}</small>
          </label>
          <label :class="{ 'sites-page__field--invalid': fieldErrors.address }">
            <span>Address</span>
            <input
              ref="addressInput"
              v-model.trim="form.address"
              required
              :disabled="isSaving"
            >
            <small v-if="fieldErrors.address">{{ fieldErrors.address }}</small>
          </label>
          <label>
            <span>Notes</span>
            <textarea
              v-model.trim="form.notes"
              rows="4"
              :disabled="isSaving"
            />
          </label>
          <p v-if="formError">
            {{ formError }}
          </p>
          <div>
            <button
              type="button"
              :disabled="isSaving"
              @click="closeForm"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isSaving"
            >
              {{ isSaving ? 'Saving...' : 'Save Site' }}
            </button>
          </div>
        </form>
      </div>
    </Transition>

    <Transition name="assetops-modal">
      <div
        v-if="sitePendingDelete"
        class="sites-page__modal"
        role="dialog"
        aria-modal="true"
      >
        <form @submit.prevent="deleteSelectedSite">
          <h3>Delete Site</h3>
          <p>
            Delete site {{ sitePendingDelete.code }}? It will be removed from the default list.
          </p>
          <div>
            <button
              type="button"
              :disabled="isDeleting"
              @click="closeDeleteDialog"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isDeleting"
            >
              {{ isDeleting ? 'Deleting...' : 'Delete Site' }}
            </button>
          </div>
        </form>
      </div>
    </Transition>
  </section>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'

import { parseFieldErrors, getApiErrorMessage, type FieldErrors } from '@/services/errors'
import { useAuthStore } from '@/stores/auth'
import { createSite, deleteSite, fetchSites, updateSite, type Site, type SitePayload } from '@/services/sites'

const authStore = useAuthStore()
const sites = ref<Site[]>([])
const count = ref(0)
const search = ref('')
const error = ref<string | null>(null)
const listError = ref<string | null>(null)
const successMessage = ref<string | null>(null)
const formError = ref<string | null>(null)
const isLoading = ref(false)
const isSaving = ref(false)
const isDeleting = ref(false)
const isFormOpen = ref(false)
const editingSite = ref<Site | null>(null)
const sitePendingDelete = ref<Site | null>(null)
const fieldErrors = reactive<FieldErrors<keyof SitePayload>>({})
const codeInput = ref<{ focus: () => void } | null>(null)
const nameInput = ref<{ focus: () => void } | null>(null)
const addressInput = ref<{ focus: () => void } | null>(null)
let searchTimer: ReturnType<typeof globalThis.setTimeout> | null = null
let latestLoadRequestId = 0

const isActionPending = computed(() => isLoading.value || isSaving.value || isDeleting.value)

const emptyForm = (): SitePayload => ({
  code: '',
  name: '',
  address: '',
  notes: '',
})

const form = reactive<SitePayload>(emptyForm())

const clearFieldErrors = () => {
  fieldErrors.code = undefined
  fieldErrors.name = undefined
  fieldErrors.address = undefined
  fieldErrors.notes = undefined
}

const resetFeedback = () => {
  error.value = null
  successMessage.value = null
}

const loadSites = async () => {
  if (!authStore.accessToken) {
    return
  }

  const requestId = latestLoadRequestId + 1
  latestLoadRequestId = requestId
  isLoading.value = true
  listError.value = null

  try {
    const response = await fetchSites(
      {
        search: search.value,
        ordering: 'code',
        page_size: 100,
      },
      authStore.accessToken,
    )
    if (requestId !== latestLoadRequestId) {
      return
    }
    sites.value = response.results
    count.value = response.count
  } catch (loadError) {
    if (requestId !== latestLoadRequestId) {
      return
    }
    listError.value = getApiErrorMessage(loadError, 'Unable to load sites.')
  } finally {
    if (requestId === latestLoadRequestId) {
      isLoading.value = false
    }
  }
}

const startCreate = () => {
  resetFeedback()
  editingSite.value = null
  Object.assign(form, emptyForm())
  formError.value = null
  clearFieldErrors()
  isFormOpen.value = true
  void nextTick(() => nameInput.value?.focus())
}

const startEdit = (site: Site) => {
  resetFeedback()
  editingSite.value = site
  Object.assign(form, {
    code: site.code,
    name: site.name,
    address: site.address,
    notes: site.notes,
  })
  formError.value = null
  clearFieldErrors()
  isFormOpen.value = true
  void nextTick(() => codeInput.value?.focus())
}

const closeForm = () => {
  isFormOpen.value = false
  editingSite.value = null
  formError.value = null
  clearFieldErrors()
  Object.assign(form, emptyForm())
}

const focusFirstInvalidField = async () => {
  await nextTick()
  if (fieldErrors.code) {
    codeInput.value?.focus()
    return
  }

  if (fieldErrors.name) {
    nameInput.value?.focus()
    return
  }

  if (fieldErrors.address) {
    addressInput.value?.focus()
  }
}

const saveSite = async () => {
  if (!authStore.accessToken || isSaving.value) {
    return
  }

  isSaving.value = true
  formError.value = null
  resetFeedback()
  clearFieldErrors()

  try {
    const wasEdit = Boolean(editingSite.value)
    const payload: SitePayload = {
      name: form.name,
      address: form.address,
      notes: form.notes,
    }

    if (editingSite.value) {
      payload.code = form.code
      await updateSite(editingSite.value.id, payload, authStore.accessToken)
    } else {
      await createSite(payload, authStore.accessToken)
    }

    closeForm()
    await loadSites()
    successMessage.value = wasEdit ? 'Site updated successfully.' : 'Site created successfully.'
  } catch (saveError) {
    Object.assign(fieldErrors, parseFieldErrors(saveError, ['code', 'name', 'address', 'notes']))
    if (Object.values(fieldErrors).some(Boolean)) {
      await focusFirstInvalidField()
    } else {
      formError.value = getApiErrorMessage(saveError, 'Unable to save site.')
    }
  } finally {
    isSaving.value = false
  }
}

const confirmDelete = (site: Site) => {
  resetFeedback()
  sitePendingDelete.value = site
}

const closeDeleteDialog = () => {
  if (!isDeleting.value) {
    sitePendingDelete.value = null
  }
}

const deleteSelectedSite = async () => {
  if (!authStore.accessToken || !sitePendingDelete.value || isDeleting.value) {
    return
  }

  const site = sitePendingDelete.value
  isDeleting.value = true
  resetFeedback()

  try {
    await deleteSite(site.id, authStore.accessToken)
    sitePendingDelete.value = null
    await loadSites()
    successMessage.value = `Site ${site.code} deleted successfully.`
  } catch (deleteError) {
    error.value = getApiErrorMessage(deleteError, 'Unable to delete site.')
  } finally {
    isDeleting.value = false
  }
}

const formatDate = (value: string) =>
  new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
  }).format(new Date(value))

watch(search, () => {
  if (searchTimer) {
    globalThis.clearTimeout(searchTimer)
  }

  searchTimer = globalThis.setTimeout(() => {
    void loadSites()
  }, 300)
})

onMounted(loadSites)

onBeforeUnmount(() => {
  if (searchTimer) {
    globalThis.clearTimeout(searchTimer)
  }
})
</script>

<style scoped>
.sites-page {
  padding: 0 32px 34px;
}

.sites-page__panel {
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

.sites-page__panel:hover {
  border-color: rgba(0, 216, 255, 0.42);
}

.sites-page__header,
.sites-page__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 20px 22px;
}

.sites-page__header {
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
}

.sites-page__header p {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.sites-page__header h2,
.sites-page__modal h3 {
  margin: 0;
  color: var(--assetops-text);
}

.sites-page__header button,
.sites-page__filters button,
.sites-page__modal button:last-child {
  border: 1px solid rgba(36, 212, 255, 0.62);
  border-radius: 8px;
  color: #ffffff;
  background: linear-gradient(110deg, #058cff, #123de8);
  padding: 11px 16px;
  font-weight: 800;
  box-shadow: 0 0 18px rgba(0, 132, 255, 0.24);
}

.sites-page__filters {
  display: grid;
  grid-template-columns: minmax(240px, 1fr) auto;
  gap: 14px;
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  padding: 18px 22px;
}

.sites-page label {
  display: grid;
  gap: 7px;
}

.sites-page span {
  color: var(--assetops-muted);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.sites-page input,
.sites-page textarea {
  border: 1px solid var(--assetops-border-muted);
  border-radius: 8px;
  color: var(--assetops-text);
  background: rgba(7, 21, 40, 0.8);
  padding: 12px;
  outline: 0;
}

.sites-page input:focus,
.sites-page textarea:focus {
  border-color: var(--assetops-cyan);
  box-shadow: 0 0 16px rgba(0, 216, 255, 0.18);
}

.sites-page input:disabled,
.sites-page textarea:disabled,
.sites-page button:disabled {
  cursor: not-allowed;
  opacity: 0.62;
}

.sites-page__field--invalid input,
.sites-page__field--invalid textarea {
  border-color: rgba(255, 77, 94, 0.72);
  box-shadow: 0 0 14px rgba(255, 77, 94, 0.12);
}

.sites-page label small {
  color: #ffb9c0;
  font-size: 12px;
  font-weight: 700;
}

.sites-page__feedback {
  margin: 0;
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  padding: 12px 22px;
  font-size: 13px;
  font-weight: 700;
}

.sites-page__feedback--success {
  color: #a6ffd3;
  background: rgba(27, 196, 125, 0.1);
}

.sites-page__feedback--error {
  color: #ffb9c0;
  background: rgba(255, 77, 94, 0.1);
}

.sites-page__table {
  width: 100%;
  border-collapse: collapse;
}

.sites-page__table th,
.sites-page__table td {
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  padding: 14px 16px;
  text-align: left;
}

.sites-page__table th {
  color: var(--assetops-muted);
  background: rgba(10, 26, 45, 0.8);
  font-size: 12px;
  text-transform: uppercase;
}

.sites-page__table td {
  color: var(--assetops-muted-strong);
  font-size: 14px;
}

.sites-page__table tbody tr {
  transition:
    background var(--assetops-motion-standard) var(--assetops-ease-standard),
    box-shadow var(--assetops-motion-standard) var(--assetops-ease-standard);
}

.sites-page__table tbody tr:hover {
  background: rgba(10, 132, 255, 0.07);
  box-shadow: inset 2px 0 0 rgba(0, 216, 255, 0.52);
}

.sites-page__actions {
  display: flex;
  gap: 10px;
}

.sites-page__actions button,
.sites-page__modal button:first-child {
  border: 1px solid rgba(30, 155, 255, 0.32);
  border-radius: 8px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
  padding: 9px 12px;
  cursor: pointer;
  font-weight: 700;
}

.sites-page button:not(:disabled):hover,
.sites-page button:not(:disabled):focus-visible {
  border-color: var(--assetops-cyan);
  box-shadow: 0 0 18px rgba(0, 132, 255, 0.18);
  outline: 0;
}

.sites-page__state {
  display: grid;
  min-height: 240px;
  place-items: center;
  color: var(--assetops-muted);
  font-weight: 700;
}

.sites-page__state--error,
.sites-page__modal p {
  color: #ffb9c0;
}

.sites-page__footer {
  color: var(--assetops-muted);
  font-size: 13px;
}

.sites-page__modal {
  position: fixed;
  z-index: 20;
  inset: 0;
  display: grid;
  place-items: center;
  background: rgba(2, 7, 19, 0.78);
}

.sites-page__modal form {
  display: grid;
  width: min(520px, calc(100vw - 32px));
  gap: 16px;
  border: 1px solid var(--assetops-border);
  border-radius: 12px;
  background: var(--assetops-panel-strong);
  padding: 24px;
  box-shadow: var(--assetops-strong-glow);
}

.sites-page__modal div {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (prefers-reduced-motion: reduce) {
  .sites-page__panel,
  .sites-page__table tbody tr {
    transition: none;
  }
}

@media (max-width: 720px) {
  .sites-page {
    padding: 0 18px 24px;
  }

  .sites-page__filters,
  .sites-page__header {
    grid-template-columns: 1fr;
  }
}
</style>
