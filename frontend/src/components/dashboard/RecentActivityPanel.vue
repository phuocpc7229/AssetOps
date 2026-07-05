<template>
  <section class="recent-activity-panel">
    <header>
      <div>
        <p>Recent Activity</p>
        <h2>Operations Activity</h2>
      </div>
      <span>Temporary</span>
    </header>

    <div class="recent-activity-panel__notice">
      {{ note }}
    </div>

    <div
      v-if="activities.length"
      class="recent-activity-panel__list"
    >
      <RouterLink
        v-for="activity in activities"
        :key="activity.id"
        class="recent-activity-panel__item"
        :class="`recent-activity-panel__item--${activity.severity}`"
        :to="activity.route"
      >
        <span>{{ actionLabel(activity.action) }}</span>
        <strong>{{ activity.title }}</strong>
        <small>{{ activity.metadata }}</small>
        <time>{{ formatTime(activity.occurred_at) }}</time>
      </RouterLink>
    </div>
    <div
      v-else
      class="recent-activity-panel__empty"
    >
      No recent activity.
    </div>
  </section>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'

import type { DashboardActivity } from '@/services/dashboard'

defineProps<{
  activities: DashboardActivity[]
  note: string
}>()

const actionLabel = (action: DashboardActivity['action']) => {
  const labels = {
    created: 'Created',
    updated: 'Updated',
    archived: 'Archived',
  }

  return labels[action]
}

const formatTime = (value: string) =>
  new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
</script>

<style scoped>
.recent-activity-panel {
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

.recent-activity-panel header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 12px;
}

.recent-activity-panel p {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.recent-activity-panel h2 {
  margin: 0;
  color: var(--assetops-text);
  font-size: 20px;
}

.recent-activity-panel header > span {
  border: 1px solid rgba(255, 149, 26, 0.34);
  border-radius: 6px;
  color: #ff951a;
  background: rgba(255, 149, 26, 0.1);
  padding: 5px 8px;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
}

.recent-activity-panel__notice {
  border: 1px solid rgba(142, 168, 203, 0.16);
  border-radius: 8px;
  color: var(--assetops-muted);
  background: rgba(7, 21, 40, 0.58);
  padding: 10px;
  font-size: 12px;
  line-height: 1.4;
}

.recent-activity-panel__list {
  display: grid;
  gap: 10px;
  margin-top: 12px;
}

.recent-activity-panel__item {
  display: grid;
  grid-template-columns: 82px minmax(0, 1fr) auto;
  gap: 4px 10px;
  border: 1px solid rgba(30, 155, 255, 0.22);
  border-left-color: var(--assetops-cyan);
  border-radius: 8px;
  background: rgba(7, 21, 40, 0.62);
  padding: 10px;
}

.recent-activity-panel__item span {
  grid-row: span 2;
  align-self: center;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 900;
  text-transform: uppercase;
}

.recent-activity-panel__item strong {
  overflow: hidden;
  color: var(--assetops-text);
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recent-activity-panel__item small {
  overflow: hidden;
  color: var(--assetops-muted);
  font-size: 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recent-activity-panel__item time {
  grid-row: span 2;
  align-self: center;
  color: var(--assetops-muted);
  font-size: 11px;
  text-align: right;
}

.recent-activity-panel__item--success {
  border-left-color: #00d48a;
}

.recent-activity-panel__item--warning {
  border-left-color: #ff951a;
}

.recent-activity-panel__item--danger {
  border-left-color: #ff4d5e;
}

.recent-activity-panel__empty {
  display: grid;
  min-height: 120px;
  place-items: center;
  color: var(--assetops-muted);
  font-size: 13px;
  font-weight: 700;
}
</style>
