# 🐧 Debian — Investigación

> Investigación sobre Debian, el sistema operativo base del servidor.

---

## Rol en el proyecto

- **Debian 13** será el sistema operativo del servidor inicial → [Servidor](../02%20-%20Desarrollo/Servidor.md).
- Debian seguirá siendo el **sistema operativo real**; Lumina es la capa de administración encima → [Vision](../00%20-%20Inicio/Vision.md).

---

## Temas a investigar

- [ ] Instalación y configuración de Debian 13.
- [ ] Gestión de paquetes (`apt`).
- [ ] Servicios y systemd → [systemd](systemd.md).
- [ ] Redes y firewall → [Redes](Redes.md).
- [ ] Seguridad y endurecimiento → [seguridad del sistema](../03%20-%20Seguridad/Seguridad.md).
- [ ] Programación de tareas (cron/systemd timers).

---

## Comandos útiles (base)

```text
# Actualizar el sistema
sudo apt update
sudo apt upgrade
sudo apt full-upgrade

# Instalar / eliminar paquetes
sudo apt install <paquete>
sudo apt remove <paquete>
sudo apt purge <paquete>

# Buscar paquetes
apt search <termino>
apt show <paquete>

# Estado y versión del sistema
cat /etc/os-release
uname -a

# Servicios
systemctl status <servicio>
journalctl -u <servicio>
ufw status
```

---

## Relacionado

- [Servidor](../02%20-%20Desarrollo/Servidor.md) · Dónde se usa.
- [Linux](Linux.md) · Conocimientos base.
- [systemd](systemd.md) · Gestión de servicios.
- [Redes](Redes.md) · Conectividad.
- [Inicio](../00%20-%20Inicio/Inicio.md)
