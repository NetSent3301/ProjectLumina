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

## Requisitos técnicos (propuestos)

| Área | Propuesta | Notas |
|------|-----------|-------|
| Backend | Python — Flask o FastAPI | Elección final pendiente |
| Frontend | HTML, CSS, JavaScript | Interfaz responsive |
| API | REST | WebSockets a futuro |
| Base de datos | SQLite | Migración a PostgreSQL a futuro |
| SO servidor | Debian 13 | |
| Gestión de servicios | systemd | |
| Control de versiones | Git + GitHub | |

## Requisitos no funcionales

- **Modularidad** — cada parte modificable sin romper el todo.
- **Simplicidad inicial** — no implementar complejidad antes de necesitarla.
- **Seguridad** — toda ejecución remota es una operación privilegiada.
- **Observabilidad** — estados y logs para saber qué ocurre.
- **Escalabilidad progresiva** — crecer sin infraestructura gigantesca.
- **Responsive** — usable en laptop e iPhone.

---

Volver a [índice](README.md).
