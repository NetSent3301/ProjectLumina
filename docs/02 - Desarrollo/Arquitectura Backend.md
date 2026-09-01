# 🏗️ Arquitectura del Backend — ProjectLumina

> Estructura en capas del backend (v0.1+). Diseñada para ser portable, testeable y desacoplada del init system.

---

## Estructura de directorios

```
app/
├── main.py                 # Factory de FastAPI, montaje de routers y estáticos
├── config.py               # Settings con pydantic-settings (prefijo LUMINA_)
├── db.py                   # Inicialización SQLite + SQLModel
├── lumina.py               # Re-exporta app.main:app para uvicorn
├── api/                    # Capa HTTP (routers, auth, validación)
│   ├── __init__.py
│   ├── auth.py             # require_token dependency
│   ├── servidor.py         # GET /servidor, /procesos, /servicios, /init
│   ├── servicios.py        # CRUD + acciones + logs de servicios registrados
│   └── servidores.py       # CRUD agentes remotos + /conexion
├── services/               # Capa de lógica de negocio
│   ├── __init__.py
│   ├── servidor.py         # Métricas (psutil) + lista servicios activos
│   ├── servicios.py        # Gestión de bots/webs registrados en BD
│   └── servidores.py       # Gestión agentes remotos + healthchecks
├── models/                 # Modelos Pydantic/SQLModel
│   ├── __init__.py
│   ├── servidor.py         # ServidorCreate (agentes remotos)
│   └── servicio.py         # ServicioCreate/Update (bots/webs)
└── system/                 # Capa de abstracción del init system
    ├── __init__.py
    ├── base.py             # InitBackend (ABC) + InitError
    ├── detector.py         # Auto-detección + singleton cacheado
    ├── systemd.py          # Backend systemd (systemctl/journalctl)
    ├── openrc.py           # Backend OpenRC (rc-service/rc-status/syslog)
    ├── runit.py            # Backend Runit (sv/svlogd)
    ├── sysv.py             # Backend SysV (service/init.d) — experimental
    └── metricas.py         # Métricas de sistema vía psutil
```

---

## Flujo de una petición

```
HTTP Request
     │
     ▼
┌─────────────────────────────────────┐
│  API Router (auth → validación)     │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  Service Layer (lógica de negocio)  │
│  - servicios.crear/listar/accion    │
│  - servidor.resumen/servicios_activos│
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  System Layer (init system)         │
│  get_backend() → InitBackend        │
│  - systemd / openrc / runit / sysv  │
└─────────────────────────────────────┘
     │
     ▼
  Host OS (systemd, OpenRC, Runit, SysV)
```

---

## Capa System: Abstracción del Init System

### Contrato: `InitBackend` (`app/system/base.py`)

Interfaz que **todos** los backends deben implementar:

| Método | Propósito |
|--------|-----------|
| `nombre()` | Identificador corto: `"systemd"`, `"openrc"`, `"runit"`, `"sysv"` |
| `disponible()` | `True` si el binario principal está en PATH |
| `info()` | Metadatos para `GET /api/servidor/init` |
| `is_active(nombre)` | ¿Está corriendo el servicio? (no lanza, devuelve `False`) |
| `iniciar/detener/reiniciar(nombre)` | Acciones; lanzan `InitError(no_existe=True)` si no existe |
| `log_lines(nombre, lines)` | Últimas líneas de log |
| `servicios_activos()` | Lista de servicios corriendo |

### Excepción unificada: `InitError`

```python
class InitError(RuntimeError):
    def __init__(self, mensaje: str, *, no_existe: bool = False):
        self.mensaje = mensaje
        self.no_existe = no_existe  # → HTTP 404 en capa de servicios
```

### Detector (`app/system/detector.py`)

```python
_BACKENDS_ORDENADOS = [
    SystemdBackend(),  # 1. systemctl existe
    OpenRCBackend(),   # 2. rc-service existe
    RunitBackend(),    # 3. sv existe
    SysVBackend(),     # 4. service o /etc/init.d existe
]
```

- **Singleton cacheado**: `get_backend()` detecta una vez y reusa
- **`resetear_cache()`**: Solo para tests
- Lanza `RuntimeError` si ningún backend está disponible

