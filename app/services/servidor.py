"""Lógica de negocio del servidor: métricas y servicios activos.

Conecta la capa de sistema (psutil para métricas, init system para servicios)
con la capa de API. Delega en el backend auto-detectado para listar servicios,
en lugar de asumir siempre systemd.
"""

from fastapi import HTTPException  # Para envolver errores del sistema en respuestas HTTP.

# Importamos las métricas del sistema (CPU, RAM, disco, etc.).
from ..system import metricas

# Importamos el backend auto-detectado y la excepción base.
# Antes se importaba ``systemd`` directamente; ahora usamos get_backend()
# para que funcione en Alpine (OpenRC), Void (Runit), etc.
from ..system import get_backend, InitError


def resumen() -> dict:
    """Devuelve un resumen de las métricas actuales del servidor.

    Delega completamente en ``metricas.sistema()`` que usa psutil internamente.
    No lanza excepciones: si psutil falla, deja que el error suba al handler
    global de FastAPI.

    Returns:
        Dict con cpu, ram, disco, red, uptime y número de procesos.
    """
    return metricas.sistema()


def procesos(limite: int = 20) -> list[dict]:
    """Devuelve los procesos más activos por uso de CPU.

    Args:
        limite: Número máximo de procesos a devolver (clampado en metricas).

    Returns:
        Lista de dicts con pid, nombre, cpu% y memoria% de cada proceso.
    """
    return metricas.procesos(limite=limite)


def servicios_activos() -> list[dict]:
    """Devuelve los servicios del init system que están corriendo actualmente.

    Delega en el backend auto-detectado del host. El backend puede ser
    systemd, OpenRC, Runit o SysV según el sistema donde corre el agente.

    Returns:
        Lista de dicts con al menos ``unidad`` y ``estado`` por servicio.

    Raises:
        HTTPException: Con status 502 si el init system reporta un error.
    """
    backend = get_backend()  # Obtiene el backend cacheado del detector.

    try:
        return backend.servicios_activos()
    except InitError as error:
        # Cualquier error del init system se convierte en HTTP 502 (Bad Gateway)
        # ya que el agente no pudo obtener la información del sistema subyacente.
        raise HTTPException(status_code=502, detail=error.mensaje)