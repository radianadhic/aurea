<template>
  <div ref="chartRef" :style="{ height: height + 'px' }" class="pie-chart"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts/core';
import { PieChart } from 'echarts/charts';
import { TooltipComponent, LegendComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([PieChart, TooltipComponent, LegendComponent, CanvasRenderer]);

const props = defineProps<{
  data: { name: string; value: number }[];
  height: number;
  donut?: boolean;
}>();

const chartRef = ref<HTMLElement>();
let chart: echarts.ECharts | null = null;

onMounted(() => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value);
    chart.setOption({
      color: ['#1e40af', '#d97706', '#16a34a', '#7c3aed', '#0891b2', '#dc2626'],
      tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
      legend: { orient: 'vertical', right: 16, top: 'center', textStyle: { color: '#374151' } },
      series: [{
        type: 'pie',
        radius: props.donut ? ['50%', '75%'] : '70%',
        center: ['38%', '50%'],
        data: props.data,
        itemStyle: { borderColor: 'white', borderWidth: 2 },
        label: { show: !props.donut, formatter: '{b}\n{d}%' },
      }],
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
