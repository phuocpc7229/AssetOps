<template>
  <span
    class="assetops-logo"
    :class="{
      'assetops-logo--with-wordmark': showWordmark,
    }"
    :style="{ '--assetops-logo-size': resolvedSize }"
    aria-label="AssetOps Portal"
  >
    <img
      class="assetops-logo__mark"
      :src="assetOpsLogoSymbol"
      alt=""
      aria-hidden="true"
    >

    <span
      v-if="showWordmark"
      class="assetops-logo__wordmark"
      aria-hidden="true"
    >
      <span class="assetops-logo__brand">
        <span class="assetops-logo__asset">ASSET</span><span class="assetops-logo__ops">OPS</span>
      </span>
      <span class="assetops-logo__portal">
        <span />
        <strong>PORTAL</strong>
        <span />
      </span>
    </span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import assetOpsLogoSymbol from '@/assets/brand/assetops-logo-symbol.png'

const props = withDefaults(
  defineProps<{
    size?: number | string
    glow?: boolean
  }>(),
  {
    size: 'medium',
    glow: true,
  },
)

const sizePresets: Record<string, string> = {
  small: '80px',
  medium: '154px',
  large: '276px',
}

const resolvedSize = computed(() => {
  if (typeof props.size === 'number') {
    return `${props.size}px`
  }

  return sizePresets[props.size] ?? props.size
})

const showWordmark = computed(() => props.size === 'large')
</script>

<style scoped>
.assetops-logo {
  --assetops-logo-size: 154px;

  display: inline-flex;
  width: var(--assetops-logo-size);
  flex-direction: column;
  align-items: center;
  color: var(--assetops-text);
  line-height: 1;
}

.assetops-logo__mark {
  display: block;
  width: auto;
  max-width: 100%;
  height: auto;
  object-fit: contain;
}

.assetops-logo__wordmark {
  display: grid;
  justify-items: center;
  margin-top: 22px;
}

.assetops-logo__brand {
  color: #f7fbff;
  font-size: 58px;
  font-weight: 800;
  letter-spacing: 8px;
  line-height: 1;
  text-shadow: 0 0 18px rgba(255, 255, 255, 0.22);
}

.assetops-logo__ops {
  margin-left: 8px;
  color: var(--assetops-blue);
  text-shadow: 0 0 18px rgba(0, 132, 255, 0.92);
}

.assetops-logo__portal {
  display: grid;
  width: 100%;
  max-width: 420px;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 24px;
  margin-top: 20px;
  color: #7488ad;
}

.assetops-logo__portal span {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--assetops-cyan));
}

.assetops-logo__portal span:last-child {
  background: linear-gradient(90deg, var(--assetops-cyan), transparent);
}

.assetops-logo__portal strong {
  font-size: 20px;
  font-weight: 500;
  letter-spacing: 22px;
  line-height: 1;
}

@media (max-width: 1024px) {
  .assetops-logo__brand {
    font-size: 42px;
  }
}

@media (max-width: 640px) {
  .assetops-logo__brand {
    font-size: 32px;
    letter-spacing: 5px;
  }

  .assetops-logo__portal strong {
    font-size: 14px;
    letter-spacing: 12px;
  }
}
</style>
