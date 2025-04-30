
FROM python:3.9-slim

WORKDIR /app

# Copiar y instalar requerimientos
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar todo el código
COPY . .

# IMPORTANTE: Usa el puerto de la variable de entorno PORT
CMD streamlit run --server.port=$PORT --server.enableCORS=false Dashboard@101_rescataditos.py