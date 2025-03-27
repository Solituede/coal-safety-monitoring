from fastapi import APIRouter
from database import read_historical_data

router = APIRouter()


@router.get("/real-time")
async def get_real_time_data():
    """获取最新实时数据"""
    query = '''
    from(bucket: "wasi")
      |> range(start: -1m)
      |> last()
    '''
    raw_data = read_historical_data()
    if not raw_data:
        return {"message": "No data available"}

    latest = {}
    for record in raw_data[-1].records:
        latest[record.get_field()] = record.get_value()
    return latest


@router.get("/historical")
async def get_historical_data(hours: int = 6, limit: int = 1000):
    """获取历史数据（带分页）"""
    raw_data = read_historical_data(hours)
    processed = []
    for table in raw_data:
        for record in table.records[:limit]:
            processed.append({
                "timestamp": record.get_time().isoformat(),
                "metric": record.get_field(),
                "value": record.get_value(),
                "device": record.values.get("device", "unknown")
            })
    return {"data": processed}