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
