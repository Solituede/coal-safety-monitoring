# 使用 Python 作为基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制代码到容器
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 运行 FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
