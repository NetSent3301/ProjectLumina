# 🔌 API — ProjectLumina

> Comunicación entre el frontend y el backend.

---

## Comunicación inicial: REST

La comunicación inicial utilizará una **API REST**.

```text
Frontend → HTTP → REST API → Backend → Servidor
```

- El frontend ([[Frontend]]) envía solicitudes HTTP.
- La API enruta al backend ([[Backend]]).
- El backend interactúa con el servidor ([[Servidor]]).

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

## Métodos típicos (conceptual)

| Acción | Concepto |
|--------|----------|
| Consultar estado | `GET` estado de bot/web |
| Iniciar | Acción de inicio |
| Detener | Acción de detención |
| Reiniciar | Acción de reinicio |
| Ver logs | Recuperar logs → [[Dashboard#Logs]] |
| Métricas | Consultar Inf. del servidor |

> Los nombres concretos de endpoints se definirán en la implementación.

---

## Relacionado

- [[Backend]] · Lógica que sirve la API.
- [[Frontend]] · Cliente de la API.
- [[Acceso Remoto]] · Exposición segura.
- [[Autenticacion]] · [[Permisos]] · Seguridad.
- [[Dashboard]] · Consumo de la API.
- [Ver planificación completa](ProjectLumina_Planificacion)
