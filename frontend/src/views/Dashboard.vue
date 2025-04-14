<template>
  <div class="dashboard">
    <!-- Alert Panel -->
    <div v-show="showAlert" class="alert-panel">
      ⚠️ 安全警报：检测到瓦斯异常
    </div>

    <!-- Main Dashboard Layout -->
    <div class="header">
      <h1>🏭 矿山智能监控系统</h1>
      <div class="threshold-info">
        当前安全阈值: {{ safeThreshold.toFixed(2) }} m/min
      </div>
    </div>

    <!-- Chart Container -->
    <Chart1 :chart-data="chartData" />

    <div class="data-container">
      <div class="metrics-grid">
        <DataCard title="实时割煤速度" :value="currentSpeed" unit="m/min"/>
        <DataCard title="瓦斯浓度" :value="gasConcentration" unit="%"/>
        <!-- 添加查看历史按钮 -->
        <div class="info-box history-button" @click="showHistoryPopup">
          <div class="info-box-title">查看历史</div>
          <div class="info-box-value">📜</div>
        </div>
      </div>

      <DataTable />
    </div>

    <!-- 历史记录弹窗 -->
    <HistoryPopup v-if="isHistoryPopupOpen" :history-data="formattedHistoryData" @close="closeHistoryPopup"/>

    <div v-for="(meteor, index) in meteors"
         :key="index"
         class="meteor"
         :style="meteorStyle(index)"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useStore } from 'vuex';
import Chart1 from '@/components/Chart1.vue';
import DataCard from '@/components/DataCard.vue';
import DataTable from '@/components/DataTable.vue';
import HistoryPopup from '@/components/HistoryPopup.vue';

// Vuex store
const store = useStore();

// 响应式数据
const currentSpeed = computed(() => store.getters['coalMining/getCurrentSpeed'] || 0);
const gasConcentration = computed(() => store.getters['coalMining/getGasConcentration'] || 0);
const safeThreshold = computed(() => store.getters['coalMining/getSafeSpeed'] || 3.2);
const historyData = computed(() => store.getters['coalMining/getHistoryData'] || []);
const isHistoryPopupOpen = ref(false);
const showAlert = computed(() => (store.getters['coalMining/getGasConcentration'] || 0) > 1);

let updateInterval;

// 图表数据
const chartData = ref({
  labels: [],
  datasets: [
    { label: '瓦斯浓度', data: [], borderColor: 'red' },
    { label: '安全阈值', data: [], borderColor: 'green' },
    { label: '割煤速度', data: [], borderColor: 'blue' }
  ]
});

// 格式化历史数据以适配 HistoryPopup
const formattedHistoryData = computed(() => {
  return historyData.value.map(item => ({
    time: new Date(item.timestamp).toLocaleString(),
    current_speed: item.current_speed,
    current_state: item.current_state,
    gas_concentration: item.gas_concentration,
    gas_state: item.gas_state,
    safe_speed: item.safe_speed,
    extraction: item.extraction
  }));
});

// 更新图表数据
const updateChart = () => {
  const timestamp = new Date().toLocaleTimeString();
  chartData.value.labels.push(timestamp);
  chartData.value.datasets[0].data.push(gasConcentration.value);
  chartData.value.datasets[1].data = Array(chartData.value.labels.length).fill(safeThreshold.value);
  chartData.value.datasets[2].data.push(currentSpeed.value);

  if (chartData.value.labels.length > 20) {
    chartData.value.labels.shift();
    chartData.value.datasets.forEach(d => d.data.shift());
  }
};

// 历史记录弹窗控制
const showHistoryPopup = () => {
  isHistoryPopupOpen.value = true;
};
const closeHistoryPopup = () => {
  isHistoryPopupOpen.value = false;
};

// 流星效果
const meteors = ref(Array(5).fill({}));
const meteorStyle = (index) => ({
  top: `${Math.random() * 100}%`,
  left: `${Math.random() * 100}%`,
  animationDelay: `${index * 0.5}s`
});

// 生命周期钩子
onMounted(() => {
  store.dispatch('coalMining/updateData');
  updateInterval = setInterval(() => {
    store.dispatch('coalMining/updateData');
    updateChart();
  }, 5000); // 修改为 5 秒
});

onUnmounted(() => {
  clearInterval(updateInterval);
});
</script>

<style scoped>
.dashboard {
  width: 100%;
  max-width: 1920px;
  min-width: 1200px;
  margin: 1rem auto;
  background: rgba(0, 20, 40, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 32px rgba(0, 100, 255, 0.15);
  position: relative;
  z-index: 1;
}

.alert-panel {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px 40px;
  background: rgba(255, 0, 60, 0.9);
  border-radius: 12px;
  animation: alertPulse 0.5s infinite;
  border: 2px solid white;
  box-shadow: 0 0 30px #FF003C;
  z-index: 999;
  color: white;
  font-weight: bold;
}

@keyframes alertPulse {
  0% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.1); }
  100% { transform: translate(-50%, -50%) scale(1); }
}

.chart-container {
  height: 400px;
  padding: 20px;
  width: 100%;
}

.data-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  padding: 20px;
  width: 100%;
}

.metrics-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.info-box {
  background: rgba(0, 40, 80, 0.5);
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 15px;
}

.info-box-title {
  color: #7FDBFF;
  font-size: 16px;
}

.info-box-value {
  font-size: 32px;
  font-weight: bold;
}

.history-button {
  cursor: pointer;
}

.meteor {
  position: absolute;
  width: 200px;
  height: 2px;
  background: linear-gradient(90deg,
          rgba(255, 255, 255, 0),
          rgba(255, 255, 255, 0.8),
          rgba(255, 255, 255, 0));
  animation: meteorFall 1s linear forwards;
}

@keyframes meteorFall {
  0% {
    transform: translateX(-100%);
    opacity: 1;
  }
  100% {
    transform: translateX(200%);
    opacity: 0;
  }
}
</style>