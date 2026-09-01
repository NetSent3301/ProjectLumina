# 🏔️ Despliegue en Alpine Linux (OpenRC) — ProjectLumina

> Guía completa para correr ProjectLumina en **Alpine Linux** usando **OpenRC** como init system, tanto en contenedor Docker como en metal.

---

## Por qué Alpine + OpenRC

- **Imagen base ~5 MB** (vs ~80 MB Debian slim)
- **OpenRC nativo**: `rc-service`, `rc-status`, syslog en `/var/log/messages`
- **Seguridad**: musl libc, stack smashing protection, PIE por defecto
- **Velocidad**: Arranque más rápido, menos superficie de ataque
- **Homelab friendly**: Ideal para Raspberry Pi, VPS pequeños, contenedores

---

## Requisitos del host Alpine

```bash
# Paquetes necesarios en el host Alpine
apk add openrc  # Ya viene por defecto en Alpine
# Para el agente (acceso a servicios del host):
# - El contenedor necesita --pid=host --privileged
# - No requiere montar /run/systemd (no existe en OpenRC)
```

---

## Opción A: Docker (Recomendado)

### 1. Construir imagen Alpine

```bash
# Desde la raíz del proyecto
docker build --build-arg BASE_IMAGE=python:3.12-alpine -t lumina-alpine .
```

> El Dockerfile detecta `apk` automáticamente e instala: `procps`, `curl`, `gcc`, `musl-dev`, `linux-headers` (necesarios para compilar `psutil` en musl).

### 2. Panel central (solo UI + API local)

```bash
# No necesita acceso al init system del host
docker run -d \
  --name lumina-panel \
  --restart unless-stopped \
  -p 8127:8127 \
  -v ./data:/app/data \
  -e LUMINA_TOKEN=tu-token-secreto \
  -e LUMINA_DEBUG=false \
  lumina-alpine
```

### 3. Agente (gestiona servicios del host Alpine)

```bash
# En CADA máquina Alpine del homelab
docker run -d \
  --name lumina-agente \
  --restart unless-stopped \
  --pid=host \
  --privileged \
  -p 8127:8127 \
  -v ./data:/app/data \
  -e LUMINA_TOKEN=tu-token-secreto \
  -e LUMINA_DEBUG=false \
  lumina-alpine
```

> **Diferencia clave vs systemd**: En Alpine/OpenRC **NO** se montan `/run/systemd`, `/var/run/dbus`, `/sys/fs/cgroup`. OpenRC no los usa.

### 4. Docker Compose (Perfil `agente-alpine`)

Ver [docker-compose.yml actualizado](../docker-compose.yml) con perfil `agente-alpine`.

```bash
# Panel central
docker compose --profile panel up -d

# Agente en máquina Alpine (desde esa máquina)
docker compose --profile agente-alpine up -d
```

---

## Opción B: Metal (Instalación directa en Alpine)

### 1. Instalar dependencias

```bash
# Como root
apk add python3 py3-pip py3-venv git procps curl
# psutil compila extensiones C:
apk add gcc musl-dev linux-headers
```

### 2. Clonar y configurar

```bash
git clone <repo> /opt/lumina
cd /opt/lumina
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar variables

```bash
cat > .env <<EOF
LUMINA_HOST=0.0.0.0
LUMINA_PORT=8127
LUMINA_DB=/opt/lumina/data/lumina.db
LUMINA_TOKEN=tu-token-secreto
LUMINA_DEBUG=false
EOF
mkdir -p data logs
```

### 4. Servicio OpenRC (para que arranque al boot)

```bash
# /etc/init.d/lumina
cat > /etc/init.d/lumina <<'EOF'
#!/sbin/openrc-run
name="ProjectLumina"
description="Panel de administración remota de servidores/bots/webs"
command="/opt/lumina/.venv/bin/uvicorn"
command_args="lumina:app --host 0.0.0.0 --port 8127"
directory="/opt/lumina"
user="lumina"
pidfile="/run/lumina.pid"
depend() {
    need net
    after firewall
}
EOF
chmod +x /etc/init.d/lumina

# Usuario dedicado
adduser -D -H -s /sbin/nologin lumina
chown -R lumina:lumina /opt/lumina

# Habilitar e iniciar
rc-update add lumina default
rc-service lumina start
rc-status | grep lumina
```

### 5. Verificar

```bash
# Healthcheck
curl http://localhost:8127/api/health
# → {"status":"ok","version":"0.1.0"}

