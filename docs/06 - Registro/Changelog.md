# 📒 Changelog — ProjectLumina

> Registro de cambios del proyecto, orden cronológico (lo más reciente arriba).

---

## [v0.1.0-dev] - 2026-08-30

### Añadido
- **UX/UI del dashboard mejorado**:
  - **Métricas rápidas en Resumen**: tarjetas de CPU, RAM, servicios (activos/totales) y uptime desde `GET /api/servidor`, con barras de uso (color según carga) y refresco cada 10 s mientras la vista está activa.
  - **Skeleton loaders**: tarjetas animadas mientras conecta con el backend (antes de mostrar los estados vacíos).
  - **Terminal de logs en la vista Registro**: visor con fondo negro, fuente JetBrains Mono, barra de terminal, selector de servicio con unidad systemd, botones recargar/live (cola cada 4 s) y resaltado de sintaxis (marcas de tiempo, niveles, IPs, URLs).
  - **Legibilidad**: textos secundarios más claros, títulos de sección y navegación en mayúsculas con tracking.
  - **Consistencia**: botones primarios con mayor peso tipográfico, estados vacíos con bordes suaves y fondos `navy`.
- **"Conectar un servicio" funcional**: modal con formulario (tipo bot/web, nombre, unidad systemd, comando, ruta, check HTTP, auto-inicio/reinicio) que registra vía `POST /api/servicios` y refresca el panel al instante. Se abre desde las tarjetas vacías y los botones "+ añadir servicio".
- **Cambio de orientación**: ProjectLumina pasa a **gestionar la máquina donde corre** (sistema, servicios systemd, bots y webs), funcional de forma local. El acceso remoto (iPhone/otros dispositivos) queda como **fase posterior** → [Estado Actual](../00%20-%20Inicio/Estado%20Actual.md).
- **Estructura definitiva `app/` aplicada** (backend en capas) → [Arquitectura](../01%20-%20Planificacion/Arquitectura.md):
  - `app/config.py` — configuración con pydantic-settings (prefijo `LUMINA_`, desde `.env`).
  - `app/db.py` — motor SQLite + SQLModel + `init_db()` (tabla `servicios`).
  - `app/models/servicio.py` — modelo `Servicio` y esquemas `ServicioCreate`/`ServicioUpdate`.
  - `app/system/systemd.py` — capa que toca el SO (`systemctl`/`journalctl`) con degradación controlada (unidad inexistente → `SystemdError.no_existe`).
  - `app/system/metricas.py` — psutil (CPU, RAM, disco, red, uptime, procesos).
  - `app/services/` — lógica de negocio (servicios + servidor; estado en vivo: systemd y check HTTP con httpx).
  - `app/api/` — `require_token` (X-API-Key / Bearer) + routers de `servicios` y `servidor` → [API](../02%20-%20Desarrollo/API.md) · [Seguridad](../03%20-%20Seguridad/Seguridad.md).
  - `app/main.py` — aplicación: `/`, `/index.html`, `/servicios` (atajo), `/static`, `/api/health`, API en `/api`.
- `lumina.py` pasa a ser un **atalajo** de `app.main` (sigue funcionando `uvicorn lumina:app`) → [Backend](../02%20-%20Desarrollo/Backend.md).
- `scripts/run.sh` arranca ahora `app.main:app` respetando `LUMINA_HOST` / `LUMINA_PORT`.
- **Dashboard conectado a la API real** → [Frontend](../02%20-%20Desarrollo/Frontend.md):
  - `loadServicios()` con `GET /api/servicios` y render de tarjetas reales (estado en vivo, botones iniciar/detener/reiniciar/logs).
  - Botones de acción con `POST /api/servicios/{id}/...` y revisión de logs con `GET /api/servicios/{id}/logs` (volcado en el registro de actividad).
  - Contadores de pestañas y subtítulos con números reales; estados vacíos **honestos** si la API falla o no hay servicios.
  - CSS: recuadro de logs `.log-pre` y botones deshabilitados durante operaciones.
- **Tests v0.1** (pytest, 6 passed) → [Implementacion](Implementacion.md):
  - `pruebas/conftest.py` — base de datos temporal + `LUMINA_TOKEN=tokentest` (no toca `data/lumina.db`).
  - `pruebas/test_api.py` — auth (401 sin token), CRUD, acciones y logs.
  - `pruebas/test_health.py` — health, frontend, estáticos y atajos.
- **Hardware del servidor documentado**: [Dell Inspiron (2010)](../02%20-%20Desarrollo/Servidor.md), renovación prevista.

### Cambiado
- Estado del proyecto: **desarrollo v0.1 en curso (local)**, sin esperar al servidor → [Estado Actual](../00%20-%20Inicio/Estado%20Actual.md).

### Corregido
- CSS y JS del dashboard no cargaban (404) → [Errores](Errores.md).
- Datos de ejemplo proyectados en la UI → [Errores](Errores.md).

---

## [No publicado]

### Añadido
- Documentación inicial del proyecto en Obsidian (mapa completo).
- Documento de planificación general → [Inicio](../00%20-%20Inicio/Inicio.md).
- **Base inicial del proyecto** montada y funcional → [Implementacion](Implementacion.md).
  - Repositorio Git inicializado.
  - Backend mínimo con **FastAPI** (`lumina.py`): endpoint `/api/health` y página web en `/`.
  - Frontend mínimo (`web/index.html`), script de arranque `scripts/run.sh`, test básico.
- Decisión técnica **FastAPI** → [Decisiones](Decisiones.md).

---

## Formato

Para añadir una entrada usa este formato, lo más reciente arriba:

```text
## [Versión] - [Fecha]
### Añadido
- ...
### Cambiado
- ...
### Corregido
- ...
### Eliminado
- ...
```

---

## Relacionado

- [Roadmap](../01%20-%20Planificacion/Roadmap.md) · Versiones planificadas.
- [Decisiones](Decisiones.md) · Cambios con contexto.
- [Errores](Errores.md) · Problemas resueltos.
- [Git y GitHub](../02%20-%20Desarrollo/Git%20y%20GitHub.md) · Control de versiones.
- [Inicio](../00%20-%20Inicio/Inicio.md)
