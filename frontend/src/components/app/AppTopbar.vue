<template>
  <header class="app-topbar">
    <div>
      <p class="app-topbar__eyebrow">
        Operations Console
      </p>
      <h1>{{ routeTitle }}</h1>
    </div>

    <div
      ref="userMenuRoot"
      class="app-topbar__user-menu"
    >
      <button
        type="button"
        class="app-topbar__user"
        aria-haspopup="menu"
        :aria-expanded="isUserMenuOpen"
        @click="isUserMenuOpen = !isUserMenuOpen"
      >
        <span class="app-topbar__avatar">{{ initials }}</span>
        <span>{{ authStore.user?.username ?? 'Admin' }}</span>
        <small>Account</small>
      </button>

      <div
        v-if="isUserMenuOpen"
        class="app-topbar__menu"
        role="menu"
      >
        <button
          type="button"
          role="menuitem"
          @click="openChangePassword"
        >
          Change Password
        </button>
        <button
          type="button"
          role="menuitem"
          @click="signOut"
        >
          Sign out
        </button>
      </div>
    </div>

    <ChangePasswordModal
      v-if="isChangePasswordOpen"
      @close="isChangePasswordOpen = false"
      @success="handlePasswordChanged"
    />

    <div
      v-if="toastMessage"
      class="app-topbar__toast"
      role="status"
    >
      {{ toastMessage }}
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import ChangePasswordModal from '@/components/app/ChangePasswordModal.vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const isUserMenuOpen = ref(false)
const isChangePasswordOpen = ref(false)
const toastMessage = ref<string | null>(null)
const userMenuRoot = ref<{ contains: (target: unknown) => boolean } | null>(null)
let toastTimer: ReturnType<typeof globalThis.setTimeout> | null = null

const routeTitle = computed(() => (typeof route.meta.title === 'string' ? route.meta.title : 'Dashboard'))
const initials = computed(() => (authStore.user?.username?.slice(0, 2) ?? 'AD').toUpperCase())

const openChangePassword = () => {
  isUserMenuOpen.value = false
  isChangePasswordOpen.value = true
}

const handlePasswordChanged = (message: string) => {
  isChangePasswordOpen.value = false
  toastMessage.value = message

  if (toastTimer) {
    globalThis.clearTimeout(toastTimer)
  }

  toastTimer = globalThis.setTimeout(() => {
    toastMessage.value = null
  }, 3200)
}

const signOut = () => {
  authStore.signOut()
  router.push({ name: 'login' })
}

const closeUserMenuOnOutsideClick = (event: { target: unknown }) => {
  if (userMenuRoot.value && !userMenuRoot.value.contains(event.target)) {
    isUserMenuOpen.value = false
  }
}

onMounted(() => {
  globalThis.document?.addEventListener('mousedown', closeUserMenuOnOutsideClick)
})

onBeforeUnmount(() => {
  globalThis.document?.removeEventListener('mousedown', closeUserMenuOnOutsideClick)
  if (toastTimer) {
    globalThis.clearTimeout(toastTimer)
  }
})
</script>

<style scoped>
.app-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 28px 32px 18px;
}

.app-topbar__eyebrow {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.6px;
  text-transform: uppercase;
}

.app-topbar h1 {
  margin: 0;
  color: var(--assetops-text);
  font-size: 28px;
  font-weight: 800;
}

.app-topbar__user-menu {
  position: relative;
}

.app-topbar__avatar {
  display: inline-grid;
  width: 34px;
  height: 34px;
  place-items: center;
  border-radius: 50%;
  color: #ffffff;
  background: linear-gradient(135deg, var(--assetops-blue), var(--assetops-cyan));
  font-size: 12px;
  font-weight: 800;
  box-shadow: 0 0 18px rgba(0, 216, 255, 0.28);
}

.app-topbar__user {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  align-items: center;
  gap: 2px 12px;
  min-width: 168px;
  border: 1px solid rgba(30, 155, 255, 0.24);
  border-radius: 10px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
  padding: 8px 10px;
  text-align: left;
  cursor: pointer;
}

.app-topbar__user > span:not(.app-topbar__avatar),
.app-topbar__user small {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.app-topbar__user > span:not(.app-topbar__avatar) {
  color: var(--assetops-text);
  font-size: 13px;
  font-weight: 800;
}

.app-topbar__user small {
  grid-column: 2;
  color: var(--assetops-muted);
  font-size: 11px;
  font-weight: 700;
}

.app-topbar button {
  border: 1px solid rgba(30, 155, 255, 0.36);
  border-radius: 7px;
  color: var(--assetops-text);
  background: rgba(10, 132, 255, 0.12);
  padding: 8px 10px;
  cursor: pointer;
}

.app-topbar button:hover {
  border-color: var(--assetops-cyan);
}

.app-topbar__menu {
  position: absolute;
  z-index: 20;
  top: calc(100% + 8px);
  right: 0;
  display: grid;
  min-width: 190px;
  gap: 6px;
  border: 1px solid rgba(30, 155, 255, 0.36);
  border-radius: 10px;
  background: var(--assetops-panel-strong);
  padding: 8px;
  box-shadow: var(--assetops-strong-glow);
}

.app-topbar__menu button {
  width: 100%;
  text-align: left;
}

.app-topbar__toast {
  position: fixed;
  z-index: 45;
  top: 22px;
  right: 28px;
  border: 1px solid rgba(0, 212, 138, 0.42);
  border-radius: 10px;
  color: #a6ffd3;
  background: rgba(0, 54, 44, 0.92);
  padding: 12px 16px;
  font-size: 13px;
  font-weight: 800;
  box-shadow: 0 0 24px rgba(0, 212, 138, 0.18);
}

@media (max-width: 720px) {
  .app-topbar {
    align-items: flex-start;
    flex-direction: column;
    padding: 22px 18px 14px;
  }
}
</style>
