<template>
  <section class="dashboard-content-grid">
    <div class="dashboard-content-grid__main">
      <slot name="main" />
    </div>
    <aside class="dashboard-content-grid__side">
      <slot name="side" />
    </aside>
  </section>
</template>

<style scoped>
.dashboard-content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.9fr) minmax(360px, 0.95fr);
  gap: 18px;
}

.dashboard-content-grid__main,
.dashboard-content-grid__side {
  display: grid;
  align-content: start;
  gap: 18px;
  min-width: 0;
}

@media (max-width: 1180px) {
  .dashboard-content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
