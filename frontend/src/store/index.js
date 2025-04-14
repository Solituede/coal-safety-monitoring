import { createStore } from 'vuex';
import coalMining from './modules/coalMining';

export default createStore({
  modules: {
    coalMining
  }
});