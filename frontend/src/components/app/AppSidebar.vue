<template>
  <aside
    class="app-sidebar"
    aria-label="Main navigation"
  >
    <div class="app-sidebar__brand">
      <AssetOpsLogo size="small" />
      <div>
        <strong>AssetOps</strong>
        <span>Portal</span>
      </div>
    </div>

    <nav class="app-sidebar__nav">
      <RouterLink
        v-for="item in primaryItems"
        :key="item.to"
        :to="item.to"
        class="app-sidebar__item"
      >
        <span
          class="app-sidebar__icon"
          aria-hidden="true"
        >{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </RouterLink>

      <span
        v-for="item in comingSoonItems"
        :key="item.label"
        class="app-sidebar__item app-sidebar__item--disabled"
      >
        <span
          class="app-sidebar__icon"
          aria-hidden="true"
        >{{ item.icon }}</span>
        <span>{{ item.label }}</span>
        <small>Coming Soon</small>
      </span>
    </nav>

    <div class="app-sidebar__version">
      <strong>AssetOps Portal</strong>
      <span>Milestone 2</span>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'

import AssetOpsLogo from '@/components/ui/AssetOpsLogo.vue'

const primaryItems = [
  { label: 'Dashboard', to: '/dashboard', icon: 'D' },
  { label: 'Assets', to: '/dashboard/assets', icon: 'A' },
  { label: 'Sites', to: '/dashboard/sites', icon: 'S' },
  { label: 'Asset Types', to: '/dashboard/master-data/asset-types', icon: 'Y' },
  { label: 'Vendors', to: '/dashboard/master-data/vendors', icon: 'V' },
  { label: 'Device Types', to: '/dashboard/master-data/device-types', icon: 'T' },
  { label: 'Locations', to: '/dashboard/master-data/locations', icon: 'L' },
]

const comingSoonItems = [
  { label: 'Import', icon: 'I' },
  { label: 'Reports', icon: 'R' },
  { label: 'Users', icon: 'U' },
  { label: 'Settings', icon: 'G' },
]
</script>

<style scoped>
.app-sidebar {
  position: relative;
  display: grid;
  min-height: 100vh;
  grid-template-rows: auto 1fr auto;
  overflow: hidden;
  padding: 24px 18px;
  border: 1px solid rgba(30, 155, 255, 0.4);
  border-width: 0 1px 0 0;
  background:
    linear-gradient(180deg, rgba(7, 20, 38, 0.96), rgba(4, 11, 24, 0.98)),
    var(--assetops-navy);
  box-shadow: inset -1px 0 18px rgba(0, 132, 255, 0.12);
}

.app-sidebar::after {
  position: absolute;
  right: -70px;
  bottom: -60px;
  width: 190px;
  height: 190px;
  border: 1px solid rgba(0, 216, 255, 0.2);
  border-radius: 50%;
  box-shadow: var(--assetops-glow);
  content: "";
}

.app-sidebar__brand {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 4px 8px 28px;
}

.app-sidebar__brand strong,
.app-sidebar__brand span {
  display: block;
  line-height: 1;
}

.app-sidebar__brand strong {
  color: var(--assetops-text);
  font-size: 22px;
  font-weight: 800;
}

.app-sidebar__brand span {
  margin-top: 7px;
  color: var(--assetops-cyan);
  font-size: 13px;
  letter-spacing: 3px;
  text-transform: uppercase;
}

.app-sidebar__nav {
  position: relative;
  z-index: 1;
  display: grid;
  align-content: start;
  gap: 8px;
}

.app-sidebar__item {
  display: grid;
  min-height: 44px;
  grid-template-columns: 30px minmax(0, 1fr) auto;
  align-items: center;
  gap: 10px;
  border: 1px solid transparent;
  border-radius: 8px;
  padding: 0 12px;
  color: var(--assetops-muted-strong);
  font-size: 14px;
  font-weight: 600;
  transition:
    border-color 160ms ease,
    background 160ms ease,
    box-shadow 160ms ease,
    color 160ms ease;
}

.app-sidebar__item.router-link-active {
  border-color: rgba(0, 216, 255, 0.58);
  color: #ffffff;
  background: linear-gradient(90deg, rgba(10, 132, 255, 0.32), rgba(0, 216, 255, 0.09));
  box-shadow: 0 0 20px rgba(0, 132, 255, 0.24);
}

.app-sidebar__item--disabled {
  cursor: not-allowed;
  opacity: 0.58;
}

.app-sidebar__item small {
  color: var(--assetops-muted);
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
}

.app-sidebar__icon {
  display: inline-grid;
  width: 28px;
  height: 28px;
  place-items: center;
  border: 1px solid rgba(30, 155, 255, 0.35);
  border-radius: 7px;
  color: var(--assetops-cyan);
  background: rgba(7, 21, 40, 0.72);
  font-size: 12px;
}

.app-sidebar__version {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 6px;
  border: 1px solid rgba(30, 155, 255, 0.26);
  border-radius: 10px;
  padding: 14px;
  background: rgba(7, 21, 40, 0.76);
}

.app-sidebar__version strong {
  color: var(--assetops-text);
  font-size: 14px;
}

.app-sidebar__version span {
  color: var(--assetops-muted);
  font-size: 12px;
}

@media (max-width: 900px) {
  .app-sidebar {
    min-height: auto;
    grid-template-rows: auto auto;
    padding: 16px;
  }

  .app-sidebar__nav {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .app-sidebar__version {
    display: none;
  }
}
</style>
