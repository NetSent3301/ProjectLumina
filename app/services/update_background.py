"""Servicio de actualizaciones en segundo plano.

Ejecuta chequeos periódicos de actualizaciones en GitHub y mantiene
el estado actualizado para notificaciones push.
"""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional

from ..api.update import chequear_actualizacion
from ..config import get_settings

log = logging.getLogger("lumina.update.background")

# Referencia a la tarea background para poder cancelarla
_background_task: Optional[asyncio.Task] = None


async def _update_check_loop() -> None:
    """Loop principal de chequeo periódico de actualizaciones."""
    settings = get_settings()

    if not settings.update_notify_enabled:
        log.info("Notificaciones de actualización desactivadas (LUMINA_UPDATE_NOTIFY_ENABLED=false)")
        return

    # Chequeo inicial al arrancar (con pequeño delay para no bloquear startup)
    await asyncio.sleep(30)
    try:
        await chequear_actualizacion()
        log.info("Chequeo inicial de actualizaciones completado")
    except Exception as e:
        log.warning(f"Error en chequeo inicial de actualizaciones: {e}")

    # Loop periódico
    while True:
        try:
            intervalo_seg = settings.update_check_interval_hours * 3600
            await asyncio.sleep(intervalo_seg)
            await chequear_actualizacion()
            log.debug("Chequeo periódico de actualizaciones completado")
        except asyncio.CancelledError:
            log.info("Tarea de actualizaciones cancelada")
            break
        except Exception as e:
            log.error(f"Error en chequeo periódico de actualizaciones: {e}")
            # Esperar un poco antes de reintentar para no spamear en caso de error persistente
            await asyncio.sleep(300)


def iniciar_background_updates() -> None:
    """Inicia la tarea background de chequeo de actualizaciones."""
    global _background_task
    if _background_task is None or _background_task.done():
        _background_task = asyncio.create_task(_update_check_loop())
        log.info("Tarea background de actualizaciones iniciada")


def detener_background_updates() -> None:
    """Detiene la tarea background de chequeo de actualizaciones."""
    global _background_task
    if _background_task and not _background_task.done():
        _background_task.cancel()
        log.info("Tarea background de actualizaciones detenida")