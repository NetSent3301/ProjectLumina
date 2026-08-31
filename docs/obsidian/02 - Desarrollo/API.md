# 🔌 API — ProjectLumina

> Comunicación entre el frontend y el backend.

---

## Autenticación (MVP)

Todas las rutas de la API (salvo `/api/health`) exigen un **token**:

- Cabecera `X-API-Key: <token>` (o `Authorization: Bearer <token>`).
- El token vive en la configuración (`LUMINA_TOKEN` desde `.env`) → [[Seguridad]].
- Sin token → `401 Unauthorized` → [[Decisiones#Seguridad MVP con token de API]].

---

## Esquema de endpoints v0.1

> Fijado en los [[Requisitos#Requisitos técnicos (definitivos)]]. `{id}` = id del servicio (bot o web).

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

### Mapa con el dashboard

- "Actualizar estado" → `GET /api/servicios`.
- Pestañas bots/webs → `GET /api/servicios?tipo=bot|web`.
- Botones iniciar/detener/reiniciar → `POST /api/servicios/{id}/…`.
- Logs → `GET /api/servicios/{id}/logs`.
- Sección servidor → `GET /api/servidor`.

El registro de actividad de **Resumen** se alimenta de los resultados de estas llamadas.

---

## WebSockets (futuro)

WebSockets podrán incorporarse **posteriormente** cuando se necesite **información en tiempo real**.

- Notificaciones en vivo → [[Notificaciones]].
- Métricas en tiempo real → [[Dashboard#Información del servidor]].

---

## Seguridad de la API

Al exponerse a Internet → [[Acceso Remoto]], la API debe protegerse:

- ✅ HTTPS.
- ✅ Autenticación → [[Autenticacion]].
- ✅ Autorización → [[Permisos]].
- ✅ Gestión de credenciales.
- ✅ Protección contra accesos no autorizados.
- ✅ Control de acceso.

---

## Relacionado

- [[Backend]] · Lógica que sirve la API.
- [[Frontend]] · Cliente de la API.
- [[Acceso Remoto]] · Exposición segura.
- [[Autenticacion]] · [[Permisos]] · Seguridad.
- [[Dashboard]] · Consumo de la API.
- [[Requisitos#Requisitos técnicos (definitivos)]] · Stack que sostiene la API.
- [Ver planificación completa](ProjectLumina_Planificacion)
