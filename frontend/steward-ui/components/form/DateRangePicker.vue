<template>
  <div class="date-range-picker">
    <div class="dr-header">
      <h4 class="dr-title">{{ title }}</h4>
      <div v-if="showPresets" class="dr-presets">
        <button
          v-for="preset in presets"
          :key="preset.value"
          class="dr-preset-btn"
          :class="{ active: selectedPreset === preset.value }"
          @click="applyPreset(preset.value)"
        >
          {{ preset.label }}
        </button>
      </div>
    </div>
    <div class="dr-content">
      <div class="dr-section">
        <label>Dari</label>
        <DatePicker
          v-model="startDate"
          type="date"
          :disabled-date="(date) => date > endDateValue"
          @change="handleChange"
        />
      </div>
      <div class="dr-section">
        <label>Sampai</label>
        <DatePicker
          v-model="endDate"
          type="date"
          :disabled-date="(date) => date < startDateValue"
          @change="handleChange"
        />
      </div>
    </div>
    <div v-if="showDuration" class="dr-footer">
      <span>Durasi: <strong>{{ duration }}</strong></span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import dayjs from 'dayjs';

interface Preset {
  label: string;
  value: string;
  range: () => [Date, Date];
}

interface Props {
  modelValue?: [string, string] | null;
  title?: string;
  showPresets?: boolean;
  showDuration?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  title: 'Pilih Rentang Tanggal',
  showPresets: true,
  showDuration: true,
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: [string, string] | null): void;
  (e: 'change', value: [string, string] | null): void;
}>();

const startDate = ref<string | null>(props.modelValue?.[0] || null);
const endDate = ref<string | null>(props.modelValue?.[1] || null);
const selectedPreset = ref<string | null>(null);

const startDateValue = computed(() => startDate.value ? new Date(startDate.value) : new Date(1900, 0, 1));
const endDateValue = computed(() => endDate.value ? new Date(endDate.value) : new Date(2100, 0, 1));

const duration = computed(() => {
  if (!startDate.value || !endDate.value) return '-';
  const days = dayjs(endDate.value).diff(dayjs(startDate.value), 'day') + 1;
  if (days < 31) return `${days} hari`;
  if (days < 365) return `${Math.floor(days / 30)} bulan`;
  return `${(days / 365).toFixed(1)} tahun`;
});

const presets: Preset[] = [
  { label: 'Hari ini', value: 'today', range: () => [new Date(), new Date()] },
  {
    label: '7 hari', value: '7d', range: () => {
      const end = new Date();
      const start = new Date();
      start.setDate(start.getDate() - 6);
      return [start, end];
    },
  },
  {
    label: '30 hari', value: '30d', range: () => {
      const end = new Date();
      const start = new Date();
      start.setDate(start.getDate() - 29);
      return [start, end];
    },
  },
  {
    label: 'Bulan ini', value: 'thisMonth', range: () => {
      const now = new Date();
      return [new Date(now.getFullYear(), now.getMonth(), 1), new Date()];
    },
  },
  {
    label: 'Bulan lalu', value: 'lastMonth', range: () => {
      const now = new Date();
      return [new Date(now.getFullYear(), now.getMonth() - 1, 1), new Date(now.getFullYear(), now.getMonth(), 0)];
    },
  },
  {
    label: 'Q1', value: 'q1', range: () => {
      const now = new Date();
      const q = Math.floor(now.getMonth() / 3);
      return [new Date(now.getFullYear(), q * 3, 1), new Date(now.getFullYear(), q * 3 + 3, 0)];
    },
  },
  {
    label: 'YTD', value: 'ytd', range: () => {
      const now = new Date();
      return [new Date(now.getFullYear(), 0, 1), now];
    },
  },
  {
    label: '1 tahun', value: '1y', range: () => {
      const end = new Date();
      const start = new Date();
      start.setFullYear(start.getFullYear() - 1);
      return [start, end];
    },
  },
];

function applyPreset(value: string) {
  const preset = presets.find((p) => p.value === value);
  if (!preset) return;
  selectedPreset.value = value;
  const [start, end] = preset.range();
  startDate.value = dayjs(start).format('YYYY-MM-DD');
  endDate.value = dayjs(end).format('YYYY-MM-DD');
  emitChange();
}

function handleChange() {
  selectedPreset.value = null;
  emitChange();
}

function emitChange() {
  if (startDate.value && endDate.value) {
    const value: [string, string] = [startDate.value, endDate.value];
    emit('update:modelValue', value);
    emit('change', value);
  } else {
    emit('update:modelValue', null);
    emit('change', null);
  }
}
</script>

<style scoped>
.date-range-picker {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
}

.dr-header {
  margin-bottom: 16px;
}

.dr-title {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 8px;
}

.dr-presets {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.dr-preset-btn {
  padding: 4px 10px;
  font-size: 12px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  color: #374151;
  transition: all 0.15s;
}

.dr-preset-btn:hover {
  background: #e5e7eb;
}

.dr-preset-btn.active {
  background: #1e40af;
  color: white;
  border-color: #1e40af;
}

.dr-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.dr-section label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 4px;
}

.dr-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
  font-size: 13px;
  color: #6b7280;
}

.dr-footer strong {
  color: #1e40af;
  font-weight: 600;
}

@media (max-width: 640px) {
  .dr-content {
    grid-template-columns: 1fr;
  }
}
</style>
