<template>
  <main class="app-shell">
    <AppSidebar />

    <section class="app-shell__workspace">
      <AppTopbar />
      <RouterView v-slot="{ Component, route }">
        <Transition
          :name="transitionName(route.name)"
          mode="out-in"
        >
          <component
            :is="Component"
            :key="route.fullPath"
          />
        </Transition>
      </RouterView>
    </section>
  </main>
</template>

<script setup lang="ts">
import type { RouteRecordNameGeneric } from 'vue-router'
import { RouterView } from 'vue-router'

import AppSidebar from '@/components/app/AppSidebar.vue'
import AppTopbar from '@/components/app/AppTopbar.vue'

const transitionName = (routeName: RouteRecordNameGeneric | null | undefined) => {
  if (routeName === 'dashboard') {
    return 'route-dashboard'
  }

  if (routeName === 'assets') {
    return 'route-assets'
  }

  if (routeName === 'sites' || routeName === 'master-data') {
    return 'route-directory'
  }

  if (routeName === 'asset-new' || routeName === 'asset-edit') {
    return 'route-form'
  }

  return 'route-dashboard'
}
</script>

<style scoped>
.app-shell {
  display: grid;
  min-height: 100vh;
  grid-template-columns: 282px minmax(0, 1fr);
  gap: 0;
  overflow: hidden;
  background:
    linear-gradient(90deg, rgba(0, 132, 255, 0.12) 1px, transparent 1px),
    linear-gradient(0deg, rgba(0, 132, 255, 0.08) 1px, transparent 1px),
    radial-gradient(circle at 18% 16%, rgba(0, 216, 255, 0.12), transparent 24%),
    var(--assetops-black);
  background-size:
    52px 52px,
    52px 52px,
    auto,
    auto;
}

.app-shell__workspace {
  min-width: 0;
  overflow-y: auto;
  border-left: 1px solid rgba(30, 155, 255, 0.34);
  background: linear-gradient(135deg, rgba(2, 7, 19, 0.84), rgba(5, 12, 26, 0.96));
}

.route-dashboard-enter-active,
.route-dashboard-leave-active,
.route-assets-enter-active,
.route-assets-leave-active,
.route-directory-enter-active,
.route-directory-leave-active,
.route-form-enter-active,
.route-form-leave-active {
  transition:
    opacity var(--assetops-motion-standard) var(--assetops-ease-standard),
    transform var(--assetops-motion-standard) var(--assetops-ease-standard);
}

.route-dashboard-enter-from,
.route-dashboard-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

.route-assets-enter-from {
  opacity: 0;
  transform: translateX(14px);
}

.route-assets-leave-to {
  opacity: 0;
  transform: translateX(-8px);
}

.route-directory-enter-from,
.route-directory-leave-to {
  opacity: 0;
  transform: scale(0.992);
}

.route-form-enter-from,
.route-form-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .route-dashboard-enter-active,
  .route-dashboard-leave-active,
  .route-assets-enter-active,
  .route-assets-leave-active,
  .route-directory-enter-active,
  .route-directory-leave-active,
  .route-form-enter-active,
  .route-form-leave-active {
    transition: none;
  }
}

@media (max-width: 900px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .app-shell__workspace {
    border-left: 0;
  }
}
</style>
