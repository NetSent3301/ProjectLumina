# 🐳 Despliegue con Docker — Guía Completa

> Guía técnica para construir y desplegar ProjectLumina en contenedores Docker.
> Cubre imagen **slim** (Debian) y **Alpine**, modo panel y modo agente,
> y compatibilidad con todos los init systems soportados.

---

## Prerequisitos

Antes de continuar necesitas tener instalado:

- **Docker** `>= 24.0` — [docs.docker.com/get-docker](https://docs.docker.com/get-docker/)
- **Docker Compose** `>= 2.20` (incluido en Docker Desktop)
- Acceso a la terminal del servidor donde desplegarás el agente

Verifica las versiones:

```bash
docker --version
docker compose version
```

---

## Arquitectura de despliegue

ProjectLumina se compone de dos roles de contenedor:

| Rol | Descripción | Dónde corre |
|---|---|---|
| **Panel** | Sirve la UI web y gestiona la base de datos local | Tu máquina / servidor principal |
| **Agente** | Habla con el init system del host para controlar servicios | Cada servidor del homelab |

```
[Tu navegador]
      │ HTTP
      ▼
[Panel :8127] ─── API REST ──► [Agente servidor-1 :8127]
                           ──► [Agente servidor-2 :8127]
                           ──► [Agente servidor-N :8127]
```

---

## Elegir la imagen base

El `Dockerfile` acepta un argumento `BASE_IMAGE` que permite elegir entre
dos variantes:

| Argumento | Imagen | Tamaño aprox. | Cuándo usar |
|---|---|---|---|
| *(sin argumento)* | `python:3.12-slim` | ~180 MB | Debian/Ubuntu (recomendado) |
| `BASE_IMAGE=python:3.12-alpine` | `python:3.12-alpine` | ~60 MB | Alpine Linux en el host |

> [!NOTE]
> El contenedor en sí nunca instala un init system. Se conecta al del **host**
> mediante volúmenes y el flag `--pid=host`. La imagen solo necesita Python y
> las herramientas mínimas.

---

## Construcción de la imagen

### Imagen estándar (Debian slim)

```bash
# Desde la raíz del proyecto
docker build -t lumina:latest .
```

### Imagen Alpine

```bash
docker build \
  --build-arg BASE_IMAGE=python:3.12-alpine \
  -t lumina:alpine \
  .
```

### Etiquetar con versión

```bash
# Reemplaza v0.x.x con la versión actual (ver docs/05 - Versiones/)
docker build -t lumina:v0.x.x -t lumina:latest .
```

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto (nunca lo versiones, ya está en `.gitignore`):

```bash
cp .env.example .env
$EDITOR .env
```

Variables disponibles:

| Variable | Descripción | Requerida | Default |
|---|---|---|---|
| `LUMINA_TOKEN` | Token de autenticación de la API | **Sí en producción** | *(vacío = sin auth)* |
| `LUMINA_PORT` | Puerto publicado en el host | No | `8127` |
| `LUMINA_DEBUG` | Activa logs verbosos | No | `false` |
| `LUMINA_DB` | Ruta de la base de datos dentro del contenedor | No | `/app/data/lumina.db` |

Genera un token seguro con:

```bash
openssl rand -hex 32
```

---

## Modo Panel

El panel no necesita acceso al init system del host. Solo sirve la interfaz web.

### Con docker compose (recomendado)

```bash
docker compose --profile panel up -d
```

### Con docker run

```bash
docker run -d \
  --name lumina-panel \
  --restart unless-stopped \
  -p 8127:8127 \
  -v ./data:/app/data \
  --env-file .env \
  lumina:latest
```

Accede a la UI en: `http://localhost:8127`

---

## Modo Agente

El agente necesita hablar con el init system del host para controlar servicios.
Los flags necesarios varían según el init system del servidor destino.

> [!IMPORTANT]
> El agente debe correr en **cada servidor** que quieras controlar desde el panel.
> Registra cada agente en la UI del panel con su `IP:puerto` y token.

### Host con systemd (Debian, Ubuntu, Arch, Fedora…)

```bash
docker run -d \
  --name lumina-agente \
  --restart unless-stopped \
  -p 8127:8127 \
  --pid=host \
  --privileged \
  -v /run/systemd:/run/systemd:ro \
  -v /var/run/dbus:/var/run/dbus:ro \
  -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
  -v ./data:/app/data \
  --env-file .env \
  lumina:latest
```

O con docker compose:

```bash
docker compose --profile agente up -d
```

### Host con OpenRC (Alpine Linux, Gentoo, Artix-openrc)

OpenRC no usa `/run/systemd`; el agente solo necesita `--pid=host` para
poder ejecutar `rc-service` en el contexto del host:

```bash
docker run -d \
  --name lumina-agente \
  --restart unless-stopped \
  -p 8127:8127 \
  --pid=host \
  --privileged \
  -v ./data:/app/data \
  --env-file .env \
  lumina:alpine          # Usa la imagen construida para Alpine
```

> [!NOTE]
> `rc-service` y `rc-status` deben estar instalados **en el host** (no en el
> contenedor). El contenedor los llama vía el namespace de PID del host.

### Host con Runit (Void Linux, Artix-runit)

```bash
docker run -d \
  --name lumina-agente \
  --restart unless-stopped \
  -p 8127:8127 \
  --pid=host \
  --privileged \
  -v /var/service:/var/service:ro \
  -v /var/log:/var/log:ro \
  -v ./data:/app/data \
  --env-file .env \
  lumina:latest
```

Los volúmenes montados permiten:
- `/var/service` → detectar y listar servicios supervisados por runit
- `/var/log` → leer los logs de svlogd (`/var/log/<servicio>/current`)

### Host con SysV — experimental (Devuan, MX Linux, RHEL 6)

```bash
docker run -d \
  --name lumina-agente \
  --restart unless-stopped \
  -p 8127:8127 \
  --pid=host \
  --privileged \
  -v /etc/init.d:/etc/init.d:ro \
  -v /var/log:/var/log:ro \
  -v ./data:/app/data \
  --env-file .env \
  lumina:latest
```

> [!WARNING]
> El soporte SysV es **experimental**. El comportamiento de `service --status-all`
> y los scripts de `/etc/init.d/` varía entre distros. Úsalo bajo tu propio riesgo.

---

## Verificar el init system detectado

Después de levantar el agente, puedes confirmar qué backend detectó con:

```bash
curl -s http://localhost:8127/api/servidor/init \
  -H "X-API-Key: tu-token" | python3 -m json.tool
```

Respuesta esperada en Alpine (OpenRC):

```json
{
  "backend": "openrc",
  "version": "0.54.2",
  "pid1": "openrc-init"
}
```

Respuesta esperada en un sistema con systemd:

```json
{
  "backend": "systemd",
  "version": "255",
  "pid1": "systemd"
}
```

---

## Healthcheck

El contenedor tiene un healthcheck configurado. Verifica el estado con:

```bash
docker inspect --format='{{.State.Health.Status}}' lumina-agente
```

Valores posibles: `starting` → `healthy` → `unhealthy`

El endpoint de healthcheck es `GET /api/health`.

---

## Logs del contenedor

```bash
# Últimas 100 líneas
docker logs lumina-agente --tail 100

# Streaming en tiempo real
docker logs -f lumina-agente

# Con timestamps
docker logs -t lumina-agente
```

---

## Actualizar la imagen

```bash
# 1. Reconstruir la imagen con el código nuevo
docker build -t lumina:latest .

# 2. Recrear el contenedor (compose lo hace automático)
docker compose --profile agente up -d --force-recreate

# O con docker run, para el agente manual:
docker stop lumina-agente
docker rm lumina-agente
docker run -d ... lumina:latest  # (mismo comando de antes)
```

---

## Persistencia de datos

La base de datos SQLite se guarda en `./data/lumina.db` del **host**.
El volumen `-v ./data:/app/data` garantiza que no se pierda al recrear el contenedor.

> [!CAUTION]
> Si eliminas el volumen (`docker compose down -v`), perderás toda la configuración
> de servicios registrados en el panel. Haz backup antes.

Backup manual:

```bash
cp ./data/lumina.db ./data/lumina.db.bak-$(date +%Y%m%d)
```

---

## Relacionado

- [Configuración](../Configuracion.md) · Variables de entorno detalladas
- [Sistema Adaptable](../Sistema%20Adaptable.md) · Detección de init system
- [Seguridad](../../03%20-%20Seguridad/Seguridad.md) · Token de API y HTTPS
- [Control Remoto](../Control%20Remoto.md) · Cómo el panel habla con los agentes
