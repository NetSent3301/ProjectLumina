# Changelog

Todos los cambios notables de ProjectLumina se documentarán en este archivo.

## [v0.1.0-dev] - 2026-08-30

### Añadido
- Dashboard web base en **una sola página** (`web/templates/index.html`):
  - **Resumen** (`#/resumen`): cabecera de estado, tarjeta vacía "conectar un servicio" y registro de actividad.
  - **Servicios** (`#/servicios`): selector bots/webs con pestañas y estados vacíos por tipo.
  - Sidebar compartida con identidad y navegación; cambio de vista sin recargar (hash).
- Estilos y lógica separados: `web/static/css/style.css` y `web/static/js/script.js`.
- Micro-animaciones: entrada escalonada al cargar, elevaciones al hover, flotación de los estados vacíos, animación de entradas del registro y respeto de `prefers-reduced-motion`.
- Backend con **FastAPI** (`lumina.py`).
  - Endpoint `GET /api/health` de verificación.
  - Sirve la plantilla en `/`; `/servicios` redirige a `/#/servicios`; estáticos montados en `/static`.
- Script de arranque `scripts/run.sh` (crea venv, instala dependencias y arranca).
- Test básico del endpoint (`pruebas/test_health.py`).
- Entorno virtual `.venv` y `requirements.txt` (fastapi, uvicorn, pytest, httpx).
- Formato `.env.example` con variables opcionales (incluye `LUMINA_TOKEN`).
- Repositorio Git inicializado (rama `main`).
- Logo **LUMINA** en la sidebar (blanco con glow de acento y palpitación sutil que respeta `prefers-reduced-motion`).
- **Requisitos técnicos cerrados**: stack definitivo, esquema de endpoints v0.1 y modelo de datos → [requisitos.md](docs/requisitos.md#requisitos-técnicos-definitivos) · [api.md](docs/desarrollo/api.md) · [base-de-datos.md](docs/desarrollo/base-de-datos.md).
- **Arquitectura definitiva del MVP** (estructura `app/` en capas, flujo de acciones, despliegue systemd y transición desde `lumina.py`) → [arquitectura.md](docs/arquitectura.md#arquitectura-definitiva-del-mvp).
- README renovado: resumen, stack definitivo, estructura del proyecto, inicio rápido y estado por fases.

### Cambiado
- Frontend reorganizado: `web/index.html` → `web/templates/index.html`; CSS, JS y assets en `web/static/`.
- Panel convertido a **una sola página**: las vistas (resumen/servicios) cambian con el hash sin recargar; `/servicios` redirige a `/#/servicios`.
- Eliminados los datos de ejemplo de la UI (maqueta con estados vacíos, sin tira de KPIs ni métricas inventadas).
- Elegido **FastAPI** como framework de backend (decisión registrada).

### Corregido
- Los archivos CSS y JS no cargaban (404): montado `/static` con `StaticFiles` en `lumina.py`.

## [No publicado]

### Añadido
- Estructura inicial del proyecto.
- Documentación general completa en `docs/` (visión, objetivos, arquitectura, requisitos, roadmap, seguridad, desarrollo, investigación, configuración, estado actual).
- Mapa de notas en Obsidian (`docs/obsidian/` y bóveda local).
- Diagramas Mermaid e iconos en documentación y README.
- `PLANNING.md` como índice de planificación.
