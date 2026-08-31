# 💻 Frontend — ProjectLumina

> Interfaz web del proyecto y plataformas compatibles.

---

## Estado actual

El **dashboard web está en maqueta** con estados vacíos (sin datos falsos) → [[Dashboard#Base actual]].

Estructura real del frontend:

- `web/templates/index.html` — única plantilla del panel; contiene las vistas **resumen** y **servicios** (y las futuras registro/ajustes).
- `web/static/css/style.css` — estilos (tokens, layout, componentes, micro-animaciones).
- `web/static/js/script.js` — interacciones de la maqueta (reloj, cambio de vista por hash, pestañas, acciones).
- `web/static/assets/` — imágenes (favicon, logo LUMINA.png).

El panel es **una sola página**: la navegación cambia de vista con el hash (`#/resumen`, `#/servicios`) sin recargar el navegador. El backend sirve la plantilla en `/` y monta `web/static` en `/static` (`StaticFiles`) → [[Decisiones#Sirviendo estáticos con StaticFiles]] · [[Backend]]. La ruta `/servicios` es un atajo que redirige a `/#/servicios`.

---

## Tecnologías propuestas

- **HTML.**
- **CSS.**
- **JavaScript.**

La primera interfaz será **web** y debe ser **usable desde laptop y iPhone** (responsive). → Decisión de stack en [[Decisiones#Frontend vanilla]].

---

## Plataformas

### Primera etapa
- Laptop principal. 🖥️
- iPhone. 📱

### Futuro
- Aplicación nativa para iPhone.
- Aplicación universal para Android y otros dispositivos.

**Intención:** las interfaces futuras utilizarán el **mismo backend** → [[Backend]].

```text
                  Backend Lumina
                       |
             +---------+---------+
             |         |         |
            Web       iOS     Android
```

---

## Diseño y animaciones

La identidad visual y las micro-animaciones del dashboard están descritas en [[UI - Sistema de Diseno]]:

- Entrada escalonada al cargar.
- Elevaciones al hover (tarjetas, botones, navegación).
- Flotación del estado vacío y animación de entradas del registro.
- Respeto de `prefers-reduced-motion`.

## Dashboard

El dashboard es el centro de control → [[Dashboard]].

---

## Relacionado

- [[Backend]] · Lógica del servidor.
- [[API]] · Comunicación con el backend.
- [[Dashboard]] · Interfaz principal.
- [[UI - Sistema de Diseno]] · Identidad visual.
- [[Bots]] · [[Webs]] · Gestión desde la UI.
- [[Requisitos]] · Plataformas requeridas.
- [Ver planificación completa](ProjectLumina_Planificacion)
