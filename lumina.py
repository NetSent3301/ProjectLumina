# ProjectLumina - Backend mínimo (v0.1.0)

# FastAPI es un framework de Python para crear APIs.
# - Sirve la página web/ (el frontend) en la raíz /.
# - Expone el endpoint /api/health para comprobar que todo funciona.
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

# @app es la aplicación. FastAPI la usa para registrar rutas y servir la API.
app = FastAPI(title="ProjectLumina", version="0.1.0")

# Ruta absoluta a la carpeta web/ (donde está el frontend).
WEB_DIR = Path(__file__).parent / "web"


# La raíz / muestra la página web/index.html
@app.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html")


# Endpoint de verificación.
# Prueba con:  curl http://127.0.0.1:8000/api/health
@app.get("/api/health")
def health():
    """Devuelve ok si el backend está funcionando."""
    return JSONResponse({"status": "ok", "version": "0.1.0"})
