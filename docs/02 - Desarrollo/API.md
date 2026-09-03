# 🔌 API — ProjectLumina

> Comunicación entre el frontend y el backend.

---

## Autenticación (MVP)

Todas las rutas de la API (salvo `/api/health`) exigen un **token**:

- Cabecera `X-API-Key: <token>` (o `Authorization: Bearer <token>`).
- El token vive en la configuración (`LUMINA_TOKEN` desde `.env`) → [Seguridad](../03%20-%20Seguridad/Seguridad.md).
- Sin token → `401 Unauthorized` → [Decisiones](../06%20-%20Registro/Decisiones.md).

---

## Esquema de endpoints v0.1

> Fijado en los [Requisitos](../01%20-%20Planificacion/Requisitos.md). `{id}` = id del servicio (bot o web).

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Estado del backend (sin token). |
| GET | `/api/servicios?tipo=bot\|web` | Lista de servicios con estado (sin tipo → todos). |
| POST | `/api/servicios` | Registrar un servicio. |
| GET | `/api/servicios/{id}` | Detalle y estado. |
| POST | `/api/servicios/{id}/iniciar` | Iniciar. |
| POST | `/api/servicios/{id}/detener` | Detener. |
| POST | `/api/servicios/{id}/reiniciar` | Reiniciar. |
| GET | `/api/servicios/{id}/logs?lines=100` | Últimas líneas del log. |
| GET | `/api/servidor` | Métricas: CPU, RAM, disco, red, uptime. |
| GET | `/api/servidor/procesos` | Procesos activos. |
| GET | `/api/servidor/servicios` | Servicios systemd activos. |

### Endpoints v0.2 (despliegue + terminal)

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/despliegues` | Desplegar un bot desde un repo git y dejarlo corriendo como servicio. |
| WS | `/api/terminal?token=…` | Terminal interactiva (WebSocket). Autentica con el token en el query string. |

#### `POST /api/despliegues`

Despliega un bot git (público o privado) como servicio:

```json
{
  "nombre": "mi-bot",
  "repo_url": "https://github.com/usuario/repo",          // o SSH / file://
  "token": "…",                                            // opcional, repo privado (no se guarda)
  "ruta": "/srv/bots/mi-bot",
  "comando": "python3 main.py",                            // opcional; si se omite, se autodetecta
  "auto_inicio": true,                                     // opcional, arrancar con el sistema
  "auto_reinicio": true,                                   // opcional, reiniciar si falla
  "instalar_deps": true                                    // opcional, pip/npm según el proyecto
}
```

- El panel clona el repo (con `--depth 1`), autodetecta el lenguaje y comando por defecto
  (`main.py`/`requirements.txt` → `python3 main.py`, `package.json` → `node .`,
  `go.mod` → `go run .`), crea la unidad del gestor de arranque detectado
  (systemd en Linux, OpenRC en Alpine), la habilita e inicia el bot.
- Response `201` con el servicio creado (mismo shape que `GET /api/servicios`).
- Errores del despliegue → `502` con el motivo en `detail`.
- Los repos privados se autentican con el `token` del cuerpo (usado una sola vez,
  nunca persistido).

#### `WS /api/terminal`

Abre un shell interactivo en el servidor (como el usuario del panel).

- Autenticación: `?token=<API token>`. Si `LUMINA_TOKEN` está vacío no se exige (solo dev local).
- Token erróneo → el servidor cierra con código `4401`.
- `?cwd=/ruta` (opcional): inicia el shell en un directorio concreto (p. ej. el del servicio).
- Flujo: el cliente manda texto → se escribe al PTY; el PTY manda salida → el cliente la pinta.
- Adecuado para usarse con Xterm.js en el frontend.

### Mapa con el dashboard

- "Actualizar estado" → `GET /api/servicios`.
- Pestañas bots/webs → `GET /api/servicios?tipo=bot|web`.
- Botones iniciar/detener/reiniciar → `POST /api/servicios/{id}/…`.
- Logs → `GET /api/servicios/{id}/logs`.
- Sección servidor → `GET /api/servidor`.

El registro de actividad de **Resumen** se alimenta de los resultados de estas llamadas.

---

## WebSockets

- **Terminal interactiva** (v0.2) → `WS /api/terminal` (ver arriba).
- **Futuro:** notificaciones y métricas en tiempo real → [Notificaciones](Notificaciones.md), [Dashboard](Dashboard.md).

---

## Seguridad de la API

Al exponerse a Internet → [Acceso Remoto](../03%20-%20Seguridad/Acceso%20Remoto.md), la API debe protegerse:

- ✅ HTTPS.
- ✅ Autenticación → [Autenticacion](../03%20-%20Seguridad/Autenticacion.md).
- ✅ Autorización → [Permisos](../03%20-%20Seguridad/Permisos.md).
- ✅ Gestión de credenciales.
- ✅ Protección contra accesos no autorizados.
- ✅ Control de acceso.

---

## Relacionado

- [Backend](Backend.md) · Lógica que sirve la API.
- [Frontend](Frontend.md) · Cliente de la API.
- [Acceso Remoto](../03%20-%20Seguridad/Acceso%20Remoto.md) · Exposición segura.
- [Autenticacion](../03%20-%20Seguridad/Autenticacion.md) · [Permisos](../03%20-%20Seguridad/Permisos.md) · Seguridad.
- [Dashboard](Dashboard.md) · Consumo de la API.
- [Requisitos](../01%20-%20Planificacion/Requisitos.md) · Stack que sostiene la API.
- [Inicio](../00%20-%20Inicio/Inicio.md)
