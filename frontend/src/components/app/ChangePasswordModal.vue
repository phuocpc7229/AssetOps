<template>
  <div
    class="change-password-modal"
    role="dialog"
    aria-modal="true"
    aria-labelledby="change-password-title"
  >
    <form @submit.prevent="submit">
      <header>
        <div>
          <p>Account Settings</p>
          <h2 id="change-password-title">
            Change Password
          </h2>
        </div>
        <button
          type="button"
          aria-label="Close change password dialog"
          :disabled="isSubmitting"
          @click="close"
        >
          Close
        </button>
      </header>

      <label :class="{ 'change-password-modal__field--invalid': fieldErrors.current_password }">
        <span>Current Password</span>
        <div class="change-password-modal__password">
          <input
            v-model="form.current_password"
            :type="visibleFields.current ? 'text' : 'password'"
            autocomplete="current-password"
            :disabled="isSubmitting"
          >
          <button
            type="button"
            :disabled="isSubmitting"
            @click="visibleFields.current = !visibleFields.current"
          >
            {{ visibleFields.current ? 'Hide' : 'Show' }}
          </button>
        </div>
        <small v-if="fieldErrors.current_password">{{ fieldErrors.current_password }}</small>
      </label>

      <label :class="{ 'change-password-modal__field--invalid': fieldErrors.new_password }">
        <span>New Password</span>
        <div class="change-password-modal__password">
          <input
            v-model="form.new_password"
            :type="visibleFields.new ? 'text' : 'password'"
            autocomplete="new-password"
            :disabled="isSubmitting"
          >
          <button
            type="button"
            :disabled="isSubmitting"
            @click="visibleFields.new = !visibleFields.new"
          >
            {{ visibleFields.new ? 'Hide' : 'Show' }}
          </button>
        </div>
        <small v-if="fieldErrors.new_password">{{ fieldErrors.new_password }}</small>
      </label>

      <label :class="{ 'change-password-modal__field--invalid': fieldErrors.confirm_password }">
        <span>Confirm Password</span>
        <div class="change-password-modal__password">
          <input
            v-model="form.confirm_password"
            :type="visibleFields.confirm ? 'text' : 'password'"
            autocomplete="new-password"
            :disabled="isSubmitting"
          >
          <button
            type="button"
            :disabled="isSubmitting"
            @click="visibleFields.confirm = !visibleFields.confirm"
          >
            {{ visibleFields.confirm ? 'Hide' : 'Show' }}
          </button>
        </div>
        <small v-if="fieldErrors.confirm_password">{{ fieldErrors.confirm_password }}</small>
      </label>

      <p
        v-if="formError"
        class="change-password-modal__error"
        role="alert"
      >
        {{ formError }}
      </p>

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
          {{ isSubmitting ? 'Saving...' : 'Save Password' }}
        </button>
      </footer>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'

import { changePassword, type ChangePasswordPayload } from '@/services/auth'
import { getApiErrorMessage, parseFieldErrors, type FieldErrors } from '@/services/errors'
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits<{
  close: []
  success: [message: string]
}>()

const authStore = useAuthStore()
const isSubmitting = ref(false)
const formError = ref<string | null>(null)
const form = reactive<ChangePasswordPayload>({
  current_password: '',
  new_password: '',
  confirm_password: '',
})
const fieldErrors = reactive<FieldErrors<keyof ChangePasswordPayload>>({})
const visibleFields = reactive({
  current: false,
  new: false,
  confirm: false,
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
  visibleFields.current = false
  visibleFields.new = false
  visibleFields.confirm = false
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
  if (!authStore.accessToken || isSubmitting.value || !validateForm()) {
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
.change-password-modal {
  position: fixed;
  z-index: 40;
  inset: 0;
  display: grid;
  place-items: center;
  background: rgba(2, 7, 19, 0.78);
  padding: 18px;
}

.change-password-modal form {
  display: grid;
  width: min(520px, 100%);
  gap: 16px;
  border: 1px solid var(--assetops-border);
  border-radius: 12px;
  background:
    linear-gradient(145deg, rgba(13, 33, 56, 0.96), rgba(3, 10, 24, 0.98)),
    var(--assetops-panel-strong);
  padding: 22px;
  box-shadow: var(--assetops-strong-glow);
}

.change-password-modal header,
.change-password-modal footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.change-password-modal header {
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  padding-bottom: 16px;
}

.change-password-modal p {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.change-password-modal h2 {
  margin: 0;
  color: var(--assetops-text);
  font-size: 21px;
}

.change-password-modal label {
  display: grid;
  gap: 8px;
}

.change-password-modal label > span {
  color: var(--assetops-text);
  font-size: 13px;
  font-weight: 700;
}

.change-password-modal__password {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 74px;
  gap: 8px;
}

.change-password-modal input {
  width: 100%;
  border: 1px solid var(--assetops-border-muted);
  border-radius: 8px;
  color: var(--assetops-text);
  background: linear-gradient(145deg, rgba(13, 33, 56, 0.74), rgba(6, 15, 30, 0.9));
  padding: 12px 14px;
  outline: 0;
}

.change-password-modal input:focus {
  border-color: var(--assetops-cyan);
  box-shadow: 0 0 16px rgba(0, 216, 255, 0.18);
}

.change-password-modal__field--invalid input {
  border-color: rgba(255, 77, 94, 0.72);
  box-shadow: 0 0 14px rgba(255, 77, 94, 0.12);
}

.change-password-modal small,
.change-password-modal__error {
  color: #ffb9c0;
  font-size: 12px;
  font-weight: 700;
}

.change-password-modal__error {
  margin: 0;
  border: 1px solid rgba(255, 77, 94, 0.38);
  border-radius: 8px;
  background: rgba(255, 77, 94, 0.1);
  padding: 10px 12px;
  text-transform: none;
}

.change-password-modal button {
  border: 1px solid rgba(30, 155, 255, 0.32);
  border-radius: 8px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
  padding: 10px 12px;
  cursor: pointer;
  font-weight: 800;
}

.change-password-modal footer button:last-child {
  border-color: rgba(36, 212, 255, 0.62);
  color: #ffffff;
  background: linear-gradient(110deg, #058cff, #123de8);
  box-shadow: 0 0 18px rgba(0, 132, 255, 0.24);
}

.change-password-modal button:disabled {
  cursor: not-allowed;
  opacity: 0.62;
}
</style>
