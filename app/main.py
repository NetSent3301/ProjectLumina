"""ProjectLumina - aplicación FastAPI.

Sustituye al antiguo `lumina.py`: además de servir el frontend y los
estáticos, expone la API REST de v0.1 (estructura en capas de la
arquitectura definitiva del MVP).

Rutas:
- Frontend:  /               (una sola página, vistas por hash)
- Estáticos: /static
- API:       /api/health (sin token), /api/servicios*, /api/servidor*
"""

from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from .api import servidor, servicios
from .api.auth import require_token
from .config import get_settings
from .db import init_db

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"


def create_app() -> FastAPI:
    init_db()

    app = FastAPI(title="ProjectLumina", version="0.1.0")

    app.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")

    @app.get("/")
    @app.get("/index.html", include_in_schema=False)
    def index():
        return FileResponse(WEB_DIR / "templates" / "index.html")

    @app.get("/servicios")
    @app.get("/servicios.html", include_in_schema=False)
    def servicios_atajo():
        return RedirectResponse("/#/servicios")

    @app.get("/favicon.ico", include_in_schema=False)
    def favicon():
        return FileResponse(WEB_DIR / "static" / "assets" / "favicon.ico")

    @app.get("/api/health")
    def health():
        """Estado del backend (no requiere token)."""
        return JSONResponse({"status": "ok", "version": "0.1.0"})

    # El resto de la API requiere token cuando LUMINA_TOKEN está configurado.
    app.include_router(
        servicios.router,
        prefix="/api",
        tags=["servicios"],
        dependencies=[Depends(require_token)],
    )
    app.include_router(
        servidor.router,
        prefix="/api",
        tags=["servidor"],
        dependencies=[Depends(require_token)],
    )

    return app


app = create_app()