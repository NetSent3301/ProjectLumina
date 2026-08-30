# Linux — Investigación

> Conocimientos base de Linux para administrar el servidor y ejecutar acciones de forma remota.

## Rol en el proyecto

Linux (Debian 13) es la capa base sobre la que ProjectLumina **administra el servidor y ejecuta acciones**: iniciar servicios, ver logs, gestionar procesos y consultar el estado del sistema.

## Temas a investigar

- [ ] Procesos y señales.
- [ ] Servicios y daemons.
- [ ] Permisos de archivos.
- [ ] Variables de entorno.
- [ ] Automatización de tareas.
- [ ] Shell y scripting.

## Conceptos clave

| Concepto | Relación con el proyecto |
|----------|--------------------------|
| Procesos / PID | Identificar y gestionar lo que corre en el servidor |
| Servicios | Gestión de bots y webs vía systemd |
| Permisos | Control de acceso a archivos, comandos y operaciones sensibles |
| Variables de entorno | Configuración de bots, webs y el propio backend |

Enlaces relacionados:

- Procesos y servicios → [systemd](systemd.md).
- Permisos y operaciones sensibles → [seguridad](../seguridad.md).
- Ejecución remota de acciones → [control remoto](../desarrollo/control-remoto.md).

---

Volver a [investigación](README.md).