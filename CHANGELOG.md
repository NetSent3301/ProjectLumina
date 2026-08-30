# Changelog

Todos los cambios notables de ProjectLumina se documentarán en este archivo.

## [v0.1.0-dev] - 2026-08-30

### Añadido
- Backend mínimo con **FastAPI** (`lumina.py`).
  - Endpoint `GET /api/health` de verificación.
  - Sirve la página `web/index.html` en la raíz `/`.
- Frontend mínimo (`web/index.html`) que comprueba la conexión con el backend.
- Script de arranque `scripts/run.sh` (crea venv, instala dependencias y arranca).
- Test básico del endpoint (`pruebas/test_health.py`).
- Entorno virtual `.venv` y `requirements.txt` (fastapi, uvicorn, pytest, httpx).
- Formato `.env.example` con variables opcionales.
- Repositorio Git inicializado (rama `main`).

### Cambiado
- Elegido **FastAPI** como framework de backend (decisión registrada).

## [No publicado]

### Añadido
- Estructura inicial del proyecto.
- Documentación general completa en `docs/` (visión, objetivos, arquitectura, requisitos, roadmap, seguridad, desarrollo, investigación, configuración, estado actual).
- Mapa de notas en Obsidian (`docs/obsidian/` y bóveda local).
- Diagramas Mermaid e iconos en documentación y README.
- `PLANNING.md` como índice de planificación.
