import random
import time
from datetime import datetime, timezone
import schedule
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB 配置
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "lVTN7VF0jvRt5PB2Ub6z4kEbkUc5qaXrB-sKzwuX-EZoOTJPscDj1jahy4i8lQ9jRJB-8fXcZ2753hz7nhgn6A=="
INFLUXDB_ORG = "xiankejidaxue"
INFLUXDB_BUCKET = "wasi"

# 初始化 InfluxDB 客户端
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# 数据生成函数
def generate_speed(): return round(random.uniform(2.0, 4.5), 1)
def generate_extraction(): return float(random.randint(20, 40))
def generate_airflow(): return float(random.randint(800, 1500))
def generate_gas_concentration(): return round(random.uniform(0.1, 1.0), 1)
def generate_safe_speed(): return round(random.uniform(3.0, 5.0), 1)
def generate_gas_emission(): return float(random.randint(10, 20))

# 写入数据到 InfluxDB
def write_to_influxdb():
    try:
        # 生成随机数据
        current_speed = generate_speed()
        extraction = generate_extraction()
        airflow = generate_airflow()
        gas_concentration = generate_gas_concentration()
        safe_speed = generate_safe_speed()
        gas_emission = generate_gas_emission()

        # 生成“当前整分钟”时间戳，实现覆盖
        fixed_time = datetime.now(timezone.utc).replace(second=0, microsecond=0)

        # 创建数据点
        point = Point("coal_safety") \
            .tag("source", "manual") \
            .field("current_speed", current_speed) \
            .field("extraction", extraction) \
            .field("airflow", airflow) \
            .field("gas_concentration", gas_concentration) \
            .field("safe_speed", safe_speed) \
            .field("gas_emission", gas_emission) \
            .time(fixed_time, write_precision="s")  # 秒级时间戳

        # 写入数据
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print(f"[INFO] Data written at {fixed_time.isoformat()} with values: "
              f"current_speed={current_speed}, extraction={extraction}, airflow={airflow}, "
              f"gas_concentration={gas_concentration}, safe_speed={safe_speed}, gas_emission={gas_emission}")
    except Exception as e:
        print(f"[ERROR] Failed to write to InfluxDB: {e}")

# 定时任务
def schedule_task():
    schedule.every(10).seconds.do(write_to_influxdb)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Data generator stopped by user.")
    finally:
        client.close()
        print("[INFO] InfluxDB client closed.")

# 主函数
if __name__ == "__main__":
    print("Starting data generator for InfluxDB (overwriting mode)...")
    write_to_influxdb()
    schedule_task()
