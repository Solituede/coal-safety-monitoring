# 数据库配置
INFLUXDB_URL = "http://host.docker.internal:8086"
INFLUXDB_TOKEN = "lVTN7VF0jvRt5PB2Ub6z4kEbkUc5qaXrB-sKzwuX-EZoOTJPscDj1jahy4i8lQ9jRJB-8fXcZ2753hz7nhgn6A=="
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