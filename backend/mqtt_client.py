import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 添加当前目录
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # 添加上级目录

import paho.mqtt.client as mqtt
import json
import logging
from .config import MQTT_BROKER, MQTT_PORT, MQTT_TOPICS
from database import write_mining_data
from safety_calculator import SafetyCalculator

logging.basicConfig(level=logging.INFO)


class MQTTDataProcessor:
    def __init__(self):
        self.current_data = {"speed": 0.0, "extraction": 30, "airflow": 1000}

    def process_message(self, msg):
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
            Q = SafetyCalculator.calculate_gas_emission(
                self.current_data["speed"],
                self.current_data["extraction"]
            )
            gas_concentration = SafetyCalculator.calculate_gas_concentration(Q, self.current_data["airflow"])
            safe_speed = SafetyCalculator.find_safe_speed(
                self.current_data["airflow"],
                self.current_data["extraction"]
            )

            # 写入数据库
            write_mining_data({
                "speed": self.current_data["speed"],
                "extraction": self.current_data["extraction"],
                "airflow": self.current_data["airflow"],
                "gas_concentration": gas_concentration,
                "safe_speed": safe_speed,
                "gas_emission": Q
            })
            logging.info("数据写入成功")
        except Exception as e:
            logging.error(f"处理MQTT消息失败: {e}")


def start_mqtt():
    client = mqtt.Client()
    processor = MQTTDataProcessor()
    client.on_connect = lambda c, u, f, rc: [c.subscribe(topic) for topic in MQTT_TOPICS.values()]
    client.on_message = lambda c, u, msg: processor.process_message(msg)
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()

