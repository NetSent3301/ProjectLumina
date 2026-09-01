# 📋 Instalación Paso a Paso — Panel + Agentes

> Guía práctica para levantar **ProjectLumina** en producción: un panel central y tantos agentes como servidores tengas en tu homelab.

---

## Requisitos previos

- **Panel central**: 1 máquina (tu laptop, VPS principal, Raspberry Pi 4+)
- **Agentes**: 1 por cada server que quieras controlar (Debian, Ubuntu, Alpine, Arch, Void, etc.)
- **Docker + Docker Compose** en TODAS las máquinas (recomendado)
- **Mismo token** (`LUMINA_TOKEN`) en panel y todos los agentes

---

## 1. Preparar el repositorio (en tu máquina de desarrollo)

```bash
git clone <tu-repo> ProjectLumina
cd ProjectLumina

# Generar token seguro (copia y guarda, lo usarás en TODOS los .env)
openssl rand -hex 32
# Ejemplo salida: a1b2c3d4e5f6...
```

---

## 2. Panel Central — Máquina Principal

### 2.1 Configurar `.env`

```bash
cd ProjectLumina
cat > .env <<EOF
LUMINA_TOKEN=a1b2c3d4e5f6...   # Tu token generado
LUMINA_PORT=8127
LUMINA_DEBUG=false
EOF
```

### 2.2 Levantar con Docker Compose

```bash
# Construir imagen (solo la primera vez o tras cambios de código)
docker compose build

# Levantar panel en background
docker compose --profile panel up -d

# Ver logs
docker compose logs -f panel
```

### 2.3 Verificar panel

```bash
# Healthcheck
curl http://localhost:8127/api/health
# → {"status":"ok","version":"0.1.0"}

# UI en navegador
# http://TU_IP_PANEL:8127/
```

> **Nota**: El panel NO necesita `--pid=host` ni `--privileged`. Solo sirve la UI y su API local.

---

## 3. Agente — En CADA Server del Homelab

Repite este proceso en **cada servidor** que quieras controlar.

### 3.1 Copiar archivos necesarios al server

Opción A: Clonar repo completo
```bash
# En el server destino
git clone <tu-repo> /opt/lumina
cd /opt/lumina
```

Opción B: Solo archivos mínimos (más ligero)
```bash
# En tu máquina local, crear paquete mínimo
tar -czf lumina-agent.tar.gz Dockerfile docker-compose.yml requirements.txt app/ web/ lumina.py

# Copiar al server
scp lumina-agent.tar.gz user@server-ip:/opt/
ssh user@server-ip "cd /opt && tar -xzf lumina-agent.tar.gz && cd lumina-agent"
```

### 3.2 Configurar `.env` (MISMO token que el panel)

```bash
cd /opt/lumina   # o /opt/lumina-agent

cat > .env <<EOF
LUMINA_TOKEN=a1b2c3d4e5f6...   # ¡MISMO TOKEN que el panel!
LUMINA_PORT=8127
LUMINA_DEBUG=false
EOF
```

### 3.3 Levantar agente según el init system del host

#### 🐧 Host con **systemd** (Debian, Ubuntu, Arch, Fedora, RHEL, openSUSE...)
```bash
# Construir imagen (si no la construiste antes)
docker compose build

# Levantar agente systemd
docker compose --profile agente up -d

# Ver logs
docker compose logs -f agente
```

#### 🏔️ Host con **OpenRC** (Alpine Linux, Gentoo, Artix-openrc)
```bash
# Construir imagen Alpine (más ligera)
docker compose build agente-alpine

# Levantar agente OpenRC
docker compose --profile agente-alpine up -d

# Ver logs
docker compose logs -f agente-alpine
```

#### 🏃 Host con **Runit** (Void Linux, Artix-runit)
```bash
# Usar imagen estándar (Debian slim) - Runit no necesita imagen especial
docker compose build

# Levantar con comando manual (no hay perfil runit en compose aún)
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

### 3.4 Verificar agente

```bash
# Healthcheck
curl http://localhost:8127/api/health

