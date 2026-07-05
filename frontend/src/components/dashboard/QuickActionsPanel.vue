<template>
  <section class="quick-actions-panel">
    <header>
      <p>Quick Actions</p>
      <h2>Asset Operations</h2>
    </header>

    <div class="quick-actions-panel__grid">
      <template
        v-for="action in actions"
        :key="action.label"
      >
        <RouterLink
          v-if="!action.disabled && action.to"
          class="quick-actions-panel__action"
          :to="action.to"
        >
          <span>{{ action.icon }}</span>
          <strong>{{ action.label }}</strong>
          <small>{{ action.helper }}</small>
          <em v-if="action.badge !== undefined">{{ action.badge }}</em>
        </RouterLink>
        <button
          v-else
          class="quick-actions-panel__action quick-actions-panel__action--disabled"
          type="button"
          disabled
        >
          <span>{{ action.icon }}</span>
          <strong>{{ action.label }}</strong>
          <small>Coming Soon</small>
        </button>
      </template>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, type RouteLocationRaw } from 'vue-router'

const props = defineProps<{
  badges: {
    maintenance_assets: number
    archived_assets: number
    expiring_warranty: number
  }
}>()

type QuickAction = {
  label: string
  helper: string
  icon: string
  to?: RouteLocationRaw
  badge?: number
  disabled?: boolean
}

const actions = computed<QuickAction[]>(() => [
  {
    label: 'Add Asset',
    helper: 'Create inventory record',
    icon: '+',
    to: { name: 'asset-new' },
  },
  {
    label: 'Open Assets',
    helper: 'Browse inventory',
    icon: 'A',
    to: { name: 'assets' },
  },
  {
    label: 'Maintenance',
    helper: 'Review maintenance queue',
    icon: 'M',
    to: { name: 'assets', query: { status: 'in_maintenance' } },
    badge: props.badges.maintenance_assets,
  },
  {
    label: 'Archived',
    helper: 'View retained records',
    icon: 'R',
    to: { name: 'assets', query: { status: 'archived', include_archived: 'true' } },
    badge: props.badges.archived_assets,
  },
  {
    label: 'Warranty Risk',
    helper: 'Assets expiring soon',
    icon: 'W',
    to: { name: 'assets', query: { warranty: 'expiring' } },
    badge: props.badges.expiring_warranty,
  },
  {
    label: 'Manage Sites',
    helper: 'Site registry',
    icon: 'S',
    to: { name: 'sites' },
  },
  {
    label: 'Import Assets',
    helper: 'Coming Soon',
    icon: 'I',
    disabled: true,
  },
  {
    label: 'Export Assets',
    helper: 'Coming Soon',
    icon: 'E',
    disabled: true,
  },
])
</script>

<style scoped>
.quick-actions-panel {
  border: 1px solid rgba(30, 155, 255, 0.34);
  border-radius: 12px;
  background:
    linear-gradient(145deg, rgba(13, 33, 56, 0.82), rgba(3, 10, 24, 0.95)),
    var(--assetops-panel);
  padding: 18px;
  box-shadow:
    var(--assetops-glow),
    inset 0 0 42px rgba(18, 107, 255, 0.06);
}

.quick-actions-panel header {
  margin-bottom: 14px;
}

.quick-actions-panel p {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.quick-actions-panel h2 {
  margin: 0;
  color: var(--assetops-text);
  font-size: 20px;
}

.quick-actions-panel__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.quick-actions-panel__action {
  position: relative;
  display: grid;
  min-height: 92px;
  align-content: center;
  gap: 6px;
  border: 1px solid rgba(30, 155, 255, 0.28);
  border-radius: 8px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
  padding: 12px 12px 12px 46px;
  text-align: left;
}

.quick-actions-panel__action span {
  position: absolute;
  top: 14px;
  left: 12px;
  display: grid;
  width: 24px;
  height: 24px;
  place-items: center;
  border: 1px solid rgba(0, 216, 255, 0.34);
  border-radius: 6px;
  color: var(--assetops-cyan);
  font-weight: 900;
}

.quick-actions-panel__action strong {
  color: var(--assetops-text);
  font-size: 13px;
}

.quick-actions-panel__action small {
  color: var(--assetops-muted);
  font-size: 12px;
}

.quick-actions-panel__action em {
  position: absolute;
  top: 10px;
  right: 10px;
  min-width: 24px;
  border-radius: 999px;
  color: #ffffff;
  background: rgba(10, 132, 255, 0.58);
  padding: 3px 7px;
  font-size: 11px;
  font-style: normal;
  font-weight: 900;
  text-align: center;
}

.quick-actions-panel__action--disabled {
  cursor: not-allowed;
  opacity: 0.58;
}
</style>
