<template>
  <el-dialog
    v-model="visible"
    :title="title"
    :width="width"
    :close-on-click-modal="false"
    :show-close="!loading"
    :center="center"
    @close="handleClose"
  >
    <div class="confirm-content">
      <div v-if="icon" class="confirm-icon" :class="`type-${type}`">
        {{ iconText }}
      </div>
      <div class="confirm-body">
        <h4 v-if="message" class="confirm-message">{{ message }}</h4>
        <p v-if="description" class="confirm-description">{{ description }}</p>
        <slot />
      </div>
    </div>
    <template #footer>
      <div class="confirm-footer">
        <el-button :disabled="loading" @click="handleCancel">
          {{ cancelText }}
        </el-button>
        <el-button
          :type="type === 'danger' ? 'danger' : 'primary'"
          :loading="loading"
          @click="handleConfirm"
        >
          {{ confirmText }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

interface Props {
  modelValue: boolean;
  title?: string;
  message?: string;
  description?: string;
  type?: 'primary' | 'success' | 'warning' | 'danger' | 'info';
  icon?: boolean;
  confirmText?: string;
  cancelText?: string;
  width?: string;
  center?: boolean;
  loading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Konfirmasi',
  message: 'Apakah Anda yakin?',
  description: '',
  type: 'warning',
  icon: true,
  confirmText: 'Konfirmasi',
  cancelText: 'Batal',
  width: '480px',
  center: false,
  loading: false,
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
  (e: 'confirm'): void;
  (e: 'cancel'): void;
  (e: 'close'): void;
}>();

const visible = ref(props.modelValue);

watch(() => props.modelValue, (val) => {
  visible.value = val;
});

watch(visible, (val) => {
  emit('update:modelValue', val);
});

const iconText = ref('!');
const handleTypeIcon = () => {
  const icons: Record<string, string> = {
    success: '✓',
    warning: '!',
    danger: '✕',
    info: 'i',
    primary: '?',
  };
  iconText.value = icons[props.type] || '!';
};
handleTypeIcon();

function handleConfirm() {
  emit('confirm');
}

function handleCancel() {
  visible.value = false;
  emit('cancel');
}

function handleClose() {
  emit('close');
}
</script>

<style scoped>
.confirm-content {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.confirm-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 600;
  flex-shrink: 0;
}

.confirm-icon.type-success {
  background: rgba(22, 163, 74, 0.1);
  color: #16a34a;
}

.confirm-icon.type-warning {
  background: rgba(234, 88, 12, 0.1);
  color: #ea580c;
}

.confirm-icon.type-danger {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
}

.confirm-icon.type-info, .confirm-icon.type-primary {
  background: rgba(2, 132, 199, 0.1);
  color: #0284c7;
}

.confirm-body {
  flex: 1;
}

.confirm-message {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 4px;
  line-height: 1.4;
}

.confirm-description {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.confirm-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
