# API — ProjectLumina

## Comunicación: REST + JSON

```
Frontend → HTTP/JSON → REST API → Backend → Servidor (systemd)
```

- WebSockets **no** se usan en el MVP: el frontend consulta por polling → [requisitos](../requisitos.md#requisitos-técnicos-definitivos).
- Documentación automática: `/docs` (Swagger) y `/redoc`, generadas por FastAPI.
- Formato de respuesta: JSON. Errores con `HTTP 4xx/5xx` y cuerpo `{"detail": "..."}`.

## Autenticación (MVP)

Todas las rutas de la API (salvo `/api/health`) exigen un **token**:

- Cabecera `X-API-Key: <token>` (o `Authorization: Bearer <token>`).
- El token vive en la configuración (`LUMINA_TOKEN` desde `.env`).
- Sin este token → `401 Unauthorized`.

## Esquema de endpoints v0.1

Rutas agrupadas por recurso. `{id}` es el id del servicio (bot o web).

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Estado del backend (sin token). |
| GET | `/api/servicios?tipo=bot\|web` | Lista de servicios con su estado (sin tipo → todos). |
| POST | `/api/servicios` | Registrar un servicio (body: nombre, tipo, ruta, comando, servicio, check_url…). |
| GET | `/api/servicios/{id}` | Detalle y estado de un servicio. |
| POST | `/api/servicios/{id}/iniciar` | Iniciar servicio. |
| POST | `/api/servicios/{id}/detener` | Detener servicio. |
| POST | `/api/servicios/{id}/reiniciar` | Reiniciar servicio. |
| GET | `/api/servicios/{id}/logs?lines=100` | Últimas líneas del log. |
| GET | `/api/servidor` | Métricas: CPU, RAM, disco, red, uptime. |
| GET | `/api/servidor/procesos` | Procesos activos. |
| GET | `/api/servidor/servicios` | Servicios systemd activos. |

### Mapa con el dashboard

- "Actualizar estado" → `GET /api/servicios` (refresca estados).
- Pestañas bots/webs → `GET /api/servicios?tipo=bot|web`.
- Botones iniciar/detener/reiniciar → `POST /api/servicios/{id}/…` (+ `GET /api/servicios/{id}` para confirmar).
- Logs → `GET /api/servicios/{id}/logs`.
- Sección servidor → `GET /api/servidor`.

> El registro de actividad de la vista **Resumen** se alimenta de los resultados de estas llamadas (eventos reales del backend).

## Métodos típicos (conceptual)

| Acción | Concepto |
|--------|----------|
| Consultar estado | `GET /api/servicios` |
| Iniciar | `POST /api/servicios/{id}/iniciar` |
| Detener | `POST /api/servicios/{id}/detener` |
| Reiniciar | `POST /api/servicios/{id}/reiniciar` |
| Ver logs | `GET /api/servicios/{id}/logs` |
| Métricas | `GET /api/servidor` |

## Seguridad de la API

Al exponerse a Internet → [seguridad](../seguridad.md):

- HTTPS.
- Token de API (`LUMINA_TOKEN`).
- Toda ejecución remota es una **operación privilegiada** → [control-remoto](control-remoto.md).

> Los nombres de endpoints quedan fijados para v0.1; se podrán ajustar solo con registro en [Decisiones.md](../obsidian/06%20-%20Registro/Decisiones.md).

---

Volver a [desarrollo](README.md).