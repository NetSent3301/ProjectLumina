# 🗄️ Base de Datos — ProjectLumina

> Almacenamiento del proyecto.

---

## Elección inicial: SQLite

Inicialmente se utilizará **SQLite**, alojado en `data/lumina.db` → [Arquitectura](../01%20-%20Planificacion/Arquitectura.md).

### Ventaja
- Simple, sin servidor adicional.
- Suficiente para un MVP personal.

---

## Datos almacenados

Podrá almacenar configuraciones como:

- ✅ Bots → [Bots](Bots.md) · [Configuracion de Bots](Configuracion%20de%20Bots.md).
- ✅ Webs → [Webs](Webs.md).
- ✅ Rutas.
- ✅ Comandos.
- ✅ Opciones de automatización → [Auto Restart](Auto%20Restart.md).
- ✅ Estados.
- ✅ Configuración de servicios → [systemd](../04%20-%20Investigacion/systemd.md).

---

## Migración futura: PostgreSQL

Si el proyecto **crece considerablemente** se podrá migrar a **PostgreSQL**.

- Escalabilidad → [Roadmap](../01%20-%20Planificacion/Roadmap.md).
- Multi-servidor → mayor carga y concurrencia.

---

## Relacionado

- [Backend](Backend.md) · Usa la BD.
- [Arquitectura](../01%20-%20Planificacion/Arquitectura.md) · Ubicación de `lumina.db`.
- [Configuracion de Bots](Configuracion%20de%20Bots.md) · Estructura típica guardada.
- [Decisiones](../06%20-%20Registro/Decisiones.md) · Decisión de elegir SQLite.
- [Inicio](../00%20-%20Inicio/Inicio.md)
