# backend/Dockerfile

# 基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 将本地 backend/ 目录复制到容器的 /app/backend
COPY . /app/backend

# 设置工作目录和 PYTHONPATH
WORKDIR /app/backend
ENV PYTHONPATH=/app/backend

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置 Python 模块搜索路径（关键！）
ENV PYTHONPATH=/app

# 启动命令（假设 app.py 中的 FastAPI 实例名为 `app`）
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]