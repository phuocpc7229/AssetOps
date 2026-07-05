<template>
  <main class="dashboard-page">
    <section class="dashboard-page__panel">
      <p>Authentication milestone complete</p>
      <h2>Dashboard</h2>
      <span>Asset operations metrics will appear here as later modules are implemented.</span>
    </section>
  </main>
</template>

<style scoped>
.dashboard-page {
  padding: 0 32px 34px;
}

.dashboard-page__panel {
  border: 1px solid rgba(30, 155, 255, 0.34);
  border-radius: 12px;
  background:
    linear-gradient(145deg, rgba(13, 33, 56, 0.82), rgba(3, 10, 24, 0.95)),
    var(--assetops-panel);
  padding: 24px;
  box-shadow:
    var(--assetops-glow),
    inset 0 0 42px rgba(18, 107, 255, 0.06);
}

.dashboard-page__panel p {
  margin: 0 0 6px;
  color: var(--assetops-cyan);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.dashboard-page__panel h2 {
  margin: 0;
  color: var(--assetops-text);
  font-size: 24px;
}

.dashboard-page__panel span {
  display: block;
  margin-top: 10px;
  color: var(--assetops-muted-strong);
}

@media (max-width: 720px) {
  .dashboard-page {
    padding: 0 18px 24px;
  }
}
</style>
