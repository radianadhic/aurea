<template>
  <div class="tabs-component" :class="[`tabs-${position}`, { boxed, 'with-icons': $slots.icon }]">
    <div class="tabs-nav">
      <div class="tabs-nav-inner" ref="navRef">
        <button
          v-for="(tab, idx) in tabs"
          :key="tab.id || tab.name || idx"
          class="tab-button"
          :class="{
            active: idx === activeIndex,
            disabled: tab.disabled,
          }"
          :style="idx === activeIndex ? activeStyle : {}"
          :disabled="tab.disabled"
          @click="selectTab(idx)"
        >
          <span v-if="$slots.icon || tab.icon" class="tab-icon">
            <slot :name="`icon-${tab.name}`">
              {{ tab.icon }}
            </slot>
          </span>
          <span class="tab-label">
            {{ tab.label }}
            <span v-if="tab.badge !== undefined" class="tab-badge" :class="`badge-${tab.badgeType || 'primary'}`">
              {{ tab.badge }}
            </span>
          </span>
          <span v-if="closable && !tab.disabled" class="tab-close" @click.stop="closeTab(idx)">✕</span>
        </button>
        <div v-if="!boxed" class="tab-indicator" :style="indicatorStyle" />
      </div>
    </div>
    <div class="tabs-content">
      <div
        v-for="(tab, idx) in tabs"
        :key="`panel-${tab.id || tab.name || idx}`"
        v-show="idx === activeIndex"
        class="tab-panel"
        :class="{ active: idx === activeIndex }"
      >
        <slot :name="tab.name" :tab="tab" :index="idx" :active="idx === activeIndex" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue';

export interface Tab {
  name: string;
  id?: string;
  label: string;
  icon?: string;
  disabled?: boolean;
  closable?: boolean;
  badge?: string | number;
  badgeType?: 'primary' | 'success' | 'warning' | 'danger' | 'info';
}

interface Props {
  modelValue?: string | number;
  tabs: Tab[];
  position?: 'top' | 'bottom' | 'left' | 'right';
  boxed?: boolean;
  closable?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: 0,
  position: 'top',
  boxed: false,
  closable: false,
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void;
  (e: 'change', tab: Tab, index: number): void;
  (e: 'close', tab: Tab, index: number): void;
}>();

const activeIndex = ref<number>(typeof props.modelValue === 'number' ? props.modelValue : 0);
const navRef = ref<HTMLElement>();
const indicatorStyle = ref({});

const activeStyle = computed(() => {
  return {}; // Indicator is positioned absolutely
});

watch(() => props.modelValue, (val) => {
  if (typeof val === 'number' && val !== activeIndex.value) {
    activeIndex.value = val;
    updateIndicator();
  } else if (typeof val === 'string') {
    const idx = props.tabs.findIndex((t) => t.name === val || t.id === val);
    if (idx !== -1 && idx !== activeIndex.value) {
      activeIndex.value = idx;
      updateIndicator();
    }
  }
});

function selectTab(idx: number) {
  if (props.tabs[idx].disabled) return;
  activeIndex.value = idx;
  emit('update:modelValue', idx);
  emit('change', props.tabs[idx], idx);
  updateIndicator();
}

function closeTab(idx: number) {
  emit('close', props.tabs[idx], idx);
}

function updateIndicator() {
  if (!navRef.value) return;
  nextTick(() => {
    const activeBtn = navRef.value?.querySelector('.tab-button.active') as HTMLElement;
    if (activeBtn && navRef.value) {
      const navRect = navRef.value.getBoundingClientRect();
      const btnRect = activeBtn.getBoundingClientRect();
      indicatorStyle.value = {
        left: `${btnRect.left - navRect.left}px`,
        width: `${btnRect.width}px`,
      };
    }
  });
}

watch(() => props.tabs, () => {
  updateIndicator();
}, { deep: true });

if (typeof window !== 'undefined') {
  window.addEventListener('resize', updateIndicator);
}
</script>

<style scoped>
.tabs-component {
  display: flex;
  flex-direction: column;
}

.tabs-component.tabs-bottom {
  flex-direction: column-reverse;
}

.tabs-component.tabs-left {
  flex-direction: row;
}

.tabs-component.tabs-right {
  flex-direction: row-reverse;
}

.tabs-nav {
  border-bottom: 1px solid #e5e7eb;
  background: white;
}

.boxed .tabs-nav {
  border-bottom: 0;
  padding: 0 16px;
}

.tabs-nav-inner {
  display: flex;
  position: relative;
  overflow-x: auto;
  scrollbar-width: thin;
}

.tabs-left .tabs-nav-inner,
.tabs-right .tabs-nav-inner {
  flex-direction: column;
  border-bottom: 0;
  border-right: 1px solid #e5e7eb;
}

.tab-button {
  background: transparent;
  border: 0;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  white-space: nowrap;
  position: relative;
  font-family: inherit;
}

.tab-button:hover:not(.disabled) {
  color: #111827;
  background: rgba(30, 64, 175, 0.04);
}

.tab-button.active {
  color: #1e40af;
  font-weight: 600;
}

.boxed .tab-button {
  border: 1px solid transparent;
  border-bottom: 0;
  border-radius: 8px 8px 0 0;
  margin-bottom: -1px;
}

.boxed .tab-button.active {
  border-color: #e5e7eb;
  background: white;
  color: #1e40af;
  position: relative;
  z-index: 1;
}

.tab-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.tab-icon {
  font-size: 16px;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 6px;
}

.tab-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9999px;
  font-size: 10px;
  font-weight: 600;
}

.badge-primary { background: #dbeafe; color: #1e40af; }
.badge-success { background: #d1fae5; color: #15803d; }
.badge-warning { background: #fed7aa; color: #c2410c; }
.badge-danger { background: #fee2e2; color: #b91c1c; }
.badge-info { background: #e0f2fe; color: #075985; }

.tab-close {
  margin-left: 4px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  font-size: 10px;
  cursor: pointer;
  opacity: 0;
  transition: all 0.15s;
}

.tab-button:hover .tab-close {
  opacity: 1;
}

.tab-close:hover {
  background: #fee2e2;
  color: #b91c1c;
}

.tab-indicator {
  position: absolute;
  bottom: 0;
  height: 2px;
  background: #1e40af;
  transition: all 0.2s ease;
}

.tabs-left .tab-indicator,
.tabs-right .tab-indicator {
  bottom: auto;
  width: 2px;
  height: auto;
  top: 0;
}

.tabs-content {
  flex: 1;
  padding: 16px 0;
}

.tab-panel {
  display: none;
}

.tab-panel.active {
  display: block;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
