# 🖥️ Configuracion — ProjectLumina

> Guía para configurar el servidor y el dashboard.

---

## Vista general

ProjectLumina se ejecuta sobre un servidor **Debian 13** → [Servidor](Servidor.md).

La configuración se distribuye en:

- **Archivo de entorno** (variables) — configuración sensible y de despliegue.
- **Base de datos SQLite** → [Base de Datos](Base%20de%20Datos.md) — configuraciones de bots/webs.
- **Servicios systemd** → [systemd](../04%20-%20Investigacion/systemd.md) — gestión de procesos.

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

> ⚠️ En **producción** (exposición a Internet) activar HTTPS y la clave secreta → [Seguridad](../03%20-%20Seguridad/Seguridad.md).

---

## Configuración de bots y webs

Cada bot/web se define por **Nombre, Ruta, Comando, Tipo y Servicio** → [Bots](Bots.md) · [Webs](Webs.md).

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

```text
systemctl start <servicio>
systemctl stop <servicio>
systemctl restart <servicio>
systemctl enable <servicio>
```

→ [systemd](../04%20-%20Investigacion/systemd.md)

---

## Configuración futura

- Variables de entorno por bot/web.
- Auto-restart configurable (intentos y espera) → [Auto Restart](Auto%20Restart.md).
- Permisos por usuario/dispositivo (futuro) → [Permisos](../03%20-%20Seguridad/Permisos.md).

---

## Relacionado

- [Servidor](Servidor.md) · Dónde corre el sistema.
- [Base de Datos](Base%20de%20Datos.md) · Almacenamiento.
- [systemd](../04%20-%20Investigacion/systemd.md) · Gestión de servicios.
- [Seguridad](../03%20-%20Seguridad/Seguridad.md) · Protección en producción.
- [Inicio](../00%20-%20Inicio/Inicio.md) · Mapa general.