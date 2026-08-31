# Base de datos — ProjectLumina

## Elección: SQLite con SQLModel

- **SQLite** (`data/lumina.db`) — simple, sin servidor adicional, suficiente para el MVP → [requisitos](../requisitos.md#requisitos-técnicos-definitivos).
- **SQLModel** (SQLAlchemy + Pydantic) — modelos tipados y convalidados por Pydantic, integrados con FastAPI.
- Migración futura a **PostgreSQL** solo si el proyecto crece considerablemente.

## Modelo de datos (v0.1)

**Una sola tabla `servicios`** con el campo `tipo` distinguiendo bot y web (ambos comparten estructura; la web añade URL de chequeo).

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | int (PK) | Identificador único. |
| `tipo` | texto | `bot` o `web`. |
| `nombre` | texto | Nombre visible en el dashboard. |
| `ruta` | texto | Directorio de trabajo del servicio. |
| `comando` | texto | Comando a ejecutar en `ruta`. |
| `servicio` | texto | Nombre de la unidad systemd asociada. |
| `check_url` | texto (nullable) | URL para comprobar disponibilidad (solo webs). |
| `auto_inicio` | bool | Iniciar al arrancar el sistema (v0.2+). |
| `auto_reinicio` | bool | Reiniciar si se cae (v0.2+). |
| `creado` | datetime | Fecha de alta. |
| `ultimo_estado` | tekst | Estado observado: online / offline / reiniciando. |
| `ultimo_cambio` | datetime | Cuándo cambió `ultimo_estado`. |

## Datos asociados (v0.1)

- El **estado en vivo** (PID, CPU, RAM de cada servicio, logs) NO se persiste: se consulta al sistema (psutil/systemd) al momento → [servidor](../desarrollo/servidor.md).
- Los **logs** se leen de systemd/ficheros; solo se guardan los campos de configuración anteriores.

## Migración futura

- A **PostgreSQL** cuando el proyecto crezca (escalabilidad, multi-servidor).
- Los modelos SQLModel hacen la migración más sencilla que con SQL crudo.

---

Volver a [desarrollo](README.md).