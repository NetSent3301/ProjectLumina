# 🔔 Sistema de Notificaciones de Actualización — ProjectLumina

> Chequea automáticamente **GitHub Releases** y muestra una notificación push en el dashboard cuando hay una nueva versión disponible.

---

## Cómo funciona

```
┌─────────────────────────────────────────────────────────────────┐
│                      ProjectLumina (Panel/Agente)               │
│                                                                 │
│  ┌──────────────┐    Cada 6h (configurable)    ┌────────────┐  │
│  │ Background   │ ───────────────────────────► │ GitHub API │  │
│  │ Task         │   GET /repos/{owner}/{repo}  │  Releases  │  │
│  └──────────────┘    /releases/latest          └────────────┘  │
│        │                                                 │       │
│        ▼                                                 ▼       │
│  Compara versiones                                    │       │
│  (semver: v0.1.1 < v0.2.0)                            │       │
│        │                                                 │       │
│        ▼                                                 │       │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Cache en memoria + Persistencia en data/            │  │
│  │ update_state.json                                    │  │
│  └─────────────────────────────────────────────────────┘  │
│        │                                                 │       │
│        ▼                                                 │       │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Frontend: Polling cada 30 min + Notificación push   │  │
│  │ Toast en esquina inferior derecha                   │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Configuración

### Variables de entorno (`.env`)

```bash
# GitHub repository (owner/repo)
LUMINA_GITHUB_REPO=netsent/ProjectLumina

# Opcional: GitHub Personal Access Token (clásico)
# Necesario para evitar rate limit (60 req/h sin token → 5000 req/h con token)
# Crear en: GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
# Permisos: public_repo (para repos públicos) o repo (para privados)
LUMINA_GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Intervalo de chequeo en horas (default: 6)
LUMINA_UPDATE_CHECK_INTERVAL_HOURS=6

# Activar/desactivar notificaciones (default: true)
LUMINA_UPDATE_NOTIFY_ENABLED=true
```

### Ejemplo completo `.env`

```bash
LUMINA_TOKEN=a1b2c3d4e5f6...
LUMINA_PORT=8127
LUMINA_DEBUG=false

# Actualizaciones
LUMINA_GITHUB_REPO=tu-usuario/tu-repo
LUMINA_GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
LUMINA_UPDATE_CHECK_INTERVAL_HOURS=6
LUMINA_UPDATE_NOTIFY_ENABLED=true
```

---

## Endpoints API

| Endpoint | Método | Auth | Descripción |
|----------|--------|------|-------------|
| `/api/update` | GET | No | Info de actualización actual |
| `/api/update?forzar=true` | GET | No | Fuerza chequeo inmediato |
| `/api/update/dismiss` | POST | Sí | Descartar notificación N horas |
| `/api/update/check` | POST | Sí | Fuerza chequeo y retorna resultado |

### Respuesta `GET /api/update`

```json
{
  "hay_actualizacion": true,
  "version_actual": "0.1.1",
  "version_nueva": "0.2.0",
  "release_url": "https://github.com/netsent/ProjectLumina/releases/tag/v0.2.0",
  "release_notes": "## What's Changed\n- Nueva feature X\n- Fix bug Y\n",
  "publicado_en": "2026-01-15T10:30:00Z",
  "ultimo_chequeo": "2026-01-15T10:30:05Z",
  "proximo_chequeo": "2026-01-15T16:30:05Z"
}
```

---

## Frontend: Notificación Push

Aparece como **toast** en la esquina inferior derecha:

```
┌──────────────────────────────────────────────────────┐
│ 🔔  Nueva versión disponible: v0.2.0                 │
│     Estás en v0.1.1. Ver cambios en GitHub ▸         │
│     ▼ Notas de la versión                            │
│     ┌────────────────────────────────────────────┐  │
│     │ ## What's Changed                          │  │
│     │ - Nueva feature X                          │  │
│     │ - Fix bug Y                                │  │
│     └────────────────────────────────────────────┘  │
│     [✕ No avisar 24h]    [Actualizar ahora]        │
└──────────────────────────────────────────────────────┘
```

### Comportamiento

- **Auto-desaparición**: Se desvanece a los 30s si no se interactúa
- **Dismiss 24h**: Botón ✕ guarda en `localStorage` + notifica al backend
- **Persistencia**: El dismiss sobrevive a recargas de página
- **Re-activación**: Tras 24h vuelve a chequear automáticamente
- **Responsive**: En móvil ocupa ancho completo con botones apilados

---

## Flujo de actualización típico

```bash
# 1. Usuario hace release en GitHub
git tag v0.2.0
git push origin v0.2.0
# Crear release en GitHub UI o via CLI

