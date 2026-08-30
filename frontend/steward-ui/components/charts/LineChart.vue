<template>
  <div ref="chartRef" class="line-chart" :style="{ height }"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue';
import * as echarts from 'echarts/core';
import { LineChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, LegendComponent, TitleComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import { useFormat } from '~/composables/useFormat';

echarts.use([LineChart, GridComponent, TooltipComponent, LegendComponent, TitleComponent, CanvasRenderer]);

interface SeriesItem {
  name: string;
  data: number[];
}

interface Props {
  categories: string[];
  series: SeriesItem[];
  height?: string;
  smooth?: boolean;
  showArea?: boolean;
  yAxisLabel?: string;
  xAxisLabel?: string;
}

const props = withDefaults(defineProps<Props>(), {
  height: '320px',
  smooth: true,
  showArea: true,
  yAxisLabel: '',
  xAxisLabel: '',
});

const { formatNumber } = useFormat();
const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;

function buildOption() {
  const colorPalette = ['#1e40af', '#d97706', '#16a34a', '#dc2626', '#0284c7', '#7c3aed'];

  return {
    color: colorPalette,
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'white',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      textStyle: { color: '#111827', fontSize: 13 },
      axisPointer: {
        type: 'line',
        lineStyle: { color: '#9ca3af', type: 'dashed' },
      },
    },
    legend: {
      data: props.series.map((s) => s.name),
      bottom: 0,
      textStyle: { color: '#6b7280', fontSize: 12 },
      icon: 'circle',
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '12%',
      top: '5%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: props.categories,
      boundaryGap: false,
      axisLine: { lineStyle: { color: '#e5e7eb' } },
      axisLabel: { color: '#6b7280', fontSize: 12 },
      name: props.xAxisLabel,
      nameTextStyle: { color: '#6b7280', fontSize: 12, padding: [10, 0, 0, 0] },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f3f4f6', type: 'dashed' } },
      axisLabel: {
        color: '#6b7280',
        fontSize: 12,
        formatter: (val: number) => formatNumber(val),
      },
      name: props.yAxisLabel,
      nameTextStyle: { color: '#6b7280', fontSize: 12, padding: [0, 0, 0, -10] },
    },
    series: props.series.map((s, idx) => ({
      name: s.name,
      type: 'line',
      smooth: props.smooth,
      symbol: 'circle',
      symbolSize: 6,
      data: s.data,
      lineStyle: { width: 2 },
      areaStyle: props.showArea
        ? {
            opacity: 0.15,
            color: colorPalette[idx % colorPalette.length],
          }
        : undefined,
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
.line-chart {
  width: 100%;
  min-height: 200px;
}
</style>
