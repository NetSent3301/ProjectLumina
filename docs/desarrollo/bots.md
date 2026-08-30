# Bots — ProjectLumina

Una de las funciones centrales de ProjectLumina es **administrar bots remotamente**.

El objetivo es **no tener que entrar físicamente al servidor** para iniciar, detener o solucionar un bot.

## Acciones principales

- Iniciar.
- Detener.
- Reiniciar.
- Consultar estado.
- Ver logs.
- Detectar si está activo.
- Detectar si se cayó.

### Posteriores
- Auto-inicio.
- Auto-reinicio.
- Variables de entorno.
- Configuración avanzada.
- Automatización adicional.

## Configuración

Cada bot tendrá una configuración almacenada → [base-de-datos.md](base-de-datos.md).

```
Nombre: TelegramBot
Tipo: Python
Ruta: /home/bots/telegram
Comando: python bot.py
Auto-inicio: Sí
Auto-reinicio: Sí
```

Campos del MVP: **Nombre, Ruta, Comando, Tipo, Servicio**.

## Auto-restart

Lumina podrá detectar cuándo un bot se cae y tratar de reiniciarlo automáticamente → [auto-restart](auto-restart.md).

## Vista en el dashboard

→ [dashboard.md](dashboard.md#sección-bots).

---

Volver a [desarrollo](README.md).
