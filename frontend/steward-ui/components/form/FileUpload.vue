<template>
  <div class="file-upload">
    <el-upload
      ref="uploadRef"
      :action="action"
      :headers="headers"
      :data="data"
      :name="name"
      :accept="accept"
      :multiple="multiple"
      :limit="limit"
      :disabled="disabled"
      :drag="drag"
      :auto-upload="autoUpload"
      :list-type="listType"
      :before-upload="handleBeforeUpload"
      :on-success="handleSuccess"
      :on-error="handleError"
      :on-remove="handleRemove"
      :on-preview="handlePreview"
      :on-exceed="handleExceed"
      :file-list="fileList"
    >
      <template v-if="drag">
        <div class="upload-drag-area">
          <el-icon class="upload-icon"><UploadFilled /></el-icon>
          <div class="upload-text">
            <div class="upload-title">{{ dragTitle || 'Drop file di sini atau klik untuk upload' }}</div>
            <div class="upload-hint">
              Mendukung {{ acceptText }}
              <span v-if="maxSize">· Maks {{ formatFileSize(maxSize) }}</span>
            </div>
          </div>
        </div>
      </template>
      <template v-else>
        <el-button :disabled="disabled">
          <el-icon><Upload /></el-icon>
          <span>{{ buttonText }}</span>
        </el-button>
        <template v-if="tip">
          <div class="upload-tip">{{ tip }}</div>
        </template>
      </template>
    </el-upload>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Upload, UploadFilled } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

interface UploadFile {
  name: string;
  url?: string;
  status?: 'ready' | 'uploading' | 'success' | 'fail';
  size?: number;
  response?: any;
  raw?: File;
}

interface Props {
  modelValue?: UploadFile[];
  action?: string;
  headers?: Record<string, string>;
  data?: Record<string, any>;
  name?: string;
  accept?: string;
  multiple?: boolean;
  limit?: number;
  disabled?: boolean;
  drag?: boolean;
  autoUpload?: boolean;
  listType?: 'text' | 'picture' | 'picture-card';
  maxSize?: number;
  buttonText?: string;
  tip?: string;
  dragTitle?: string;
  uploadFn?: (file: File) => Promise<any>;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: () => [],
  action: '/api/v1/files/upload',
  name: 'file',
  accept: '',
  multiple: false,
  limit: 5,
  disabled: false,
  drag: false,
  autoUpload: true,
  listType: 'text',
  maxSize: 10 * 1024 * 1024, // 10MB
  buttonText: 'Pilih File',
  tip: '',
});

const emit = defineEmits<{
  (e: 'update:modelValue', files: UploadFile[]): void;
  (e: 'change', files: UploadFile[]): void;
  (e: 'success', response: any, file: UploadFile): void;
  (e: 'error', error: any): void;
  (e: 'remove', file: UploadFile): void;
  (e: 'exceed', files: File[]): void;
}>();

const uploadRef = ref();

const fileList = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
});

const acceptText = computed(() => {
  if (!props.accept) return 'semua jenis file';
  return props.accept.split(',').map((a) => a.trim()).join(', ');
});

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function handleBeforeUpload(file: File): Promise<boolean> {
  if (props.maxSize && file.size > props.maxSize) {
    ElMessage.error(`File ${file.name} terlalu besar. Maks ${formatFileSize(props.maxSize)}`);
    return false;
  }
  if (props.uploadFn) {
    try {
      const result = await props.uploadFn(file);
      const newFile: UploadFile = {
        name: file.name,
        size: file.size,
        status: 'success',
        response: result,
        url: result.url,
      };
      const updated = [...fileList.value, newFile];
      emit('update:modelValue', updated);
      emit('change', updated);
      emit('success', result, newFile);
    } catch (e) {
      ElMessage.error(`Gagal upload ${file.name}`);
      emit('error', e);
    }
    return false; // Prevent default upload
  }
  return true;
}

function handleSuccess(response: any, file: UploadFile) {
  emit('success', response, file);
}

function handleError(error: any) {
  ElMessage.error('Upload gagal');
  emit('error', error);
}

function handleRemove(file: UploadFile) {
  const updated = fileList.value.filter((f) => f.name !== file.name);
  emit('update:modelValue', updated);
  emit('change', updated);
  emit('remove', file);
}

function handlePreview(file: UploadFile) {
  if (file.url) {
    window.open(file.url, '_blank');
  }
}

function handleExceed(files: File[]) {
  ElMessage.warning(`Maks ${props.limit} file. Anda memilih ${files.length} file tambahan.`);
  emit('exceed', files);
}
</script>

<style scoped>
.upload-drag-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  text-align: center;
}

.upload-icon {
  font-size: 48px;
  color: #9ca3af;
  margin-bottom: 8px;
}

.upload-title {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

.upload-hint {
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
}

.upload-tip {
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
}

:deep(.el-upload-dragger) {
  padding: 16px;
}

:deep(.el-upload-list__item) {
  margin-top: 4px;
}
</style>
