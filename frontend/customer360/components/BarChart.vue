<template>
  <div ref="chartRef" :style="{ height: height + 'px' }" class="bar-chart"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts/core';
import { BarChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([BarChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer]);

const props = defineProps<{
  categories: string[];
  series: { name: string; data: number[] }[];
  height: number;
}>();

const chartRef = ref<HTMLElement>();
let chart: echarts.ECharts | null = null;

onMounted(() => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value);
    chart.setOption({
      color: ['#1e40af'],
      tooltip: { trigger: 'axis' },
      grid: { left: '3%', right: '4%', bottom: '3%', top: '5%', containLabel: true },
      xAxis: {
        type: 'category',
        data: props.categories,
        axisLine: { lineStyle: { color: '#e5e7eb' } },
        axisLabel: { color: '#6b7280' },
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f3f4f6', type: 'dashed' } },
        axisLabel: { color: '#6b7280' },
      },
      series: props.series.map(s => ({
        name: s.name,
        type: 'bar',
        data: s.data,
        barMaxWidth: 60,
        itemStyle: { borderRadius: [4, 4, 0, 0] },
      })),
    });
    window.addEventListener('resize', resize);
  }
});

function resize() { chart?.resize(); }

onUnmounted(() => {
  window.removeEventListener('resize', resize);
  chart?.dispose();
});
</script>
