# 🐧 Debian — Investigación

> Investigación sobre Debian, el sistema operativo base del servidor.

---

## Rol en el proyecto

- **Debian 13** será el sistema operativo del servidor inicial → [[Servidor]].
- Debian seguirá siendo el **sistema operativo real**; Lumina es la capa de administración encima → [[Vision#Idea general]].

---

## Temas a investigar

- [ ] Instalación y configuración de Debian 13.
- [ ] Gestión de paquetes (`apt`).
- [ ] Servicios y systemd → [[systemd]].
- [ ] Redes y firewall → [[Redes]].
- [ ] Seguridad y endurecimiento → [[Seguridad|seguridad del sistema]].
- [ ] Programación de tareas (cron/systemd timers).

---

## Comandos útiles (base)

```text
apt update && apt upgrade
systemctl status <servicio>
journalctl -u <servicio>
ufw status
```

---

## Relacionado

- [[Servidor]] · Dónde se usa.
- [[Linux]] · Conocimientos base.
- [[systemd]] · Gestión de servicios.
- [[Redes]] · Conectividad.
- [Ver planificación completa](ProjectLumina_Planificacion)
