<template>
  <div class="data-table" :class="{ loading }">
    <div v-if="loading" class="table-loading">
      <LoadingSpinner :message="loadingMessage" />
    </div>
    <el-table
      ref="tableRef"
      :data="data"
      :height="height"
      :max-height="maxHeight"
      :stripe="stripe"
      :border="border"
      :size="size"
      :row-key="rowKey"
      :default-expand-all="defaultExpandAll"
      :tree-props="treeProps"
      :empty-text="emptyText"
      :row-class-name="rowClassName"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      :row-style="rowStyle"
      :cell-style="cellStyle"
      :highlight-current-row="highlightCurrentRow"
      :show-summary="showSummary"
      :summary-method="summaryMethod"
      :span-method="spanMethod"
      :selectable="selectable"
      @sort-change="handleSortChange"
      @selection-change="handleSelectionChange"
      @row-click="handleRowClick"
      @row-dblclick="handleRowDblClick"
    >
      <slot />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { TableInstance } from 'element-plus';

interface Props {
  data: any[];
  loading?: boolean;
  loadingMessage?: string;
  height?: string | number;
  maxHeight?: string | number;
  stripe?: boolean;
  border?: boolean;
  size?: 'large' | 'default' | 'small';
  rowKey?: string | ((row: any) => string);
  defaultExpandAll?: boolean;
  treeProps?: { children?: string; hasChildren?: string };
  emptyText?: string;
  rowClassName?: (args: { row: any; rowIndex: number }) => string;
  cellClassName?: (args: { row: any; column: any; rowIndex: number; columnIndex: number }) => string;
  headerCellClassName?: (args: { row: any; column: any; rowIndex: number; columnIndex: number }) => string;
  rowStyle?: (args: { row: any; rowIndex: number }) => any;
  cellStyle?: (args: { row: any; column: any; rowIndex: number; columnIndex: number }) => any;
  highlightCurrentRow?: boolean;
  showSummary?: boolean;
  summaryMethod?: (args: { columns: any[]; data: any[] }) => string[];
  spanMethod?: (args: { row: any; column: any; rowIndex: number; columnIndex: number }) => number[] | { rowspan: number; colspan: number };
  selectable?: (row: any, index: number) => boolean;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  loadingMessage: 'Memuat data...',
  stripe: true,
  border: false,
  size: 'default',
  emptyText: 'Tidak ada data',
  highlightCurrentRow: true,
  showSummary: false,
});

const emit = defineEmits<{
  (e: 'sort-change', payload: { column: any; prop: string; order: 'ascending' | 'descending' | null }): void;
  (e: 'selection-change', selection: any[]): void;
  (e: 'row-click', row: any, column: any, event: Event): void;
  (e: 'row-dblclick', row: any, column: any, event: Event): void;
}>();

const tableRef = ref<TableInstance>();

function handleSortChange(payload: any) {
  emit('sort-change', payload);
}

function handleSelectionChange(selection: any[]) {
  emit('selection-change', selection);
}

function handleRowClick(row: any, column: any, event: Event) {
  emit('row-click', row, column, event);
}

function handleRowDblClick(row: any, column: any, event: Event) {
  emit('row-dblclick', row, column, event);
}

// Expose table methods
defineExpose({
  clearSelection: () => tableRef.value?.clearSelection(),
  toggleRowSelection: (row: any, selected?: boolean) => tableRef.value?.toggleRowSelection(row, selected),
  toggleAllSelection: () => tableRef.value?.toggleAllSelection(),
  setCurrentRow: (row: any) => tableRef.value?.setCurrentRow(row),
  clearSort: () => tableRef.value?.clearSort(),
  sort: (prop: string, order: 'ascending' | 'descending') => tableRef.value?.sort(prop, order),
  doLayout: () => tableRef.value?.doLayout(),
  setScrollTop: (top: number) => tableRef.value?.setScrollTop(top),
  setScrollLeft: (left: number) => tableRef.value?.setScrollLeft(left),
});
</script>

<style scoped>
.data-table {
  position: relative;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.table-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 5;
}
</style>
