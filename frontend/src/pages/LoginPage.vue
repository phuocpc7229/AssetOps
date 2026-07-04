<template>
  <AuthLayout>
    <NeonPanel>
      <div class="login-page">
        <AssetOpsLogo size="small" />

        <header class="login-page__header">
          <h1>Welcome back</h1>
          <p>Please sign in to continue</p>
        </header>

        <form class="login-page__form" aria-label="Sign in form">
          <AssetTextField
            label="Username"
            name="username"
            placeholder="Enter your username"
            autocomplete="username"
          >
            <template #icon>
              <svg viewBox="0 0 24 24" role="img">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                <circle cx="12" cy="7" r="4" />
              </svg>
            </template>
          </AssetTextField>

          <AssetTextField
            label="Password"
            name="password"
            :type="isPasswordVisible ? 'text' : 'password'"
            placeholder="Enter your password"
            autocomplete="current-password"
            :action-label="passwordVisibilityLabel"
            @action-click="togglePasswordVisibility"
          >
            <template #icon>
              <svg viewBox="0 0 24 24" role="img">
                <rect width="18" height="11" x="3" y="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
            </template>
            <template #action>
              <svg
                v-if="!isPasswordVisible"
                viewBox="0 0 24 24"
                role="img"
              >
                <title>{{ passwordVisibilityLabel }}</title>
                <path d="M17.94 17.94A10.94 10.94 0 0 1 12 20C7 20 2.73 16.89 1 12a13.16 13.16 0 0 1 5.06-5.94" />
                <path d="M10.58 10.58a2 2 0 0 0 2.83 2.83" />
                <path d="M9.9 4.24A10.77 10.77 0 0 1 12 4c5 0 9.27 3.11 11 8a13.2 13.2 0 0 1-2.42 3.74" />
                <path d="m1 1 22 22" />
              </svg>
              <svg
                v-else
                viewBox="0 0 24 24"
                role="img"
              >
                <title>{{ passwordVisibilityLabel }}</title>
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12" />
                <circle
                  cx="12"
                  cy="12"
                  r="3"
                />
              </svg>
            </template>
          </AssetTextField>

          <PrimaryButton>Sign in</PrimaryButton>
        </form>
      </div>
    </NeonPanel>
  </AuthLayout>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

import AssetOpsLogo from '@/components/ui/AssetOpsLogo.vue'
import AssetTextField from '@/components/ui/AssetTextField.vue'
import NeonPanel from '@/components/ui/NeonPanel.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

const isPasswordVisible = ref(false)

const passwordVisibilityLabel = computed(() =>
  isPasswordVisible.value ? 'Hide password' : 'Show password',
)

const togglePasswordVisibility = () => {
  isPasswordVisible.value = !isPasswordVisible.value
}
</script>

<style scoped>
.login-page {
  display: grid;
  justify-items: center;
  gap: 34px;
  padding: 58px 60px 76px;
}

.login-page__header {
  display: grid;
  gap: 10px;
  text-align: center;
}

.login-page__header h1 {
  margin: 0;
  color: var(--assetops-text);
  font-size: 40px;
  font-weight: 700;
  line-height: 1.1;
}

.login-page__header p {
  margin: 0;
  color: var(--assetops-muted);
  font-size: 20px;
  line-height: 1.4;
}

.login-page__form {
  display: grid;
  width: 100%;
  gap: 28px;
  margin-top: 8px;
}

.login-page__form svg {
  width: 24px;
  height: 24px;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.8;
}

.login-page__form .primary-button {
  margin-top: 16px;
}

@media (max-width: 640px) {
  .login-page {
    padding: 42px 22px 50px;
  }

  .login-page__header h1 {
    font-size: 32px;
  }

  .login-page__header p {
    font-size: 17px;
  }
}
</style>