# Init system detectado
curl http://localhost:8127/api/servidor/init
# systemd → {"backend":"systemd","version":"255","pid1":"systemd"}
# OpenRC  → {"backend":"openrc","version":"0.54.2","pid1":"openrc-init"}

# Servicios activos
curl http://localhost:8127/api/servidor/servicios
```

---

## 4. Registrar Agentes en el Panel Central

### 4.1 Desde la UI (recomendado)

1. Abre `http://IP_PANEL:8127/`
2. Sidebar → **Servidores**
3. Botón **"Agregar servidor"**
4. Completa:
   - **Nombre**: `vps-principal`, `raspi-casa`, `server-backups`
   - **URL**: `http://IP_DEL_AGENTE:8127` (ej: `http://192.168.1.50:8127`)
   - **Token**: El mismo `LUMINA_TOKEN`
5. Guardar → El panel hace healthcheck inmediato

### 4.2 Desde API (alternativo)

```bash
curl -X POST http://IP_PANEL:8127/api/servidores \
  -H "Content-Type: application/json" \
  -H "X-API-Key: a1b2c3d4e5f6..." \
  -d '{"nombre": "vps-principal", "url": "http://1.2.3.4:8127"}'
```

---

## 5. Verificar Conexión Panel ↔ Agentes

```bash
# Desde el panel central
curl -H "X-API-Key: a1b2c3d4e5f6..." http://IP_PANEL:8127/api/conexion

# Respuesta esperada:
{
  "principal": {
    "conectado": true,
    "backend": "systemd",
    "version": "0.1.0"
  },
  "remotos": [
    {
      "id": 1,
      "nombre": "vps-principal",
      "url": "http://1.2.3.4:8127",
      "conectado": true,
      "backend": "systemd",
      "ultimo_check": "2026-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "nombre": "raspi-casa",
      "url": "http://192.168.1.50:8127",
      "conectado": true,
      "backend": "openrc",
      "ultimo_check": "2026-01-15T10:30:05Z"
    }
  ]
}
```

En la UI: Sidebar muestra indicador 🟢 **Conectado** por cada agente.

---

## 6. Registrar Bots/Webs en Cada Agente

Desde la UI del panel → Vista **Servicios** → Botón **"Nuevo servicio"**

| Campo | Bot (ej. Discord) | Web (ej. Nginx + Node) |
|-------|-------------------|------------------------|
| **Nombre** | `bot-trading` | `web-api` |
| **Tipo** | `bot` | `web` |
| **Comando inicio** | `python3 /opt/bots/trading/main.py` | (vacío, usa systemd/OpenRC) |
| **Directorio trabajo** | `/opt/bots/trading` | (vacío) |
| **Unidad systemd/OpenRC** | `bot-trading` | `nginx` |
| **Healthcheck URL** | (vacío) | `http://localhost:3000/health` |

> **Importante**: La "Unidad systemd/OpenRC" debe coincidir con el nombre del servicio en EL HOST del agente.
> - En Debian: `bot-trading.service` → escribe `bot-trading`
> - En Alpine: `rc-service nginx status` → escribe `nginx` (sin .service)

---

## 7. Comandos Útiles Diarios

### Panel Central
```bash
# Ver estado
docker compose ps

# Logs panel
docker compose logs -f panel

# Reiniciar panel
docker compose restart panel

# Actualizar código y reconstruir
git pull
docker compose build
docker compose --profile panel up -d --force-recreate

# Backup BD
cp ./data/lumina.db ./data/lumina.db.bak-$(date +%Y%m%d)
```

