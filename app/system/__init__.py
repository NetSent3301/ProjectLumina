"""API pública del módulo ``app.system``.

Este ``__init__.py`` re-exporta los símbolos que el resto del código debe
usar al interactuar con el init system. Importar desde aquí (en lugar de
desde submódulos concretos) garantiza que el código externo no dependa de
qué backend está activo.

Uso recomendado::

    from app.system import get_backend, InitError

    backend = get_backend()          # Obtiene el backend correcto para este host.
    backend.is_active("nginx")       # True si nginx está corriendo.

    try:
        backend.iniciar("nginx")
    except InitError as e:
        print(e.mensaje)             # Mensaje legible del error.
        print(e.no_existe)           # True si el servicio no existe.
"""

# ── Excepción base ──────────────────────────────────────────────────────────
# Importamos InitError para que los módulos externos puedan hacer:
#   from app.system import InitError
# sin necesidad de saber en qué submódulo vive.
from .base import InitError  # noqa: F401  (re-exportación intencional)

# ── Clase abstracta ─────────────────────────────────────────────────────────
# Re-exportamos InitBackend para que los módulos que necesiten tipado
# estático (p. ej. para anotaciones) puedan importarla desde aquí.
from .base import InitBackend  # noqa: F401  (re-exportación intencional)

# ── Función principal ───────────────────────────────────────────────────────
# get_backend() es la única función que el código externo debería llamar.
# Devuelve el backend correcto (systemd, OpenRC, Runit o SysV) auto-detectado.
from .detector import get_backend  # noqa: F401  (re-exportación intencional)

# ── Utilidad de test ────────────────────────────────────────────────────────
# resetear_cache() solo se usa en tests; la incluimos aquí por conveniencia.
from .detector import resetear_cache  # noqa: F401  (re-exportación intencional)
