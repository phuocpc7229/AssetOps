<template>
  <header class="app-topbar">
    <div>
      <p class="app-topbar__eyebrow">
        Operations Console
      </p>
      <h1>{{ routeTitle }}</h1>
    </div>

    <div class="app-topbar__user">
      <span class="app-topbar__avatar">{{ initials }}</span>
      <span>{{ authStore.user?.username ?? 'Admin' }}</span>
      <button
        type="button"
        @click="signOut"
      >
        Sign out
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const routeTitle = computed(() => (typeof route.meta.title === 'string' ? route.meta.title : 'Dashboard'))
const initials = computed(() => (authStore.user?.username?.slice(0, 2) ?? 'AD').toUpperCase())

const signOut = () => {
  authStore.signOut()
  router.push({ name: 'login' })
}
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

.app-topbar__user {
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1px solid rgba(30, 155, 255, 0.24);
  border-radius: 10px;
  padding: 8px 10px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
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

@media (max-width: 720px) {
  .app-topbar {
    align-items: flex-start;
    flex-direction: column;
    padding: 22px 18px 14px;
  }
}
</style>
