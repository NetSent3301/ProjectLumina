# 🛠️ Implementación — ProjectLumina

> Estado actual de la base del proyecto y qué queda pendiente.

---

## Estado

La **base inicial** funciona localmente y la **v0.1 está en construcción** (también local, sin esperar al servidor): la estructura definitiva `app/` ya está aplicada, la API REST con token funciona, hay tests automatizados y el dashboard consume datos reales. El despliegue en el servidor ([Servidor](../02%20-%20Desarrollo/Servidor.md)) será la fase posterior.

---

## Qué está hecho

- ✅ Repositorio **Git** inicializado (rama `main`).
- ✅ Entorno virtual (`.venv`) y dependencias: **FastAPI**, Uvicorn, pytest, httpx.
- ✅ **`lumina.py`** — backend mínimo.
  - ✅ Servidor que arranca.
  - ✅ Endpoint `GET /api/health` de verificación → [API](../02%20-%20Desarrollo/API.md).
  - ✅ Sirve el panel en `/` con cambio de vista sin recargar (hash `#/resumen`, `#/servicios`); `/servicios` redirige a `/#/servicios`.
  - ✅ Archivos estáticos montados en `/static` (`StaticFiles`) → [Decisiones](Decisiones.md) · [Errores](Errores.md).
- ✅ **Frontend reorganizado**: `web/templates/` + `web/static/` (css, js, assets).
- ✅ **Dashboard en maqueta** con estados vacíos (sin datos falsos) → [Dashboard](../02%20-%20Desarrollo/Dashboard.md) · [UI - Sistema de Diseno](../02%20-%20Desarrollo/UI%20-%20Sistema%20de%20Diseno.md):
  - ✅ Una sola página con vistas **resumen** (`/`) y **servicios** (`/#/servicios`), sin recargas.
  - ✅ Vista servicios con selector bots/webs (pestañas 🤖/🌐) → [Bots](../02%20-%20Desarrollo/Bots.md) · [Webs](../02%20-%20Desarrollo/Webs.md).
  - ✅ Cabecera de estado y tarjetas vacías con chip "disponible en v0.1".
  - ✅ Registro de actividad con estado vacío (solo en resumen).
  - ✅ Micro-animaciones (entrada escalonada, hover, flotación, registro) y respeto de `prefers-reduced-motion` → [Frontend](../02%20-%20Desarrollo/Frontend.md).
- ✅ Script de arranque `scripts/run.sh` → arranca `app.main:app` respetando `LUMINA_HOST` / `LUMINA_PORT`.
- ✅ Tests con pytest → [Dashboard](../02%20-%20Desarrollo/Dashboard.md).
- ✅ Backend con **FastAPI** → [Decisiones](Decisiones.md).
- ✅ **Requisitos técnicos cerrados**: stack definitivo, esquema de endpoints y modelo de datos → [Requisitos](../01%20-%20Planificacion/Requisitos.md) · [API](../02%20-%20Desarrollo/API.md) · [Base de Datos](../02%20-%20Desarrollo/Base%20de%20Datos.md) · [Decisiones](Decisiones.md).
- ✅ **Arquitectura definitiva del MVP** (capa `app/`, flujo de acciones y despliegue systemd) → [Arquitectura definitiva del MVP](../01%20-%20Planificacion/Arquitectura.md).

## 🟡 v0.1 en construcción (local)

- ✅ **Estructura `app/` aplicada** → [Arquitectura](../01%20-%20Planificacion/Arquitectura.md):
  - ✅ `app/config.py` (pydantic-settings, prefijo `LUMINA_`), `app/db.py` (SQLite + SQLModel, tabla `servicios`).
  - ✅ `app/models/servicio.py` (modelo `Servicio` + esquemas).
  - ✅ `app/system/` — única capa que toca el SO: `systemd.py` (`systemctl`/`journalctl`, errores clasificados) y `metricas.py` (psutil).
  - ✅ `app/services/` — negocio: servicios (listado, CRUD, acciones, logs, estado en vivo) y servidor (métricas, procesos, unidades activas).
  - ✅ `app/api/` — `require_token` (X-API-Key / Bearer) y routers `servicios` + `servidor`.
  - ✅ `app/main.py` — `/`, `/index.html`, `/servicios` (atajo), `/static`, `/api/health` y API bajo `/api`. `lumina.py` es ahora un atajo de `app.main`.
- ✅ **API REST funcional** (con token cuando `LUMINA_TOKEN` está definido) → [API](../02%20-%20Desarrollo/API.md) · [Autenticacion](../03%20-%20Seguridad/Autenticacion.md).
- ✅ **Base de datos**: tabla `servicios` creada con `init_db()` → [Base de Datos](../02%20-%20Desarrollo/Base%20de%20Datos.md).
- ✅ **Dashboard conectado a la API**: `script.js` carga `GET /api/servicios`, render tarjetas reales con estado en vivo y botones iniciar/detener/reiniciar/logs → [Dashboard](../02%20-%20Desarrollo/Dashboard.md).
- ✅ **Tests automatizados (6)** → `pruebas/conftest.py` (BD temporal + token de test), `test_api.py`, `test_health.py`.

---

## Cómo ejecutarlo

```bash
bash scripts/run.sh
```

- Web: http://127.0.0.1:8000/
- API de prueba: http://127.0.0.1:8000/api/health
- Documentación interactiva: http://127.0.0.1:8000/docs

Para probar la API con token: `LUMINA_TOKEN=clave bash scripts/run.sh` (desde el navegador o `curl -H "X-API-Key: clave"`).

---

## Pendiente (resto de [v0.1](../05%20-%20Versiones/v0.1.md))

> Sigue siendo desarrollo local; el despliegue real espera el servidor Debian 13 → [Servidor](../02%20-%20Desarrollo/Servidor.md).

- ❌ Interfaz para **registrar servicios** (formulario; hoy solo hay CRUD por API y el botón "añadir servicio" avisa que llega).
- ❌ Vista **servidor** (métricas CPU/RAM/disco/red, procesos, unidades activas) en el dashboard → [Servidor](../02%20-%20Desarrollo/Servidor.md).
- ❌ Gestión real de bots/webs contra systemd (las acciones del API están listas; falta validarlas con unidades reales en el servidor) → [Bots](../02%20-%20Desarrollo/Bots.md) · [Webs](../02%20-%20Desarrollo/Webs.md) · [Acciones de Bots](../02%20-%20Desarrollo/Acciones%20de%20Bots.md).
- ❌ Despliegue: servicio systemd `lumina.service` + HTTPS/token si se expone → [Arquitectura](../01%20-%20Planificacion/Arquitectura.md).
- ❌ UI de **edición y desregistro** de servicios en el panel (el API ya expone `PATCH`/`DELETE`).

---

## Relacionado

- [Estado Actual](../00%20-%20Inicio/Estado%20Actual.md) · En qué fase estamos.
- [v0.1](../05%20-%20Versiones/v0.1.md) · Próximo entregable.
- [Decisiones](Decisiones.md) · Por qué FastAPI y cómo se sirven los estáticos.
- [Changelog](Changelog.md) · Registro de cambios recientes.
- [UI - Sistema de Diseno](../02%20-%20Desarrollo/UI%20-%20Sistema%20de%20Diseno.md) · Identidad visual del dashboard.
- [Git y GitHub](../02%20-%20Desarrollo/Git%20y%20GitHub.md) · Control de versiones.
- [Inicio](../00%20-%20Inicio/Inicio.md)
