"""Auto-detector del init system activo en el host.

Este módulo es el punto de entrada principal para obtener el backend de init
correcto. Es responsable de:

    1. **Detectar** cuál init system está corriendo en el host actual.
    2. **Instanciar** el backend correspondiente.
    3. **Cachear** el resultado en un singleton, ya que el init system no
       cambia durante la vida del proceso.

Orden de detección:
    El detector prueba los backends en este orden, usando el primero que
    se declare ``disponible()``:

    1. **systemd** — Si ``systemctl`` existe en PATH. Es el más común.
    2. **OpenRC**  — Si ``rc-service`` existe en PATH. Alpine, Gentoo, Artix.
    3. **Runit**   — Si ``sv`` existe en PATH. Void Linux, Artix (runit).
    4. **SysV**    — Si ``service`` o ``/etc/init.d/`` existen. Fallback legacy.

    Si ningún backend está disponible, se lanza ``RuntimeError`` con un
    mensaje claro que indica al operador qué hacer.

Uso:
    >>> from app.system.detector import get_backend
    >>> backend = get_backend()
    >>> backend.is_active("nginx")
    True
"""

from __future__ import annotations  # Anotaciones de tipo como strings (PEP 563).

import logging  # Para registrar qué backend fue seleccionado al arrancar.

from .base import InitBackend  # Tipo abstracto del backend.

# Importamos todos los backends concretos para que el detector los evalúe.
from .systemd import SystemdBackend
from .openrc import OpenRCBackend
from .runit import RunitBackend
from .sysv import SysVBackend


# ─────────────────────────────────────────────────────────────────────────────
# Logger del módulo
# ─────────────────────────────────────────────────────────────────────────────

#: Logger con namespace ``lumina.system.detector`` para poder filtrar en logs.
log = logging.getLogger("lumina.system.detector")


# ─────────────────────────────────────────────────────────────────────────────
# Orden de prioridad de los backends
# ─────────────────────────────────────────────────────────────────────────────

#: Lista de backends a probar, en orden de prioridad.
#: El detector instancia cada uno y llama a ``disponible()``; usa el primero
#: que devuelva ``True``.
#:
#: Para añadir un nuevo init system en el futuro, simplemente añádelo aquí.
_BACKENDS_ORDENADOS: list[InitBackend] = [
    SystemdBackend(),  # 1. systemd — el más común en distros modernas.
    OpenRCBackend(),   # 2. OpenRC  — Alpine Linux, Gentoo, Artix-OpenRC.
    RunitBackend(),    # 3. Runit   — Void Linux, Artix-runit.
    SysVBackend(),     # 4. SysV    — Devuan, RHEL 6, sistemas legacy (experimental).
]


# ─────────────────────────────────────────────────────────────────────────────
# Singleton del backend seleccionado
# ─────────────────────────────────────────────────────────────────────────────

#: Almacena el backend detectado después de la primera llamada a ``get_backend()``.
#: ``None`` indica que todavía no se ha hecho la detección.
_backend_cache: InitBackend | None = None


# ─────────────────────────────────────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────────────────────────────────────

def detectar() -> InitBackend:
    """Detecta y devuelve el backend de init system adecuado para este host.

    Itera los backends en ``_BACKENDS_ORDENADOS`` y devuelve el primero cuyo
    método ``disponible()`` retorne ``True``.

    Esta función **no usa caché**; se evalúa cada vez que se llama. Úsala
    solo si necesitas forzar una re-detección (p. ej. en tests). Para el
    uso normal, usa ``get_backend()``.

    Returns:
        La instancia del ``InitBackend`` apropiado para este sistema.

    Raises:
        RuntimeError: Si ningún backend conocido está disponible en el host.
                      Esto no debería ocurrir en ningún sistema Linux estándar.
    """
    for backend in _BACKENDS_ORDENADOS:
        if backend.disponible():
            # Registramos la selección en el log para facilitar el diagnóstico.
            log.info(
                "Init system detectado: %s (backend: %s)",
                backend.nombre(),
                type(backend).__name__,
            )
            return backend

    # Si llegamos aquí, ningún init system conocido fue detectado.
    # Listamos los que se probaron para ayudar al operador a diagnosticar.
    probados = [type(b).__name__ for b in _BACKENDS_ORDENADOS]
    raise RuntimeError(
        f"No se detectó ningún init system compatible. "
        f"Backends probados: {probados}. "
        f"Asegúrate de que el agente se ejecuta en un sistema Linux con "
        f"systemd, OpenRC, Runit o SysV instalado."
    )


def get_backend() -> InitBackend:
    """Devuelve el backend de init system detectado, con caché de singleton.

    La primera llamada ejecuta la detección completa y almacena el resultado.
    Las llamadas subsiguientes devuelven el mismo objeto sin re-detectar,
    lo cual es correcto ya que el init system no cambia durante la ejecución.

    Esta es la función que debe usar el resto del código (servicios, API…).

    Returns:
        La instancia cacheada del ``InitBackend`` apropiado para este sistema.

    Raises:
        RuntimeError: Si la detección falla (propagada desde ``detectar()``).

    Example:
        >>> backend = get_backend()
        >>> backend.nombre()
        'systemd'
        >>> backend.is_active("nginx")
        True
    """
    # Usamos ``global`` para poder asignar al singleton del módulo.
    global _backend_cache

    if _backend_cache is None:
        # Primera llamada: ejecutamos la detección y cacheamos el resultado.
        _backend_cache = detectar()
        log.debug(
            "Backend cacheado: %s",
            type(_backend_cache).__name__,
        )

    # Devolvemos el backend cacheado (puede ser de cualquier llamada anterior).
    return _backend_cache


def resetear_cache() -> None:
    """Limpia el singleton del backend cacheado.

    Útil principalmente para **tests unitarios** que necesitan simular
    diferentes entornos en el mismo proceso. No debe llamarse en producción.

    Después de llamar a esta función, la próxima llamada a ``get_backend()``
    ejecutará la detección de nuevo.
    """
    global _backend_cache
    _backend_cache = None  # Forzamos la re-detección en la próxima llamada.
    log.debug("Cache del backend reseteada; la próxima llamada re-detectará.")
