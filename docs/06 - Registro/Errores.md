# 🐛 Errores — ProjectLumina

> Registro de errores encontrados y su resolución.

---

## Cómo registrar

Para cada error añade una entrada como la siguiente:

```text
## [Fecha] - Descripción breve

- **Severidad:** (Baja / Media / Alta / Crítica)
- **Estado:** (Abierto / En progreso / Resuelto / Cerrado)
- **Contexto:** (dónde ocurre, versión)
- **Causa:**
- **Solución:**
- **Relacionado:** (enlace a nota relacionada, ej. `[Backend](../02%20-%20Desarrollo/Backend.md)`)
```

---

## Errores abiertos

> _(Ninguno por ahora)_

---

## Errores resueltos

### [2026-08-30] - CSS y JS del dashboard no cargaban
- **Severidad:** Alta (el panel aparecía sin estilos).
- **Estado:** Resuelto.
- **Contexto:** frontend reorganizado a `web/templates/` + `web/static/`; `lumina.py` solo servía `/`, `/favicon.ico` y `/api/health`.
- **Causa:** los archivos estáticos no estaban montados; `/static/css/style.css` y `/static/js/script.js` devolvían 404.
- **Solución:** montar la carpeta estática con `app.mount("/static", StaticFiles(...), name="static")` → [Decisiones](Decisiones.md).
- **Relacionado:** [Frontend](../02%20-%20Desarrollo/Frontend.md) · [Backend](../02%20-%20Desarrollo/Backend.md) · [Implementacion](Implementacion.md).

### [2026-08-30] - Datos de ejemplo en la UI del dashboard
- **Severidad:** Baja.
- **Estado:** Resuelto.
- **Contexto:** la maqueta mostraba servicios, logs y métricas inventadas.
- **Causa:** datos de ejemplo incrustados en la maqueta para visualizar el diseño.
- **Solución:** eliminar los datos falsos y usar **estados vacíos** (sin servicios registrados, sin conectar, `—`) → [Dashboard](../02%20-%20Desarrollo/Dashboard.md).
- **Relacionado:** [Frontend](../02%20-%20Desarrollo/Frontend.md) · [Changelog](Changelog.md).

---

## Buenas prácticas

- Registrar **errores reales** durante desarrollo y testing → [Tareas](../01%20-%20Planificacion/Tareas.md).
- Añadir al [Changelog](Changelog.md) cuando se corrija.
- Ligar con la decisión de cómo se resolvió → [Decisiones](Decisiones.md).

---

## Relacionado

- [Changelog](Changelog.md) · Registro de cambios.
- [Decisiones](Decisiones.md) · Decisiones técnicas.
- [Tareas](../01%20-%20Planificacion/Tareas.md) · Fase de testing.
- [Inicio](../00%20-%20Inicio/Inicio.md)
