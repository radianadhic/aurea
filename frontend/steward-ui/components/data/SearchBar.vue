<template>
  <div class="search-bar">
    <div class="search-input-wrapper">
      <span class="search-icon">🔍</span>
      <input
        v-model="localValue"
        type="text"
        :placeholder="placeholder"
        class="search-input"
        @input="handleInput"
        @keyup.enter="handleSearch"
        @keyup.esc="handleClear"
      />
      <button v-if="localValue" class="clear-btn" @click="handleClear" title="Clear">
        ✕
      </button>
    </div>
    <button class="search-btn" @click="handleSearch">
      Cari
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

interface Props {
  modelValue?: string;
  placeholder?: string;
  debounce?: number;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: 'Cari CIF, nama, NIK, email...',
  debounce: 300,
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
  (e: 'search', value: string): void;
  (e: 'clear'): void;
}>();

const localValue = ref(props.modelValue);
let timeoutId: any = null;

watch(() => props.modelValue, (val) => {
  localValue.value = val;
});

function handleInput() {
  emit('update:modelValue', localValue.value);
  if (timeoutId) clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    emit('search', localValue.value);
  }, props.debounce);
}

function handleSearch() {
  if (timeoutId) clearTimeout(timeoutId);
  emit('search', localValue.value);
}

function handleClear() {
  localValue.value = '';
  emit('update:modelValue', '');
  emit('clear');
  if (timeoutId) clearTimeout(timeoutId);
}
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 8px;
  width: 100%;
}

.search-input-wrapper {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 10px 36px 10px 36px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
  background: white;
}

.search-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.clear-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: #f3f4f6;
  border: 0;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 12px;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.clear-btn:hover {
  background: #e5e7eb;
  color: #111827;
}

.search-btn {
  padding: 10px 20px;
  background: #1e40af;
  color: white;
  border: 0;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.search-btn:hover {
  background: #1e3a8a;
}
</style>
