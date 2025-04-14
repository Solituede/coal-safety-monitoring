from fastapi import APIRouter
from ..database import query_with_flux
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/historical")
async def get_real_time_data():
    """获取每个指标的最新数据（带调试校验）"""
    query = """
    from(bucket: "wasi")
      |> range(start: -1h)
      |> filter(fn: (r) => 
        r._field == "airflow" or
        r._field == "extraction" or
        r._field == "gas_concentration" or
        r._field == "gas_emission" or
        r._field == "safe_speed" or
        r._field == "current_speed" 
      )
      |> group(columns: ["_field"])
      |> last()
      |> group()
    """

    try:
        raw_data = query_with_flux(query)
        logger.debug(f"原始查询结果结构: {type(raw_data)}")

        # 调试：打印原始数据结构
        for i, table in enumerate(raw_data):
            logger.debug(f"表 {i} 包含 {len(table.records)} 条记录")
            for record in table.records:
                logger.debug(f"记录内容: {record.values}")

        # 处理数据
        latest = [
            {
                "timestamp": record["_time"].isoformat(),
                "metric": record["_field"],
                "value": record["_value"],
                "device": record.values.get("source", "unknown")
            }
            for table in raw_data
            for record in table.records
        ]

        # 数据校验
        if len(latest) != 5:
            logger.error(f"数据量异常！预期5条，实际获取{len(latest)}条。详细数据：{latest}")

        return {"data": latest}

    except Exception as e:
        logger.error(f"查询失败: {str(e)}")
        return {"error": "内部服务器错误"}