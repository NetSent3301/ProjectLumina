# 🌐 Webs — ProjectLumina

> Gestión de webs similar a la de bots.

---

## Objetivo

Administrar las webs del servidor **remotamente** desde el dashboard → [[Control Remoto]].

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

→ Se muestra en [[Dashboard#Sección de WEBS]].

---

## Funciones

ProjectLumina podrá:

- Ver estado.
- Iniciar.
- Detener.
- Reiniciar.
- Consultar logs → [[Dashboard#Logs]].
- **Comprobar disponibilidad** (HTTP).
- Administrar el servicio asociado → [[systemd]].
- Eventualmente **desplegar actualizaciones** → [[Gestion Avanzada de Webs]].

---

## Comprobación de disponibilidad

Lumina puede verificar que la web responde por HTTP → ligado a [[Acciones de Bots|detección de caídas]] y a futura [[Notificaciones|notificación]].

---

## Relacionado

- [[Gestion Avanzada de Webs]] · Despliegue futuro.
- [[Dashboard]] · Interfaz de gestión.
- [[Backend]] · Lógica de webs.
- [[Servidor]] · Donde corren las webs.
- [Ver planificación completa](ProjectLumina_Planificacion)
