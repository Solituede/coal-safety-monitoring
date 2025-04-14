from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.data_routes import router as data_router
from backend.mqtt_client import start_mqtt
from backend.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPICS
from backend.database import write_mining_data

app = FastAPI(title="煤矿安全监控系统")

# CORS 配置（只需一次）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()

@api_router.get("/")  # 路径改为 "/"
async def api_root():
    return {
        "message": "欢迎使用煤矿安全监控系统 API",
        "endpoints": {
            "实时数据": "/api/real-time",
            "安全状态": "/api/safety-status",
            "历史数据": "/api/historical"
        }
    }

# 先注册 data_router（具体路径优先）
app.include_router(data_router, prefix="/api")
# 后注册 api_router（根路径）
app.include_router(api_router, prefix="/api")

# 启动 MQTT
start_mqtt()

@app.get("/")
async def root():
    return {"message": "煤矿安全监控系统 API"}