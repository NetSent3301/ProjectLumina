"""Punto de entrada compatible con la base inicial.

En v0.1 la aplicación vive en `app.main` (estructura en capas). Este
archivo se mantiene como atajo para que el arranque y las referencias
antiguas sigan funcionando:  uvicorn lumina:app
"""

from app.main import app

__all__ = ["app"]