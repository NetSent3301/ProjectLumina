# Backend — ProjectLumina

## Tecnologías propuestas

- **Python.**
- **Flask** o **FastAPI.**

> La elección final entre Flask y FastAPI se hará al comenzar la implementación.

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
