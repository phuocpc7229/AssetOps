<template>
  <section
    class="dashboard-state"
    :class="{ 'dashboard-state--error': variant === 'error' }"
  >
    <strong>{{ title }}</strong>
    <span>{{ message }}</span>
  </section>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string
    message: string
    variant?: 'default' | 'error'
  }>(),
  {
    variant: 'default',
  },
)
</script>

<style scoped>
.dashboard-state {
  display: grid;
  min-height: 260px;
  place-items: center;
  gap: 8px;
  border: 1px solid rgba(30, 155, 255, 0.34);
  border-radius: 12px;
  background:
    linear-gradient(145deg, rgba(13, 33, 56, 0.82), rgba(3, 10, 24, 0.95)),
    var(--assetops-panel);
  padding: 26px;
  text-align: center;
  box-shadow: var(--assetops-glow);
}

.dashboard-state strong {
  color: var(--assetops-text);
  font-size: 18px;
}

.dashboard-state span {
  color: var(--assetops-muted);
  font-size: 14px;
}

.dashboard-state--error strong,
.dashboard-state--error span {
  color: #ffb9c0;
}
</style>
