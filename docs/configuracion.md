# 🖥️ Configuración — ProjectLumina

> Guía para configurar el servidor y el dashboard.

---

## Vista general

ProjectLumina se ejecuta sobre un servidor **Debian 13** → [Servidor](desarrollo/servidor.md).

La configuración se distribuye en:

- **Archivo de entorno** (variables) — configuración sensible y de despliegue.
- **Base de datos SQLite** → [base-de-datos.md](desarrollo/base-de-datos.md) — configuraciones de bots/webs.
- **Servicios systemd** → [investigacion/systemd.md](investigacion/systemd.md) — gestión de procesos.

---

## Variables de entorno

> ⚠️ Las variables sensibles van en un archivo `.env` (no versionar). Ejemplo en `.env.example`.

| Variable | Descripción | Requerida | Valor por defecto |
|----------|-------------|-----------|-------------------|
| `LUMINA_HOST` | IP/interfaz de escucha del servidor | No | `127.0.0.1` |
| `LUMINA_PORT` | Puerto del dashboard | No | `8000` |
| `LUMINA_DB` | Ruta del archivo SQLite | No | `data/lumina.db` |
| `LUMINA_LOGS` | Directorio de logs | No | `logs/` |
| `LUMINA_SECRET_KEY` | Clave para sesiones/seguridad | Sí (producción) | *(sin valor)* |
| `LUMINA_TOKEN` | Token de API para autenticar las peticiones (`X-API-Key`) | Sí (producción) | *(sin valor)* |
| `LUMINA_DEBUG` | Modo depuración | No | `0` |

> ⚠️ En **producción** (exposición a Internet) activar HTTPS y la clave secreta → [seguridad.md](seguridad.md).

---

## Configuración de bots y webs

Cada bot/web se define por **Nombre, Ruta, Comando, Tipo y Servicio** → [bots.md](desarrollo/bots.md#configuración) · [webs.md](desarrollo/webs.md).

Ejemplo:

```text
Nombre: TelegramBot
Tipo: Python
Ruta: /home/bots/telegram
Comando: python bot.py
Auto-inicio: Sí
Auto-reinicio: Sí
```

---

## Servicios del sistema

Los servicios se gestionan con **systemd**:

```bash
systemctl start <servicio>
systemctl stop <servicio>
systemctl restart <servicio>
systemctl enable <servicio>
```

→ [investigacion/systemd.md](investigacion/systemd.md)

---

## Configuración futura

- Variables de entorno por bot/web.
- Auto-restart configurable (intentos y espera) → [auto-restart.md](desarrollo/auto-restart.md).
- Permisos por usuario/dispositivo (futuro) → [seguridad.md#permisos](seguridad.md#permisos).

---

Volver a [índice](README.md).
