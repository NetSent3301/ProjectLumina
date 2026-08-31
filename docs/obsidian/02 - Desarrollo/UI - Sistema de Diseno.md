# 🎨 UI - Sistema de Diseño

> Identidad visual, tokens y micro-animaciones del dashboard de ProjectLumina.

---

## Concepto

Interfaz **dark-first** orientada a sesiones largas (paneles operativos de monitorización). La elevación se consigue con **luminosidad**, no sombras; el color se reserva como **señal de estado**.

---

## Tokens (paleta)

Configurados como variables CSS en `web/static/css/style.css` → [[Frontend#Estado actual]].

| Token | Valor | Uso |
|-------|-------|-----|
| `--navy-900` | `#080b10` | Fondo base |
| `--navy-800` | `#0e141b` | Superficie (sidebar/main) |
| `--navy-700` | `#131c26` | Tarjetas |
| `--navy-600` | `#182231` | Elementos elevados |
| `--text` | `#eef1f3` | Texto principal |
| `--muted` | `#8b98a2` | Texto secundario |
| `--accent` | `#5b84ab` | Acento (brand/chrome) |
| `--ok` | `#5fbf94` | Estado correcto |
| `--warn` | `#d3a75b` | Advertencia |
| `--danger` | `#d3798a` | Error/acciones destructivas |
| gradientes glow | violeta/magenta/azul | Acentos y bordes de tarjeta |

### Principios de color

- **Un solo acento saturado** en chrome y acciones primarias; todo lo demás desaturado.
- **Color = estado**: verde/ámbar/rojo solo para señales, siempre acompañados de icono o texto.
- Semánticos ajustados para fondo oscuro (evitar «neones») y contraste WCAG AA.

---

## Tipografía

- `--font-sans`: **Inter** (títulos y cuerpo).
- `--font-mono`: **IBM Plex Mono** (valores, reloj, etiquetas técnicas).
- Texto sobre dark en blanco 85–92%, no `#fff` puro.

---

## Elevación (depth por luminosidad)

Las capas se separan subiendo la luminosidad una «capa» por nivel (base → tarjeta → modal), en lugar de sombras, que apenas se perciben en oscuro.

---

## Componentes

- **Botones**: pill (`border-radius: 999px`); primario con gradiente de acento, fantasma transparente, enlace sin borde (`link-btn`).
- **Tarjetas**: `border-radius: 20px`; borde = gradiente de acento (`card-edge`), fondo de luminosidad.
- **Pestañas** (bots/webs): contenedor pill con borde gradiente; activa con gradiente de acento e icono.
- **Chip**: etiqueta monoespaciada para indicar disponibilidad (p. ej. «disponible en v0.1»).
- **Estado vacío (hero)**: tarjeta a ancho completo, borde discontinuo, icono flotante, chip informativo.

## Micro-animaciones

- **Entrada escalonada** al cargar (topbar → cabeceras → tarjetas → registro), `riseIn` con easing suave.
- **Hover**: elevación sutil (tarjetas, botones), desplazamiento de la navegación e iconos con escala.
- **Estado vacío**: el icono «＋» flota suavemente (`floatIcon`).
- **Registro de actividad**: las entradas nuevas aparecen deslizándose (`logIn`).
- **Botón de refresco**: giro del icono mientras carga.
- **Respeto de accesibilidad**: todo se desactiva con `prefers-reduced-motion`.

---

## Estados vacíos (sin datos falsos)

Ante ausencia de datos reales la UI muestra estado neutro, nunca datos inventados:

- «sin servicios registrados» en la cabecera.
- Tarjeta vacía «conectar un servicio».
- Registro de actividad vacío.

---

## Responsive

- Escritorio: sidebar fija + contenido (`grid-template-columns: 260px 1fr`).
- Móvil (≤880px): una columna; la sidebar colapsa a una franja con marca y reloj → [[Frontend#Plataformas]].

---

## Relacionado

- [[Frontend]] · dónde vive el código de la UI.
- [[Dashboard]] · pantalla que usa este sistema.
- [[Decisiones#Frontend vanilla]] · por qué HTML/CSS/JS.
- [[Principios Tecnicos]] · simplicidad y observabilidad.
- [Ver planificación completa](ProjectLumina_Planificacion)