<template>
  <div class="stat-card">
    <div class="stat-card-header">
      <p v-if="label" class="stat-label">{{ label }}</p>
      <div v-if="icon" class="stat-icon" :style="iconStyle">
        <span>{{ icon }}</span>
      </div>
    </div>
    <div class="stat-card-body">
      <h3 class="stat-value">
        {{ value }}
        <span v-if="unit" class="stat-unit">{{ unit }}</span>
      </h3>
      <div v-if="trend" class="stat-trend" :class="trendClass">
        <span class="trend-arrow">{{ trendIcon }}</span>
        <span>{{ Math.abs(trend) }}%</span>
        <span class="trend-period">{{ trendPeriod || 'vs last period' }}</span>
      </div>
    </div>
    <div v-if="subValue" class="stat-sub">
      {{ subValue }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  label?: string;
  value: string | number;
  unit?: string;
  icon?: string;
  color?: string;
  trend?: number;
  trendPeriod?: string;
  subValue?: string;
}

const props = withDefaults(defineProps<Props>(), {
  label: '',
  unit: '',
  icon: '',
  color: '#1e40af',
  trend: 0,
  trendPeriod: '',
  subValue: '',
});

const iconStyle = computed(() => ({
  background: `${props.color}15`,
  color: props.color,
}));

const trendClass = computed(() => {
  if (!props.trend) return '';
  return props.trend > 0 ? 'up' : 'down';
});

const trendIcon = computed(() => {
  if (!props.trend) return '';
  return props.trend > 0 ? '▲' : '▼';
});
</script>

<style scoped>
.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;
  border: 1px solid #f3f4f6;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
}

.stat-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

.stat-label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin: 0;
  line-height: 1.2;
}

.stat-unit {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
  margin-left: 4px;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  font-size: 13px;
  font-weight: 500;
}

.stat-trend.up {
  color: #16a34a;
}

.stat-trend.down {
  color: #dc2626;
}

.trend-arrow {
  font-size: 10px;
}

.trend-period {
  color: #6b7280;
  font-weight: 400;
  margin-left: 4px;
}

.stat-sub {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #f3f4f6;
  font-size: 12px;
  color: #6b7280;
}
</style>
