<template>
  <div class="filter-panel" :class="{ open: open }">
    <div class="filter-header" @click="open = !open">
      <div class="filter-header-left">
        <span class="filter-icon">🎚️</span>
        <span class="filter-label">Filter</span>
        <span v-if="activeCount > 0" class="filter-count">{{ activeCount }}</span>
      </div>
      <div class="filter-header-right">
        <button v-if="activeCount > 0" class="filter-clear" @click.stop="handleClearAll">
          Hapus semua
        </button>
        <span class="filter-toggle" :class="{ rotated: open }">▼</span>
      </div>
    </div>
    <transition name="slide-down">
      <div v-if="open" class="filter-content">
        <div class="filter-grid">
          <slot />
        </div>
        <div v-if="$slots.actions" class="filter-actions">
          <slot name="actions" />
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface Props {
  modelValue?: boolean;
  activeCount?: number;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: false,
  activeCount: 0,
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
  (e: 'clear'): void;
}>();

const open = ref(props.modelValue);

watch(() => props.modelValue, (val) => {
  open.value = val;
});

watch(open, (val) => {
  emit('update:modelValue', val);
});

function handleClearAll() {
  emit('clear');
}
</script>

<style scoped>
.filter-panel {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.filter-header {
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  user-select: none;
  background: #f9fafb;
  border-bottom: 1px solid #f3f4f6;
  transition: background 0.2s;
}

.filter-header:hover {
  background: #f3f4f6;
}

.filter-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-icon {
  font-size: 18px;
}

.filter-label {
  font-weight: 600;
  color: #111827;
  font-size: 14px;
}

.filter-count {
  background: #1e40af;
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 9999px;
  min-width: 20px;
  text-align: center;
}

.filter-header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-clear {
  background: transparent;
  border: 0;
  color: #1e40af;
  font-size: 13px;
  cursor: pointer;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;
}

.filter-clear:hover {
  background: rgba(30, 64, 175, 0.1);
}

.filter-toggle {
  font-size: 10px;
  color: #6b7280;
  transition: transform 0.2s;
}

.filter-toggle.rotated {
  transform: rotate(180deg);
}

.filter-content {
  padding: 20px;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.filter-actions {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.2s ease;
  overflow: hidden;
}

.slide-down-enter-from, .slide-down-leave-to {
  max-height: 0;
  opacity: 0;
}

.slide-down-enter-to, .slide-down-leave-from {
  max-height: 800px;
  opacity: 1;
}
</style>
