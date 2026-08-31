# Backend — ProjectLumina

## Tecnologías

- **Python.**
- **FastAPI** (elegido).

> La elección Flask vs FastAPI se resolvió a favor de **FastAPI** → [decisiones (obsidian)](../obsidian/06%20-%20Registro/Decisiones.md).

## Estado de la implementación

La base del backend ya está montada en `lumina.py` (un único archivo):

- ✅ Servidor FastAPI arrancable.
- ✅ Endpoint `GET /api/health` de verificación.
- ✅ Sirve la página `web/templates/index.html` en la raíz `/` (una sola página, vistas por hash).

Pendiente (cuando se tenga acceso al servidor):

- ❌ Gestión real de bots y webs (iniciar/detener/reiniciar/estados).
- ❌ Métricas del servidor (CPU/RAM/disco/red).
- ❌ Base de datos y modelos.
- ❌ Seguridad y exposición a Internet.

> Cómo arrancarlo: `bash scripts/run.sh`

## Responsabilidades

- Recibir solicitudes del frontend.
- Consultar el estado del servidor.
- Gestionar bots.
- Gestionar webs.
- Gestionar servicios.
- Ejecutar acciones administrativas.
- Devolver resultados al frontend.
- Gestionar configuraciones.
- Mantener separada la lógica de administración de la interfaz.

## Comunicación

- API REST → [api.md](api.md).
- WebSockets a futuro para tiempo real.

## Almacenamiento

- SQLite → [base-de-datos.md](base-de-datos.md).

## Interacción con el sistema

- Servicios vía systemd → [servidor.md](servidor.md).
- Acciones administrativas → [control-remoto.md](control-remoto.md).
- Monitorización → [dashboard.md](dashboard.md).

## Posibles módulos

Según la estructura propuesta en [arquitectura](../arquitectura.md):

- `app/api/` — endpoints.
- `app/services/` — lógica de bots y webs.
- `app/models/` — modelos de datos.
- `app/system/` — interacción con el sistema.
- `app/config/` — configuración.

---

Volver a [desarrollo](README.md).
