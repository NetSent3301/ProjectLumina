# 🛠️ Backend — ProjectLumina

> Tecnologías y responsabilidades del backend del proyecto.

---

## Tecnologías propuestas

- **Python.**
- **FastAPI** (elegido) → [Decisiones](../06%20-%20Registro/Decisiones.md).

> La elección final entre Flask y FastAPI se hizo al comenzar la implementación → [Decisiones](../06%20-%20Registro/Decisiones.md).

---

## Responsabilidades

El backend será responsable de:

- ✅ Recibir solicitudes del frontend.
- ✅ Consultar el estado del servidor.
- ✅ Gestionar bots → [Bots](Bots.md).
- ✅ Gestionar webs → [Webs](Webs.md).
- ✅ Gestionar servicios → [systemd](../04%20-%20Investigacion/systemd.md).
- ✅ Ejecutar acciones administrativas → [Control Remoto](Control%20Remoto.md).
- ✅ Devolver resultados al frontend.
- ✅ Gestionar configuraciones.
- ✅ Mantener separada la lógica de administración de la interfaz.

---

## Comunicación

- Utiliza una **API REST** → [API](API.md).
- WebSockets podrán incorporarse posteriormente para datos en tiempo real.

---

## Almacenamiento

- Base de datos inicial: **SQLite** → [Base de Datos](Base%20de%20Datos.md).
- Migración a **PostgreSQL** a futuro si el proyecto crece.

---

## Interacción con el sistema

- Gestiona servicios vía **systemd** → [systemd](../04%20-%20Investigacion/systemd.md).
- Ejecuta acciones administrativas → [Control Remoto](Control%20Remoto.md).
- Monitoriza el servidor → [Servidor](Servidor.md).

---

## Posibles módulos en el código

Según [Arquitectura](../01%20-%20Planificacion/Arquitectura.md):

- `app/api/` → endpoints → [API](API.md).
- `app/services/` → lógica de bots y webs → [Bots](Bots.md) · [Webs](Webs.md).
- `app/models/` → modelos de datos → [Base de Datos](Base%20de%20Datos.md).
- `app/system/` → interacción con el sistema → [Servidor](Servidor.md).
- `app/config/` → configuración → [Configuracion de Bots](Configuracion%20de%20Bots.md).

---

## Relacionado

- [Arquitectura](../01%20-%20Planificacion/Arquitectura.md) · Estructura general.
- [Frontend](Frontend.md) · Cómo se conecta la interfaz.
- [API](API.md) · Comunicación.
- [Base de Datos](Base%20de%20Datos.md) · Almacenamiento.
- [Control Remoto](Control%20Remoto.md) · Ejecución de acciones.
- [Decisiones](../06%20-%20Registro/Decisiones.md) · Elección Flask vs FastAPI.
- [Inicio](../00%20-%20Inicio/Inicio.md)
