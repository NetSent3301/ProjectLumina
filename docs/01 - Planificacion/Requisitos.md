# 📋 Requisitos — ProjectLumina

> Requisitos funcionales, técnicos y fuera del alcance del MVP.

---

## MVP — Requisitos funcionales confirmados

> Funcionalidades que deben estar en el producto, prioridad para [v0.1](../05%20-%20Versiones/v0.1.md).

- [x] Administración remota.
- [x] Dashboard web.
- [x] Soporte inicial para laptop y iPhone mediante web.
- [x] Servidor inicial con Debian 13.
- [x] Gestión de bots.
- [x] Gestión de webs.
- [x] Iniciar bots/webs.
- [x] Detener bots/webs.
- [x] Reiniciar bots/webs.
- [x] Consulta de estados.
- [x] Logs desplegables.
- [x] Auto-restart como funcionalidad importante.
- [x] Información del servidor.
- [x] Ejecución remota de acciones.
- [x] Configuración por bot/web.
- [x] Acceso remoto por Internet como objetivo.
- [x] Evolución futura hacia múltiples servidores.
- [x] Posible administración futura de servidores de terceros.

---

## Requisitos funcionales futuros

> Funcionalidades planificadas para versiones posteriores.

- [ ] Sistema adaptable para bots/webs.
- [ ] Detección automática de configuración.
- [ ] Notificaciones.
- [ ] Aplicación nativa para iPhone.
- [ ] Aplicación universal para Android/otros dispositivos.
- [ ] Agente Lumina.
- [ ] Múltiples servidores.
- [ ] Usuarios.
- [ ] Roles.
- [ ] Permisos avanzados.
- [ ] Backend alojado externamente.
- [ ] Deploy automático.
- [ ] Automatizaciones avanzadas.

---

## Fuera del MVP

> Inicialmente NO se priorizará.

- Aplicación nativa para iPhone.
- Aplicación Android.
- Multiusuario.
- Administración de servidores de terceros.
- Agente distribuido.
- Sistema inteligente completamente adaptable.
- Notificaciones avanzadas.
- Infraestructura externa compleja.
- Arquitectura para miles de servidores.

---

## Requisitos técnicos (definitivos)

> Stack cerrado para el desarrollo de **[v0.1](../05%20-%20Versiones/v0.1.md)**. Cambios desde aquí → [Decisiones](../06%20-%20Registro/Decisiones.md).

| Área | Decisión | Detalle |
|------|----------|---------|
| **Backend** | Python + **FastAPI** | Servido con Uvicorn; documentación automática en `/docs` (Swagger) → [Backend](../02%20-%20Desarrollo/Backend.md) |
| **Frontend** | HTML, CSS, JavaScript vanilla | Una sola página (vistas por hash); la maqueta actual evoluciona → [Frontend](../02%20-%20Desarrollo/Frontend.md) |
| **API** | REST + JSON | Esquema de endpoints definido → [API](../02%20-%20Desarrollo/API.md) |
| **Base de datos** | SQLite (`data/lumina.db`) con **SQLModel** | Modelos tipados; PostgreSQL solo si crece → [Base de Datos](../02%20-%20Desarrollo/Base%20de%20Datos.md) |
| **Métricas** | **psutil** | CPU, RAM, disco, red, uptime, procesos → [Servidor](../02%20-%20Desarrollo/Servidor.md) |
| **Gestión de servicios** | **systemd** | `systemctl` vía subprocess; plantillas por tipo → [Servidor](../02%20-%20Desarrollo/Servidor.md) · [Control Remoto](../02%20-%20Desarrollo/Control%20Remoto.md) |
| **Chequeo de webs** | **HTTP** (httpx) | Disponibilidad real mediante petición HTTP → [Webs](../02%20-%20Desarrollo/Webs.md) |
| **Seguridad MVP** | **Token de API** | `X-API-Key` / Bearer desde entorno; HTTPS al exponer → [Autenticacion](../03%20-%20Seguridad/Autenticacion.md) |
| **Configuración** | Entorno + **pydantic-settings** | Variables `LUMINA_*` desde `.env` |
| **SO servidor** | Debian 13 | → [Debian](../04%20-%20Investigacion/Debian.md) |
| **Gestión de servicios** | systemd | → [systemd](../04%20-%20Investigacion/systemd.md) |
| **Control de versiones** | Git + GitHub | → [Git y GitHub](../02%20-%20Desarrollo/Git%20y%20GitHub.md) |

### Dependencias a añadir al iniciar v0.1

- `psutil` — métricas del sistema.
- `sqlmodel` — modelos de base de datos.
- `pydantic-settings` — configuración desde entorno.
- `httpx` — ya está en `requirements.txt` (chequeo HTTP de webs y pruebas).

### Reglas del MVP

- Administrar **un bot y una web** sobre Debian 13.
- **Sin agente**, sin WebSockets y sin multiusuario: REST por polling (simpleza inicial) → [Principios Tecnicos](Principios%20Tecnicos.md).
- Toda ejecución remota se trata como **operación privilegiada** → [Seguridad](../03%20-%20Seguridad/Seguridad.md).

---

## Requisitos no funcionales

> Criterios de calidad que debe cumplir el sistema.

- **Modularidad** → cada parte debe poder modificarse sin romper el todo → [Principios Tecnicos](Principios%20Tecnicos.md).
- **Simplicidad inicial** → no implementar sistemas complejos antes de necesitarlos.
- **Seguridad** → toda ejecución remota es una operación privilegiada → [Permisos](../03%20-%20Seguridad/Permisos.md).
- **Observabilidad** → estados y logs para saber qué ocurre → [Dashboard](../02%20-%20Desarrollo/Dashboard.md).
- **Escalabilidad progresiva** → crecer sin infraestructura gigantesca.
- **Responsive** → usable en laptop e iPhone.

---

## Relacionado

- [Roadmap](Roadmap.md) · Cuándo se implementa cada requisito.
- [Arquitectura](Arquitectura.md) · Cómo se cumple técnicamente.
- [Backend](../02%20-%20Desarrollo/Backend.md) · [Frontend](../02%20-%20Desarrollo/Frontend.md) · [API](../02%20-%20Desarrollo/API.md) · [Base de Datos](../02%20-%20Desarrollo/Base%20de%20Datos.md)
- [Tareas](Tareas.md) · Trabajo para cumplir requisitos.
- [Inicio](../00%20-%20Inicio/Inicio.md)
