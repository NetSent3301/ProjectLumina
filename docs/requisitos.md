# Requisitos — ProjectLumina

## Requisitos funcionales (MVP)

Funcionalidades confirmadas para v0.1:

- [x] Administración remota.
- [x] Dashboard web.
- [x] Soporte inicial para laptop y iPhone mediante web.
- [x] Servidor inicial con Debian 13.
- [x] Gestión de bots.
- [x] Gestión de webs.
- [x] Iniciar/detener/reiniciar bots y webs.
- [x] Consulta de estados.
- [x] Logs desplegables.
- [x] Auto-restart como funcionalidad importante.
- [x] Información del servidor.
- [x] Ejecución remota de acciones.
- [x] Configuración por bot/web.
- [x] Acceso remoto por Internet como objetivo.
- [x] Evolución futura hacia múltiples servidores.
- [x] Posible administración futura de servidores de terceros.

## Requisitos funcionales futuros

- [ ] Sistema adaptable para bots/webs.
- [ ] Detección automática de configuración.
- [ ] Notificaciones.
- [ ] Aplicación nativa para iPhone.
- [ ] Aplicación universal para Android/otros.
- [ ] Agente Lumina.
- [ ] Múltiples servidores.
- [ ] Usuarios, roles y permisos avanzados.
- [ ] Backend alojado externamente.
- [ ] Deploy automático.
- [ ] Automatizaciones avanzadas.

## Fuera del MVP

Inicialmente NO se priorizará:

- Aplicación nativa iOS.
- Aplicación Android.
- Multiusuario.
- Administración de servidores de terceros.
- Agente distribuido.
- Sistema inteligente completamente adaptable.
- Notificaciones avanzadas.
- Infraestructura externa compleja.
- Arquitectura para miles de servidores.

## Requisitos técnicos (definitivos)

> Stack cerrado para el desarrollo de **v0.1**. Cambios de aquí en adelante → [decisiones](obsidian/06%20-%20Registro/Decisiones.md).

| Área | Decisión | Detalle |
|------|----------|---------|
| Backend | Python + **FastAPI** | Servido con Uvicorn; documentación automática en `/docs` (Swagger) |
| Frontend | HTML, CSS, JavaScript vanilla | Una sola página (vistas por hash); la maqueta actual evoluciona |
| API | **REST + JSON** | Esquema de endpoints definido → [api](desarrollo/api.md) |
| Base de datos | **SQLite** (`data/lumina.db`) con **SQLModel** | Modelos tipados; PostgreSQL solo si el proyecto crece |
| Métricas | **psutil** | CPU, RAM, disco, red, uptime, procesos |
| Gestión de servicios | **systemd** | `systemctl` vía subprocess; plantillas por tipo de servicio |
| Chequeo de webs | **HTTP** (httpx) | Disponibilidad real mediante petición HTTP |
| Seguridad MVP | **Token de API** | Header `X-API-Key` / Bearer desde entorno; HTTPS al exponer a Internet |
| Configuración | Entorno + **pydantic-settings** | Variables `LUMINA_*` desde `.env` |
| SO servidor | Debian 13 | |
| Control de versiones | Git + GitHub | |

### Dependencias a añadir al iniciar v0.1

- `psutil` — métricas del sistema.
- `sqlmodel` — modelos de base de datos.
- `pydantic-settings` — configuración desde entorno.
- `httpx` — ya está en `requirements.txt` (chequeo HTTP de webs y pruebas).

### Reglas del MVP

- Administrar **un bot y una web** sobre Debian 13.
- **Sin agente**, sin WebSockets y sin multiusuario: REST por polling (simpleza inicial).
- Toda ejecución remota se trata como **operación privilegiada** → [seguridad](seguridad.md).

## Requisitos no funcionales

- **Modularidad** — cada parte modificable sin romper el todo.
- **Simplicidad inicial** — no implementar complejidad antes de necesitarla.
- **Seguridad** — toda ejecución remota es una operación privilegiada.
- **Observabilidad** — estados y logs para saber qué ocurre.
- **Escalabilidad progresiva** — crecer sin infraestructura gigantesca.
- **Responsive** — usable en laptop e iPhone.

---

Volver a [índice](README.md).
