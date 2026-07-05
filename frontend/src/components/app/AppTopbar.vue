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
        <span class="app-topbar__avatar">{{ accountInitials }}</span>
        <span>{{ username }}</span>
        <small>Account</small>
      </button>

      <Transition name="account-menu">
        <div
          v-if="isUserMenuOpen"
          class="app-topbar__menu"
          role="menu"
        >
          <div class="app-topbar__menu-header">
            <span class="app-topbar__menu-avatar">{{ accountInitials }}</span>
            <div>
              <strong>{{ username }}</strong>
              <small>Local Administrator</small>
            </div>
          </div>
          <button
            type="button"
            role="menuitem"
            @click="openAccountInformation"
          >
            Account Information
          </button>
          <button
            type="button"
            role="menuitem"
            @click="signOut"
          >
            Sign out
          </button>
        </div>
      </Transition>
    </div>

    <Transition name="assetops-modal">
      <AccountInformationModal
        v-if="isAccountInformationOpen"
        @close="isAccountInformationOpen = false"
        @success="handlePasswordChanged"
      />
    </Transition>

    <Transition name="app-toast">
      <div
        v-if="toastMessage"
        class="app-topbar__toast"
        role="status"
      >
        {{ toastMessage }}
      </div>
    </Transition>
  </header>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import AccountInformationModal from '@/components/app/AccountInformationModal.vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const isUserMenuOpen = ref(false)
const isAccountInformationOpen = ref(false)
const toastMessage = ref<string | null>(null)
const userMenuRoot = ref<{ contains: (target: unknown) => boolean } | null>(null)
let toastTimer: ReturnType<typeof globalThis.setTimeout> | null = null

const routeTitle = computed(() => (typeof route.meta.title === 'string' ? route.meta.title : 'Dashboard'))
const accountInitials = 'AD'
const username = computed(() => authStore.user?.username ?? 'admin')

const openAccountInformation = () => {
  isUserMenuOpen.value = false
  isAccountInformationOpen.value = true
}

const handlePasswordChanged = (message: string) => {
  isAccountInformationOpen.value = false
  toastMessage.value = message

  if (toastTimer) {
    globalThis.clearTimeout(toastTimer)
  }

  toastTimer = globalThis.setTimeout(() => {
    toastMessage.value = null
  }, 3200)
}

const signOut = () => {
  isUserMenuOpen.value = false
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
  transition:
    box-shadow var(--assetops-motion-standard) var(--assetops-ease-standard),
    transform var(--assetops-motion-standard) var(--assetops-ease-standard);
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
  transition:
    border-color var(--assetops-motion-standard) var(--assetops-ease-standard),
    background var(--assetops-motion-standard) var(--assetops-ease-standard),
    box-shadow var(--assetops-motion-standard) var(--assetops-ease-standard),
    transform var(--assetops-motion-standard) var(--assetops-ease-standard);
}

.app-topbar__user:hover,
.app-topbar__user:focus-visible,
.app-topbar__user[aria-expanded="true"] {
  border-color: rgba(0, 216, 255, 0.58);
  background: rgba(10, 132, 255, 0.15);
  box-shadow: 0 0 18px rgba(0, 132, 255, 0.18);
  outline: 0;
}

.app-topbar__user:hover .app-topbar__avatar,
.app-topbar__user[aria-expanded="true"] .app-topbar__avatar {
  box-shadow: 0 0 24px rgba(0, 216, 255, 0.34);
  transform: translateY(-1px);
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
  transition:
    border-color var(--assetops-motion-standard) var(--assetops-ease-standard),
    background var(--assetops-motion-standard) var(--assetops-ease-standard),
    box-shadow var(--assetops-motion-standard) var(--assetops-ease-standard),
    color var(--assetops-motion-standard) var(--assetops-ease-standard),
    transform var(--assetops-motion-fast) var(--assetops-ease-standard);
}

.app-topbar button:hover {
  border-color: var(--assetops-cyan);
}

.app-topbar button:active {
  transform: translateY(1px);
}

.app-topbar__menu {
  position: absolute;
  z-index: 20;
  top: calc(100% + 8px);
  right: 0;
  display: grid;
  min-width: 248px;
  gap: 8px;
  border: 1px solid rgba(30, 155, 255, 0.36);
  border-radius: 10px;
  background: var(--assetops-panel-strong);
  padding: 10px;
  box-shadow: var(--assetops-strong-glow);
  transform-origin: top right;
}

.app-topbar__menu button {
  width: 100%;
  background: rgba(7, 21, 40, 0.56);
  text-align: left;
}

.app-topbar__menu button:hover,
.app-topbar__menu button:focus-visible {
  background: rgba(10, 132, 255, 0.18);
  box-shadow: 0 0 14px rgba(0, 132, 255, 0.16);
  outline: 0;
}

.app-topbar__menu-header {
  display: grid;
  grid-template-columns: 40px minmax(0, 1fr);
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  padding: 4px 4px 10px;
}

.app-topbar__menu-avatar {
  display: inline-grid;
  width: 40px;
  height: 40px;
  place-items: center;
  border-radius: 50%;
  color: #ffffff;
  background: linear-gradient(135deg, var(--assetops-blue), var(--assetops-cyan));
  font-size: 12px;
  font-weight: 900;
  box-shadow: 0 0 20px rgba(0, 216, 255, 0.28);
}

.app-topbar__menu-header strong,
.app-topbar__menu-header small {
  display: block;
  overflow: hidden;
  text-align: left;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.app-topbar__menu-header strong {
  color: var(--assetops-text);
  font-size: 13px;
}

.app-topbar__menu-header small {
  margin-top: 3px;
  color: var(--assetops-muted);
  font-size: 11px;
  font-weight: 700;
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

.account-menu-enter-active,
.account-menu-leave-active {
  transition:
    opacity var(--assetops-motion-standard) var(--assetops-ease-standard),
    transform var(--assetops-motion-standard) var(--assetops-ease-standard);
}

.account-menu-enter-from,
.account-menu-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.98);
}

.app-toast-enter-active,
.app-toast-leave-active {
  transition:
    opacity var(--assetops-motion-standard) var(--assetops-ease-standard),
    transform var(--assetops-motion-standard) var(--assetops-ease-standard);
}

.app-toast-enter-from,
.app-toast-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (prefers-reduced-motion: reduce) {
  .account-menu-enter-active,
  .account-menu-leave-active,
  .app-toast-enter-active,
  .app-toast-leave-active,
  .app-topbar *,
  .app-topbar *::before,
  .app-topbar *::after {
    transition: none;
  }
}

@media (max-width: 720px) {
  .app-topbar {
    align-items: flex-start;
    flex-direction: column;
    padding: 22px 18px 14px;
  }
}
</style>
