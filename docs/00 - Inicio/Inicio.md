# 🏠 Inicio — ProjectLumina

> Centro de documentación del proyecto. Desde aquí navegas por la visión, el plan, el desarrollo, la seguridad, la investigación y el registro del proyecto.

---

## 🌟 Accesos rápidos

| Área | Nota de entrada |
|------|-----------------|
| 🧭 Visión y objetivos | [Vision](Vision.md) · [Objetivos](Objetivos.md) |
| 🎯 Definición | [Definicion Final](Definicion%20Final.md) |
| 📍 Estado actual | [Estado Actual](Estado%20Actual.md) |
| 🗺️ Plan | [Roadmap](../01%20-%20Planificacion/Roadmap.md) · [Requisitos](../01%20-%20Planificacion/Requisitos.md) · [Arquitectura](../01%20-%20Planificacion/Arquitectura.md) · [Tareas](../01%20-%20Planificacion/Tareas.md) |
| 🛠️ Desarrollo | [Backend](../02%20-%20Desarrollo/Backend.md) · [Frontend](../02%20-%20Desarrollo/Frontend.md) · [API](../02%20-%20Desarrollo/API.md) · [Dashboard](../02%20-%20Desarrollo/Dashboard.md) · [UI - Sistema de Diseno](../02%20-%20Desarrollo/UI%20-%20Sistema%20de%20Diseno.md) · [Arquitectura Backend](../02%20-%20Desarrollo/Arquitectura%20Backend.md) · [Init System](../02%20-%20Desarrollo/Init%20System.md) |
| 📦 Gestión | [Bots](../02%20-%20Desarrollo/Bots.md) · [Webs](../02%20-%20Desarrollo/Webs.md) · [Servidor](../02%20-%20Desarrollo/Servidor.md) |
| 🔐 Seguridad | [Acceso Remoto](../03%20-%20Seguridad/Acceso%20Remoto.md) · [Autenticacion](../03%20-%20Seguridad/Autenticacion.md) · [Permisos](../03%20-%20Seguridad/Permisos.md) |
| 📚 Investigación | [Debian](../04%20-%20Investigacion/Debian.md) · [Linux](../04%20-%20Investigacion/Linux.md) · [Redes](../04%20-%20Investigacion/Redes.md) · [SSH](../04%20-%20Investigacion/SSH.md) · [systemd](../04%20-%20Investigacion/systemd.md) |
| 🚀 Versiones | [v0.1](../05%20-%20Versiones/v0.1.md) · [v0.2](../05%20-%20Versiones/v0.2.md) · [v0.3](../05%20-%20Versiones/v0.3.md) |
| 📒 Registro | [Changelog](../06%20-%20Registro/Changelog.md) · [Errores](../06%20-%20Registro/Errores.md) · [Decisiones](../06%20-%20Registro/Decisiones.md) · [Implementacion](../06%20-%20Registro/Implementacion.md) |
| 🐳 Despliegue | [Docker](../02%20-%20Desarrollo/Despliegue/Docker.md) · [Alpine Linux](../02%20-%20Desarrollo/Despliegue%20Alpine.md) · [Instalación Paso a Paso](../02%20-%20Desarrollo/Instalacion%20Paso%20a%20Paso.md) · [Sistema de Actualizaciones](../02%20-%20Desarrollo/Sistema%20de%20Actualizaciones.md) |

---

## 📂 Índice de documentación

### 00 - Inicio
- [Vision](Vision.md) — Por qué y qué es el proyecto.
- [Objetivos](Objetivos.md) — Objetivo principal, secundario e inmediato.
- [Definicion Final](Definicion%20Final.md) — Definición formal del proyecto.
- [Estado Actual](Estado%20Actual.md) — Fase, siguiente camino y objetivo inmediato.

### 01 - Planificacion
- [Roadmap](../01%20-%20Planificacion/Roadmap.md) — Hoja de ruta por versiones.
- [Requisitos](../01%20-%20Planificacion/Requisitos.md) — Requisitos funcionales, técnicos y fuera del MVP.
- [Arquitectura](../01%20-%20Planificacion/Arquitectura.md) — Arquitectura del MVP y futura.
- [Tareas](../01%20-%20Planificacion/Tareas.md) — Gestión de tareas por fase.
- [Principios Tecnicos](../01%20-%20Planificacion/Principios%20Tecnicos.md) — Principios de diseño del proyecto.

