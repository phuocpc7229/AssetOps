<template>
  <button
    class="primary-button"
    type="button"
  >
    <slot />
  </button>
</template>

<style scoped>
.primary-button {
  position: relative;
  min-height: 64px;
  overflow: hidden;
  border: 1px solid rgba(36, 212, 255, 0.62);
  border-radius: 8px;
  color: #ffffff;
  background: linear-gradient(110deg, #058cff 0%, #0b6fff 46%, #123de8 100%);
  box-shadow:
    0 0 22px rgba(0, 132, 255, 0.5),
    0 0 44px rgba(0, 216, 255, 0.16),
    inset 0 1px 0 rgba(255, 255, 255, 0.28),
    inset 0 -14px 28px rgba(0, 45, 180, 0.22);
  cursor: pointer;
  font-size: 17px;
  font-weight: 600;
  line-height: 1;
  transition:
    border-color 160ms ease,
    box-shadow 160ms ease,
    transform 160ms ease;
}

.primary-button::before,
.primary-button::after {
  position: absolute;
  pointer-events: none;
  content: "";
}

.primary-button::before {
  inset: 0;
  background:
    radial-gradient(circle at 16% 18%, rgba(111, 237, 255, 0.42), transparent 32%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.18), transparent 42%);
}

.primary-button::after {
  inset: 0;
  background: linear-gradient(100deg, transparent 22%, rgba(255, 255, 255, 0.22) 50%, transparent 78%);
  opacity: 0;
  transition: opacity 160ms ease;
}

.primary-button:hover {
  border-color: rgba(91, 232, 255, 0.76);
  box-shadow:
    0 0 30px rgba(0, 132, 255, 0.62),
    0 0 58px rgba(0, 216, 255, 0.22),
    inset 0 1px 0 rgba(255, 255, 255, 0.32),
    inset 0 -14px 28px rgba(0, 45, 180, 0.2);
  transform: translateY(-1px);
}

.primary-button:hover::after {
  opacity: 1;
}

.primary-button:focus-visible {
  outline: 2px solid var(--assetops-cyan);
  outline-offset: 3px;
}
</style>
