# ⚙️ systemd — Investigación

> Investigación sobre systemd, el gestor de servicios del servidor.

---

## Rol en el proyecto

systemd es el **gestor de servicios** del servidor Debian → [Servidor](../02%20-%20Desarrollo/Servidor.md).

ProjectLumina deberá **interactuar con servicios del sistema** de forma controlada y estable → [Control Remoto](../02%20-%20Desarrollo/Control%20Remoto.md).

---

## Temas a investigar

- [ ] Creación de unidades (`.service`).
- [ ] Comandos de `systemctl`.
- [ ] Dependencias y orden de arranque.
- [ ] Logs con `journalctl`.
- [ ] Auto-arranque de servicios.

---

## Comandos base

```text
systemctl start <servicio>
systemctl stop <servicio>
systemctl restart <servicio>
systemctl status <servicio>
systemctl enable <servicio>
```

---

## Aplicación al proyecto

- Iniciar/detener/reiniciar servicios de bots y webs → [Acciones de Bots](../02%20-%20Desarrollo/Acciones%20de%20Bots.md) · [Webs](../02%20-%20Desarrollo/Webs.md).
- Auto-inicio de servicios (persistencia) → [Configuracion de Bots](../02%20-%20Desarrollo/Configuracion%20de%20Bots.md).
- Logs de servicios → vamos a [Dashboard](../02%20-%20Desarrollo/Dashboard.md).

---

## Relacionado

- [Servidor](../02%20-%20Desarrollo/Servidor.md) · Dónde se usa.
- [Debian](Debian.md) · Distribución.
- [Control Remoto](../02%20-%20Desarrollo/Control%20Remoto.md) · Ejecución de comandos.
- [Bots](../02%20-%20Desarrollo/Bots.md) · [Webs](../02%20-%20Desarrollo/Webs.md) · Servicios gestionados.
- [Inicio](../00%20-%20Inicio/Inicio.md)
