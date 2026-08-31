# ⚖️ Decisiones — ProjectLumina

> Registro de decisiones técnicas tomadas y sus motivos.

---

## Cómo registrar

```text
## [Fecha] - Decisión breve

- **Contexto:** ...
- **Opciones consideradas:** ...
- **Decisión:** ...
- **Motivo:** ...
- **Alternativas descartadas:** ...
- **Relacionado:** (enlace a nota relacionada, ej. `[Backend](../02%20-%20Desarrollo/Backend.md)`)
```

---

## Decisiones tomadas

### MVP sin agente
- **Contexto:** evaluar si usar un agente independiente entre backend y servidor.
- **Decisión:** no usar agente en el MVP; arquitectura simple `Web → Backend → Debian`.
- **Motivo:** simplicidad inicial → [Principios Tecnicos](../01%20-%20Planificacion/Principios%20Tecnicos.md).
- **Alternativa:** agente independiente → descartado por ahora → [Arquitectura](../01%20-%20Planificacion/Arquitectura.md).
- **Relacionado:** [Arquitectura](../01%20-%20Planificacion/Arquitectura.md)

### Backend en Python (Flask o FastAPI)
- **Contexto:** elegir tecnología de backend.
- **Decisión:** Python con Flask o FastAPI.
- **Motivo:** simplicidad y ecosistema.
- **Estado:** ⏭️ superado → decisión final **[Backend con FastAPI](Decisiones.md)**.

### Base de datos SQLite
- **Contexto:** elegir almacenamiento inicial.
- **Decisión:** SQLite.
- **Motivo:** simplicidad sin servidor adicional → [Principios Tecnicos](../01%20-%20Planificacion/Principios%20Tecnicos.md).
- **Alternativa:** PostgreSQL → solo si el proyecto crece → [Base de Datos](../02%20-%20Desarrollo/Base%20de%20Datos.md).

### API REST inicial
- **Contexto:** comunicar frontend y backend.
- **Decisión:** REST.
- **Motivo:** sencillez → [Principios Tecnicos](../01%20-%20Planificacion/Principios%20Tecnicos.md).
- **Alternativa:** WebSockets → a futuro para tiempo real → [API](../02%20-%20Desarrollo/API.md).

### Backend con FastAPI
- **Contexto:** elegir entre Flask y FastAPI → [Backend](../02%20-%20Desarrollo/Backend.md).
- **Decisión:** **FastAPI**.
- **Motivo:** async, documentación automática (Swagger), tipado moderno; buena base para crecer a WebSockets y multi-servidor.
- **Alternativa:** Flask → descartado por ahora (más simple de aprender, pero FastAPI ofrece mejor base).
- **Relacionado:** [Backend](../02%20-%20Desarrollo/Backend.md) · [API](../02%20-%20Desarrollo/API.md) · [Decisión: Flask vs FastAPI](Decisiones.md).
- **Estado:** ✅ decidido.

### Frontend vanilla (HTML + CSS + JS)
- **Contexto:** elegir el stack del frontend del dashboard.
- **Decisión:** HTML, CSS y JavaScript puros, sin compiladores ni frameworks.
- **Motivo:** simplicidad inicial → [Principios Tecnicos](../01%20-%20Planificacion/Principios%20Tecnicos.md).
- **Alternativa:** frameworks (React/Vue) → descartados por ahora; se pueden adoptar si la interfaz crece.
- **Relacionado:** [Frontend](../02%20-%20Desarrollo/Frontend.md) · [UI - Sistema de Diseno](../02%20-%20Desarrollo/UI%20-%20Sistema%20de%20Diseno.md).
- **Estado:** ✅ decidido.

### Sirviendo estáticos con StaticFiles
- **Contexto:** los archivos CSS/JS del dashboard devolvían 404 → [Errores](Errores.md).
- **Decisión:** montar `web/static` en `/static` con `app.mount("/static", StaticFiles(...), name="static")` en `lumina.py`.
- **Motivo:** FastAPI sirve estáticos de forma nativa, sin servidor adicional.
- **Alternativa:** usar `web/components` con carga manual → descartado; innecesario para el MVP.
- **Relacionado:** [Backend](../02%20-%20Desarrollo/Backend.md) · [Frontend](../02%20-%20Desarrollo/Frontend.md) · [Arquitectura](../01%20-%20Planificacion/Arquitectura.md).
- **Estado:** ✅ decidido.

### Base de datos con SQLModel
- **Contexto:** elegir cómo acceder a SQLite desde FastAPI → [Base de Datos](../02%20-%20Desarrollo/Base%20de%20Datos.md).
- **Decisión:** **SQLModel** (SQLAlchemy + Pydantic) sobre SQLite en `data/lumina.db`.
- **Motivo:** modelos tipados convalidados por Pydantic, integración natural con FastAPI y migración más fácil a PostgreSQL.
- **Alternativa:** `sqlite3` crudo del stdlib → descartado por ahora (menos tipado); SQLAlchemy puro → redundante con SQLModel.
- **Relacionado:** [Requisitos](../01%20-%20Planificacion/Requisitos.md) · [Base de Datos](../02%20-%20Desarrollo/Base%20de%20Datos.md).
- **Estado:** ✅ decidido.

