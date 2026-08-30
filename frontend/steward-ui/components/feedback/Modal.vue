<template>
  <Teleport to="body">
    <transition name="modal" appear>
      <div v-if="modelValue" class="modal-overlay" @click.self="onOverlayClick">
        <div class="modal-container" :class="[`size-${size}`, { fullscreen }]" role="dialog">
          <header v-if="title || $slots.header" class="modal-header">
            <slot name="header">
              <h3 class="modal-title">{{ title }}</h3>
            </slot>
            <button v-if="showClose" class="modal-close" @click="close" aria-label="Close">✕</button>
          </header>

          <div class="modal-body" :style="{ maxHeight: bodyMaxHeight }">
            <slot />
          </div>

          <footer v-if="$slots.footer || showDefaultFooter" class="modal-footer">
            <slot name="footer">
              <el-button v-if="showCancel" @click="close">{{ cancelText }}</el-button>
              <el-button
                v-if="showOk"
                type="primary"
                :loading="loading"
                :disabled="disableOk"
                @click="onOk"
              >
                {{ okText }}
              </el-button>
            </slot>
          </footer>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, watch, onUnmounted } from 'vue';

interface Props {
  modelValue: boolean;
  title?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
  fullscreen?: boolean;
  showClose?: boolean;
  showDefaultFooter?: boolean;
  showCancel?: boolean;
  showOk?: boolean;
  cancelText?: string;
  okText?: string;
  loading?: boolean;
  disableOk?: boolean;
  closeOnOverlay?: boolean;
  closeOnEscape?: boolean;
  bodyMaxHeight?: string;
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  size: 'md',
  fullscreen: false,
  showClose: true,
  showDefaultFooter: false,
  showCancel: true,
  showOk: true,
  cancelText: 'Batal',
  okText: 'OK',
  loading: false,
  disableOk: false,
  closeOnOverlay: true,
  closeOnEscape: true,
  bodyMaxHeight: '70vh',
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
  (e: 'close'): void;
  (e: 'ok'): void;
  (e: 'cancel'): void;
}>();

function close() {
  emit('update:modelValue', false);
  emit('close');
}

function onOk() {
  emit('ok');
}

function onOverlayClick() {
  if (props.closeOnOverlay) close();
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && props.modelValue && props.closeOnEscape) {
    close();
  }
}

watch(() => props.modelValue, (val) => {
  if (val) {
    document.addEventListener('keydown', onKeydown);
    document.body.style.overflow = 'hidden';
  } else {
    document.removeEventListener('keydown', onKeydown);
    document.body.style.overflow = '';
  }
});

onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown);
  document.body.style.overflow = '';
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 16px;
  overflow-y: auto;
}

.modal-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
  max-width: 100%;
  max-height: 100%;
  overflow: hidden;
  width: 100%;
}

.size-sm { max-width: 384px; }
.size-md { max-width: 480px; }
.size-lg { max-width: 640px; }
.size-xl { max-width: 800px; }
.size-2xl { max-width: 1024px; }
.size-full { max-width: 100%; }

.modal-container.fullscreen {
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  border-radius: 0;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.modal-close {
  background: transparent;
  border: 0;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  color: #6b7280;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #f3f4f6;
  color: #111827;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 0.2s;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
</style>
