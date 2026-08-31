# 🛠️ Backend — ProjectLumina

> Tecnologías y responsabilidades del backend del proyecto.

---

## Tecnologías propuestas

- **Python.**
- **FastAPI** (elegido) → [[Decisiones#Backend con FastAPI]].

> La elección final entre Flask y FastAPI se hizo al comenzar la implementación → [[Decisiones]].

---

## Responsabilidades

El backend será responsable de:

- ✅ Recibir solicitudes del frontend.
- ✅ Consultar el estado del servidor.
- ✅ Gestionar bots → [[Bots]].
- ✅ Gestionar webs → [[Webs]].
- ✅ Gestionar servicios → [[systemd]].
- ✅ Ejecutar acciones administrativas → [[Control Remoto]].
- ✅ Devolver resultados al frontend.
- ✅ Gestionar configuraciones.
- ✅ Mantener separada la lógica de administración de la interfaz.

---

## Comunicación

- Utiliza una **API REST** → [[API]].
- WebSockets podrán incorporarse posteriormente para datos en tiempo real.

---

## Almacenamiento

- Base de datos inicial: **SQLite** → [[Base de Datos]].
- Migración a **PostgreSQL** a futuro si el proyecto crece.

---

## Interacción con el sistema

- Gestiona servicios vía **systemd** → [[systemd]].
- Ejecuta acciones administrativas → [[Control Remoto]].
- Monitoriza el servidor → [[Servidor#Información mostrada]].

---

## Posibles módulos en el código

Según [[Arquitectura#Estructura del código]]:

- `app/api/` → endpoints → [[API]].
- `app/services/` → lógica de bots y webs → [[Bots]] · [[Webs]].
- `app/models/` → modelos de datos → [[Base de Datos]].
- `app/system/` → interacción con el sistema → [[Servidor]].
- `app/config/` → configuración → [[Configuracion de Bots]].

---

## Relacionado

- [[Arquitectura]] · Estructura general.
- [[Frontend]] · Cómo se conecta la interfaz.
- [[API]] · Comunicación.
- [[Base de Datos]] · Almacenamiento.
- [[Control Remoto]] · Ejecución de acciones.
- [[Decisiones]] · Elección Flask vs FastAPI.
- [Ver planificación completa](ProjectLumina_Planificacion)
