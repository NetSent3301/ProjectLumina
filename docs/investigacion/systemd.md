# systemd — Investigación

> Notas sobre systemd, el gestor de servicios del servidor Debian.

## Rol en el proyecto

systemd es el **gestor de servicios del servidor Debian**. ProjectLumina interactúa con los servicios del sistema de forma controlada y estable para iniciar, detener, reiniciar y monitorizar bots y webs.

## Temas a investigar

- [ ] Unidades `.service`.
- [ ] Comandos de `systemctl`.
- [ ] Dependencias entre servicios.
- [ ] Logs con `journalctl`.
- [ ] Auto-arranque (`enable`).

## Comandos base

```bash
# Estado de un servicio
sudo systemctl status <servicio>
sudo systemctl is-active <servicio>
sudo systemctl is-enabled <servicio>

# Iniciar, detener y reiniciar
sudo systemctl start <servicio>
sudo systemctl stop <servicio>
sudo systemctl restart <servicio>

# Auto-arranque
sudo systemctl enable <servicio>
sudo systemctl disable <servicio>

# Logs
journalctl -u <servicio>
journalctl -u <servicio> -f
```

## Aplicación al proyecto

- **Iniciar, detener y reiniciar** bots y webs de forma remota.
- **Auto-inicio** de los servicios al encender el servidor.
- **Logs** centralizados por servicio para diagnóstico.
- **Estado** de cada servicio para el dashboard.

## Relación con el proyecto

- Servidor y sistema → [servidor](../desarrollo/servidor.md).
- Gestión de bots → [bots](../desarrollo/bots.md).
- Gestión de webs → [webs](../desarrollo/webs.md).
- Sistema operativo → [debian](debian.md).

---

Volver a [investigación](README.md).