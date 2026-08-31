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
- **Relacionado:** (enlace a nota relacionada, ej. `[[Backend]]`)
```

---

## Decisiones tomadas

### MVP sin agente
- **Contexto:** evaluar si usar un agente independiente entre backend y servidor.
- **Decisión:** no usar agente en el MVP; arquitectura simple `Web → Backend → Debian`.
- **Motivo:** simplicidad inicial → [[Principios Tecnicos#Simplicidad inicial]].
- **Alternativa:** agente independiente → descartado por ahora → [[Arquitectura#Agente Lumina]].
- **Relacionado:** [[Arquitectura]]

### Backend en Python (Flask o FastAPI)
- **Contexto:** elegir tecnología de backend.
- **Decisión:** Python con Flask o FastAPI.
- **Motivo:** simplicidad y ecosistema.
- **Estado:** ⏭️ superado → decisión final **[[Decisiones#Backend con FastAPI|Backend con FastAPI]]**.

### Base de datos SQLite
- **Contexto:** elegir almacenamiento inicial.
- **Decisión:** SQLite.
- **Motivo:** simplicidad sin servidor adicional → [[Principios Tecnicos#Simplicidad inicial]].
- **Alternativa:** PostgreSQL → solo si el proyecto crece → [[Base de Datos]].

### API REST inicial
- **Contexto:** comunicar frontend y backend.
- **Decisión:** REST.
- **Motivo:** sencillez → [[Principios Tecnicos#Simplicidad inicial]].
- **Alternativa:** WebSockets → a futuro para tiempo real → [[API#WebSockets]].

### Backend con FastAPI
- **Contexto:** elegir entre Flask y FastAPI → [[Backend]].
- **Decisión:** **FastAPI**.
- **Motivo:** async, documentación automática (Swagger), tipado moderno; buena base para crecer a WebSockets y multi-servidor.
- **Alternativa:** Flask → descartado por ahora (más simple de aprender, pero FastAPI ofrece mejor base).
- **Relacionado:** [[Backend]] · [[API]] · [[Decisiones#Decisiones pendientes|Decisión: Flask vs FastAPI]].
- **Estado:** ✅ decidido.

### Frontend vanilla (HTML + CSS + JS)
- **Contexto:** elegir el stack del frontend del dashboard.
- **Decisión:** HTML, CSS y JavaScript puros, sin compiladores ni frameworks.
- **Motivo:** simplicidad inicial → [[Principios Tecnicos#Simplicidad inicial]].
- **Alternativa:** frameworks (React/Vue) → descartados por ahora; se pueden adoptar si la interfaz crece.
- **Relacionado:** [[Frontend]] · [[UI - Sistema de Diseno]].
- **Estado:** ✅ decidido.

### Sirviendo estáticos con StaticFiles
- **Contexto:** los archivos CSS/JS del dashboard devolvían 404 → [[Errores#CSS y JS del dashboard no cargaban]].
- **Decisión:** montar `web/static` en `/static` con `app.mount("/static", StaticFiles(...), name="static")` en `lumina.py`.
- **Motivo:** FastAPI sirve estáticos de forma nativa, sin servidor adicional.
- **Alternativa:** usar `web/components` con carga manual → descartado; innecesario para el MVP.
- **Relacionado:** [[Backend]] · [[Frontend#Base actual]] · [[Arquitectura#Estructura del código]].
- **Estado:** ✅ decidido.

### Base de datos con SQLModel
- **Contexto:** elegir cómo acceder a SQLite desde FastAPI → [[Base de Datos]].
- **Decisión:** **SQLModel** (SQLAlchemy + Pydantic) sobre SQLite en `data/lumina.db`.
- **Motivo:** modelos tipados convalidados por Pydantic, integración natural con FastAPI y migración más fácil a PostgreSQL.
- **Alternativa:** `sqlite3` crudo del stdlib → descartado por ahora (menos tipado); SQLAlchemy puro → redundante con SQLModel.
- **Relacionado:** [[Requisitos#Requisitos técnicos (definitivos)]] · [[Base de Datos]].
- **Estado:** ✅ decidido.

### Tabla única `servicios`
- **Contexto:** modelar bots y webs en la base de datos → [[Base de Datos]].
- **Decisión:** una sola tabla `servicios` con campo `tipo` (`bot` | `web`); la web añade `check_url` (nullable).
- **Motivo:** bots y webs comparten estructura y acciones; coincide con el lenguaje del dashboard ("servicios"). Simplicidad → [[Principios Tecnicos#Simplicidad inicial]].
- **Alternativa:** tablas separadas `bots` y `webs` → descartado por ahora (duplicación innecesaria).
- **Relacionado:** [[Bots#Configuración]] · [[Webs#Funciones]].
- **Estado:** ✅ decidido.

### Métricas del sistema con psutil
- **Contexto:** obtener CPU, RAM, disco, red, uptime y procesos → [[Servidor#Información mostrada]].
- **Decisión:** usar **psutil**.
- **Motivo:** API simple y multiplataforma; evita leer `/proc` a mano.
- **Alternativa:** comandos de shell (`top`, `df`, `free`) → descartado; fragilidad al parsear.
- **Relacionado:** [[Servidor]] · [[Requisitos#Requisitos técnicos (definitivos)]].
- **Estado:** ✅ decidido.

### Gestión de servicios con systemd
- **Contexto:** iniciar/detener/reiniciar bots y webs → [[Control Remoto]].
- **Decisión:** usar **systemctl** vía subprocess, con plantillas por tipo de servicio.
- **Motivo:** systemd es el gestor del servidor Debian 13 → [[systemd]]; integración con auto-start/reinicio (v0.2).
- **Alternativa:** gestionar procesos a mano (`kill`, `nohup`) → descartado por ahora; menos fiable.
- **Relacionado:** [[Servidor]] · [[Acciones de Bots]].
- **Estado:** ✅ decidido (seguridad al implementar → [[Seguridad]]).

### Seguridad MVP con token de API
- **Contexto:** proteger la API sin sistema de usuarios → [[Autenticacion]].
- **Decisión:** **token de API** (`LUMINA_TOKEN`) vía `X-API-Key` / `Authorization: Bearer`; todas las rutas menos `/api/health`.
- **Motivo:** herramienta personal; un token es simple y suficiente para el MVP. HTTPS obligatorio si se expone → [[Acceso Remoto]].
- **Alternativa:** sesiones/login → descartado por ahora (sin usuarios); JWT → innecesario en un solo usuario.
- **Relacionado:** [[API]] · [[Seguridad]] · [[Configuración]].
- **Estado:** ✅ decidido.

### Esquema de endpoints definido
- **Contexto:** fijar los nombres de endpoints antes de implementar → [[API]].
- **Decisión:** esquema REST de v0.1 en [[API#Esquema de endpoints v0.1]] (`/api/servicios`, `/api/servidor`, acciones y logs).
- **Motivo:** evita reescribir el frontend; alineado con las vistas del dashboard.
- **Relacionado:** [[Frontend]] · [[Dashboard]].
- **Estado:** ✅ decidido.

### Arquitectura definitiva del MVP
- **Contexto:** pasar de la arquitectura conceptual a una estructura de código concreta → [[Arquitectura]].
- **Decisión:** estructura `app/` en capas — `api/` (routers + token), `services/` (negocio), `system/` (única capa que toca el SO: systemd + psutil), `models/` (SQLModel), `config.py`, `db.py`; frontend en `web/`; despliegue como servicio systemd con Uvicorn → [[Arquitectura#Arquitectura definitiva del MVP|Arquitectura definitiva del MVP]].
- **Motivo:** regla de capas clara (navegador ↔ api ↔ services ↔ system) y transición suave desde `lumina.py` sin romper rutas existentes.
- **Alternativa:** un solo `main.py` con todo → descartado por ahora para no crecer sin modularidad;
- **Relacionado:** [[Backend#Posibles módulos en el código]] · [[Arquitectura#Estructura del código]].
- **Estado:** ✅ decidido.

---

## Decisiones pendientes

- [x] Elegir Flask vs FastAPI → **FastAPI** → [[Backend]].
- [x] Definir requisitos técnicos → **cerrados** → [[Requisitos#Requisitos técnicos (definitivos)]].
- [x] Definir arquitectura definitiva del MVP → **cerrada** → [[Arquitectura#Arquitectura definitiva del MVP|Arquitectura definitiva del MVP]].
- [ ] Aplicar la estructura del repositorio en el código (inicio de v0.1) → [[Arquitectura#Estructura del código]].

---

## Relacionado

- [[Changelog]] · Qué cambió.
- [[Errores]] · Problemas que motivan decisiones.
- [[Principios Tecnicos]] · Criterios que guían decisiones.
- [[Requisitos]] · Requisitos que condicionan decisiones.
- [Ver planificación completa](ProjectLumina_Planificacion)
