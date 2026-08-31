"""Contrato abstracto para los backends de init system.

Este módulo define las dos piezas centrales de la capa de abstracción:

    * ``InitError``  — excepción base que todos los backends deben lanzar
      cuando algo falla al interactuar con el init system.

    * ``InitBackend`` — clase abstracta (ABC) que establece la interfaz
      que cada backend concreto (systemd, OpenRC, Runit, SysV…) debe cumplir.

Gracias a esta abstracción el resto del código jamás importa un backend
concreto directamente; siempre habla con ``InitBackend`` y obtiene la
implementación real a través de ``detector.get_backend()``.
"""

from __future__ import annotations  # Habilita anotaciones de tipo en forma de string (PEP 563).

from abc import ABC, abstractmethod  # ABC = Abstract Base Class; abstractmethod marca métodos obligatorios.


# ─────────────────────────────────────────────────────────────────────────────
# Excepción base
# ─────────────────────────────────────────────────────────────────────────────

class InitError(RuntimeError):
    """Error producido al interactuar con el init system del host.

    Todos los backends deben lanzar esta excepción (o una subclase) cuando
    una operación falla, de modo que la capa de servicios pueda manejar
    errores sin importar cuál es el init system subyacente.

    Args:
        mensaje: Descripción legible del error. Se expone al cliente HTTP.
        no_existe: ``True`` cuando el servicio pedido no existe en el
                   init system (permite devolver HTTP 404 en lugar de 502).
    """

    def __init__(self, mensaje: str, *, no_existe: bool = False) -> None:
        # Pasamos el mensaje a RuntimeError para que sea visible en tracebacks.
        super().__init__(mensaje)

        # Guardamos el mensaje en un atributo propio para acceso fácil.
        self.mensaje: str = mensaje

        # Flag que permite a la capa de servicios distinguir "no existe" de
        # "error de ejecución", emitiendo el código HTTP apropiado.
        self.no_existe: bool = no_existe


# ─────────────────────────────────────────────────────────────────────────────
# Contrato del backend
# ─────────────────────────────────────────────────────────────────────────────

class InitBackend(ABC):
    """Interfaz que debe implementar cada backend de init system.

    Todos los métodos son abstractos; si una subclase no los implementa
    Python lanzará ``TypeError`` al intentar instanciarla, evitando
    implementaciones incompletas silenciosas.

    Convenciones de error:
        * Si el init system no está disponible → lanza ``InitError``.
        * Si la unidad/servicio no existe     → lanza ``InitError(no_existe=True)``.
        * Si el comando tarda demasiado       → lanza ``InitError`` con timeout.
    """

    # ── Información del backend ───────────────────────────────────────────────

    @abstractmethod
    def nombre(self) -> str:
        """Nombre corto del backend, p. ej. ``"systemd"``, ``"openrc"``.

        Se usa para exponer en el endpoint ``GET /api/init`` y en los logs.
        """

    @abstractmethod
    def disponible(self) -> bool:
        """Devuelve ``True`` si este backend está operativo en el sistema actual.

        El detector llama a este método para elegir el backend correcto.
        Una implementación típica comprueba si el binario principal existe en PATH
        con ``shutil.which``.
        """

    @abstractmethod
    def info(self) -> dict:
        """Metadatos del backend para el endpoint de diagnóstico.

        Returns:
            dict con al menos las claves:
                ``backend``   — nombre corto (igual que ``nombre()``).
                ``version``   — versión del binario si es detectable, o ``None``.
                ``pid1``      — nombre del proceso con PID 1 si es detectable, o ``None``.
        """

    # ── Estado de un servicio ─────────────────────────────────────────────────

    @abstractmethod
    def is_active(self, nombre: str) -> bool:
        """Comprueba si el servicio ``nombre`` está activo (corriendo).

        No debe lanzar excepciones: si el servicio no existe o el init system
        no responde, debe devolver ``False`` de forma silenciosa.

        Args:
            nombre: Nombre del servicio tal como lo conoce el init system
                    (p. ej. ``"nginx.service"`` para systemd, ``"nginx"`` para OpenRC).

        Returns:
            ``True`` si el servicio está activo, ``False`` en cualquier otro caso.
        """

    # ── Acciones sobre un servicio ────────────────────────────────────────────

    @abstractmethod
    def iniciar(self, nombre: str) -> None:
        """Inicia el servicio ``nombre``.

        Args:
            nombre: Nombre del servicio.

        Raises:
            InitError: Si el comando falla, con ``no_existe=True`` cuando
                       el servicio no está registrado en el init system.
        """

    @abstractmethod
    def detener(self, nombre: str) -> None:
        """Detiene el servicio ``nombre``.

        Args:
            nombre: Nombre del servicio.

        Raises:
            InitError: Si el comando falla.
        """

    @abstractmethod
    def reiniciar(self, nombre: str) -> None:
        """Reinicia el servicio ``nombre``.

        Args:
            nombre: Nombre del servicio.

        Raises:
            InitError: Si el comando falla.
        """

    # ── Logs ──────────────────────────────────────────────────────────────────

    @abstractmethod
    def log_lines(self, nombre: str, lines: int = 100) -> str:
        """Devuelve las últimas ``lines`` líneas del log del servicio.

        Args:
            nombre: Nombre del servicio.
            lines:  Número máximo de líneas a devolver (entre 1 y 500).

        Returns:
            Bloque de texto con los logs. Puede estar vacío si no hay logs.

        Raises:
            InitError: Si el init system falla al obtener los logs.
        """

    # ── Listado de servicios activos ──────────────────────────────────────────

    @abstractmethod
    def servicios_activos(self) -> list[dict]:
        """Devuelve la lista de servicios que están corriendo actualmente.

        Returns:
            Lista de dicts; cada uno con al menos las claves:
                ``unidad``  — nombre del servicio.
                ``estado``  — estado en texto (``"running"``, ``"active"``…).
        """
