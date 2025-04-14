<template>
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
        </tr>
      </thead>
      <tbody>
        <tr v-for="(entry, index) in limitedData" :key="index">
          <td>{{ formatTime(entry.timestamp) }}</td>
          <td>{{ entry.current_speed || 'N/A' }}</td>
          <td>{{ entry.current_state || 'N/A' }}</td>
          <td>{{ entry.gas_concentration || 'N/A' }}</td>
          <td>{{ entry.gas_state || 'N/A' }}</td>
          <td>{{ entry.safe_speed || 'N/A' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'DataTable',
  computed: {
    ...mapGetters('coalMining', {
      tableData: 'getHistoryData'
    }),
    limitedData() {
      return this.tableData.slice(0, 6);
    }
  },
  mounted() {
    this.updateData();
    this.timer = setInterval(this.updateData, 5000);
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  methods: {
    ...mapActions('coalMining', ['updateData']),
    formatTime(timestamp) {
      return new Date(timestamp).toLocaleString();
    }
  }
};
</script>

<style scoped>
.data-table {
  background: rgba(0, 30, 60, 0.8);
  border-radius: 8px;
  overflow: hidden;
  max-width: 100%;
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

th,
td {
  padding: 8px;
  text-align: center;
  font-size: 14px;
  word-wrap: break-word;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

th {
  background: rgba(0, 80, 160, 0.6);
}
</style>