### Tabla única `servicios`
- **Contexto:** modelar bots y webs en la base de datos → [Base de Datos](../02%20-%20Desarrollo/Base%20de%20Datos.md).
- **Decisión:** una sola tabla `servicios` con campo `tipo` (`bot` | `web`); la web añade `check_url` (nullable).
- **Motivo:** bots y webs comparten estructura y acciones; coincide con el lenguaje del dashboard ("servicios"). Simplicidad → [Principios Tecnicos](../01%20-%20Planificacion/Principios%20Tecnicos.md).
- **Alternativa:** tablas separadas `bots` y `webs` → descartado por ahora (duplicación innecesaria).
- **Relacionado:** [Bots](../02%20-%20Desarrollo/Bots.md) · [Webs](../02%20-%20Desarrollo/Webs.md).
- **Estado:** ✅ decidido.

### Métricas del sistema con psutil
- **Contexto:** obtener CPU, RAM, disco, red, uptime y procesos → [Servidor](../02%20-%20Desarrollo/Servidor.md).
- **Decisión:** usar **psutil**.
- **Motivo:** API simple y multiplataforma; evita leer `/proc` a mano.
- **Alternativa:** comandos de shell (`top`, `df`, `free`) → descartado; fragilidad al parsear.
- **Relacionado:** [Servidor](../02%20-%20Desarrollo/Servidor.md) · [Requisitos](../01%20-%20Planificacion/Requisitos.md).
- **Estado:** ✅ decidido.

### Gestión de servicios con systemd
- **Contexto:** iniciar/detener/reiniciar bots y webs → [Control Remoto](../02%20-%20Desarrollo/Control%20Remoto.md).
- **Decisión:** usar **systemctl** vía subprocess, con plantillas por tipo de servicio.
- **Motivo:** systemd es el gestor del servidor Debian 13 → [systemd](../04%20-%20Investigacion/systemd.md); integración con auto-start/reinicio (v0.2).
- **Alternativa:** gestionar procesos a mano (`kill`, `nohup`) → descartado por ahora; menos fiable.
- **Relacionado:** [Servidor](../02%20-%20Desarrollo/Servidor.md) · [Acciones de Bots](../02%20-%20Desarrollo/Acciones%20de%20Bots.md).
- **Estado:** ✅ decidido (seguridad al implementar → [Seguridad](../03%20-%20Seguridad/Seguridad.md)).

### Seguridad MVP con token de API
- **Contexto:** proteger la API sin sistema de usuarios → [Autenticacion](../03%20-%20Seguridad/Autenticacion.md).
- **Decisión:** **token de API** (`LUMINA_TOKEN`) vía `X-API-Key` / `Authorization: Bearer`; todas las rutas menos `/api/health`.
- **Motivo:** herramienta personal; un token es simple y suficiente para el MVP. HTTPS obligatorio si se expone → [Acceso Remoto](../03%20-%20Seguridad/Acceso%20Remoto.md).
- **Alternativa:** sesiones/login → descartado por ahora (sin usuarios); JWT → innecesario en un solo usuario.
- **Relacionado:** [API](../02%20-%20Desarrollo/API.md) · [Seguridad](../03%20-%20Seguridad/Seguridad.md) · [Configuracion](../02%20-%20Desarrollo/Configuracion.md).
- **Estado:** ✅ decidido.

### Esquema de endpoints definido
- **Contexto:** fijar los nombres de endpoints antes de implementar → [API](../02%20-%20Desarrollo/API.md).
- **Decisión:** esquema REST de v0.1 en [API](../02%20-%20Desarrollo/API.md) (`/api/servicios`, `/api/servidor`, acciones y logs).
- **Motivo:** evita reescribir el frontend; alineado con las vistas del dashboard.
- **Relacionado:** [Frontend](../02%20-%20Desarrollo/Frontend.md) · [Dashboard](../02%20-%20Desarrollo/Dashboard.md).
- **Estado:** ✅ decidido.

### Arquitectura definitiva del MVP
- **Contexto:** pasar de la arquitectura conceptual a una estructura de código concreta → [Arquitectura](../01%20-%20Planificacion/Arquitectura.md).
- **Decisión:** estructura `app/` en capas — `api/` (routers + token), `services/` (negocio), `system/` (única capa que toca el SO: systemd + psutil), `models/` (SQLModel), `config.py`, `db.py`; frontend en `web/`; despliegue como servicio systemd con Uvicorn → [Arquitectura definitiva del MVP](../01%20-%20Planificacion/Arquitectura.md).
- **Motivo:** regla de capas clara (navegador ↔ api ↔ services ↔ system) y transición suave desde `lumina.py` sin romper rutas existentes.
- **Alternativa:** un solo `main.py` con todo → descartado por ahora para no crecer sin modularidad;
- **Relacionado:** [Backend](../02%20-%20Desarrollo/Backend.md) · [Arquitectura](../01%20-%20Planificacion/Arquitectura.md).
- **Estado:** ✅ decidido.

---

## Decisiones pendientes

- [x] Elegir Flask vs FastAPI → **FastAPI** → [Backend](../02%20-%20Desarrollo/Backend.md).
- [x] Definir requisitos técnicos → **cerrados** → [Requisitos](../01%20-%20Planificacion/Requisitos.md).
- [x] Definir arquitectura definitiva del MVP → **cerrada** → [Arquitectura definitiva del MVP](../01%20-%20Planificacion/Arquitectura.md).
- [ ] Aplicar la estructura del repositorio en el código (inicio de v0.1) → [Arquitectura](../01%20-%20Planificacion/Arquitectura.md).

---

## Relacionado

- [Changelog](Changelog.md) · Qué cambió.
- [Errores](Errores.md) · Problemas que motivan decisiones.
- [Principios Tecnicos](../01%20-%20Planificacion/Principios%20Tecnicos.md) · Criterios que guían decisiones.
- [Requisitos](../01%20-%20Planificacion/Requisitos.md) · Requisitos que condicionan decisiones.
- [Inicio](../00%20-%20Inicio/Inicio.md)