---

## Backends implementados

### systemd (`app/system/systemd.py`)

- Binarios: `systemctl`, `journalctl`
- `is_active`: `systemctl is-active <unidad>` → exit 0 + "active"
- Logs: `journalctl -u <unidad> -n <lines> --no-pager`
- Lista: `systemctl list-units --type=service --state=running --no-legend`
- Nombres de unidad: con sufijo (`.service`)

### OpenRC (`app/system/openrc.py`)

- Binarios: `rc-service`, `rc-status`
- **Compatible**: Alpine Linux, Gentoo, Artix (OpenRC)
- `is_active`: `rc-service <nombre> status` → exit 0
- Logs: Prioridad 1) `/var/log/<nombre>/current` (svlogd), 2) syslog filtrado
- Lista: `rc-status --all --nocolor` → parsea líneas `* nombre [ started ]`
- Nombres de servicio: **sin sufijo** (`"nginx"`, `"sshd"`)
- Rutas syslog probadas: `/var/log/messages`, `/var/log/syslog`, `/var/log/everything/everything.log`

### Runit (`app/system/runit.py`)

- Binario: `sv`
- Compatible: Void Linux, Artix (runit)
- Logs: `/var/log/<nombre>/current` (svlogd nativo)

### SysV (`app/system/sysv.py`)

- Binario: `service` o scripts en `/etc/init.d/`
- **Experimental**: Solo como fallback legacy
- Marcado con `"experimental": true` en `info()`

---

## Capa Services: Lógica de Negocio

### `servidor.py` — Métricas y servicios del host

```python
def servicios_activos() -> list[dict]:
    backend = get_backend()
    try:
        return backend.servicios_activos()
    except InitError as error:
        raise HTTPException(status_code=502, detail=error.mensaje)
```

- Delega en `metricas.sistema()` (psutil) para CPU/RAM/disco/red/uptime
- Delega en `get_backend()` para listar servicios del init system
- Convierte `InitError` → HTTP 502 (Bad Gateway)

### `servicios.py` — Bots y Webs registrados en BD

- CRUD completo + acciones (iniciar/detener/reiniciar) + logs
- Valida que el servicio exista en el init system antes de actuar
- Usa `get_backend()` para ejecutar acciones reales

### `servidores.py` — Agentes remotos

- Registra agentes Lumina en otras máquinas
- Healthcheck cada 15s → `GET /api/health`
- Endpoint `GET /api/conexion` → resumen global (principal + remotos)

---

## Configuración (`app/config.py`)

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_prefix="LUMINA_",
        extra="ignore",
    )
    host: str = "127.0.0.1"
    port: int = 8000
    token: str = ""           # Vacío = sin auth (solo dev/local)
    db: str = "data/lumina.db"
    logs: str = "logs"
    debug: bool = False
```

Variables de entorno (prefijo `LUMINA_`):
- `LUMINA_HOST`, `LUMINA_PORT`, `LUMINA_TOKEN`, `LUMINA_DB`, `LUMINA_DEBUG`

---

## Base de Datos (`app/db.py`)

- **SQLite** + **SQLModel** (SQLAlchemy + Pydantic)
- Tablas: `servicio` (bots/webs), `servidor` (agentes remotos)
- `init_db()` crea tablas al arrancar (idempotente)

---

## Testing

```bash
pytest pruebas/
```

- `conftest.py`: Fixtures + `resetear_cache()` entre tests
- `test_init_detector.py`: Verifica detección y prioridad de backends
- `test_api.py`: Endpoints con `TestClient` + mocks
- `test_health.py`: Healthcheck básico

---

## Principios de diseño

1. **Una sola responsabilidad por capa**: API → Services → System
2. **Inversión de dependencias**: API/Services dependen de abstracciones (`InitBackend`), no de concreciones
3. **Auto-detección**: Cero configuración manual del init system
4. **Fail-fast con mensajes claros**: `InitError` con `no_existe` para HTTP 404 vs 502
5. **Portabilidad**: Funciona en Debian, Alpine, Void, Gentoo, RHEL, etc.
6. **Cacheo inteligente**: Detector singleton; backend sin estado