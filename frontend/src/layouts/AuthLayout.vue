<template>
  <main class="auth-layout">
    <section class="auth-layout__brand" aria-label="AssetOps Portal brand">
      <AssetOpsLogo size="large" />
    </section>

    <section class="auth-layout__content" aria-label="Sign in form">
      <slot />
    </section>

    <p class="auth-layout__footer">&copy; 2026 AssetOps Portal. All rights reserved.</p>
  </main>
</template>

<script setup lang="ts">
import AssetOpsLogo from '@/components/ui/AssetOpsLogo.vue'
</script>

<style scoped>
.auth-layout {
  position: relative;
  display: grid;
  min-height: 100vh;
  grid-template-columns: minmax(360px, 1fr) minmax(520px, 0.92fr);
  gap: 48px;
  overflow: hidden;
  padding: 72px 8vw 64px;
  background:
    radial-gradient(circle at 13% 72%, rgba(0, 132, 255, 0.34), transparent 3%),
    radial-gradient(circle at 35% 69%, rgba(0, 216, 255, 0.26), transparent 2%),
    linear-gradient(118deg, rgba(2, 7, 19, 0.9), rgba(2, 7, 19, 0.98)),
    var(--assetops-black);
}

.auth-layout::before,
.auth-layout::after {
  position: absolute;
  inset: 0;
  pointer-events: none;
  content: "";
}

.auth-layout::before {
  opacity: 0.72;
  background:
    linear-gradient(90deg, rgba(0, 132, 255, 0.16) 1px, transparent 1px),
    linear-gradient(0deg, rgba(0, 132, 255, 0.12) 1px, transparent 1px);
  background-position: center bottom;
  background-size: 54px 54px;
  mask-image: linear-gradient(to top, black 0%, transparent 54%);
}

.auth-layout::after {
  background:
    linear-gradient(180deg, transparent 0 58%, rgba(0, 132, 255, 0.12) 59%, transparent 60%),
    radial-gradient(circle at 3% 43%, rgba(0, 216, 255, 0.58), transparent 1.2%),
    radial-gradient(circle at 40% 70%, rgba(0, 132, 255, 0.6), transparent 1.1%);
  opacity: 0.9;
}

.auth-layout__brand,
.auth-layout__content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
}

.auth-layout__brand {
  justify-content: center;
}

.auth-layout__content {
  justify-content: center;
}

.auth-layout__footer {
  position: absolute;
  z-index: 1;
  right: 0;
  bottom: 22px;
  left: 0;
  margin: 0;
  color: var(--assetops-muted);
  font-size: 14px;
  text-align: center;
}

@media (max-width: 1024px) {
  .auth-layout {
    grid-template-columns: 1fr;
    gap: 36px;
    padding: 48px 24px 72px;
  }

  .auth-layout__brand {
    align-items: flex-end;
  }
}

@media (max-width: 640px) {
  .auth-layout {
    padding: 32px 16px 72px;
  }
}
</style>
