# Build 3
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl wget build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 10000
CMD elysia start --host 0.0.0.0 --port 10000 --no-reload
