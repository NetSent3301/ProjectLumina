# ⚙️ Capa de Abstracción del Init System — ProjectLumina

> Diseño, implementación y uso de la capa `app/system/` que permite a ProjectLumina
> funcionar en **systemd, OpenRC, Runit y SysV** sin cambios en el resto del código.

---

## Problema que resuelve

ProjectLumina necesita:
- Consultar estado de servicios (`is_active`)
- Iniciar/detener/reiniciar servicios
- Leer logs de servicios
- Listar servicios activos

Cada init system tiene **comandos, formatos de salida y convenciones de nombres diferentes**.
Sin abstracción, el código estaría lleno de `if systemd: ... elif openrc: ...`.

---

## Solución: Patrón Strategy + Factory + Singleton

```
┌─────────────────────────────────────────────────────────────┐
│                      detector.py                            │
│  get_backend() → InitBackend (singleton cacheado)          │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       ┌────────────┐  ┌────────────┐  ┌────────────┐
       │ SystemdBackend│ │OpenRCBackend│ │ RunitBackend│
       └────────────┘  └────────────┘  └────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                    ┌─────────────────────┐
                    │   InitBackend (ABC) │
                    │  (app/system/base.py)│
                    └─────────────────────┘
```

---

## Contrato: `InitBackend` (`app/system/base.py`)

```python
class InitBackend(ABC):
    @abstractmethod
    def nombre(self) -> str: ...
    @abstractmethod
    def disponible(self) -> bool: ...
    @abstractmethod
    def info(self) -> dict: ...
    @abstractmethod
    def is_active(self, nombre: str) -> bool: ...
    @abstractmethod
    def iniciar(self, nombre: str) -> None: ...
    @abstractmethod
    def detener(self, nombre: str) -> None: ...
    @abstractmethod
    def reiniciar(self, nombre: str) -> None: ...
    @abstractmethod
    def log_lines(self, nombre: str, lines: int = 100) -> str: ...
    @abstractmethod
    def servicios_activos(self) -> list[dict]: ...
```

### `InitError` — Excepción unificada

```python
class InitError(RuntimeError):
    def __init__(self, mensaje: str, *, no_existe: bool = False):
        self.mensaje = mensaje
        self.no_existe = no_existe  # True → HTTP 404; False → HTTP 502
```

Todos los backends lanzan `InitError` (o subclases). La capa de servicios la atrapa y mapea a códigos HTTP.

---

## Detector (`app/system/detector.py`)

```python
_BACKENDS_ORDENADOS = [
    SystemdBackend(),  # 1. systemctl en PATH
    OpenRCBackend(),   # 2. rc-service en PATH
    RunitBackend(),    # 3. sv en PATH
    SysVBackend(),     # 4. service o /etc/init.d
]

def get_backend() -> InitBackend:
    global _backend_cache
    if _backend_cache is None:
        _backend_cache = detectar()  # Primera llamada: detecta
    return _backend_cache
```

- **Orden de prioridad**: systemd → OpenRC → Runit → SysV
- **Singleton cacheado**: Se detecta una vez, se reusa siempre
- **`resetear_cache()`**: Solo para tests (fuerza re-detección)

---

## Backend: systemd (`app/system/systemd.py`)

| Operación | Comando |
|-----------|---------|
| Disponible | `shutil.which("systemctl")` |
| Estado | `systemctl is-active <unidad>` → exit 0 + "active" |
| Iniciar | `systemctl start <unidad>` |
| Detener | `systemctl stop <unidad>` |
| Reiniciar | `systemctl restart <unidad>` |
| Logs | `journalctl -u <unidad> -n <lines> --no-pager` |
| Lista | `systemctl list-units --type=service --state=running --no-legend` |

**Convención de nombres**: Con sufijo `.service` (`nginx.service`)

**Info expuesta**: `{"backend": "systemd", "version": "255", "pid1": "systemd"}`

---

## Backend: OpenRC (`app/system/openrc.py`)

