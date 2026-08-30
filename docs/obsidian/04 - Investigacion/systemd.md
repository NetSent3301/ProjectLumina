# ⚙️ systemd — Investigación

> Investigación sobre systemd, el gestor de servicios del servidor.

---

## Rol en el proyecto

systemd es el **gestor de servicios** del servidor Debian → [[Servidor]].

ProjectLumina deberá **interactuar con servicios del sistema** de forma controlada y estable → [[Control Remoto]].

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

- Iniciar/detener/reiniciar servicios de bots y webs → [[Acciones de Bots]] · [[Webs]].
- Auto-inicio de servicios (persistencia) → [[Configuracion de Bots#Campos futuros]].
- Logs de servicios → vamos a [[Dashboard#Logs]].

---

## Relacionado

- [[Servidor]] · Dónde se usa.
- [[Debian]] · Distribución.
- [[Control Remoto]] · Ejecución de comandos.
- [[Bots]] · [[Webs]] · Servicios gestionados.
- [Ver planificación completa](ProjectLumina_Planificacion)