# Init system detectado
curl http://localhost:8127/api/servidor/init
# → {"backend":"openrc","version":"0.54.2","pid1":"openrc-init"}

# Servicios activos
curl http://localhost:8127/api/servidor/servicios
# → [{"unidad":"sshd","estado":"started"},{"unidad":"crond","estado":"started"},...]
```

---

## Diferencias clave: systemd vs OpenRC

| Aspecto | systemd (Debian/Ubuntu) | OpenRC (Alpine/Gentoo) |
|---------|------------------------|------------------------|
| **Comando principal** | `systemctl` | `rc-service` |
| **Estado global** | `systemctl list-units` | `rc-status --all` |
| **Nombres de servicio** | `nginx.service` | `nginx` (sin sufijo) |
| **Logs** | `journalctl -u nginx` | Syslog (`/var/log/messages`) o `/var/log/nginx/current` |
| **PID 1** | `systemd` | `openrc-init` |
| **Docker agente** | `--pid=host --privileged -v /run/systemd:/run/systemd ...` | `--pid=host --privileged` (sin montajes extra) |
| **Verificar disponible** | `shutil.which("systemctl")` | `shutil.which("rc-service")` |

---

## Nombres de servicio en OpenRC

En la UI de ProjectLumina, al registrar un bot/web en una máquina Alpine:

- **NO** uses `.service`: ❌ `nginx.service`
- **SÍ** usa nombre simple: ✅ `nginx`, `sshd`, `crond`, `docker`, `mariadb`

El backend OpenRC normaliza automáticamente.

---

## Logs en OpenRC

ProjectLumina usa esta estrategia de fallback:

1. **`/var/log/<servicio>/current`** — Si el servicio usa `svlogd` (logger de runit, común en Gentoo/Alpine con s6)
2. **Syslog filtrado** — Busca en `/var/log/messages` (Alpine), `/var/log/syslog` (Gentoo), `/var/log/everything/everything.log`

> Si el agente no corre como root, los logs del syslog pueden dar "sin permiso". Ejecuta el agente como root o configura `rsyslog`/`syslog-ng` para permitir lectura.

---

## Troubleshooting Alpine

### `psutil` falla al instalar

```bash
# Asegúrate de tener headers de kernel y toolchain
apk add gcc musl-dev linux-headers
pip install --no-cache-dir psutil
```

### `rc-service` no encontrado

```bash
# Verifica que OpenRC esté instalado y en PATH
rc-service --version
which rc-service
# Debe devolver /sbin/rc-service o /usr/sbin/rc-service
```

### Permisos de logs

```bash
# Opción 1: Agente como root (en Docker: --user root o sin user)
# Opción 2: Configurar syslog para lectura grupal
# En /etc/rsyslog.conf o /etc/syslog-ng/syslog-ng.conf:
# $FileCreateMode 0644  # rsyslog
# options { perm(0644); };  # syslog-ng
```

### Puerto ya en uso

```bash
# Verifica qué usa el puerto 8127
netstat -tlnp | grep 8127
ss -tlnp | grep 8127
```

---

## Verificación completa (Checklist)

- [ ] Imagen Alpine construida: `docker images | grep lumina-alpine`
- [ ] Panel central responde: `curl http://panel-ip:8127/api/health`
- [ ] Agente Alpine detecta OpenRC: `curl http://agente-ip:8127/api/servidor/init` → `"backend":"openrc"`
- [ ] Agente lista servicios: `curl http://agente-ip:8127/api/servidor/servicios`
- [ ] Panel central ve agente: `curl http://panel-ip:8127/api/conexion`
- [ ] UI accesible: `http://panel-ip:8127/` → Vista "Servidores" muestra agente conectado
- [ ] Acciones funcionan: Iniciar/detener/reiniciar un servicio desde la UI

---

## Referencias

- [Dockerfile](../../Dockerfile) — Multi-stage con `BASE_IMAGE` configurable
- [app/system/openrc.py](../../app/system/openrc.py) — Backend OpenRC completo
- [app/system/detector.py](../../app/system/detector.py) — Auto-detección de init system
- [docs/02 - Desarrollo/Arquitectura Backend.md](../02%20-%20Desarrollo/Arquitectura%20Backend.md) — Arquitectura en capas
- [docs/02 - Desarrollo/Despliegue/Docker.md](../02%20-%20Desarrollo/Despliegue/Docker.md) — Despliegue Docker general
- Wiki Alpine OpenRC: https://wiki.alpinelinux.org/wiki/OpenRC