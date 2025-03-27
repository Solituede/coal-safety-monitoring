from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from config import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET
import time

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def write_mining_data(data):
    point = Point("mining_data") \
        .tag("device", "shearer") \
        .field("speed", data["speed"]) \
        .field("extraction", data["extraction"]) \
        .field("airflow", data["airflow"]) \
        .field("gas_concentration", data["gas_concentration"]) \
        .field("safe_speed", data["safe_speed"]) \
        .time(time.time_ns(), WritePrecision.NS)
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

def read_historical_data(hours=1):
    query = f'from(bucket: "{INFLUXDB_BUCKET}") |> range(start: -{hours}h)'
    return client.query_api().query(query, org=INFLUXDB_ORG)