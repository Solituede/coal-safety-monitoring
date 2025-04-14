<template>
  <div class="info-box">
    <div class="info-box-title">{{ title }}</div>
    <div class="info-box-value">
      {{ value.toFixed(2) }} {{ unit }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataCard',
  props: {
    title: String,
    value: Number,
    unit: String
  }
}
</script>

<style scoped>
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
</style>