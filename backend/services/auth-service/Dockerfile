# services/auth-service/Dockerfile

# Base image
FROM python:3.11-slim

# Working directory
WORKDIR /app

# Bağımlılıkları kopyala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# FastAPI uygulamasını Uvicorn ile başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
