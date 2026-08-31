"""Endpoints de información del servidor: métricas, procesos, servicios e init system.

Todos los endpoints de este router son de solo lectura (GET).
No modifican el estado del servidor; solo devuelven información de diagnóstico.

Endpoints disponibles:
    GET /servidor              — CPU, RAM, disco, red, uptime.
    GET /servidor/procesos     — Top procesos por CPU (psutil).
    GET /servidor/servicios    — Servicios del init system activos.
    GET /servidor/init         — Backend de init detectado + metadatos.
"""

from typing import Optional  # Para el parámetro opcional ``limite``.

from fastapi import APIRouter, Query  # Router de FastAPI y parámetros de query.

from ..services import servidor  # Lógica de negocio del servidor.
from ..system import get_backend  # Para el endpoint /init.

#: Router que agrupa todos los endpoints de información del servidor.
#: Se monta en el router principal de la aplicación con el prefijo /api.
router = APIRouter()


@router.get("/servidor")
def resumen_servidor():
    """Devuelve las métricas actuales del servidor (CPU, RAM, disco, red, uptime).

    Usa psutil internamente; funciona en cualquier plataforma Linux.
    No requiere privilegios especiales.
    """
    return servidor.resumen()


@router.get("/servidor/procesos")
def procesos_servidor(limite: Optional[int] = Query(default=20, ge=1, le=200)):
    """Devuelve los procesos más activos por uso de CPU.

    Args (query params):
        limite: Número de procesos a devolver (entre 1 y 200, default 20).
    """
    return servidor.procesos(limite=limite)


@router.get("/servidor/servicios")
def servicios_sistema():
    """Devuelve los servicios del init system que están corriendo actualmente.

    El init system usado varía según el host donde corre el agente:
    puede ser systemd, OpenRC, Runit o SysV. El resultado siempre incluye
    al menos las claves ``unidad`` y ``estado``.
    """
    return servidor.servicios_activos()


@router.get("/servidor/init")
def info_init_system():
    """Devuelve información del init system detectado en este agente.

    Útil para que el panel sepa qué init system usa cada agente registrado,
    y para diagnóstico cuando algo no funciona como se espera.

    Returns:
        JSON con las claves:
            ``backend``   — nombre del backend (``"systemd"``, ``"openrc"``, etc.).
            ``version``   — versión del init system si es detectable, o ``null``.
            ``pid1``      — nombre del proceso con PID 1 si es detectable.
            (+ campos extra dependiendo del backend, p. ej. ``experimental: true`` en SysV)
    """
    # get_backend() usa el singleton cacheado; no re-detecta en cada request.
    backend = get_backend()
    # Llamamos a info() que devuelve metadatos específicos del backend detectado.
    return backend.info()