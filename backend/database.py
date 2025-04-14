from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time

# InfluxDB配置
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "lVTN7VF0jvRt5PB2Ub6z4kEbkUc5qaXrB-sKzwuX-EZoOTJPscDj1jahy4i8lQ9jRJB-8fXcZ2753hz7nhgn6A=="
INFLUXDB_ORG = "xiankejidaxue"
INFLUXDB_BUCKET = "wasi"

# 创建InfluxDB客户端
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)


def write_mining_data(data):
    point = Point("mining_data") \
        .tag("device", "shearer") \
        .field("current_speed", data["current_speed"]) \
        .field("extraction", data["extraction"]) \
        .field("airflow", data["airflow"]) \
        .field("gas_concentration", data["gas_concentration"]) \
        .field("safe_speed", data["safe_speed"]) \
        .field("gas_emission", data["gas_emission"]) \
        .time(time.time_ns(), WritePrecision.NS)
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)


def read_latest_speed_data(minutes: int):
    # 原来按分钟读取 speed 的函数，重命名避免混淆
    query = f'''
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: -{minutes}m)
      |> filter(fn: (r) => r._measurement == "mining_data")
      |> filter(fn: (r) => r._field == "current_speed")
      |> last()
    '''

    return client.query_api().query(query, org=INFLUXDB_ORG)


def query_with_flux(flux_query: str):
    # 新增：直接执行外部传入的 Flux 查询语句
    return client.query_api().query(flux_query, org=INFLUXDB_ORG)



# 示例调用
if __name__ == "__main__":
    # 写入示例数据
    sample_data = {
        "current_speed": 100,
        "extraction": 50,
        "airflow": 200,
        "gas_concentration": 0.5,
        "safe_speed": 90,
        "gas_emission": 0.3
    }
    write_mining_data(sample_data)

    # 读取历史数据

