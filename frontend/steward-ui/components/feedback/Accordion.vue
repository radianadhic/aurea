<template>
  <div class="accordion" :class="[`accordion-${variant}`]">
    <div
      v-for="(item, idx) in items"
      :key="item.key || idx"
      class="accordion-item"
      :class="{
        active: isOpen(idx),
        disabled: item.disabled,
      }"
    >
      <button
        class="accordion-header"
        :disabled="item.disabled"
        @click="toggle(idx)"
      >
        <div class="header-left">
          <span v-if="item.icon" class="header-icon">{{ item.icon }}</span>
          <div class="header-content">
            <div class="header-title">{{ item.title }}</div>
            <div v-if="item.subtitle" class="header-subtitle">{{ item.subtitle }}</div>
          </div>
        </div>
        <div class="header-right">
          <span v-if="item.badge" class="header-badge">{{ item.badge }}</span>
          <span class="header-chevron" :class="{ rotated: isOpen(idx) }">▼</span>
        </div>
      </button>
      <transition name="accordion-slide">
        <div v-show="isOpen(idx)" class="accordion-body">
          <div class="accordion-content">
            <slot :name="item.key || `item-${idx}`" :item="item" :index="idx" :open="isOpen(idx)">
              {{ item.content }}
            </slot>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface AccordionItem {
  key?: string;
  title: string;
  subtitle?: string;
  icon?: string;
  content?: string;
  disabled?: boolean;
  badge?: string | number;
}

interface Props {
  items: AccordionItem[];
  modelValue?: string | number | (string | number)[];
  multiple?: boolean;
  variant?: 'default' | 'bordered' | 'flush';
}

const props = withDefaults(defineProps<Props>(), {
  multiple: false,
  variant: 'default',
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number | (string | number)[]): void;
  (e: 'change', key: string | number, open: boolean): void;
}>();

function isOpen(idx: number): boolean {
  const key = props.items[idx].key ?? idx;
  if (Array.isArray(props.modelValue)) {
    return props.modelValue.includes(key);
  }
  return props.modelValue === key;
}

function toggle(idx: number) {
  if (props.items[idx].disabled) return;
  const key = props.items[idx].key ?? idx;

  if (props.multiple) {
    const current = Array.isArray(props.modelValue) ? [...props.modelValue] : [];
    const i = current.indexOf(key);
    if (i === -1) {
      current.push(key);
    } else {
      current.splice(i, 1);
    }
    emit('update:modelValue', current);
    emit('change', key, i === -1);
  } else {
    const willOpen = !isOpen(idx);
    emit('update:modelValue', willOpen ? key : -1);
    emit('change', key, willOpen);
  }
}
</script>

<style scoped>
.accordion {
  width: 100%;
}

.accordion-default .accordion-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 8px;
  overflow: hidden;
}

.accordion-bordered .accordion-item {
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.accordion-flush .accordion-item {
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.accordion-flush .accordion-item:first-child {
  border-top: 1px solid #e5e7eb;
}

.accordion-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: transparent;
  border: 0;
  cursor: pointer;
  font-family: inherit;
  text-align: left;
  transition: background 0.15s;
}

.accordion-header:hover:not(:disabled) {
  background: #f9fafb;
}

.accordion-item.active .accordion-header {
  background: #f9fafb;
}

.accordion-header:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.header-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.header-content {
  flex: 1;
  min-width: 0;
}

.header-title {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.header-subtitle {
  font-size: 12px;
  color: #6b7280;
  margin-top: 2px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-badge {
  background: #f3f4f6;
  color: #6b7280;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 600;
}

.header-chevron {
  font-size: 10px;
  color: #6b7280;
  transition: transform 0.2s;
}

.header-chevron.rotated {
  transform: rotate(180deg);
}

.accordion-body {
  overflow: hidden;
}

.accordion-content {
  padding: 0 16px 16px;
  font-size: 14px;
  color: #374151;
  line-height: 1.6;
}

.accordion-slide-enter-active, .accordion-slide-leave-active {
  transition: all 0.2s ease;
  overflow: hidden;
}

.accordion-slide-enter-from, .accordion-slide-leave-to {
  max-height: 0;
  opacity: 0;
}

.accordion-slide-enter-to, .accordion-slide-leave-from {
  max-height: 1000px;
  opacity: 1;
}
</style>
