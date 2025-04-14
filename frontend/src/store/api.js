// 引入axios库用于发起HTTP请求
import axios from 'axios';

// 创建axios实例并配置基础URL
const api = axios.create({
    baseURL: 'http://localhost:8000/api'
});

// 封装实时数据接口（合并后的单一接口）
export const getRealTimeData = () => {
    // 发起GET请求到实时数据端点
    return api.get('/historical');
};