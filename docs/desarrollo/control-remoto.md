# Control remoto — ProjectLumina

La visión de ProjectLumina incluye **acceso remoto amplio** al servidor.

## Ejemplos conceptuales

```
systemctl restart nginx
systemctl stop bot
git pull
python bot.py
```

## Ámbitos de administración

- Procesos.
- Servicios (systemd).
- Bots.
- Webs.
- SSH.
- Sistema.

## Seguridad (crítico)

> Esta capacidad debe implementarse con **especial atención a la seguridad**.

- Toda ejecución remota se trata como **operación privilegiada**.
- Protección → [seguridad](../seguridad.md), [permisos](../seguridad.md#permisos).

---

Volver a [desarrollo](README.md).
