<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps } from 'vue';
import { Chart } from 'chart.js/auto';

// 定义 props 以接受来自父级的图表数据
const props = defineProps({
  chartData: Object
});

const chartCanvas = ref(null);
let chartInstance = null;

// 初始化图表
const initChart = () => {
  const ctx = chartCanvas.value.getContext('2d');
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: JSON.parse(JSON.stringify(props.chartData)), // 深拷贝初始数据
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#E0F2FE' } }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.1)' },
          ticks: { color: '#E0F2FE' }
        },
        y: {
          title: { text: '速度 (m/min)', color: '#E0F2FE' },
          grid: { color: 'rgba(255, 255, 255, 0.1)' },
          ticks: { color: '#E0F2FE' }
        }
      }
    }
  });
};

// 监听 chartData 变化，更新图表
watch(() => props.chartData, (newData) => {
  if (chartInstance) {
    // 深拷贝 newData，避免响应式问题
    chartInstance.data = JSON.parse(JSON.stringify(newData));
    chartInstance.update();
  }
}, { deep: true });

onMounted(() => {
  initChart();
});
</script>

<style scoped>
.chart-container {
  height: 400px;
  padding: 20px;
}
</style>