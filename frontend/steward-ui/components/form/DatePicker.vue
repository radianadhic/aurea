<template>
  <el-date-picker
    v-model="localValue"
    :type="type"
    :format="format"
    :value-format="valueFormat"
    :placeholder="placeholder"
    :start-placeholder="startPlaceholder"
    :end-placeholder="endPlaceholder"
    :range-separator="rangeSeparator"
    :disabled="disabled"
    :clearable="clearable"
    :shortcuts="computedShortcuts"
    :disabled-date="disabledDate"
    :size="size"
    style="width: 100%"
  />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface Props {
  modelValue?: string | string[] | Date | Date[] | null;
  type?: 'date' | 'datetime' | 'datetimerange' | 'daterange' | 'month' | 'monthrange' | 'year' | 'yearrange' | 'week';
  format?: string;
  valueFormat?: string;
  placeholder?: string;
  startPlaceholder?: string;
  endPlaceholder?: string;
  rangeSeparator?: string;
  disabled?: boolean;
  clearable?: boolean;
  size?: 'large' | 'default' | 'small';
  showShortcuts?: boolean;
  disabledDate?: (date: Date) => boolean;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'date',
  format: 'DD MMM YYYY',
  valueFormat: 'YYYY-MM-DD',
  placeholder: 'Pilih tanggal',
  startPlaceholder: 'Dari',
  endPlaceholder: 'Sampai',
  rangeSeparator: '→',
  disabled: false,
  clearable: true,
  size: 'default',
  showShortcuts: true,
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: any): void;
  (e: 'change', value: any): void;
}>();

const localValue = ref<any>(props.modelValue);

const computedShortcuts = computed(() => {
  if (!props.showShortcuts) return undefined;

  if (props.type === 'daterange' || props.type === 'datetimerange') {
    return [
      {
        text: 'Hari ini',
        value: () => {
          const today = new Date();
          return [today, today];
        },
      },
      {
        text: '7 hari terakhir',
        value: () => {
          const end = new Date();
          const start = new Date();
          start.setDate(start.getDate() - 7);
          return [start, end];
        },
      },
      {
        text: '30 hari terakhir',
        value: () => {
          const end = new Date();
          const start = new Date();
          start.setDate(start.getDate() - 30);
          return [start, end];
        },
      },
      {
        text: 'Bulan ini',
        value: () => {
          const now = new Date();
          const start = new Date(now.getFullYear(), now.getMonth(), 1);
          const end = new Date(now.getFullYear(), now.getMonth() + 1, 0);
          return [start, end];
        },
      },
      {
        text: 'Bulan lalu',
        value: () => {
          const now = new Date();
          const start = new Date(now.getFullYear(), now.getMonth() - 1, 1);
          const end = new Date(now.getFullYear(), now.getMonth(), 0);
          return [start, end];
        },
      },
    ];
  }

  return [
    {
      text: 'Hari ini',
      value: new Date(),
    },
    {
      text: 'Kemarin',
      value: () => {
        const d = new Date();
        d.setDate(d.getDate() - 1);
        return d;
      },
    },
    {
      text: '1 minggu lalu',
      value: () => {
        const d = new Date();
        d.setDate(d.getDate() - 7);
        return d;
      },
    },
    {
      text: '1 bulan lalu',
      value: () => {
        const d = new Date();
        d.setMonth(d.getMonth() - 1);
        return d;
      },
    },
  ];
});
</script>
