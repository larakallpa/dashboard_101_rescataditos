
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Comando optimizado
CMD streamlit run --server.port=$PORT --server.enableCORS=false --server.enableWebsocketCompression=false --server.headless=true Dashboard@101_rescataditos.py