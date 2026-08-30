<template>
  <div class="loading-spinner" :class="sizeClass">
    <div class="spinner" :style="spinnerStyle"></div>
    <p v-if="message" class="loading-message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
  message?: string;
  inline?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  color: '#1e40af',
  message: '',
  inline: false,
});

const sizeClass = computed(() => `size-${props.size}`);

const spinnerStyle = computed(() => ({
  borderColor: `${props.color}20`,
  borderTopColor: props.color,
  width: props.size === 'sm' ? '20px' : props.size === 'lg' ? '48px' : '32px',
  height: props.size === 'sm' ? '20px' : props.size === 'lg' ? '48px' : '32px',
}));
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px;
  gap: 12px;
}

.loading-spinner.inline {
  display: inline-flex;
  flex-direction: row;
  padding: 0;
}

.spinner {
  border: 3px solid;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-message {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

.size-sm { padding: 8px; }
.size-lg { padding: 48px; }

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
