<template>
  <div class="page-header">
    <div class="page-header-content">
      <div v-if="back" class="back-button" @click="handleBack">
        <span>←</span>
      </div>
      <div>
        <div v-if="breadcrumb && breadcrumb.length" class="breadcrumb">
          <span v-for="(item, idx) in breadcrumb" :key="idx">
            <a v-if="item.to && idx < breadcrumb.length - 1" @click="navigateTo(item.to)">
              {{ item.label }}
            </a>
            <span v-else>{{ item.label }}</span>
            <span v-if="idx < breadcrumb.length - 1" class="separator">/</span>
          </span>
        </div>
        <h1 class="page-title">{{ title }}</h1>
        <p v-if="subtitle" class="page-subtitle">{{ subtitle }}</p>
      </div>
    </div>
    <div v-if="$slots.actions" class="page-header-actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string;
  subtitle?: string;
  back?: boolean;
  breadcrumb?: { label: string; to?: string }[];
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  subtitle: '',
  back: false,
  breadcrumb: () => [],
});

const emit = defineEmits<{
  (e: 'back'): void;
}>();

function handleBack() {
  emit('back');
}
</script>

<style scoped>
.page-header {
  background: white;
  padding: 20px 32px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.page-header-content {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.back-button {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
  color: #374151;
  transition: background 0.2s;
}

.back-button:hover {
  background: #e5e7eb;
}

.breadcrumb {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 4px;
}

.breadcrumb a {
  color: #1e40af;
  cursor: pointer;
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.breadcrumb .separator {
  margin: 0 6px;
  color: #9ca3af;
}

.page-title {
  font-size: 22px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.page-subtitle {
  font-size: 13px;
  color: #6b7280;
  margin: 4px 0 0;
}

.page-header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