### Agente (en cada server)
```bash
# Ver estado agente
docker compose ps

# Logs agente systemd
docker compose logs -f agente

# Logs agente Alpine
docker compose logs -f agente-alpine

# Reiniciar agente
docker compose restart agente   # o agente-alpine

# Actualizar agente
git pull
docker compose build agente     # o agente-alpine
docker compose --profile agente up -d --force-recreate
```

---

## 8. Troubleshooting Común

### Agente no conecta al panel
```bash
# 1. Verificar que el agente responde localmente
curl http://localhost:8127/api/health

# 2. Verificar firewall (puerto 8127 abierto)
# En el server del agente:
sudo ufw allow 8127/tcp    # Ubuntu/Debian
sudo firewall-cmd --add-port=8127/tcp --permanent  # RHEL/Fedora

# 3. Verificar token coincide en .env de panel y agente
cat .env | grep LUMINA_TOKEN
```

### Agente detecta init system incorrecto
```bash
# Ver qué detecta
curl http://localhost:8127/api/servidor/init

# Forzar re-detección (reiniciar contenedor)
docker compose restart agente
```

### Permisos logs en Alpine/OpenRC
```bash
# Si logs salen "[sin permiso para leer /var/log/messages]"
# Opción A: Agente como root (ya es --privileged)
# Opción B: Configurar syslog en host Alpine
echo '$FileCreateMode 0644' >> /etc/rsyslog.conf
rc-service rsyslog restart
```

### Puerto 8127 ya en uso
```bash
# Cambiar puerto en .env del agente
echo "LUMINA_PORT=8128" >> .env
# Y actualizar URL en panel: http://IP:8128
```

---

## 9. Estructura Final Típica

```
HOMELAB
├── LAPTOP (Panel Central)          ← docker compose --profile panel up -d
│   └── http://192.168.1.10:8127
│
├── VPS DIGITALOCEAN (Agente)       ← docker compose --profile agente up -d
│   ├── bot-trading (systemd)
│   ├── bot-discord (systemd)
│   └── nginx (systemd)
│   └── http://1.2.3.4:8127
│
├── RASPBERRY PI (Agente Alpine)    ← docker compose --profile agente-alpine up -d
│   ├── home-assistant (OpenRC)
│   ├── pihole (OpenRC)
│   └── nginx (OpenRC)
│   └── http://192.168.1.50:8127
│
└── SERVER BACKUPS (Agente Void)    ← docker run ... (Runit)
    ├── borgmatic (runit)
    └── syncthing (runit)
    └── http://192.168.1.100:8127
```

---

## 10. Checklist de Verificación Final

- [ ] Panel central responde en `http://IP_PANEL:8127/api/health`
- [ ] UI carga en navegador: `http://IP_PANEL:8127/`
- [ ] Cada agente responde en `http://IP_AGENTE:8127/api/health`
- [ ] Cada agente reporta backend correcto (`/api/servidor/init`)
- [ ] Panel muestra 🟢 Conectado para todos los agentes (`/api/conexion`)
- [ ] Puedes ver servicios activos de cada agente (`/api/servidor/servicios`)
- [ ] Registras un bot/web en el panel y aparece en la vista Servicios
- [ ] Acciones (Iniciar/Detener/Reiniciar) funcionan desde la UI
- [ ] Logs se ven correctamente en la UI
- [ ] Backup de `data/lumina.db` programado

---

## Referencias Rápidas

| Documento | Qué cubre |
|-----------|-----------|
| [Despliegue Docker](../02%20-%20Desarrollo/Despliegue/Docker.md) | Detalles completos Docker, variables, healthchecks |
| [Despliegue Alpine](../02%20-%20Desarrollo/Despliegue%20Alpine.md) | Guía específica Alpine/OpenRC, servicio nativo |
| [Init System](../02%20-%20Desarrollo/Init%20System.md) | Cómo funciona la abstracción multi-init |
| [Arquitectura Backend](../02%20-%20Desarrollo/Arquitectura%20Backend.md) | Estructura de capas y patrones |