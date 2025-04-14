<template>
  <div class="history-popup">
    <h2>历史记录</h2>
    <div class="data-table">
      <table>
        <thead>
          <tr>
            <th>时间</th>
            <th>割煤速度</th>
            <th>割煤状态</th>
            <th>瓦斯浓度</th>
            <th>瓦斯状态</th>
            <th>安全阈值</th>
            <th>抽采量</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in historyData" :key="entry.time">
            <td>{{ entry.time }}</td>
            <td>{{ entry.current_speed }}</td>
            <td>{{ entry.current_state }}</td>
            <td>{{ entry.gas_concentration }}</td>
            <td>{{ entry.gas_state }}</td>
            <td>{{ entry.safe_speed }}</td>
            <td>{{ entry.extraction }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <button @click="$emit('close')">关闭</button>
  </div>
</template>

<script>
export default {
  name: 'HistoryPopup',
  props: {
    historyData: Array
  }
};
</script>

<style scoped>
.history-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 20, 40, 0.95);
  padding: 20px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  z-index: 1000;
  max-height: 80vh;
  overflow-y: auto;
}

.data-table {
  background: rgba(0, 30, 60, 0.8);
  border-radius: 8px;
  overflow: hidden;
}

table {
  width: 100%;
  color: #E0F2FE;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

button {
  margin-top: 15px;
  padding: 8px 16px;
  background: #2A8CFF;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
}
</style>