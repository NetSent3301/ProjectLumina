# 📒 Changelog — ProjectLumina

> Registro de cambios del proyecto, orden cronológico (lo más reciente arriba).

---

## [v0.1.0-dev] - 2026-08-30

### Añadido
- **Dashboard web en maqueta** → [[Dashboard#Base actual]] · [[Frontend]].
  - Reestructura del frontend: `web/templates/` + `web/static/` (css, js, assets) → [[Arquitectura#Estructura del código]].
  - Una sola página con vistas **resumen** (`/`) y **servicios** (`/#/servicios`), con cambio de vista sin recargar.
  - Vista servicios con **selector bots/webs** (pestañas con icono y contador) → [[Bots]] · [[Webs]].
  - Sidebar, cabeceras y estados vacíos sin datos falsos (sin servicios conectados).
  - Micro-animaciones (entrada escalonada, hover, flotación, registro) → [[UI - Sistema de Diseno]].
- Servido de archivos estáticos con `StaticFiles` en `/static` → [[Decisiones#Sirviendo estáticos con StaticFiles]].
- Logo **LUMINA** en la sidebar (blanco con glow de acento + palpitación sutil, `prefers-reduced-motion`) → [[UI - Sistema de Diseno]].
- **Requisitos técnicos cerrados** → [[Requisitos#Requisitos técnicos (definitivos)]] · [[API#Esquema de endpoints v0.1]] · [[Base de Datos]] · [[Decisiones]].
  - Stack definitivo: FastAPI, SQLite + SQLModel, psutil, systemd, check HTTP, token de API, pydantic-settings.
  - Esquema de endpoints v0.1 y modelo de datos (tabla única `servicios`).
- **Arquitectura definitiva del MVP** cerrada → [[Arquitectura#Arquitectura definitiva del MVP|Arquitectura definitiva del MVP]] · [[Decisiones#Arquitectura definitiva del MVP]].
  - Estructura `app/` en capas (api · services · system · models · config · db), frontend en `web/`, despliegue como servicio systemd y transición desde `lumina.py`.
- README renovado → estructura definitiva, stack y estado por fases.

### Corregido
- CSS y JS del dashboard no cargaban (404) → [[Errores#CSS y JS del dashboard no cargaban]].
- Datos de ejemplo proyectados en la UI → [[Errores#Datos de ejemplo en la UI del dashboard]].

---

## [No publicado]

### Añadido
- Documentación inicial del proyecto en Obsidian (mapa completo).
- Documento de planificación general → [ProjectLumina_Planificacion](ProjectLumina_Planificacion).
- **Base inicial del proyecto** montada y funcional → [[Implementacion]].
  - Repositorio Git inicializado.
  - Backend mínimo con **FastAPI** (`lumina.py`): endpoint `/api/health` y página web en `/`.
  - Frontend mínimo (`web/index.html`), script de arranque `scripts/run.sh`, test básico.
- Decisión técnica **FastAPI** → [[Decisiones#Backend con FastAPI]].

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

- [[Roadmap]] · Versiones planificadas.
- [[Decisiones]] · Cambios con contexto.
- [[Errores]] · Problemas resueltos.
- [[Git y GitHub]] · Control de versiones.
- [Ver planificación completa](ProjectLumina_Planificacion)
