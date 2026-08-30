<template>
  <div ref="chartRef" class="pie-chart" :style="{ height }"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue';
import * as echarts from 'echarts/core';
import { PieChart } from 'echarts/charts';
import { TooltipComponent, LegendComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import { useFormat } from '~/composables/useFormat';

echarts.use([PieChart, TooltipComponent, LegendComponent, CanvasRenderer]);

interface DataItem {
  name: string;
  value: number;
}

interface Props {
  data: DataItem[];
  height?: string;
  showLegend?: boolean;
  donut?: boolean;
  title?: string;
}

const props = withDefaults(defineProps<Props>(), {
  height: '320px',
  showLegend: true,
  donut: true,
  title: '',
});

const { formatNumber } = useFormat();
const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;

function buildOption() {
  const colorPalette = ['#1e40af', '#d97706', '#16a34a', '#dc2626', '#0284c7', '#7c3aed', '#db2777', '#65a30d'];

  return {
    color: colorPalette,
    tooltip: {
      trigger: 'item',
      backgroundColor: 'white',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      textStyle: { color: '#111827', fontSize: 13 },
      formatter: (params: any) => {
        const pct = params.percent.toFixed(1);
        return `<strong>${params.name}</strong><br/>${formatNumber(params.value)} (${pct}%)`;
      },
    },
    legend: props.showLegend
      ? {
          orient: 'vertical',
          right: 16,
          top: 'center',
          textStyle: { color: '#374151', fontSize: 13 },
          icon: 'circle',
        }
      : { show: false },
    title: props.title
      ? {
          text: props.title,
          left: 'center',
          top: 16,
          textStyle: { color: '#111827', fontSize: 14, fontWeight: 600 },
        }
      : undefined,
    series: [
      {
        type: 'pie',
        radius: props.donut ? ['50%', '75%'] : '70%',
        center: ['38%', '50%'],
        data: props.data,
        label: {
          show: !props.donut,
          formatter: '{b}\n{d}%',
          color: '#374151',
          fontSize: 12,
        },
        labelLine: {
          show: !props.donut,
        },
        itemStyle: {
          borderColor: 'white',
          borderWidth: 2,
        },
      },
    ],
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

watch(() => props.data, () => {
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
.pie-chart {
  width: 100%;
  min-height: 200px;
}
</style>
