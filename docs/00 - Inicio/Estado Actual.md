# 📍 Estado Actual — ProjectLumina

> Situación del proyecto y siguiente camino a seguir.

---

## Fase actual

**Desarrollo de la v0.1.0 en curso (local).** 🟡

La planificación está completa (requisitos técnicos y arquitectura definitiva cerrados) y se está construyendo la v0.1 **localmente, sin esperar al servidor**: estructura `app/` en capas (api → services → system → models → config → db), API REST con token, SQLite + SQLModel, tests con pytest y dashboard conectado a datos reales. El despliegue en el servidor ([Dell Inspiron de 2010](../02%20-%20Desarrollo/Servidor.md), pendiente de renovación) llegará en una fase posterior.

---

## Siguiente camino

```text
PLANIFICACIÓN ✅
     ↓
BASE DEL PROYECTO ✅
     ↓
DASHBOARD WEB (MAQUETA) ✅
     ↓
REQUISITOS TÉCNICOS ✅
     ↓
ARQUITECTURA DEFINITIVA DEL MVP ✅
     ↓
ESTRUCTURA DEL REPOSITORIO ✅ (decidida)
     ↓
DESARROLLO v0.1.0  🟡 en curso (local)
     ↓
TESTING ✅ (pytest backend)
     ↓
DEPLOY (espera servidor)
```

---

## Progreso por fases

> Marca `[x]` cuando completes cada hito en [Tareas](../01%20-%20Planificacion/Tareas.md).

| Fase | Estado |
|------|--------|
| Planificación | ✅ Documentación técnica completa |
| Base del proyecto | ✅ Backend mínimo con FastAPI funcional |
| Dashboard web (maqueta) | ✅ Interfaz con estados vacíos y micro-animaciones |
| Requisitos técnicos | ✅ **Cerrados** → [Requisitos](../01%20-%20Planificacion/Requisitos.md) |
| Arquitectura definitiva MVP | ✅ **Cerrada** → [Arquitectura definitiva del MVP](../01%20-%20Planificacion/Arquitectura.md) |
| Estructura del repositorio | ✅ Definida (aplicada en v0.1) |
| Desarrollo v0.1.0 | 🟡 **En curso (local, sin esperar servidor)** |
| Testing | ✅ Automatizado (pytest) en el backend v0.1 |
| Deploy | ⏳ Pendiente (espera el servidor → [Servidor](../02%20-%20Desarrollo/Servidor.md)) |

---

## Objetivo inmediato

> **Conseguir que ProjectLumina pueda administrar correctamente un bot y una web desde un dashboard web.**

A partir de ahí se construirá el resto del sistema.

→ [Objetivos](Objetivos.md)

---

## Siguientes acciones sugeridas

1. ✅ Definir los **requisitos técnicos** definitivos → [Requisitos](../01%20-%20Planificacion/Requisitos.md) · [Decisiones](../06%20-%20Registro/Decisiones.md).
2. ✅ Cerrar la **arquitectura definitiva del MVP** → [Arquitectura definitiva del MVP](../01%20-%20Planificacion/Arquitectura.md).
3. ✅ Definir la **estructura del repositorio** → [Arquitectura](../01%20-%20Planificacion/Arquitectura.md).
4. 🟡 **Desarrollo de v0.1 en curso (local)**: estructura `app/`, API REST con token, SQLite + SQLModel, tests y dashboard conectado a la API → [v0.1](../05%20-%20Versiones/v0.1.md) · [Implementacion](../06%20-%20Registro/Implementacion.md).
5. ✅ Conectar el dashboard a **datos reales** (endpoints v0.1) → [Frontend](../02%20-%20Desarrollo/Frontend.md) · [API](../02%20-%20Desarrollo/API.md).
6. ⏳ (Cuando haya servidor) desplegar como servicio systemd → [Arquitectura](../01%20-%20Planificacion/Arquitectura.md) · [Servidor](../02%20-%20Desarrollo/Servidor.md).

---

## Relacionado

- [Implementacion](../06%20-%20Registro/Implementacion.md) · Qué está hecho y qué falta.
- [Tareas](../01%20-%20Planificacion/Tareas.md) · Gestión de tareas.
- [Objetivos](Objetivos.md) · Objetivo inmediato.
- [Roadmap](../01%20-%20Planificacion/Roadmap.md) · El plan.
- [v0.1](../05%20-%20Versiones/v0.1.md) · Primer entregable.
- [Inicio](Inicio.md)
