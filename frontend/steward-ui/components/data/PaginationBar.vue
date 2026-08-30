<template>
  <div class="pagination-bar">
    <div class="pagination-info">
      <span>
        Menampilkan <strong>{{ startItem }}</strong>–<strong>{{ endItem }}</strong>
        dari <strong>{{ total }}</strong> data
      </span>
    </div>
    <div class="pagination-controls">
      <el-select
        v-model="localPageSize"
        size="small"
        style="width: 100px;"
        @change="handlePageSizeChange"
      >
        <el-option v-for="size in pageSizes" :key="size" :value="size" :label="`${size}/hal`" />
      </el-select>
      <el-pagination
        v-model:current-page="localPage"
        :page-size="localPageSize"
        :total="total"
        layout="prev, pager, next, jumper"
        :pager-count="5"
        background
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue';

interface Props {
  page: number;
  pageSize: number;
  total: number;
  pageSizes?: number[];
}

const props = withDefaults(defineProps<Props>(), {
  page: 1,
  pageSize: 20,
  total: 0,
  pageSizes: () => [10, 20, 50, 100],
});

const emit = defineEmits<{
  (e: 'update:page', value: number): void;
  (e: 'update:pageSize', value: number): void;
  (e: 'change', payload: { page: number; pageSize: number }): void;
}>();

const localPage = ref(props.page);
const localPageSize = ref(props.pageSize);

watch(() => props.page, (val) => {
  localPage.value = val;
});

watch(() => props.pageSize, (val) => {
  localPageSize.value = val;
});

const startItem = computed(() => {
  if (props.total === 0) return 0;
  return (localPage.value - 1) * localPageSize.value + 1;
});

const endItem = computed(() => {
  return Math.min(localPage.value * localPageSize.value, props.total);
});

function handlePageChange(page: number) {
  emit('update:page', page);
  emit('change', { page, pageSize: localPageSize.value });
}

function handlePageSizeChange(size: number) {
  localPage.value = 1;
  emit('update:page', 1);
  emit('update:pageSize', size);
  emit('change', { page: 1, pageSize: size });
}
</script>

<style scoped>
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  margin-top: 16px;
  gap: 16px;
  flex-wrap: wrap;
}

.pagination-info {
  font-size: 13px;
  color: #6b7280;
}

.pagination-info strong {
  color: #111827;
  font-weight: 600;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

@media (max-width: 640px) {
  .pagination-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .pagination-controls {
    justify-content: space-between;
  }
}
</style>
