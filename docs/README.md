# 📖 Documentación — ProjectLumina

> Plataforma personal de administración remota de servidores, bots, webs y servicios.

Este `docs/` es la **única fuente de documentación**: funciona como *vault* de Obsidian (abre esta carpeta como vault) y a la vez se lee directamente en GitHub. Todo está organizado en carpetas numeradas:

```text
00 - Inicio           visión, objetivos y estado actual
01 - Planificacion    requisitos, arquitectura, roadmap y tareas
02 - Desarrollo       backend, frontend, API, dashboard, bots, webs, servidor…
03 - Seguridad        acceso remoto, autenticación, permisos
04 - Investigacion    Debian, Linux, redes, SSH, systemd
05 - Versiones        v0.1 · v0.2 · v0.3
06 - Registro         changelog, errores, decisiones, implementación
```

## Punto de entrada

1. [00 - Inicio/Inicio](00%20-%20Inicio/Inicio.md) — mapa central del proyecto.
2. [00 - Inicio/Estado Actual](00%20-%20Inicio/Estado%20Actual.md) — dónde estamos y qué sigue.
3. [00 - Inicio/Vision](00%20-%20Inicio/Vision.md) — el qué y el porqué.

## Índice por áreas

### 🏠 Inicio
- [00 - Inicio/Inicio](00%20-%20Inicio/Inicio.md) — centro de documentación.
- [Vision](00%20-%20Inicio/Vision.md) · [Objetivos](00%20-%20Inicio/Objetivos.md) · [Definición final](00%20-%20Inicio/Definicion%20Final.md) · [Estado actual](00%20-%20Inicio/Estado%20Actual.md).

### 🗺️ Planificación
- [Requisitos](01%20-%20Planificacion/Requisitos.md) · [Arquitectura](01%20-%20Planificacion/Arquitectura.md) · [Roadmap](01%20-%20Planificacion/Roadmap.md) · [Tareas](01%20-%20Planificacion/Tareas.md) · [Principios técnicos](01%20-%20Planificacion/Principios%20Tecnicos.md).

### 🛠️ Desarrollo
- [Backend](02%20-%20Desarrollo/Backend.md) · [Frontend](02%20-%20Desarrollo/Frontend.md) · [API](02%20-%20Desarrollo/API.md) · [Base de datos](02%20-%20Desarrollo/Base%20de%20Datos.md) · [Dashboard](02%20-%20Desarrollo/Dashboard.md) · [UI - Sistema de Diseño](02%20-%20Desarrollo/UI%20-%20Sistema%20de%20Diseno.md) · [Configuración](02%20-%20Desarrollo/Configuracion.md) · [Arquitectura Backend](02%20-%20Desarrollo/Arquitectura%20Backend.md) · [Init System](02%20-%20Desarrollo/Init%20System.md).
- Bots: [Bots](02%20-%20Desarrollo/Bots.md) · [Configuración de Bots](02%20-%20Desarrollo/Configuracion%20de%20Bots.md) · [Acciones de Bots](02%20-%20Desarrollo/Acciones%20de%20Bots.md) · [Auto Restart](02%20-%20Desarrollo/Auto%20Restart.md).
- Webs: [Webs](02%20-%20Desarrollo/Webs.md) · [Gestión avanzada de Webs](02%20-%20Desarrollo/Gestion%20Avanzada%20de%20Webs.md).
- Sistema: [Servidor](02%20-%20Desarrollo/Servidor.md) · [Control Remoto](02%20-%20Desarrollo/Control%20Remoto.md) · [Sistema Adaptable](02%20-%20Desarrollo/Sistema%20Adaptable.md) · [Notificaciones](02%20-%20Desarrollo/Notificaciones.md) · [Git y GitHub](02%20-%20Desarrollo/Git%20y%20GitHub.md).

### 🚀 Despliegue
- [Docker](02%20-%20Desarrollo/Despliegue/Docker.md) · [Alpine Linux](02%20-%20Desarrollo/Despliegue%20Alpine.md) · [Instalación Paso a Paso](02%20-%20Desarrollo/Instalacion%20Paso%20a%20Paso.md).

### 🔐 Seguridad
- [Seguridad](03%20-%20Seguridad/Seguridad.md) · [Acceso Remoto](03%20-%20Seguridad/Acceso%20Remoto.md) · [Autenticacion](03%20-%20Seguridad/Autenticacion.md) · [Permisos](03%20-%20Seguridad/Permisos.md) · [Usuarios](03%20-%20Seguridad/Usuarios.md).

### 📚 Investigación
- [Debian](04%20-%20Investigacion/Debian.md) · [Linux](04%20-%20Investigacion/Linux.md) · [Redes](04%20-%20Investigacion/Redes.md) · [SSH](04%20-%20Investigacion/SSH.md) · [systemd](04%20-%20Investigacion/systemd.md).

### 🚀 Versiones
- [v0.1](05%20-%20Versiones/v0.1.md) · [v0.2](05%20-%20Versiones/v0.2.md) · [v0.3](05%20-%20Versiones/v0.3.md).

### 📒 Registro
- [Changelog](06%20-%20Registro/Changelog.md) · [Errores](06%20-%20Registro/Errores.md) · [Decisiones](06%20-%20Registro/Decisiones.md) · [Implementación](06%20-%20Registro/Implementacion.md) · [Histórico de planificación](06%20-%20Registro/Historico%20-%20Planificacion.md).

---

## Inicio rápido

```bash
bash scripts/run.sh
```

- Web: http://127.0.0.1:8000/ · API: http://127.0.0.1:8000/api/health · Swagger: http://127.0.0.1:8000/docs

## En Obsidian

Abre **esta carpeta `docs/`** como vault en Obsidian: verás la organización por carpetas numeradas, los índices y el grafo de notas conectadas con enlaces relativos.