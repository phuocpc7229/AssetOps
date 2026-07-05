<template>
  <div
    class="account-information-modal"
    role="dialog"
    aria-modal="true"
    aria-labelledby="account-information-title"
    @click.self="close"
  >
    <form @submit.prevent="submit">
      <header class="account-information-modal__header">
        <div>
          <p>Account Settings</p>
          <h2 id="account-information-title">
            Account Information
          </h2>
        </div>
        <button
          type="button"
          class="account-information-modal__close"
          aria-label="Close account information dialog"
          :disabled="isSubmitting"
          @click="close"
        >
          Close
        </button>
      </header>

      <section class="account-information-modal__identity">
        <span class="account-information-modal__avatar">AD</span>
        <div>
          <strong>{{ username }}</strong>
          <small>Local Administrator</small>
        </div>
      </section>

      <section
        class="account-information-modal__details"
        aria-label="Read-only account information"
      >
        <div>
          <span>Username</span>
          <strong>{{ username }}</strong>
        </div>
        <div>
          <span>Role</span>
          <strong>Administrator</strong>
        </div>
        <div>
          <span>Account type</span>
          <strong>Local account</strong>
        </div>
      </section>

      <section class="account-information-modal__password-section">
        <div class="account-information-modal__section-header">
          <div>
            <p>Security</p>
            <h3>Change Password</h3>
          </div>
        </div>

        <label :class="{ 'account-information-modal__field--invalid': fieldErrors.current_password }">
          <span>Current Password</span>
          <div class="account-information-modal__password">
            <input
              v-model="form.current_password"
              :type="visibleFields.current_password ? 'text' : 'password'"
              autocomplete="current-password"
              :disabled="isSubmitting"
            >
            <button
              type="button"
              :aria-label="visibleFields.current_password ? 'Hide current password' : 'Show current password'"
              :disabled="isSubmitting"
              @click="visibleFields.current_password = !visibleFields.current_password"
            >
              {{ visibleFields.current_password ? 'Hide' : 'Show' }}
            </button>
          </div>
          <small v-if="fieldErrors.current_password">{{ fieldErrors.current_password }}</small>
        </label>

        <label :class="{ 'account-information-modal__field--invalid': fieldErrors.new_password }">
          <span>New Password</span>
          <div class="account-information-modal__password">
            <input
              v-model="form.new_password"
              :type="visibleFields.new_password ? 'text' : 'password'"
              autocomplete="new-password"
              :disabled="isSubmitting"
            >
            <button
              type="button"
              :aria-label="visibleFields.new_password ? 'Hide new password' : 'Show new password'"
              :disabled="isSubmitting"
              @click="visibleFields.new_password = !visibleFields.new_password"
            >
              {{ visibleFields.new_password ? 'Hide' : 'Show' }}
            </button>
          </div>
          <small v-if="fieldErrors.new_password">{{ fieldErrors.new_password }}</small>
        </label>

        <label :class="{ 'account-information-modal__field--invalid': fieldErrors.confirm_password }">
          <span>Confirm Password</span>
          <div class="account-information-modal__password">
            <input
              v-model="form.confirm_password"
              :type="visibleFields.confirm_password ? 'text' : 'password'"
              autocomplete="new-password"
              :disabled="isSubmitting"
            >
            <button
              type="button"
              :aria-label="visibleFields.confirm_password ? 'Hide password confirmation' : 'Show password confirmation'"
              :disabled="isSubmitting"
              @click="visibleFields.confirm_password = !visibleFields.confirm_password"
            >
              {{ visibleFields.confirm_password ? 'Hide' : 'Show' }}
            </button>
          </div>
          <small v-if="fieldErrors.confirm_password">{{ fieldErrors.confirm_password }}</small>
        </label>

        <p
          v-if="formError"
          class="account-information-modal__error"
          role="alert"
        >
          {{ formError }}
        </p>
      </section>

      <footer>
        <button
          type="button"
          :disabled="isSubmitting"
          @click="close"
        >
          Cancel
        </button>
        <button
          type="submit"
          :disabled="isSubmitting"
        >
          {{ isSubmitting ? 'Updating...' : 'Update Password' }}
        </button>
      </footer>
    </form>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'

