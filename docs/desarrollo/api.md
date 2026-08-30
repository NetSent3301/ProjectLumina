# API — ProjectLumina

## Comunicación inicial: REST

```
Frontend → HTTP → REST API → Backend → Servidor
```

WebSockets podrán incorporarse posteriormente para información en tiempo real.

## Seguridad de la API

Al exponerse a Internet → [seguridad](../seguridad.md), la API debe protegerse:

- HTTPS.
- Autenticación.
- Autorización.
- Gestión de credenciales.
- Protección contra accesos no autorizados.
- Control de acceso.

## Métodos típicos (conceptual)

| Acción | Concepto |
|--------|----------|
| Consultar estado | Estado de bot/web |
| Iniciar | Acción de inicio |
| Detener | Acción de detención |
| Reiniciar | Acción de reinicio |
| Ver logs | Recuperar logs |
| Métricas | Información del servidor |

> Los nombres concretos de endpoints se definirán durante la implementación.

---

Volver a [desarrollo](README.md).
