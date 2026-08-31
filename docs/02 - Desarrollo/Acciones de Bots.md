# 🔧 Acciones de Bots — ProjectLumina

> Operaciones que se pueden realizar sobre los bots.

---

## Acciones principales (MVP)

- ▶️ **Iniciar.**
- ⏹️ **Detener.**
- 🔄 **Reiniciar.**
- 📊 **Consultar estado.**
- 📄 **Ver logs** → [Dashboard](Dashboard.md).
- 🔍 **Detectar si está activo.**
- ⚠️ **Detectar si se cayó.**

---

## Acciones posteriores

- **Auto-inicio** al arrancar el servidor.
- **Auto-reinicio** ante fallos → [Auto Restart](Auto%20Restart.md).
- **Variables de entorno.**
- **Configuración avanzada** → [Configuracion de Bots](Configuracion%20de%20Bots.md).
- **Automatización adicional.**

---

## Flujo conceptual

```text
Usuario pulsa: [ Iniciar/Detener/Reiniciar Bot ]
       ↓
Backend Lumina
       ↓
Debian ejecuta la operación
       ↓
Lumina comprueba el estado
       ↓
Dashboard actualizado 🟢/🔴
```

→ Mismo patrón que [Arquitectura](../01%20-%20Planificacion/Arquitectura.md).

---

## Relacionado

- [Bots](Bots.md) · Vista general.
- [Auto Restart](Auto%20Restart.md) · Reinicio automático.
- [Dashboard](Dashboard.md) · Dónde se ejecutan las acciones.
- [Control Remoto](Control%20Remoto.md) · Ejecución de comandos.
- [Inicio](../00%20-%20Inicio/Inicio.md)
