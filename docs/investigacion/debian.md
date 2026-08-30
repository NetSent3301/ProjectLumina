# Debian — Investigación

> Notas sobre Debian, el sistema operativo base del servidor del proyecto.

## Rol en el proyecto

Debian 13 es el **SO base del servidor** sobre el que corren ProjectLumina, los bots y las webs. Todas las operaciones administrativas del proyecto se ejecutan sobre este sistema.

Ver también [servidor](../desarrollo/servidor.md).

## Temas a investigar

- [ ] Instalación y actualización de Debian 13.
- [ ] Gestión de paquetes con `apt`.
- [ ] Servicios y systemd.
- [ ] Redes y firewall.
- [ ] Seguridad y endurecimiento.
- [ ] Programación de tareas (`cron` y relacionados).

## Comandos base

```bash
# Actualizar el sistema
sudo apt update
sudo apt upgrade
sudo apt full-upgrade

# Instalar y eliminar paquetes
sudo apt install <paquete>
sudo apt remove <paquete>
sudo apt purge <paquete>

# Buscar paquetes
apt search <termino>
apt show <paquete>

# Estado y versión del sistema
cat /etc/os-release
uname -a
```

## Relación con el proyecto

- Debian + systemd → [servidor](../desarrollo/servidor.md).
- Seguridad del sistema → [seguridad](../seguridad.md).
- Gestión de servicios → [systemd](systemd.md).

---

Volver a [investigación](README.md).