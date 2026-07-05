<template>
  <div
    ref="rootElement"
    class="searchable-select"
    :class="{ 'searchable-select--open': isOpen, 'searchable-select--invalid': error }"
  >
    <div
      role="button"
      tabindex="0"
      class="searchable-select__control"
      :aria-expanded="isOpen"
      @click="toggleOpen"
      @keydown.enter.prevent="toggleOpen"
      @keydown.space.prevent="toggleOpen"
      @keydown.down.prevent="openAndMove(1)"
      @keydown.up.prevent="openAndMove(-1)"
      @keydown.esc.prevent="close"
    >
      <span :class="{ 'searchable-select__placeholder': !selectedOption }">
        {{ selectedOption?.label ?? placeholder }}
      </span>
      <button
        v-if="clearable && selectedOption"
        type="button"
        class="searchable-select__clear"
        aria-label="Clear selection"
        @click.stop="selectOption(null)"
      >
        Clear
      </button>
    </div>

    <div
      v-if="isOpen"
      class="searchable-select__menu"
    >
      <input
        ref="searchInput"
        v-model.trim="search"
        class="searchable-select__search"
        :placeholder="searchPlaceholder"
        @keydown.down.prevent="moveActive(1)"
        @keydown.up.prevent="moveActive(-1)"
        @keydown.enter.prevent="selectActiveOption"
        @keydown.esc.prevent="close"
      >
      <div class="searchable-select__list">
        <button
          v-for="(option, index) in filteredOptions"
          :key="option.id"
          type="button"
          class="searchable-select__option"
          :class="{ 'searchable-select__option--active': index === activeIndex }"
          @click="selectOption(option.id)"
        >
          <strong>{{ option.label }}</strong>
          <span v-if="option.detail">{{ option.detail }}</span>
        </button>
        <p
          v-if="filteredOptions.length === 0"
          class="searchable-select__empty"
        >
          No matching records.
        </p>
      </div>
    </div>

    <small v-if="error">{{ error }}</small>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

type SearchableSelectOption = {
  id: number | string
  label: string
  detail?: string
}

const props = withDefaults(
  defineProps<{
    modelValue: number | string | null
    options: SearchableSelectOption[]
    placeholder: string
    searchPlaceholder?: string
    clearable?: boolean
    error?: string | null
  }>(),
  {
    searchPlaceholder: 'Search',
    clearable: false,
    error: null,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: number | string | null]
}>()

const isOpen = ref(false)
const search = ref('')
const searchInput = ref<{ focus: () => void } | null>(null)
const rootElement = ref<{ contains: (target: unknown) => boolean } | null>(null)
const activeIndex = ref(0)

const selectedOption = computed(() => props.options.find((option) => option.id === props.modelValue) ?? null)

const filteredOptions = computed(() => {
  const normalizedSearch = search.value.toLowerCase()
  if (!normalizedSearch) {
    return props.options
  }

  return props.options.filter((option) =>
    `${option.label} ${option.detail ?? ''}`.toLowerCase().includes(normalizedSearch),
  )
})

const open = async () => {
  isOpen.value = true
  search.value = ''
  activeIndex.value = 0
  await nextTick()
  searchInput.value?.focus()
}

const close = () => {
  isOpen.value = false
  search.value = ''
}

const toggleOpen = () => {
  if (isOpen.value) {
    close()
    return
  }

  void open()
}

const selectOption = (value: number | string | null) => {
  emit('update:modelValue', value)
  close()
}

const moveActive = (step: number) => {
  if (filteredOptions.value.length === 0) {
    activeIndex.value = 0
    return
  }

  activeIndex.value = (activeIndex.value + step + filteredOptions.value.length) % filteredOptions.value.length
}

const openAndMove = (step: number) => {
  if (!isOpen.value) {
    void open()
    return
  }

  moveActive(step)
}

const selectActiveOption = () => {
  const option = filteredOptions.value[activeIndex.value]
  if (option) {
    selectOption(option.id)
  }
}

const closeOnOutsideClick = (event: { target: unknown }) => {
  if (rootElement.value && !rootElement.value.contains(event.target)) {
    close()
  }
}

watch(filteredOptions, () => {
  activeIndex.value = 0
})

onMounted(() => {
  globalThis.document?.addEventListener('mousedown', closeOnOutsideClick)
})

onBeforeUnmount(() => {
  globalThis.document?.removeEventListener('mousedown', closeOnOutsideClick)
})

</script>

<style scoped>
.searchable-select {
  position: relative;
  display: grid;
  gap: 6px;
}

.searchable-select__control {
  display: flex;
  width: 100%;
  min-height: 45px;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  border: 1px solid var(--assetops-border-muted);
  border-radius: 8px;
  color: var(--assetops-text);
  background: linear-gradient(145deg, rgba(13, 33, 56, 0.74), rgba(6, 15, 30, 0.9));
  padding: 0 12px;
  text-align: left;
  cursor: pointer;
}

.searchable-select--open .searchable-select__control,
.searchable-select__control:focus {
  border-color: var(--assetops-cyan);
  box-shadow: 0 0 16px rgba(0, 216, 255, 0.18);
  outline: 0;
}

.searchable-select--invalid .searchable-select__control {
  border-color: rgba(255, 77, 94, 0.72);
}

.searchable-select__placeholder {
  color: var(--assetops-muted);
}

.searchable-select__clear {
  border: 1px solid rgba(30, 155, 255, 0.26);
  border-radius: 7px;
  color: var(--assetops-muted-strong);
  background: rgba(7, 21, 40, 0.72);
  padding: 5px 8px;
  font-size: 12px;
  font-weight: 700;
}

.searchable-select__menu {
  position: absolute;
  z-index: 40;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  overflow: hidden;
  border: 1px solid rgba(30, 155, 255, 0.42);
  border-radius: 8px;
  background: var(--assetops-panel-strong);
  box-shadow: var(--assetops-strong-glow);
}

.searchable-select__search {
  width: 100%;
  border: 0;
  border-bottom: 1px solid rgba(142, 168, 203, 0.16);
  color: var(--assetops-text);
  background: rgba(7, 21, 40, 0.94);
  padding: 12px;
  outline: 0;
}

.searchable-select__list {
  max-height: 240px;
  overflow-y: auto;
  padding: 6px;
}

.searchable-select__option {
  display: grid;
  width: 100%;
  gap: 4px;
  border: 0;
  border-radius: 7px;
  color: var(--assetops-text);
  background: transparent;
  padding: 10px;
  text-align: left;
  cursor: pointer;
}

.searchable-select__option:hover,
.searchable-select__option--active,
.searchable-select__option:focus {
  background: rgba(0, 132, 255, 0.2);
  outline: 0;
}

.searchable-select__option span,
.searchable-select__empty,
.searchable-select small {
  color: var(--assetops-muted);
  font-size: 12px;
}

.searchable-select small {
  color: #ffb9c0;
  font-weight: 700;
}

.searchable-select__empty {
  margin: 0;
  padding: 12px;
}
</style>
