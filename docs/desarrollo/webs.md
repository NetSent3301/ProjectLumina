# Webs — ProjectLumina

Las webs tendrán una **gestión similar a los bots**.

## Funciones

- Ver estado.
- Iniciar.
- Detener.
- Reiniciar.
- Consultar logs.
- **Comprobar disponibilidad** (HTTP).
- Administrar el servicio asociado.
- Eventualmente **desplegar actualizaciones**.

## Ejemplo

```
🌐 NetSent

Estado: 🟢 Online

[ Iniciar ] [ Detener ] [ Reiniciar ] [ Logs ]
```

## Gestión avanzada (futuro)

Flujo de despliegue (no obligatorio para el MVP):

```
Actualizar web → git pull → Instalar dependencias → Ejecutar procesos
→ Reiniciar servicio → Comprobar HTTP → 🟢 Online
```

## Vista en el dashboard

→ [dashboard.md](dashboard.md#sección-webs).

---

Volver a [desarrollo](README.md).
