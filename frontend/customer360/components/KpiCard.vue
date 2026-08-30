<template>
  <div class="kpi-card">
    <div class="kpi-header">
      <span class="kpi-label">{{ label }}</span>
      <div class="kpi-icon" :style="iconStyle">{{ icon }}</div>
    </div>
    <div class="kpi-value-row">
      <div class="kpi-value">
        {{ value }}
        <span v-if="unit" class="kpi-unit">{{ unit }}</span>
      </div>
    </div>
    <div v-if="trend !== undefined" class="kpi-trend" :class="trend > 0 ? 'up' : trend < 0 ? 'down' : ''">
      <span>{{ trend > 0 ? '▲' : trend < 0 ? '▼' : '━' }}</span>
      <span>{{ Math.abs(trend) }}%</span>
      <span class="trend-period">vs last period</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  label: string;
  value: string | number;
  unit?: string;
  icon?: string;
  color?: string;
  trend?: number;
}>(), {
  color: '#1e40af',
  unit: '',
  icon: '📊',
});

const iconStyle = computed(() => ({
  background: `${props.color}15`,
  color: props.color,
}));
</script>

<style scoped>
.kpi-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 18px;
  transition: all 0.2s;
}

.kpi-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
}

.kpi-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.kpi-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.kpi-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.kpi-value {
  font-size: 26px;
  font-weight: 700;
  color: #111827;
  line-height: 1.2;
}

.kpi-unit {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
  margin-left: 4px;
}

.kpi-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  font-size: 12px;
  font-weight: 600;
}

.kpi-trend.up { color: #16a34a; }
.kpi-trend.down { color: #dc2626; }

.trend-period {
  color: #6b7280;
  font-weight: 400;
  margin-left: 4px;
}
</style>
