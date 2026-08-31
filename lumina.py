# ProjectLumina - Backend mínimo (v0.1.0)

# FastAPI es un framework de Python para crear APIs.
# - Sirve la página web/ (el frontend) en la raíz /.
# - Expone el endpoint /api/health para comprobar que todo funciona.
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

# @app es la aplicación. FastAPI la usa para registrar rutas y servir la API.
app = FastAPI(title="ProjectLumina", version="0.1.0")

# Ruta absoluta a la carpeta web/ (donde está el frontend).
WEB_DIR = Path(__file__).parent / "web"

# Archivos estáticos (css, js, imágenes).
app.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")

# Páginas del panel. El frontend es una sola página: las vistas se
# cambian con el hash (#/resumen, #/servicios) sin recargar el navegador.
# Las rutas /servicios y /servicios.html se mantienen como atajos.
@app.get("/")
@app.get("/index.html", include_in_schema=False)
def index():
    return FileResponse(WEB_DIR / "templates" / "index.html")

@app.get("/servicios")
@app.get("/servicios.html", include_in_schema=False)
def servicios():
    return RedirectResponse("/#/servicios")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse(WEB_DIR / "static" / "assets" / "favicon.ico")

# Endpoint de verificación.
# Prueba con:  curl http://127.0.0.1:8000/api/health
@app.get("/api/health")
def health():
    """Devuelve ok si el backend está funcionando."""
    return JSONResponse({"status": "ok", "version": "0.1.0"})
