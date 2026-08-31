"""Lógica de negocio del servidor: métricas y servicios activos (psutil + systemd).
"""

from fastapi import HTTPException

from ..system import metricas, systemd


def resumen() -> dict:
    return metricas.sistema()


def procesos(limite: int = 20) -> list[dict]:
    return metricas.procesos(limite=limite)


def servicios_activos() -> list[dict]:
    try:
        return systemd.servicios_activos()
    except systemd.SystemdError as error:
        raise HTTPException(status_code=502, detail=error.mensaje)