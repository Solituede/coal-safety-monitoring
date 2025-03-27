from fastapi import APIRouter
from database import read_historical_data
from safety_calculator import SafetyCalculator

router = APIRouter()

@router.get("/safety-status")
async def get_safety_status():
    raw_data = read_historical_data(0.1)  # 获取最近6分钟数据
    if not raw_data:
        return {"error": "No data available"}
    latest = {record.get_field(): record.get_value() for table in raw_data for record in table.records[-1:]}
    return {
        "current_speed": latest.get("speed", 0.0),
        "safe_speed": latest.get("safe_speed", 3.2),
        "gas_concentration": latest.get("gas_concentration", 0.0),
        "status": SafetyCalculator.get_safety_status(latest.get("speed", 0.0))
    }