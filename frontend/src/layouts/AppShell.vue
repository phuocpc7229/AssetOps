<template>
  <main class="app-shell">
    <AppSidebar />

    <section class="app-shell__workspace">
      <AppTopbar />
      <RouterView />
    </section>
  </main>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'

import AppSidebar from '@/components/app/AppSidebar.vue'
import AppTopbar from '@/components/app/AppTopbar.vue'
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

@media (max-width: 900px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .app-shell__workspace {
    border-left: 0;
  }
}
</style>
