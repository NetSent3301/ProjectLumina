# 📍 Estado actual — ProjectLumina

> Situación del proyecto y siguiente camino.

---

## Fase actual

**Base del proyecto inicializada y dashboard en maqueta.** 🟢

La etapa de planificación avanzó y la **base inicial** ya está montada y funciona localmente (sin servidor). Además, se construyó una **maqueta del dashboard web** con estados vacíos (sin datos falsos), a la espera de conectar datos reales.

> Detalles en [implementación (obsidian)](../docs/obsidian/06%20-%20Registro/Implementacion.md)

---

## Siguiente camino

```mermaid
flowchart TD
    A[Planificación] --> B[Base del proyecto ✅]
    B --> C[Dashboard web en maqueta ✅]
    C --> D[Requisitos técnicos]
    D --> E[Arquitectura definitiva del MVP]
    E --> F[Desarrollo v0.1.0]
    F --> G[Testing]
    G --> H[Deploy]
```

---

## Progreso por fases

> Marca `[x]` cuando completes cada hito.

| Fase | Estado |
|------|--------|
| Planificación | ✅ Documentación generada |
| Base del proyecto | ✅ Backend mínimo con FastAPI, arranca y verifica conectividad |
| Dashboard web (maqueta) | ✅ Interfaz con estados vacíos y micro-animaciones (sin datos reales) |
| Requisitos técnicos | ⏳ Pendiente |
| Arquitectura definitiva MVP | ⏳ Pendiente |
| Desarrollo v0.1.0 | ⏳ Pendiente (requiere acceso al servidor) |
| Testing | ⏳ Pendiente |
| Deploy | ⏳ Pendiente |

---

## Objetivo inmediato

> **Conseguir que ProjectLumina pueda administrar correctamente un bot y una web desde un dashboard web.**

A partir de ahí se construirá el resto del sistema.

---

## Siguientes acciones

1. ✅ Elegir backend → **FastAPI**.
2. ✅ Estructurar el repositorio y montar la base ejecutable.
3. ✅ Montar una maqueta del dashboard web (interfaz, estáticos servidos, micro-animaciones).
4. Definir los **requisitos técnicos** definitivos.
5. Fijar la **arquitectura definitiva del MVP**.
6. (Cuando se recupere acceso al servidor) iniciar el **desarrollo de v0.1**: gestión de bots/webs.

---

Volver a [índice](README.md).