import { changePassword, type ChangePasswordPayload } from '@/services/auth'
import { getApiErrorMessage, parseFieldErrors, type FieldErrors } from '@/services/errors'
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits<{
  close: []
  success: [message: string]
}>()

const authStore = useAuthStore()
const username = computed(() => authStore.user?.username ?? 'admin')
const isSubmitting = ref(false)
const formError = ref<string | null>(null)
const form = reactive<ChangePasswordPayload>({
  current_password: '',
  new_password: '',
  confirm_password: '',
})
const fieldErrors = reactive<FieldErrors<keyof ChangePasswordPayload>>({})
const visibleFields = reactive<Record<keyof ChangePasswordPayload, boolean>>({
  current_password: false,
  new_password: false,
  confirm_password: false,
})

const clearErrors = () => {
  fieldErrors.current_password = undefined
  fieldErrors.new_password = undefined
  fieldErrors.confirm_password = undefined
  formError.value = null
}

const resetForm = () => {
  form.current_password = ''
  form.new_password = ''
  form.confirm_password = ''
  visibleFields.current_password = false
  visibleFields.new_password = false
  visibleFields.confirm_password = false
  clearErrors()
}

const validateForm = () => {
  clearErrors()

  if (!form.current_password) {
    fieldErrors.current_password = 'Current password is required.'
  }

  if (!form.new_password) {
    fieldErrors.new_password = 'New password is required.'
  } else if (form.new_password.length < 8) {
    fieldErrors.new_password = 'New password must be at least 8 characters.'
  }

  if (!form.confirm_password) {
    fieldErrors.confirm_password = 'Confirm password is required.'
  } else if (form.new_password !== form.confirm_password) {
    fieldErrors.confirm_password = 'New password and confirmation do not match.'
  }

  return !Object.values(fieldErrors).some(Boolean)
}

const close = () => {
  if (!isSubmitting.value) {
    resetForm()
    emit('close')
  }
}

