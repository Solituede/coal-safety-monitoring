from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.data_routes import router as data_router
from routes.safety_routes import router as safety_router
from mqtt_client import start_mqtt

app = FastAPI(title="煤矿安全监控系统")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(data_router, prefix="/api")
app.include_router(safety_router, prefix="/api")

# 启动MQTT
start_mqtt()

@app.get("/")
async def root():
    return {"message": "煤矿安全监控系统 API"}