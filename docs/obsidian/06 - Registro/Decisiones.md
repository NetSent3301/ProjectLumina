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

---

## Decisiones pendientes

- [ ] Elegir Flask vs FastAPI → [[Backend]].
- [ ] Definir arquitectura definitiva del MVP → [[Arquitectura]].
- [ ] Definir estructura exacta del repositorio → [[Arquitectura#Estructura del código]].

---

## Relacionado

- [[Changelog]] · Qué cambió.
- [[Errores]] · Problemas que motivan decisiones.
- [[Principios Tecnicos]] · Criterios que guían decisiones.
- [[Requisitos]] · Requisitos que condicionan decisiones.
- [Ver planificación completa](ProjectLumina_Planificacion)
