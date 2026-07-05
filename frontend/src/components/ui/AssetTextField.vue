<template>
  <label class="asset-text-field">
    <span class="asset-text-field__label">{{ label }}</span>
    <span class="asset-text-field__control">
      <span class="asset-text-field__icon" aria-hidden="true">
        <slot name="icon" />
      </span>
      <input
        :value="modelValue"
        :type="type"
        :name="name"
        :autocomplete="autocomplete"
        :placeholder="placeholder"
        :disabled="disabled"
        :aria-invalid="invalid"
        class="asset-text-field__input"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
      <button
        v-if="$slots.action"
        type="button"
        class="asset-text-field__action"
        :aria-label="actionLabel"
        :title="actionLabel"
        @click="$emit('action-click')"
      >
        <slot name="action" />
      </button>
    </span>
  </label>
</template>

<script setup lang="ts">
defineEmits<{
  'action-click': []
  'update:modelValue': [value: string]
}>()

withDefaults(
  defineProps<{
    label: string
    name: string
    placeholder: string
    modelValue?: string
    type?: 'text' | 'password'
    autocomplete?: string
    actionLabel?: string
    disabled?: boolean
    invalid?: boolean
  }>(),
  {
    modelValue: '',
    type: 'text',
    autocomplete: 'off',
    actionLabel: 'Field action',
    disabled: false,
    invalid: false,
  },
)
</script>

<style scoped>
.asset-text-field {
  display: grid;
  gap: 12px;
}

.asset-text-field__label {
  color: var(--assetops-text);
  font-size: 16px;
  font-weight: 500;
}

.asset-text-field__control {
  display: grid;
  min-height: 64px;
  grid-template-columns: 34px 1fr auto;
  align-items: center;
  gap: 14px;
  border: 1px solid var(--assetops-border-muted);
  border-radius: 9px;
  background: linear-gradient(145deg, rgba(13, 33, 56, 0.72), rgba(6, 15, 30, 0.86));
  padding: 0 18px;
  box-shadow: inset 0 0 24px rgba(0, 0, 0, 0.18);
  transition:
    border-color 160ms ease,
    box-shadow 160ms ease;
}

.asset-text-field__control:focus-within {
  border-color: var(--assetops-cyan);
  box-shadow:
    0 0 20px rgba(0, 184, 255, 0.22),
    inset 0 0 24px rgba(0, 0, 0, 0.2);
}

.asset-text-field__icon {
  display: inline-flex;
  color: var(--assetops-blue);
}

.asset-text-field__input {
  min-width: 0;
  border: 0;
  outline: 0;
  color: var(--assetops-text);
  background: transparent;
  font-size: 16px;
}

.asset-text-field__input:disabled {
  cursor: not-allowed;
  opacity: 0.72;
}

.asset-text-field__input::placeholder {
  color: var(--assetops-muted);
  opacity: 1;
}

.asset-text-field__action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border: 0;
  color: var(--assetops-muted);
  background: transparent;
  cursor: pointer;
}

.asset-text-field__action:hover {
  color: var(--assetops-cyan);
}
</style>
