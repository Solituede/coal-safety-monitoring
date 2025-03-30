# 数据库配置
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "docker-compose down"
INFLUXDB_ORG = "xiankejidaxue"
INFLUXDB_BUCKET = "wasi"

# MQTT配置
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPICS = {
    "speed": "coal/mining/speed",
    "extraction": "coal/mining/extraction",
    "airflow": "coal/mining/airflow"
}

# 安全阈值
SAFETY_THRESHOLDS = {
    "speed_green": 2.5,
    "speed_yellow": 3.2,
    "gas_concentration": 1.0  # 百分比
}