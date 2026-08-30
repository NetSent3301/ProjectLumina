# 🗄️ Base de Datos — ProjectLumina

> Almacenamiento del proyecto.

---

## Elección inicial: SQLite

Inicialmente se utilizará **SQLite**, alojado en `data/lumina.db` → [[Arquitectura#Estructura del código]].

### Ventaja
- Simple, sin servidor adicional.
- Suficiente para un MVP personal.

---

## Datos almacenados

Podrá almacenar configuraciones como:

- ✅ Bots → [[Bots]] · [[Configuracion de Bots]].
- ✅ Webs → [[Webs]].
- ✅ Rutas.
- ✅ Comandos.
- ✅ Opciones de automatización → [[Auto Restart]].
- ✅ Estados.
- ✅ Configuración de servicios → [[systemd]].

---

## Migración futura: PostgreSQL

Si el proyecto **crece considerablemente** se podrá migrar a **PostgreSQL**.

- Escalabilidad → [[Roadmap#Etapas futuras]].
- Multi-servidor → mayor carga y concurrencia.

---

## Relacionado

- [[Backend]] · Usa la BD.
- [[Arquitectura]] · Ubicación de `lumina.db`.
- [[Configuracion de Bots]] · Estructura típica guardada.
- [[Decisiones]] · Decisión de elegir SQLite.
- [Ver planificación completa](ProjectLumina_Planificacion)
