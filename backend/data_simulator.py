import random
import time
import paho.mqtt.client as mqtt
from backend.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPICS


class DataSimulator:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT)

    def generate_speed(self):
        """生成割煤速度 (m/min)"""
        return round(random.uniform(2.0, 4.5), 1)

    def generate_extraction(self):
        """生成抽采量 (m³/min)"""
        return random.randint(20, 40)

    def generate_airflow(self):
        """生成工作面风量 (m³/min)"""
        return random.randint(800, 1500)

    def publish_data(self):
        """周期发布模拟数据"""
        while True:
            speed = self.generate_speed()
            extraction = self.generate_extraction()
            airflow = self.generate_airflow()

            # 发布到MQTT
            self.client.publish(
                MQTT_TOPICS["speed"],
                payload=json.dumps({"speed": speed})
            )
            self.client.publish(
                MQTT_TOPICS["extraction"],
                payload=json.dumps({"extraction": extraction})
            )
            self.client.publish(
                MQTT_TOPICS["airflow"],
                payload=json.dumps({"airflow": airflow})
            )

            time.sleep(2)  # 每2秒生成一次数据


if __name__ == "__main__":
    simulator = DataSimulator()
    simulator.publish_data()