import paho.mqtt.client as mqtt
import json
import logging
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPICS
from database import write_mining_data
from safety_calculator import SafetyCalculator

logging.basicConfig(level=logging.INFO)


class MQTTDataProcessor:
    def __init__(self):
        self.current_data = {
            "speed": 0.0,
            "extraction": 30,
            "airflow": 1000,
            "gas_concentration": 0.0,
            "safe_speed": 3.2
        }
        self.safety_calculator = SafetyCalculator()

    def process_message(self, msg):
        """处理MQTT消息并触发安全计算"""
        try:
            payload = json.loads(msg.payload)
            topic = msg.topic

            if topic == MQTT_TOPICS["speed"]:
                self.current_data["speed"] = float(payload["speed"])
            elif topic == MQTT_TOPICS["extraction"]:
                self.current_data["extraction"] = int(payload["extraction"])
            elif topic == MQTT_TOPICS["airflow"]:
                self.current_data["airflow"] = int(payload["airflow"])

            # 计算安全参数
            self._calculate_safety_parameters()

            # 写入数据库
            write_mining_data(self.current_data)

            logging.info(f"Processed data: {self.current_data}")

        except Exception as e:
            logging.error(f"Error processing MQTT message: {e}")

    def _calculate_safety_parameters(self):
        """执行安全计算"""
        Q = self.safety_calculator.calculate_gas_emission(
            self.current_data["speed"],
            self.current_data["extraction"]
        )
        self.current_data["gas_concentration"] = round(
            self.safety_calculator.calculate_gas_concentration(Q, self.current_data["airflow"]),
            2
        )
        self.current_data["safe_speed"] = self.safety_calculator.find_safe_speed(
            self.current_data["airflow"],
            self.current_data["extraction"]
        )


def start_mqtt():
    """启动MQTT客户端并保持长连接"""
    client = mqtt.Client()
    processor = MQTTDataProcessor()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT Broker")
            for topic in MQTT_TOPICS.values():
                client.subscribe(topic)
        else:
            logging.error(f"Connection failed with code {rc}")

    def on_message(client, userdata, msg):
        processor.process_message(msg)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()