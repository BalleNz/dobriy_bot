FROM python:3.12-slim

# Установите системные зависимости
RUN apt-get update && apt-get install -y \
    postgresql-server-dev-all \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .