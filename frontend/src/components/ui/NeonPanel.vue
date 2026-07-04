<template>
  <section class="neon-panel">
    <slot />
  </section>
</template>

<style scoped>
.neon-panel {
  position: relative;
  width: min(100%, 610px);
  overflow: hidden;
  border: 1px solid var(--assetops-border);
  border-radius: 32px;
  background:
    linear-gradient(145deg, rgba(13, 33, 56, 0.84), rgba(3, 10, 24, 0.92)),
    var(--assetops-panel);
  box-shadow:
    0 0 0 1px rgba(0, 216, 255, 0.05),
    var(--assetops-glow),
    inset 0 0 40px rgba(18, 107, 255, 0.08);
}

.neon-panel::before,
.neon-panel::after {
  position: absolute;
  left: 14%;
  width: 72%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--assetops-blue), transparent);
  box-shadow: 0 0 22px rgba(0, 132, 255, 0.95);
  content: "";
}

.neon-panel::before {
  top: 0;
}

.neon-panel::after {
  bottom: 0;
}
</style>
