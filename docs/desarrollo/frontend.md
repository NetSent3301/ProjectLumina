# Frontend — ProjectLumina

## Tecnologías propuestas

- **HTML.**
- **CSS.**
- **JavaScript.**

La primera interfaz será **web** y debe ser **usable desde laptop y iPhone** (responsive).

## Plataformas

| Etapa | Plataformas |
|-------|-------------|
| Primera | Laptop principal, iPhone |
| Futuro | App nativa iOS, app Android |

La intención es que las interfaces futuras utilicen el **mismo backend** → [backend.md](backend.md).

```
          Backend Lumina
               |
     +---------+---------+
     |         |         |
    Web       iOS     Android
```

## Base actual (maqueta del dashboard)

El dashboard actual es una **maqueta con estados vacíos** (sin datos falsos) e **una sola página**: las vistas se cambian con el hash (`#/resumen`, `#/servicios`) sin recargar. Vive en:

- `web/templates/index.html` — única plantilla, contiene las vistas **resumen** y **servicios** (más las futuras registro/ajustes).
- `web/static/css/style.css` — estilos (tokens, layout, componentes, micro-animaciones).
- `web/static/js/script.js` — interacciones de la maqueta (reloj, cambio de vistas por hash, pestañas, acciones).
- `web/static/assets/` — imágenes (favicon, logo LUMINA.png).

El backend sirve la plantilla y monta la carpeta estática en `/static` con `StaticFiles` → [backend.md](backend.md).

> Rutas del panel: `/` (resumen) y `/servicios` (redirige a `/#/servicios`). La maqueta aún **no consume el backend**: todo corre en memoria y solo registra actividad real (sin datos falsos). Al iniciar v0.1 se conectará a la API REST → [api.md](api.md).

### Micro-animaciones

Transiciones sutiles que siguen `prefers-reduced-motion` → [dashboard.md](dashboard.md) · [UI - Sistema de Diseño (obsidian)](../obsidian/02%20-%20Desarrollo/UI%20-%20Sistema%20de%20Diseno.md).

## Componentes

Según [arquitectura](../arquitectura.md#estructura-propuesta-del-código):

- `web/templates/` — vistas HTML.
- `web/static/css/` — estilos.
- `web/static/js/` — lógica del navegador.
- `web/components/` — componentes reutilizables.

## Dashboard

El dashboard es el centro de control → [dashboard.md](dashboard.md).

---

Volver a [desarrollo](README.md).