### 02 - Desarrollo
- [Backend](../02%20-%20Desarrollo/Backend.md) — Tecnologías y responsabilidades del backend.
- [Frontend](../02%20-%20Desarrollo/Frontend.md) — Interfaz web y plataformas.
- [API](../02%20-%20Desarrollo/API.md) — Comunicación REST.
- [Base de Datos](../02%20-%20Desarrollo/Base%20de%20Datos.md) — Almacenamiento SQLite → PostgreSQL.
- [Dashboard](../02%20-%20Desarrollo/Dashboard.md) — Centro de control.
- [UI - Sistema de Diseno](../02%20-%20Desarrollo/UI%20-%20Sistema%20de%20Diseno.md) — Tokens, estados y micro-animaciones.
- [Arquitectura Backend](../02%20-%20Desarrollo/Arquitectura%20Backend.md) — Estructura en capas, patrones y contratos.
- [Init System](../02%20-%20Desarrollo/Init%20System.md) — Abstracción multi-init (systemd/OpenRC/Runit/SysV).
- [Bots](../02%20-%20Desarrollo/Bots.md) — Gestión de bots. → [Configuracion de Bots](../02%20-%20Desarrollo/Configuracion%20de%20Bots.md) · [Acciones de Bots](../02%20-%20Desarrollo/Acciones%20de%20Bots.md) · [Auto Restart](../02%20-%20Desarrollo/Auto%20Restart.md)
- [Webs](../02%20-%20Desarrollo/Webs.md) — Gestión de webs. → [Gestion Avanzada de Webs](../02%20-%20Desarrollo/Gestion%20Avanzada%20de%20Webs.md)
- [Servidor](../02%20-%20Desarrollo/Servidor.md) — Laptop servidor con Debian 13.
- [Control Remoto](../02%20-%20Desarrollo/Control%20Remoto.md) — Ejecución remota general.
- [Sistema Adaptable](../02%20-%20Desarrollo/Sistema%20Adaptable.md) — Detección automática de configuración.
- [Notificaciones](../02%20-%20Desarrollo/Notificaciones.md) — Alertas futuras.

### 🐳 Despliegue
- [Docker](../02%20-%20Desarrollo/Despliegue/Docker.md) — Imagen slim y Alpine, panel y agente multi-init.
- [Alpine Linux](../02%20-%20Desarrollo/Despliegue%20Alpine.md) — Guía completa OpenRC/Alpine.
- [Instalación Paso a Paso](../02%20-%20Desarrollo/Instalacion%20Paso%20a%20Paso.md) — Guía práctica panel + agentes.
- [Sistema de Actualizaciones](../02%20-%20Desarrollo/Sistema%20de%20Actualizaciones.md) — Notificaciones push GitHub Releases.

### 03 - Seguridad
- [Acceso Remoto](../03%20-%20Seguridad/Acceso%20Remoto.md) — Exposición a Internet y medidas.
- [Autenticacion](../03%20-%20Seguridad/Autenticacion.md) — Login y usuarios (futuro).
- [Permisos](../03%20-%20Seguridad/Permisos.md) — Permisos y operaciones privilegiadas.
- [Usuarios](../03%20-%20Seguridad/Usuarios.md) — Modelo de usuarios a futuro.

### 04 - Investigacion
- [Debian](../04%20-%20Investigacion/Debian.md) · [Linux](../04%20-%20Investigacion/Linux.md) · [Redes](../04%20-%20Investigacion/Redes.md) · [SSH](../04%20-%20Investigacion/SSH.md) · [systemd](../04%20-%20Investigacion/systemd.md)

### 05 - Versiones
- [v0.1](../05%20-%20Versiones/v0.1.md) — Base funcional.
- [v0.2](../05%20-%20Versiones/v0.2.md) — Automatización.
- [v0.3](../05%20-%20Versiones/v0.3.md) — Sistema adaptable.

### 06 - Registro
- [Changelog](../06%20-%20Registro/Changelog.md) · [Errores](../06%20-%20Registro/Errores.md) · [Decisiones](../06%20-%20Registro/Decisiones.md)

---

## 🧭 Cómo usar este mapa

1. **Empieza por [Vision](Vision.md)** para entender el qué y el porqué.
2. **Revisa [Estado Actual](Estado%20Actual.md)** para saber dónde estamos.
3. **Consulta [Roadmap](../01%20-%20Planificacion/Roadmap.md)** y [Requisitos](../01%20-%20Planificacion/Requisitos.md) para ver hacia dónde vamos.
4. **Profundiza en [Documentacion](../02%20-%20Desarrollo/Documentacion.md)** según tu interés.
5. **Registra avances** en [Changelog](../06%20-%20Registro/Changelog.md), [Errores](../06%20-%20Registro/Errores.md) y [Decisiones](../06%20-%20Registro/Decisiones.md).

---

> 📍 **Fase actual:** [Planificación](Estado%20Actual.md) · 🔗 [Inicio](Inicio.md)
