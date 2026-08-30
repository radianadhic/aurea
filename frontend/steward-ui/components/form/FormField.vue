<template>
  <div class="form-field" :class="{ 'has-error': error, disabled, required }">
    <label v-if="label" :for="fieldId" class="form-label">
      {{ label }}
      <span v-if="required" class="required-mark">*</span>
    </label>
    <div class="form-input-wrapper">
      <slot />
      <div v-if="hint && !error" class="form-hint">{{ hint }}</div>
      <div v-if="error" class="form-error">{{ error }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  label?: string;
  hint?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  id?: string;
}

const props = withDefaults(defineProps<Props>(), {
  label: '',
  hint: '',
  error: '',
  required: false,
  disabled: false,
  id: '',
});

const fieldId = computed(() => props.id || `field-${Math.random().toString(36).slice(2, 9)}`);
</script>

<style scoped>
.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 2px;
}

.required-mark {
  color: #dc2626;
  font-weight: 600;
}

.form-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-hint {
  font-size: 12px;
  color: #6b7280;
  line-height: 1.4;
}

.form-error {
  font-size: 12px;
  color: #dc2626;
  display: flex;
  align-items: center;
  gap: 4px;
  line-height: 1.4;
}

.form-error::before {
  content: '⚠';
  font-size: 11px;
}

.has-error :deep(input),
.has-error :deep(textarea),
.has-error :deep(.el-input__wrapper) {
  border-color: #dc2626 !important;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1) !important;
}

.disabled {
  opacity: 0.5;
  pointer-events: none;
}
</style>
