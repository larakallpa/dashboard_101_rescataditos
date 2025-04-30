FROM python:3.9-slim

# Instalar locales
RUN apt-get update && apt-get install -y locales \
    && sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen

# Configurar variables de entorno
ENV LANG es_ES.UTF-8
ENV LC_ALL es_ES.UTF-8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Comando optimizado
CMD streamlit run --server.port=$PORT --server.enableCORS=false --server.enableWebsocketCompression=false --server.headless=true Dashboard@101_rescataditos.py