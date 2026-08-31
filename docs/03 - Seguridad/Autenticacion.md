# 🔐 Autenticacion — ProjectLumina

> Cómo se identifica al usuario en el sistema.

---

## MVP

**No habrá sistema de usuarios.**

ProjectLumina será una **herramienta personal** destinada al propietario del servidor.

---

## MVP — token de API

La API de v0.1 se protege con un **token de API**:

- Header `X-API-Key: <token>` (o `Authorization: Bearer <token>`) en todas las rutas salvo `/api/health`.
- El token se define en la configuración (`LUMINA_TOKEN` desde `.env`) → [Configuracion](../02%20-%20Desarrollo/Configuracion.md).
- Si `LUMINA_TOKEN` está vacío (desarrollo local), la autenticación queda **desactivada** → [API](../02%20-%20Desarrollo/API.md).
- Si se expone a Internet: **HTTPS obligatorio** (cifrado) además del token → [Acceso Remoto](Acceso%20Remoto.md).

## Futuro

Podrán incorporarse:

- Login.
- Autenticación.
- Usuarios → [Usuarios](Usuarios.md).
- Roles.
- Permisos → [Permisos](Permisos.md).
- Dispositivos autorizados.

> Esto será especialmente importante cuando el proyecto llegue a administrar **servidores de terceros** → [Roadmap](../01%20-%20Planificacion/Roadmap.md).

---

## ¿Cuándo se necesitará?

- Cuando se exponga a Internet → [Acceso Remoto](Acceso%20Remoto.md).
- Cuando haya multiusuario o servidores de terceros → [Requisitos](../01%20-%20Planificacion/Requisitos.md).

---

## Relacionado

- [Usuarios](Usuarios.md) · Modelo de usuarios.
- [Permisos](Permisos.md) · Qué puede hacer cada usuario.
- [Acceso Remoto](Acceso%20Remoto.md) · Necesidad de autenticar.
- [API](../02%20-%20Desarrollo/API.md) · Seguridad de endpoints.
- [Inicio](../00%20-%20Inicio/Inicio.md)