const submit = async () => {
  if (isSubmitting.value || !validateForm()) {
    return
  }

  if (!authStore.accessToken) {
    formError.value = 'Your session is not available. Please sign in again.'
    return
  }

  isSubmitting.value = true

  try {
    const response = await changePassword({ ...form }, authStore.accessToken)
    resetForm()
    emit('success', response.detail)
  } catch (error) {
    Object.assign(
      fieldErrors,
      parseFieldErrors(error, ['current_password', 'new_password', 'confirm_password']),
    )
    if (!Object.values(fieldErrors).some(Boolean)) {
      formError.value = getApiErrorMessage(error, 'Unable to change password.')
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.account-information-modal {
  position: fixed;
  z-index: 40;
  inset: 0;
  display: grid;
  place-items: center;
  background: rgba(2, 7, 19, 0.78);
  padding: 18px;
}

.account-information-modal form {
  display: grid;
  width: min(680px, 100%);
  max-height: min(92vh, 760px);
  gap: 16px;
  overflow-y: auto;
  border: 1px solid var(--assetops-border);
  border-radius: 12px;
  background:
    linear-gradient(145deg, rgba(13, 33, 56, 0.96), rgba(3, 10, 24, 0.98)),
    var(--assetops-panel-strong);
  padding: 22px;
  box-shadow: var(--assetops-strong-glow);
}

.account-information-modal__header,
.account-information-modal footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.account-information-modal__header {
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  padding-bottom: 16px;
}

.account-information-modal p {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.account-information-modal h2,
.account-information-modal h3 {
  margin: 0;
  color: var(--assetops-text);
}

.account-information-modal h2 {
  font-size: 21px;
}

.account-information-modal h3 {
  font-size: 17px;
}

.account-information-modal__identity {
  display: flex;
  align-items: center;
  gap: 14px;
  border: 1px solid rgba(30, 155, 255, 0.22);
  border-radius: 10px;
  background: rgba(7, 21, 40, 0.58);
  padding: 14px;
}

.account-information-modal__avatar {
  display: inline-grid;
  width: 48px;
  height: 48px;
  flex: 0 0 auto;
  place-items: center;
  border-radius: 50%;
  color: #ffffff;
  background: linear-gradient(135deg, var(--assetops-blue), var(--assetops-cyan));
  font-size: 14px;
  font-weight: 900;
  box-shadow: 0 0 22px rgba(0, 216, 255, 0.3);
}

.account-information-modal__identity strong,
.account-information-modal__identity small {
  display: block;
}

.account-information-modal__identity strong {
  color: var(--assetops-text);
  font-size: 15px;
}

.account-information-modal__identity small {
  margin-top: 3px;
  color: var(--assetops-muted);
  font-size: 12px;
  font-weight: 700;
}

.account-information-modal__details {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.account-information-modal__details div {
  display: grid;
  gap: 6px;
  border: 1px solid rgba(142, 168, 203, 0.16);
  border-radius: 8px;
  background: rgba(4, 11, 24, 0.48);
  padding: 12px;
}

.account-information-modal__details span {
  color: var(--assetops-muted);
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
}

.account-information-modal__details strong {
  overflow: hidden;
  color: var(--assetops-text);
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.account-information-modal__password-section {
  display: grid;
  gap: 13px;
  border: 1px solid rgba(30, 155, 255, 0.22);
  border-radius: 10px;
  background: rgba(7, 21, 40, 0.44);
  padding: 16px;
}

.account-information-modal__section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.account-information-modal label {
  display: grid;
  gap: 8px;
}

.account-information-modal label > span {
  color: var(--assetops-text);
  font-size: 13px;
  font-weight: 700;
}

.account-information-modal__password {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 76px;
  gap: 8px;
}

.account-information-modal input {
  width: 100%;
  border: 1px solid var(--assetops-border-muted);
  border-radius: 8px;
  color: var(--assetops-text);
  background: linear-gradient(145deg, rgba(13, 33, 56, 0.74), rgba(6, 15, 30, 0.9));
  padding: 12px 14px;
  outline: 0;
}

.account-information-modal input:focus {
  border-color: var(--assetops-cyan);
  box-shadow: 0 0 16px rgba(0, 216, 255, 0.18);
}

.account-information-modal__field--invalid input {
  border-color: rgba(255, 77, 94, 0.72);
  box-shadow: 0 0 14px rgba(255, 77, 94, 0.12);
}

.account-information-modal small,
.account-information-modal__error {
  color: #ffb9c0;
  font-size: 12px;
  font-weight: 700;
}

.account-information-modal__error {
  margin: 0;
  border: 1px solid rgba(255, 77, 94, 0.38);
  border-radius: 8px;
  background: rgba(255, 77, 94, 0.1);
  padding: 10px 12px;
  text-transform: none;
}

.account-information-modal button {
  border: 1px solid rgba(30, 155, 255, 0.32);
  border-radius: 8px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
  padding: 10px 12px;
  cursor: pointer;
  font-weight: 800;
}

.account-information-modal footer button:last-child {
  border-color: rgba(36, 212, 255, 0.62);
  color: #ffffff;
  background: linear-gradient(110deg, #058cff, #123de8);
  box-shadow: 0 0 18px rgba(0, 132, 255, 0.24);
}

.account-information-modal button:disabled {
  cursor: not-allowed;
  opacity: 0.62;
}

@media (max-width: 640px) {
  .account-information-modal form {
    padding: 18px;
  }

  .account-information-modal__details {
    grid-template-columns: 1fr;
  }

  .account-information-modal__password {
    grid-template-columns: minmax(0, 1fr);
  }

  .account-information-modal__header,
  .account-information-modal footer {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
