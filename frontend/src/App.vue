<template>
  <div id="app">
    <Dashboard />
  </div>
</template>

<script>
import Dashboard from './views/Dashboard.vue';

export default {
  name: 'App',
  components: {
    Dashboard
  }
};
</script>

<style>
body {
  margin: 0;
  min-height: 100vh;
  background: linear-gradient(135deg, #000b15, #000);
  font-family: 'Microsoft YaHei', sans-serif;
  color: #E0F2FE;
  overflow-x: hidden; /* 防止水平滚动条 */
  position: relative;
}

#app {
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
}

/* 确保按钮可点击 */
button, .history-button {
  position: relative;
  z-index: 1000; /* 确保按钮在最上层 */
  pointer-events: auto; /* 确保点击事件生效 */
}
</style>