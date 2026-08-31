"""Endpoints de servicios (bots y webs). Esquema en docs/desarrollo/api.md.
"""

from typing import Optional

from fastapi import APIRouter, Query, Response, status

from ..models.servicio import ServicioCreate, ServicioUpdate
from ..services import servicios

router = APIRouter()


@router.get("/servicios")
def listar_servicios(tipo: Optional[str] = Query(default=None)):
    """Lista servicios con su estado en vivo."""
    return servicios.listar(tipo=tipo)


@router.post("/servicios", status_code=status.HTTP_201_CREATED)
def crear_servicio(datos: ServicioCreate):
    """Registra un servicio nuevo."""
    return servicios.crear(datos)


@router.get("/servicios/{servicio_id}")
def detalle_servicio(servicio_id: int):
    return servicios.detalle(servicio_id)


@router.delete("/servicios/{servicio_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_servicio(servicio_id: int):
    servicios.eliminar(servicio_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/servicios/{servicio_id}")
def editar_servicio(servicio_id: int, cambios: ServicioUpdate):
    return servicios.actualizar(servicio_id, cambios)


@router.post("/servicios/{servicio_id}/iniciar")
def iniciar_servicio(servicio_id: int):
    return servicios.accion(servicio_id, "iniciar")


@router.post("/servicios/{servicio_id}/detener")
def detener_servicio(servicio_id: int):
    return servicios.accion(servicio_id, "detener")


@router.post("/servicios/{servicio_id}/reiniciar")
def reiniciar_servicio(servicio_id: int):
    return servicios.accion(servicio_id, "reiniciar")


@router.get("/servicios/{servicio_id}/logs")
def logs_servicio(servicio_id: int, lines: int = Query(default=100)):
    return servicios.logs(servicio_id, lines=lines)