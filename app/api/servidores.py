"""Endpoints de servidores remotos (agentes Lumina) y estado de conexión.
"""

from fastapi import APIRouter, Response, status

from ..models.servidor import ServidorCreate
from ..services import servidores

router = APIRouter()


@router.get("/servidores")
def listar_servidores():
    """Servidores remotos (agentes Lumina) con su conexión en vivo."""
    return servidores.listar()


@router.post("/servidores", status_code=status.HTTP_201_CREATED)
def crear_servidor(datos: ServidorCreate):
    "Registra un agente Lumina remoto."
    return servidores.crear(datos)


@router.delete("/servidores/{servidor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_servidor(servidor_id: int):
    servidores.eliminar(servidor_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/conexion")
def estado_conexion():
    """Resumen de conexión: servidor principal y servidores remotos."""
    return servidores.resumen_conexion()