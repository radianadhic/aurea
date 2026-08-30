<template>
  <Teleport to="body">
    <div class="toast-container" :class="`toast-${position}`">
      <transition-group name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="toast-item"
          :class="`toast-${toast.type}`"
          @mouseenter="pause(toast)"
          @mouseleave="resume(toast)"
        >
          <div class="toast-icon">
            <span v-if="toast.type === 'success'">✓</span>
            <span v-else-if="toast.type === 'error'">✕</span>
            <span v-else-if="toast.type === 'warning'">!</span>
            <span v-else>i</span>
          </div>
          <div class="toast-body">
            <div v-if="toast.title" class="toast-title">{{ toast.title }}</div>
            <div class="toast-message">{{ toast.message }}</div>
          </div>
          <button v-if="toast.closable" class="toast-close" @click="dismiss(toast.id)">✕</button>
          <div v-if="toast.duration > 0" class="toast-progress" :style="{ animationDuration: `${toast.duration}ms` }" />
        </div>
      </transition-group>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface Toast {
  id: number;
  type: ToastType;
  title?: string;
  message: string;
  duration: number;
  closable: boolean;
  timestamp: number;
  timeoutId?: any;
  paused?: boolean;
  remaining?: number;
}

interface Props {
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
  max?: number;
}

const props = withDefaults(defineProps<Props>(), {
  position: 'top-right',
  max: 5,
});

const toasts = ref<Toast[]>([]);
let nextId = 1;

// Public API via window for global access
function show(message: string, options: Partial<Toast> = {}) {
  const toast: Toast = {
    id: nextId++,
    type: 'info',
    message,
    duration: 4000,
    closable: true,
    timestamp: Date.now(),
    ...options,
  };
  toasts.value.push(toast);
  if (toasts.value.length > props.max) {
    dismiss(toasts.value[0].id);
  }
  if (toast.duration > 0) {
    toast.remaining = toast.duration;
    scheduleTimeout(toast);
  }
}

function scheduleTimeout(toast: Toast) {
  toast.timeoutId = setTimeout(() => {
    dismiss(toast.id);
  }, toast.remaining);
}

function pause(toast: Toast) {
  if (toast.timeoutId) {
    clearTimeout(toast.timeoutId);
    toast.timeoutId = null;
  }
}

function resume(toast: Toast) {
  if (toast.duration > 0 && !toast.timeoutId) {
    scheduleTimeout(toast);
  }
}

function dismiss(id: number) {
  const idx = toasts.value.findIndex((t) => t.id === id);
  if (idx !== -1) {
    if (toasts.value[idx].timeoutId) {
      clearTimeout(toasts.value[idx].timeoutId);
    }
    toasts.value.splice(idx, 1);
  }
}

function success(message: string, title?: string) { show(message, { type: 'success', title }); }
function error(message: string, title?: string) { show(message, { type: 'error', title }); }
function warning(message: string, title?: string) { show(message, { type: 'warning', title }); }
function info(message: string, title?: string) { show(message, { type: 'info', title }); }
function clear() { toasts.value = []; }

defineExpose({ show, success, error, warning, info, clear, dismiss });

onMounted(() => {
  if (typeof window !== 'undefined') {
    (window as any).$toast = { show, success, error, warning, info, clear };
  }
});

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    delete (window as any).$toast;
  }
});
</script>

<style scoped>
.toast-container {
  position: fixed;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 360px;
  pointer-events: none;
}

.toast-top-right { top: 16px; right: 16px; }
.toast-top-left { top: 16px; left: 16px; }
.toast-bottom-right { bottom: 16px; right: 16px; }
.toast-bottom-left { bottom: 16px; left: 16px; }
.toast-top-center { top: 16px; left: 50%; transform: translateX(-50%); }
.toast-bottom-center { bottom: 16px; left: 50%; transform: translateX(-50%); }

.toast-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border-left: 4px solid #6b7280;
  pointer-events: auto;
  position: relative;
  overflow: hidden;
  min-width: 280px;
}

.toast-success { border-left-color: #16a34a; }
.toast-error { border-left-color: #dc2626; }
.toast-warning { border-left-color: #ea580c; }
.toast-info { border-left-color: #0284c7; }

.toast-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
  color: white;
}

.toast-success .toast-icon { background: #16a34a; }
.toast-error .toast-icon { background: #dc2626; }
.toast-warning .toast-icon { background: #ea580c; }
.toast-info .toast-icon { background: #0284c7; }

.toast-body {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-size: 13px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 2px;
}

.toast-message {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.4;
}

.toast-close {
  background: transparent;
  border: 0;
  font-size: 14px;
  color: #9ca3af;
  cursor: pointer;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  flex-shrink: 0;
  transition: all 0.15s;
}

.toast-close:hover {
  background: #f3f4f6;
  color: #111827;
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  background: rgba(0, 0, 0, 0.1);
  animation: toastProgress linear forwards;
  transform-origin: left;
}

@keyframes toastProgress {
  from { width: 100%; }
  to { width: 0; }
}

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.toast-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
