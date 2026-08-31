# ProjectLumina — Dockerfile multietapa con soporte para imagen slim y Alpine.
#
# Uso básico (imagen slim — Debian, igual que antes):
#   docker build -t lumina .
#
# Uso con Alpine Linux (más ligero, usa OpenRC en el host):
#   docker build --build-arg BASE_IMAGE=python:3.12-alpine -t lumina-alpine .
#
# Correr el panel central:
#   docker run --rm -p 8127:8127 -v ./data:/app/data lumina
#
# Correr el agente (acceso al init system del host):
#   docker run --rm -p 8127:8127 --pid=host --privileged \
#     -v /run/systemd:/run/systemd \        ← Solo si el host usa systemd
#     -v /var/run/dbus:/var/run/dbus \      ← Solo si el host usa systemd
#     -v ./data:/app/data lumina
#
# Para un host Alpine (OpenRC), el agente no necesita montar /run/systemd.
# Solo necesita acceso a los sockets de OpenRC si los hay:
#   docker run --rm -p 8127:8127 --pid=host --privileged \
#     -v ./data:/app/data lumina-alpine

# ─────────────────────────────────────────────────────────────────────────────
# ARG: imagen base seleccionable en tiempo de build.
#
# Valor por defecto: python:3.12-slim (basada en Debian Bookworm).
# Para Alpine:       python:3.12-alpine
#
# La ARG debe declararse ANTES del primer FROM para estar disponible en él.
# ─────────────────────────────────────────────────────────────────────────────
ARG BASE_IMAGE=python:3.12-slim

# ─────────────────────────────────────────────────────────────────────────────
# Stage: base
# Construye la imagen final a partir de la imagen seleccionada.
# ─────────────────────────────────────────────────────────────────────────────
FROM ${BASE_IMAGE} AS base

# Volvemos a declarar ARG después del FROM para que esté disponible dentro
# del stage. Las ARGs declaradas antes del primer FROM no se heredan
# automáticamente en los stages (comportamiento de Docker multi-stage).
ARG BASE_IMAGE=python:3.12-slim

# ─────────────────────────────────────────────────────────────────────────────
# Dependencias de sistema
#
# Usamos un script de shell para detectar el gestor de paquetes disponible:
#   - apt-get → imágenes basadas en Debian (slim, bookworm, etc.)
#   - apk     → imágenes Alpine Linux
#
# Paquetes instalados:
#   procps   → provee herramientas como ps, top; requerido por psutil en algunos casos.
#   curl     → usado por el healthcheck de docker-compose.
#   (systemd se elimina: el agente habla con el init del HOST, no instala uno propio)
# ─────────────────────────────────────────────────────────────────────────────
RUN if command -v apt-get > /dev/null 2>&1; then \
        # Imagen Debian/slim: usamos apt-get.
        apt-get update && \
        apt-get install -y --no-install-recommends \
            procps \
            curl \
        && rm -rf /var/lib/apt/lists/*; \
    elif command -v apk > /dev/null 2>&1; then \
        # Imagen Alpine: usamos apk.
        # --no-cache evita mantener el índice de paquetes en la imagen.
        apk add --no-cache \
            procps \
            curl \
            gcc \
            musl-dev \
            linux-headers; \
        # gcc, musl-dev y linux-headers son necesarios para compilar
        # extensiones C de psutil en Alpine (usa musl en lugar de glibc).
    else \
        echo "ERROR: gestor de paquetes no reconocido (ni apt-get ni apk)" && exit 1; \
    fi

# ─────────────────────────────────────────────────────────────────────────────
# Directorio de trabajo dentro del contenedor.
# ─────────────────────────────────────────────────────────────────────────────
WORKDIR /app

# ─────────────────────────────────────────────────────────────────────────────
# Dependencias Python
#
# Copiamos solo requirements.txt primero (antes que el código fuente) para
# aprovechar el caché de capas de Docker: si el código cambia pero
# requirements.txt no, esta capa no se reconstruye.
# ─────────────────────────────────────────────────────────────────────────────
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# --no-cache-dir → no guarda el caché de pip en la imagen, reduciendo su tamaño.

# ─────────────────────────────────────────────────────────────────────────────
# Código fuente de la aplicación
# ─────────────────────────────────────────────────────────────────────────────
COPY app ./app      # Código Python de la aplicación.
COPY web ./web      # Assets del frontend (HTML, CSS, JS).
COPY lumina.py .    # Punto de entrada que re-exporta app.main:app para uvicorn.

# ─────────────────────────────────────────────────────────────────────────────
# Usuario no-root para el modo panel
#
# El modo panel no necesita acceso privilegiado al init system del host,
# así que corremos como usuario sin privilegios por seguridad.
#
# Nota: el modo agente que necesita hablar con systemd/OpenRC del host
# puede necesitar correr como root (o con CAP_SYS_PTRACE). Esto se
# configura en docker-compose.yml con ``user: root`` si es necesario.
# ─────────────────────────────────────────────────────────────────────────────
RUN useradd --no-create-home --shell /bin/bash lumina \
    && chown -R lumina:lumina /app
# lumina es el nombre del usuario no-root; /app le pertenece completamente.

# ─────────────────────────────────────────────────────────────────────────────
# Variables de entorno con valores por defecto.
#
# Todas llevan el prefijo LUMINA_ para que pydantic-settings las recoja.
# Los valores aquí son los defaults del contenedor; se sobreescriben con
# -e o en el .env del docker-compose.
# ─────────────────────────────────────────────────────────────────────────────
ENV PYTHONUNBUFFERED=1 \
    # PYTHONUNBUFFERED=1 → los prints y logs salen inmediatamente (sin buffer).
    LUMINA_HOST=0.0.0.0 \
    # 0.0.0.0 → escucha en todas las interfaces del contenedor.
    LUMINA_PORT=8127 \
    # Puerto en el que uvicorn escucha dentro del contenedor.
    LUMINA_DB=/app/data/lumina.db \
    # Ruta de la base de datos SQLite dentro del contenedor.
    LUMINA_TOKEN=
    # Token de autenticación. Vacío = sin autenticación (solo para dev/local).

# ─────────────────────────────────────────────────────────────────────────────
# Puerto expuesto por el contenedor.
# EXPOSE es solo documentación; el mapeo real se hace en docker run o compose.
# ─────────────────────────────────────────────────────────────────────────────
EXPOSE 8127

# ─────────────────────────────────────────────────────────────────────────────
# Entrypoint: uvicorn sirve la app ASGI definida en lumina.py.
#
# lumina:app → módulo lumina.py, objeto app (re-exportado de app.main:app).
# --host / --port → leídos de las ENV vars por uvicorn (o se pueden pasar aquí).
# ─────────────────────────────────────────────────────────────────────────────
CMD ["uvicorn", "lumina:app", "--host", "0.0.0.0", "--port", "8127"]