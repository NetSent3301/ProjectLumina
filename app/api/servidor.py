"""Endpoints de información del servidor (métricas, procesos, servicios).
"""

from typing import Optional

from fastapi import APIRouter, Query

from ..services import servidor

router = APIRouter()


@router.get("/servidor")
def resumen_servidor():
    """CPU, RAM, disco, red, uptime."""
    return servidor.resumen()


@router.get("/servidor/procesos")
def procesos_servidor(limite: Optional[int] = Query(default=20, ge=1, le=200)):
    return servidor.procesos(limite=limite)


@router.get("/servidor/servicios")
def servicios_sistema():
    """Unidades systemd de tipo servicio activas."""
    return servidor.servicios_activos()