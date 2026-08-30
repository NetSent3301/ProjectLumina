# 🔧 Acciones de Bots — ProjectLumina

> Operaciones que se pueden realizar sobre los bots.

---

## Acciones principales (MVP)

- ▶️ **Iniciar.**
- ⏹️ **Detener.**
- 🔄 **Reiniciar.**
- 📊 **Consultar estado.**
- 📄 **Ver logs** → [[Dashboard#Logs]].
- 🔍 **Detectar si está activo.**
- ⚠️ **Detectar si se cayó.**

---

## Acciones posteriores

- **Auto-inicio** al arrancar el servidor.
- **Auto-reinicio** ante fallos → [[Auto Restart]].
- **Variables de entorno.**
- **Configuración avanzada** → [[Configuracion de Bots]].
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

→ Mismo patrón que [[Arquitectura#Ejemplo de flujo]].

---

## Relacionado

- [[Bots]] · Vista general.
- [[Auto Restart]] · Reinicio automático.
- [[Dashboard]] · Dónde se ejecutan las acciones.
- [[Control Remoto]] · Ejecución de comandos.
- [Ver planificación completa](ProjectLumina_Planificacion)
