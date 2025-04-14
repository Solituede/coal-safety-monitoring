import { getRealTimeData } from '../api';

export default {
  namespaced: true,
  state: {
    current_speed: null,
    gas_concentration: null,
    gas_emission: null,
    airflow: null,
    safe_speed: 3.2,
    extraction: null,
    historyData: []
  },
  mutations: {
    UPDATE_REAL_TIME_DATA(state, data) {
      state.current_speed = data.current_speed ?? state.current_speed;
      state.gas_concentration = data.gas_concentration ?? state.gas_concentration;
      state.gas_emission = data.gas_emission ?? state.gas_emission;
      state.airflow = data.airflow ?? state.airflow;
      state.safe_speed = data.safe_speed ?? state.safe_speed;
      state.extraction = data.extraction ?? state.extraction;
    },
    SAVE_HISTORY_DATA(state, { timestamp, current_state, gas_state }) {
      state.historyData.push({
        timestamp,
        current_speed: state.current_speed,
        current_state,
        gas_concentration: state.gas_concentration,
        gas_state,
        safe_speed: state.safe_speed,
        extraction: state.extraction
      });
      const oneHourAgo = new Date().getTime() - 60 * 60 * 1000;
      state.historyData = state.historyData.filter(item => {
        return new Date(item.timestamp).getTime() >= oneHourAgo;
      });
    }
  },
  actions: {
    async updateData({ commit }) {
      try {
        const response = await getRealTimeData();
        console.log('后端返回数据:', response.data);

        // 检查 response.data 是否为对象且包含 data 字段
        if (!response.data || typeof response.data !== 'object' || !Array.isArray(response.data.data)) {
          throw new Error('后端返回数据格式不正确: ' + JSON.stringify(response.data));
        }

        // 提取 response.data.data（数组）
        const dataArray = response.data.data;
        console.log('提取的数组:', dataArray);

        // 将数组转换为对象
        const data = {};
        dataArray.forEach(item => {
          switch (item.metric) {
            case 'current_speed':
              data.current_speed = item.value;
              break;
            case 'gas_concentration':
              data.gas_concentration = item.value;
              break;
            case 'gas_emission':
              data.gas_emission = item.value;
              break;
            case 'airflow':
              data.airflow = item.value;
              break;
            case 'safe_speed':
              data.safe_speed = item.value;
              break;
            case 'extraction':
              data.extraction = item.value;
              break;
          }
        });

        // 确保字段存在，若不存在则提供默认值
        const processedData = {
          current_speed: data.current_speed ?? 0,
          gas_concentration: data.gas_concentration ?? 0,
          gas_emission: data.gas_emission ?? 0,
          airflow: data.airflow ?? 0,
          safe_speed: data.safe_speed ?? 3.2,
          extraction: data.extraction ?? 0
        };

        commit('UPDATE_REAL_TIME_DATA', processedData);

        const timestamp = new Date();
        let current_state;
        const currentSpeed = processedData.current_speed;
        const safeSpeed = processedData.safe_speed;
        if (currentSpeed === null || safeSpeed === null) {
          current_state = '数据缺失';
        } else if (currentSpeed <= safeSpeed * 0.78) {
          current_state = '正常作业';
        } else if (currentSpeed > safeSpeed * 0.78 && currentSpeed < safeSpeed) {
          current_state = '加强瓦斯监测和管理';
        } else {
          current_state = '强制停止作业';
        }

        let gas_state;
        const gasConcentration = processedData.gas_concentration;
        const gasEmission = processedData.gas_emission;
        const airflow = processedData.airflow;
        const extraction = processedData.extraction;
        if (gasConcentration === null || gasEmission === null || airflow === null || extraction === null) {
          gas_state = '数据缺失';
        } else {
          gas_state = (gasConcentration > 1 || gasEmission > (airflow * 0.01 + extraction)) ? '异常' : '正常';
        }

        commit('SAVE_HISTORY_DATA', { timestamp, current_state, gas_state });
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
  },
  getters: {
    getCurrentSpeed: state => state.current_speed,
    getGasConcentration: state => state.gas_concentration,
    getSafeSpeed: state => state.safe_speed,
    getHistoryData: state => state.historyData
  }
};