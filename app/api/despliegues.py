"""Endpoints de despliegue de bots desde repositorios git.

Permite entregar solo nombre + URL del repo y que Lumina clone, instale
dependencias, cree la unidad systemd, la habilite e inicie el bot.
"""

from fastapi import APIRouter, HTTPException, status

from ..models.despliegue import DespliegueGit
from ..services import despliegues

router = APIRouter()


@router.post("/despliegues", status_code=status.HTTP_201_CREATED)
def desplegar_bot(datos: DespliegueGit):
    """Despliega un bot git y lo deja corriendo como servicio."""
    try:
        return despliegues.desplegar(datos)
    except HTTPException:
        raise
    except Exception as error:  # noqa: BLE001 - fallo inesperado del despliegue
        raise HTTPException(status_code=502, detail=f"el despliegue falló: {error}")