# 2. En ≤6 horas (o 30 min en frontend), ProjectLumina detecta
# 3. Dashboard muestra notificación push
# 4. Usuario click "Actualizar ahora" → fuerza chequeo inmediato
# 5. Usuario actualiza su deployment:
```

### Actualizar con Docker Compose

```bash
# En cada máquina (panel y agentes)
cd /opt/lumina
git pull
docker compose build
docker compose --profile panel up -d --force-recreate     # Panel
docker compose --profile agente up -d --force-recreate    # Agente systemd
docker compose --profile agente-alpine up -d --force-recreate  # Agente Alpine
```

### Actualizar en metal (systemd/OpenRC)

```bash
cd /opt/lumina
git pull
source .venv/bin/activate
pip install -r requirements.txt
# Reiniciar servicio
sudo systemctl restart lumina        # systemd
sudo rc-service lumina restart       # OpenRC
```

---

## Detalles técnicos

### Comparación de versiones (semver simple)

```python
def _comparar_versiones(actual: str, nueva: str) -> bool:
    # "0.1.1" < "0.2.0" → True
    # "0.1.1" < "0.1.1" → False
    # "1.0.0" < "0.9.9" → False
    # Ignora prerelease: "1.0.0-beta" → (1,0,0)
```

### Fallback a tags

Si no hay **GitHub Releases** formales, busca **tags semver** (`vX.Y.Z` o `X.Y.Z`):
- Útil para repos que solo usan tags sin release notes
- Obtiene fecha del tag via GitHub Git API

### Rate limiting GitHub

| Sin token | Con token (PAT clásico) |
|-----------|------------------------|
| 60 req/h por IP | 5000 req/h por token |

> **Recomendado**: Configurar `LUMINA_GITHUB_TOKEN` en producción.

### Persistencia

Archivo: `data/update_state.json`

```json
{
  "ultima_version_vista": "0.2.0",
  "ultima_notificacion": "2026-01-15T10:30:05Z",
  "dismiss_hasta": "2026-01-16T10:30:05Z"
}
```

- `dismiss_hasta`: Hasta cuándo no molestar (24h por defecto)
- Sobrevive a reinicios del contenedor/servicio

---

## Troubleshooting

### "No hay actualización" pero sí hay release en GitHub

1. Verificar `LUMINA_GITHUB_REPO` (formato: `owner/repo`)
2. Verificar que el release **no sea draft** ni **prerelease**
3. Verificar tag semver: `v0.2.0` o `0.2.0`
4. Forzar chequeo: `curl -X POST /api/update/check -H "X-API-Key: token"`

### Rate limit 403

```bash
# Configurar token
echo "LUMINA_GITHUB_TOKEN=ghp_xxx" >> .env
docker compose restart panel
```

### Notificación no aparece

1. Verificar `LUMINA_UPDATE_NOTIFY_ENABLED=true`
2. Verificar consola del navegador (F12) → Network → `/api/update`
3. Verificar `localStorage.getItem('lumina_update_dismissed')`
4. Forzar chequeo manual en consola: `chequearActualizacion(true)`

### Logs del backend

```bash
docker compose logs -f panel | grep -i update
# O en metal:
journalctl -u lumina -f | grep -i update
```

---

## Referencias

- [Configuración](../Configuracion.md) — Variables de entorno
- [Despliegue Docker](../Despliegue/Docker.md) — Actualizar contenedores
- [app/api/update.py](../../app/api/update.py) — Implementación backend
- [app/services/update_background.py](../../app/services/update_background.py) — Tarea background
- [web/static/js/script.js](../../web/static/js/script.js) — Frontend notifications