| Operación | Comando |
|-----------|---------|
| Disponible | `shutil.which("rc-service")` |
| Estado | `rc-service <nombre> status` → exit 0 |
| Iniciar | `rc-service <nombre> start` |
| Detener | `rc-service <nombre> stop` |
| Reiniciar | `rc-service <nombre> restart` |
| Logs | 1) `/var/log/<nombre>/current` (svlogd) 2) Syslog filtrado |
| Lista | `rc-status --all --nocolor` → parsea `* nombre [ started ]` |

**Convención de nombres**: **Sin sufijo** (`nginx`, `sshd`, `crond`)

**Info expuesta**: `{"backend": "openrc", "version": "0.54.2", "pid1": "openrc-init"}`

**Rutas syslog probadas**:
1. `/var/log/messages` (Alpine/busybox)
2. `/var/log/syslog` (Gentoo/syslog-ng)
3. `/var/log/everything/everything.log` (metalog)

---

## Backend: Runit (`app/system/runit.py`)

| Operación | Comando |
|-----------|---------|
| Disponible | `shutil.which("sv")` |
| Estado | `sv status <nombre>` |
| Iniciar | `sv start <nombre>` |
| Detener | `sv stop <nombre>` |
| Reiniciar | `sv restart <nombre>` |
| Logs | `/var/log/<nombre>/current` (svlogd nativo) |
| Lista | `sv status /var/service/*` |

**Convención de nombres**: Directorio en `/var/service/<nombre>`

---

## Backend: SysV (`app/system/sysv.py`) — Experimental

| Operación | Comando |
|-----------|---------|
| Disponible | `shutil.which("service")` o `/etc/init.d/` existe |
| Estado | `service <nombre> status` |
| Iniciar | `service <nombre> start` |
| Detener | `service <nombre> stop` |
| Reiniciar | `service <nombre> restart` |
| Logs | Syslog filtrado (igual que OpenRC) |
| Lista | `service --status-all` → parsea salida variable |

**Marcado**: `"experimental": true` en `info()`

---

## Uso en el código

### En API/Services (patrón recomendado)

```python
from app.system import get_backend, InitError

def servicios_activos():
    backend = get_backend()  # Singleton cacheado
    try:
        return backend.servicios_activos()
    except InitError as e:
        raise HTTPException(502, detail=e.mensaje)
```

### En endpoints de diagnóstico

```python
@router.get("/servidor/init")
def info_init():
    backend = get_backend()
    return backend.info()  # {"backend": "openrc", "version": "...", "pid1": "..."}
```

### Para forzar re-detección (solo tests)

```python
from app.system.detector import resetear_cache
resetear_cache()
backend = get_backend()  # Re-detecta
```

---

## Añadir un nuevo init system

1. Crear `app/system/nuevo.py` implementando `InitBackend`
2. Importar en `app/system/detector.py`
3. Añadir a `_BACKENDS_ORDENADOS` en la posición de prioridad deseada
4. Tests en `pruebas/test_init_detector.py`

---

## Testing

```bash
# Verificar detección actual
python3 -c "from app.system import get_backend; b=get_backend(); print(b.nombre(), b.info())"

# Tests unitarios (mockean backends)
pytest pruebas/test_init_detector.py -v
```

---

## Referencias

- [Arquitectura Backend](../02%20-%20Desarrollo/Arquitectura%20Backend.md) — Visión general de capas
- [Despliegue Alpine](../02%20-%20Desarrollo/Despliegue%20Alpine.md) — Guía Alpine/OpenRC
- [Despliegue Docker](../02%20-%20Desarrollo/Despliegue/Docker.md) — Perfiles docker-compose
- [app/system/base.py](../../app/system/base.py) — Contrato abstracto
- [app/system/detector.py](../../app/system/detector.py) — Factory + Singleton
- [app/system/openrc.py](../../app/system/openrc.py) — Implementación OpenRC completa