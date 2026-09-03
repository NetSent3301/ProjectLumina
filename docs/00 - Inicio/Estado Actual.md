# 📍 Estado Actual — ProjectLumina

> Situación del proyecto y siguiente camino a seguir.

---

## Fase actual

**Desarrollo de la v0.1 completado** ✅ — panel local funcional.

**Cambio de orientación:** ProjectLumina pasa de "centro de control remoto de un servidor ajeno" a un **panel que gestiona la máquina donde corre** — sistema operativo, servicios systemd, procesos, bots y webs. Todo es funcional ya en el equipo de desarrollo: estructura `app/` en capas (api → services → system → models → config → db), API REST con token, SQLite + SQLModel, tests con pytest, dashboard conectado a datos reales y **registro de servicios desde la interfaz** (formulario → `POST /api/servicios`).

**Novedad v0.1.1:** **Multi-servidor (agentes Lumina)** — el panel central puede registrar y vigilar otras instancias de Lumina corriendo en otras máquinas (homelab, VPS, Raspberry Pi). Cada agente expone su API y el panel central la consulta cada 15s. Indicador global de conexión en la barra lateral: “conectado · este equipo”, “sin acceso al servidor principal”, “sin acceso a N servidor(es)”.

**Novedad v0.1.2:** **Automatización (despliegue + terminal)**
- **Despliegue de bots desde git**: `POST /api/despliegues` entrega solo nombre + URL del repo y Lumina clona, autodetecta el lenguaje/comando, crea la unidad del gestor de arranque (**systemd** o **OpenRC/Alpine**), la habilita e inicia el bot. Repos privados vía token temporal (nunca persistido).
- **Terminal interactiva**: `WS /api/terminal` + Xterm.js en el panel (shell en el servidor), con selector de cwd desde los servicios.
- Escritura privilegiada segura (sin corromper archivos de sistema con la contraseña de sudo).

La **administración remota** (acceso desde otro dispositivo, p. ej. el iPhone) queda como **fase posterior**, una vez el producto funcione de forma local.

**Despliegue Docker listo:** `Dockerfile` + `docker-compose.yml` con dos perfiles:
- `panel` — panel central (sin acceso a systemd del host)
- `agente` — para cada máquina del homelab (con `--pid=host --privileged` y bind mounts para `systemctl`/`journalctl`)

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
DESARROLLO v0.1.0 ✅ completado
     ↓
TESTING ✅ (pytest backend)
     ↓
REGISTRO DE SERVICIOS ✅ (desde la interfaz)
     ↓
MULTI-SERVIDOR (AGENTES) ✅ v0.1.1
     ↓
DESPLIEGUE DOCKER ✅ docker-compose
     ↓
AUTOMATIZACIÓN (DEPLOY GIT + TERMINAL) ✅ v0.1.2
     ↓
INSTALACIÓN EN OTROS EQUIPOS (fase posterior)
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
| Desarrollo v0.1.0 | ✅ **Completado** (local, sin esperar servidor) |
| Multi-servidor v0.1.1 | ✅ Agentes + indicador conexión |
| Automatización v0.1.2 | ✅ Deploy desde git + terminal interactiva (systemd/OpenRC) |
| Testing | ✅ Automatizado (pytest) en el backend v0.1 |
| Deploy Docker | ✅ `Dockerfile` + `docker-compose.yml` |
| Deploy systemd | ⏳ Pendiente (cuando haya servidor → [Servidor](../02%20-%20Desarrollo/Servidor.md)) |

---

## Objetivo inmediato

> **ProjectLumina gestiona la máquina donde corre + vigila agentes remotos en el homelab.**

→ [Objetivos](Objetivos.md)

---

## Siguientes acciones sugeridas

1. ✅ Definir los **requisitos técnicos** definitivos → [Requisitos](../01%20-%20Planificacion/Requisitos.md) · [Decisiones](../06%20-%20Registro/Decisiones.md).
2. ✅ Cerrar la **arquitectura definitiva del MVP** → [Arquitectura definitiva del MVP](../01%20-%20Planificacion/Arquitectura.md).
3. ✅ Definir la **estructura del repositorio** → [Arquitectura](../01%20-%20Planificacion/Arquitectura.md).
4. ✅ **Desarrollo de v0.1 completado**: estructura `app/`, API REST con token, SQLite + SQLModel, tests y dashboard conectado a la API → [v0.1](../05%20-%20Versiones/v0.1.md) · [Implementacion](../06%20-%20Registro/Implementacion.md).
5. ✅ **Multi-servidor v0.1.1**: agentes Lumina + indicador conexión global → [Frontend](../02%20-%20Desarrollo/Frontend.md) · [API](../02%20-%20Desarrollo/API.md).
6. ✅ **Docker para homelab**: `docker compose --profile panel up -d` (panel central) / `docker compose --profile agente up -d` (en cada server).
7. ✅ **Automatización v0.1.2**: despliegue de bots desde git (`POST /api/despliegues`) + terminal interactiva (Xterm.js + WebSocket), con unidades systemd y OpenRC → [API](../02%20-%20Desarrollo/API.md) · [Changelog](../06%20-%20Registro/Changelog.md).
8. ⏳ (Cuando haya servidor) desplegar como servicio systemd → [Arquitectura](../01%20-%20Planificacion/Arquitectura.md) · [Servidor](../02%20-%20Desarrollo/Servidor.md).

---

## Relacionado

- [Implementacion](../06%20-%20Registro/Implementacion.md) · Qué está hecho y qué falta.
- [Tareas](../01%20-%20Planificacion/Tareas.md) · Gestión de tareas.
- [Objetivos](Objetivos.md) · Objetivo inmediato.
- [Roadmap](../01%20-%20Planificacion/Roadmap.md) · El plan.
- [v0.1](../05%20-%20Versiones/v0.1.md) · Primer entregable.
- [Inicio](Inicio.md)
