<template>
  <div ref="chartRef" class="bar-chart" :style="{ height }"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue';
import * as echarts from 'echarts/core';
import { BarChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import { useFormat } from '~/composables/useFormat';

echarts.use([BarChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer]);

interface SeriesItem {
  name: string;
  data: number[];
}

interface Props {
  categories: string[];
  series: SeriesItem[];
  height?: string;
  horizontal?: boolean;
  stacked?: boolean;
  yAxisLabel?: string;
  xAxisLabel?: string;
}

const props = withDefaults(defineProps<Props>(), {
  height: '320px',
  horizontal: false,
  stacked: false,
  yAxisLabel: '',
  xAxisLabel: '',
});

const { formatNumber } = useFormat();
const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;

function buildOption() {
  const colorPalette = ['#1e40af', '#d97706', '#16a34a', '#dc2626', '#0284c7', '#7c3aed'];

  const swap = props.horizontal;
  return {
    color: colorPalette,
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'white',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      textStyle: { color: '#111827', fontSize: 13 },
      axisPointer: {
        type: 'shadow',
      },
    },
    legend: {
      data: props.series.map((s) => s.name),
      bottom: 0,
      textStyle: { color: '#6b7280', fontSize: 12 },
      icon: 'roundRect',
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '12%',
      top: '5%',
      containLabel: true,
    },
    xAxis: swap
      ? {
          type: 'value',
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { lineStyle: { color: '#f3f4f6', type: 'dashed' } },
          axisLabel: { color: '#6b7280', fontSize: 12, formatter: (val: number) => formatNumber(val) },
          name: props.xAxisLabel,
          nameTextStyle: { color: '#6b7280', fontSize: 12, padding: [10, 0, 0, 0] },
        }
      : {
          type: 'category',
          data: props.categories,
          axisLine: { lineStyle: { color: '#e5e7eb' } },
          axisLabel: { color: '#6b7280', fontSize: 12 },
          name: props.xAxisLabel,
          nameTextStyle: { color: '#6b7280', fontSize: 12, padding: [10, 0, 0, 0] },
        },
    yAxis: swap
      ? {
          type: 'category',
          data: props.categories,
          axisLine: { lineStyle: { color: '#e5e7eb' } },
          axisLabel: { color: '#6b7280', fontSize: 12 },
          name: props.yAxisLabel,
          nameTextStyle: { color: '#6b7280', fontSize: 12, padding: [0, 0, 0, -10] },
        }
      : {
          type: 'value',
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { lineStyle: { color: '#f3f4f6', type: 'dashed' } },
          axisLabel: { color: '#6b7280', fontSize: 12, formatter: (val: number) => formatNumber(val) },
          name: props.yAxisLabel,
          nameTextStyle: { color: '#6b7280', fontSize: 12, padding: [0, 0, 0, -10] },
        },
    series: props.series.map((s) => ({
      name: s.name,
      type: 'bar',
      data: s.data,
      barMaxWidth: 40,
      stack: props.stacked ? 'stack' : undefined,
      itemStyle: { borderRadius: [4, 4, 0, 0] },
    })),
  };
}

function resize() {
  if (chart) chart.resize();
}

onMounted(() => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value);
    chart.setOption(buildOption());
    window.addEventListener('resize', resize);
  }
});

watch(() => [props.categories, props.series], () => {
  if (chart) chart.setOption(buildOption());
}, { deep: true });

onUnmounted(() => {
  window.removeEventListener('resize', resize);
  if (chart) {
    chart.dispose();
    chart = null;
  }
});
</script>

<style scoped>
.bar-chart {
  width: 100%;
  min-height: 200px;
}
</style>
