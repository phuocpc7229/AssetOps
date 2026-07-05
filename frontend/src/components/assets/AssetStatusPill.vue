<template>
  <span
    class="asset-status-pill"
    :class="`asset-status-pill--${tone}`"
  >
    {{ label }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { AssetCriticality, AssetStatus } from '@/services/assets'

const props = defineProps<{
  value: AssetStatus | AssetCriticality
  type: 'status' | 'criticality'
}>()

const labels: Record<string, string> = {
  active: 'Active',
  in_maintenance: 'In Maintenance',
  archived: 'Archived',
  low: 'Low',
  medium: 'Medium',
  high: 'High',
  critical: 'Critical',
}

const toneByValue: Record<string, string> = {
  active: 'success',
  in_maintenance: 'warning',
  archived: 'muted',
  low: 'muted',
  medium: 'info',
  high: 'warning',
  critical: 'danger',
}

const label = computed(() => labels[props.value] ?? props.value)
const tone = computed(() => (props.type === 'status' ? toneByValue[props.value] : toneByValue[props.value]))
</script>

<style scoped>
.asset-status-pill {
  display: inline-flex;
  min-width: 78px;
  justify-content: center;
  border: 1px solid currentColor;
  border-radius: 6px;
  padding: 5px 8px;
  font-size: 12px;
  font-weight: 700;
  line-height: 1;
}

.asset-status-pill--success {
  color: #00d48a;
  background: rgba(0, 212, 138, 0.1);
}

.asset-status-pill--warning {
  color: #ff951a;
  background: rgba(255, 149, 26, 0.12);
}

.asset-status-pill--danger {
  color: #ff4d5e;
  background: rgba(255, 77, 94, 0.12);
}

.asset-status-pill--info {
  color: #00d8ff;
  background: rgba(0, 216, 255, 0.1);
}

.asset-status-pill--muted {
  color: var(--assetops-muted);
  background: rgba(142, 168, 203, 0.1);
}
</style>
