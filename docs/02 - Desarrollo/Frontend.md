# 💻 Frontend — ProjectLumina

> Interfaz web del proyecto y plataformas compatibles.

---

## Estado actual

El **dashboard consume la API REST de v0.1** (estados reales, sin datos falsos) → [Dashboard](Dashboard.md) · [API](API.md).

Estructura real del frontend:

- `web/templates/index.html` — única plantilla del panel; contiene las vistas **resumen** y **servicios** (y las futuras registro/ajustes).
- `web/static/css/style.css` — estilos (tokens, layout, componentes, micro-animaciones).
- `web/static/js/script.js` — lógica: reloj, cambio de vista por hash, pestañas bots/webs y llamadas a la API.
- `web/static/assets/` — imágenes (favicon, logo LUMINA.png).

El panel es **una sola página**: la navegación cambia de vista con el hash (`#/resumen`, `#/servicios`) sin recargar el navegador. El backend sirve la plantilla en `/` y monta `web/static` en `/static` (`StaticFiles`) → [Decisiones](../06%20-%20Registro/Decisiones.md) · [Backend](Backend.md). La ruta `/servicios` es un atajo que redirige a `/#/servicios`.

### Consume de la API v0.1

- `GET /api/servicios` — listado con estado en vivo (tarjetas, contadores y subtítulos reales).
- `POST /api/servicios/{id}/iniciar|detener|reiniciar` — botones de acción.
- `GET /api/servicios/{id}/logs` — volcado de logs en el registro de actividad.

Token: si hay `lumina_token` en `localStorage`, se envía como `X-API-Key`. **Si la API no responde, se mantienen los estados vacíos** y se avisa en el registro (no se inventan datos). Registro de cambios → [Changelog](../06%20-%20Registro/Changelog.md).

---

## Tecnologías propuestas

- **HTML.**
- **CSS.**
- **JavaScript.**

La primera interfaz será **web** y debe ser **usable desde laptop y iPhone** (responsive). → Decisión de stack en [Decisiones](../06%20-%20Registro/Decisiones.md).

---

## Plataformas

### Primera etapa
- Laptop principal. 🖥️
- iPhone. 📱

### Futuro
- Aplicación nativa para iPhone.
- Aplicación universal para Android y otros dispositivos.

**Intención:** las interfaces futuras utilizarán el **mismo backend** → [Backend](Backend.md).

```text
                  Backend Lumina
                       |
             +---------+---------+
             |         |         |
            Web       iOS     Android
```

---

## Diseño y animaciones

La identidad visual y las micro-animaciones del dashboard están descritas en [UI - Sistema de Diseno](UI%20-%20Sistema%20de%20Diseno.md):

- Entrada escalonada al cargar.
- Elevaciones al hover (tarjetas, botones, navegación).
- Flotación del estado vacío y animación de entradas del registro.
- Respeto de `prefers-reduced-motion`.

## Dashboard

El dashboard es el centro de control → [Dashboard](Dashboard.md).

---

## Relacionado

- [Backend](Backend.md) · Lógica del servidor.
- [API](API.md) · Comunicación con el backend.
- [Dashboard](Dashboard.md) · Interfaz principal.
- [UI - Sistema de Diseno](UI%20-%20Sistema%20de%20Diseno.md) · Identidad visual.
- [Bots](Bots.md) · [Webs](Webs.md) · Gestión desde la UI.
- [Requisitos](../01%20-%20Planificacion/Requisitos.md) · Plataformas requeridas.
- [Inicio](../00%20-%20Inicio/Inicio.md)
