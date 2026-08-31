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
- **Estado:** elección final **pendiente** al comenzar la implementación → [[Backend]].

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

---

## Decisiones pendientes

- [x] Elegir Flask vs FastAPI → **FastAPI** → [[Backend]].
- [ ] Definir arquitectura definitiva del MVP → [[Arquitectura]].
- [ ] Definir estructura exacta del repositorio → [[Arquitectura#Estructura del código]].

---

## Relacionado

- [[Changelog]] · Qué cambió.
- [[Errores]] · Problemas que motivan decisiones.
- [[Principios Tecnicos]] · Criterios que guían decisiones.
- [[Requisitos]] · Requisitos que condicionan decisiones.
- [Ver planificación completa](ProjectLumina_Planificacion)
