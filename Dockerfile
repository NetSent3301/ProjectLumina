# ProjectLumina — Dockerfile multietapa
# Uso: docker build -t luminia .
#   Panel central:    docker run --rm -p 8127:8127 -v ./data:/app/data luminia
#   Agente (host):    docker run --rm -p 8127:8127 --pid=host --privileged -v /run/systemd:/run/systemd -v /var/run/dbus:/var/run/dbus -v ./data:/app/data luminia

FROM python:3.12-slim AS base

# Dependencias de sistema para psutil, httpx y (opcional) systemctl/journalctl
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    systemd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código de la aplicación
COPY app ./app
COPY web ./web
COPY lumina.py .

# Usuario no-root para panel (agente usa root por systemd)
RUN useradd --no-create-home --shell /bin/bash luminia \
    && chown -R luminia:luminia /app

ENV PYTHONUNBUFFERED=1 \
    LUMINA_HOST=0.0.0.0 \
    LUMINA_PORT=8127 \
    LUMINA_DB=/app/data/lumina.db \
    LUMINA_TOKEN=

EXPOSE 8127

# Entrypoint: usa uvicorn directo (lumina.py reexporta app.main:app)
CMD ["uvicorn", "lumina:app", "--host", "0.0.0.0", "--port", "8127"]