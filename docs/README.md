# Documentación de ProjectLumina

> Plataforma personal de administración remota de servidores, bots, webs y servicios.

## Índice

### Visión general
- [Estado actual](estado-actual.md) — Dónde está el proyecto y siguiente camino.
- [Visión y definición](vision.md) — Qué es ProjectLumina y hacia dónde va.
- [Objetivos](objetivos.md) — Objetivo principal, secundario e inmediato.
- [Arquitectura](arquitectura.md) — Arquitectura del MVP y evolución futura.
- [Requisitos](requisitos.md) — Requisitos funcionales, técnicos y fuera del alcance.
- [Roadmap](roadmap.md) — Hoja de ruta por versiones.
- [Seguridad](seguridad.md) — Seguridad y acceso remoto.

### Desarrollo
- [Desarrollo](desarrollo/README.md) — Visión general de desarrollo.
  - [Backend](desarrollo/backend.md)
  - [Frontend](desarrollo/frontend.md)
  - [API](desarrollo/api.md)
  - [Base de datos](desarrollo/base-de-datos.md)
  - [Dashboard](desarrollo/dashboard.md)
  - [Bots](desarrollo/bots.md)
  - [Webs](desarrollo/webs.md)
  - [Servidor](desarrollo/servidor.md)

### Operación
- [Configuración](configuracion.md) — Configuración del sistema.

### Referencia
- [Notas en Obsidian](obsidian/) — Mapa de notas enlazadas (fuente complementaria).
- [Planificación completa](obsidian/ProjectLumina_Planificacion.md)
- [Changelog](../CHANGELOG.md) — Registro de cambios.

---

## Punto de entrada

1. Empieza por [Estado actual](estado-actual.md) para saber dónde estamos.
2. Lee [Visión](vision.md) para entender el qué y el porqué.
3. Revisa [Objetivos](objetivos.md) para conocer las metas.
4. Consulta [Arquitectura](arquitectura.md) y [Requisitos](requisitos.md) para lo técnico.
5. Sigue [Roadmap](roadmap.md) para ver el plan.
6. Profundiza en [Desarrollo](desarrollo/README.md) por área.

## Inicio rápido

```bash
bash scripts/run.sh
```

- Web: http://127.0.0.1:8000/ · API: http://127.0.0.1:8000/api/health
- Estado de la base: [implementación (obsidian)](obsidian/06%20-%20Registro/Implementacion.md)
