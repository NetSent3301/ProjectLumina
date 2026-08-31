# 🌐 Webs — ProjectLumina

> Gestión de webs similar a la de bots.

---

## Objetivo

Administrar las webs del servidor **remotamente** desde el dashboard → [Control Remoto](Control%20Remoto.md).

---

## Ejemplo (tarjeta del dashboard)

```text
🌐 NetSent

Estado: 🟢 Online

[ Iniciar ]
[ Detener ]
[ Reiniciar ]
[ Logs ]
```

→ Se muestra en [Dashboard](Dashboard.md).

---

## Funciones

ProjectLumina podrá:

- Ver estado.
- Iniciar.
- Detener.
- Reiniciar.
- Consultar logs → [Dashboard](Dashboard.md).
- **Comprobar disponibilidad** (HTTP).
- Administrar el servicio asociado → [systemd](../04%20-%20Investigacion/systemd.md).
- Eventualmente **desplegar actualizaciones** → [Gestion Avanzada de Webs](Gestion%20Avanzada%20de%20Webs.md).

---

## Comprobación de disponibilidad

Lumina puede verificar que la web responde por HTTP → ligado a [detección de caídas](Acciones%20de%20Bots.md) y a futura [notificación](Notificaciones.md).

---

## Relacionado

- [Gestion Avanzada de Webs](Gestion%20Avanzada%20de%20Webs.md) · Despliegue futuro.
- [Dashboard](Dashboard.md) · Interfaz de gestión.
- [Backend](Backend.md) · Lógica de webs.
- [Servidor](Servidor.md) · Donde corren las webs.
- [Inicio](../00%20-%20Inicio/Inicio.md)
