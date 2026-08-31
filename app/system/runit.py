"""Backend de init system: **Runit**.

Runit es un init system minimalista orientado a la velocidad y simplicidad.
Lo usan Void Linux, Artix (runit) y algunos sistemas embebidos. Sus comandos
son más simples que systemd pero el mecanismo de logging es diferente:
usa ``svlogd`` para escribir logs en un directorio por servicio.

Comandos principales:
    * ``sv``           — gestión de servicios (start, stop, restart, status).
    * ``/var/service/`` — directorio donde están los symlinks de servicios activos.
    * ``/var/log/<svc>/current`` — logs de cada servicio (binario TAI64N).

Formato de logs TAI64N:
    ``svlogd`` escribe timestamps en formato TAI64N (``@400000...``). Este
    backend los decodifica a texto legible cuando es posible; si no, los
    muestra tal cual ya que son legibles como líneas de log aunque el timestamp
    sea opaco.

Referencias:
    http://smarden.org/runit/
    https://docs.voidlinux.org/config/services/index.html
"""

from __future__ import annotations  # Anotaciones de tipo como strings (PEP 563).

import shutil      # Para verificar que ``sv`` exista en PATH.
import subprocess  # Para ejecutar comandos y capturar la salida.
from pathlib import Path  # Para listar directorios y leer archivos de log.

from .base import InitBackend, InitError  # Contrato abstracto y excepción base.


# ─────────────────────────────────────────────────────────────────────────────
# Constantes
# ─────────────────────────────────────────────────────────────────────────────

#: Directorio donde Runit mantiene los symlinks de servicios supervisados.
#: En Void Linux es ``/var/service``; en algunas configs puede ser ``/service``.
_SERVICE_DIRS = [
    Path("/var/service"),   # Void Linux (estándar).
    Path("/service"),       # Runit vanilla.
    Path("/run/runit/supervise"),  # Algunos sistemas con supervise explícito.
]

#: Directorio raíz donde svlogd escribe los logs por servicio.
_LOG_BASE = Path("/var/log")

#: Timeout en segundos para los comandos de runit.
_TIMEOUT = 15


# ─────────────────────────────────────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────────────────────────────────────

def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    """Ejecuta un comando de Runit y captura su salida.

    Args:
        cmd: Lista de tokens del comando (sin shell).

    Returns:
        ``CompletedProcess`` con ``stdout``, ``stderr`` y ``returncode``.

    Raises:
        InitError: Si el binario no existe en PATH o supera el timeout.
    """
    # Verificamos que el binario principal exista en PATH antes de ejecutar.
    if shutil.which(cmd[0]) is None:
        raise InitError(f"'{cmd[0]}' no está disponible en este sistema")

    try:
        return subprocess.run(
            cmd,
            capture_output=True,  # Captura stdout y stderr por separado.
            text=True,            # Decodifica la salida a str.
            timeout=_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        raise InitError(f"'{cmd[0]}' tardó demasiado (timeout={_TIMEOUT}s)") from None


def _texto(r: subprocess.CompletedProcess) -> str:
    """Extrae el texto más relevante del resultado de un proceso.

    Args:
        r: Resultado del proceso.

    Returns:
        Texto de stderr o stdout, sin espacios al inicio/final.
    """
    return (r.stderr or r.stdout or "").strip()


def _directorio_servicio() -> Path | None:
    """Devuelve el primer directorio de servicios de Runit que exista.

    Runit mantiene los servicios como symlinks en un directorio especial.
    Probamos las rutas conocidas en orden.

    Returns:
        La primera ``Path`` existente de ``_SERVICE_DIRS``, o ``None`` si
        ninguna existe en este sistema.
    """
    for ruta in _SERVICE_DIRS:
        if ruta.exists() and ruta.is_dir():
            return ruta
    return None  # No encontramos directorio de servicios.


def _decodificar_tai64n_linea(linea: str) -> str:
    """Decodifica (best-effort) el timestamp TAI64N del inicio de una línea de svlogd.

    ``svlogd`` prefija cada línea con ``@<hex-timestamp> ``. Si la línea
    tiene ese formato, reemplazamos el timestamp por un marcador legible.
    Si no, devolvemos la línea tal cual.

    Nota: La decodificación exacta de TAI64N a UTC requiere aritmética de
    64 bits y la tabla de leap seconds. Aquí solo indicamos que era un
    timestamp, lo cual es suficiente para que los logs sean legibles.

    Args:
        linea: Una línea de log de svlogd, posiblemente con TAI64N prefix.

    Returns:
        La línea con el timestamp simplificado o sin cambios.
    """
    # Las líneas TAI64N comienzan con '@' seguido de exactamente 16 hex chars y un espacio.
    if linea.startswith("@") and len(linea) > 17 and linea[17] == " ":
        # Extraemos la parte del mensaje (después del timestamp y el espacio).
        mensaje = linea[18:]
        # Marcamos que el timestamp fue omitido para no confundir al usuario.
        return f"[ts] {mensaje}"

    # Si no tiene el formato TAI64N, devolvemos sin cambios.
    return linea


# ─────────────────────────────────────────────────────────────────────────────
# Backend
# ─────────────────────────────────────────────────────────────────────────────

class RunitBackend(InitBackend):
    """Backend que controla servicios a través del comando ``sv``.

    Compatible con Void Linux, Artix (runit) y cualquier sistema que use
    Runit como init principal.

    Los servicios en Runit son directorios en ``/etc/sv/<nombre>/``, pero
    se gestionan a través de symlinks en ``/var/service/<nombre>/``.
    El comando ``sv`` acepta el nombre simple (``"nginx"``, ``"sshd"``…).
    """

    # ── Información del backend ───────────────────────────────────────────────

    def nombre(self) -> str:
        """Devuelve el identificador del backend: ``"runit"``."""
        return "runit"

    def disponible(self) -> bool:
        """Devuelve ``True`` si ``sv`` está en PATH.

        ``sv`` es el comando central de Runit. Si está disponible asumimos
        que Runit está activo como init system.
        """
        return shutil.which("sv") is not None

    def info(self) -> dict:
        """Retorna metadatos del backend para el endpoint ``GET /api/init``.

        Runit no expone su versión fácilmente; intentamos con ``runit --version``
        pero es posible que no exista ese flag en todas las versiones.
        """
        version: str | None = None

        try:
            # Algunos builds de runit responden a ``--version``; otros no.
            r = _run(["sv", "--version"])
            salida = (r.stdout or r.stderr or "").strip()
            if salida:
                # Tomamos el primer token que parezca una versión (empieza con dígito).
                for token in salida.split():
                    if token[0].isdigit():
                        version = token
                        break
        except InitError:
            pass  # No pudimos obtener la versión; dejamos None.

        return {
            "backend": self.nombre(),  # "runit"
            "version": version,        # Versión de runit o None.
            "pid1": "runit",           # En Void Linux, PID 1 es el binario runit.
        }

    # ── Estado de un servicio ─────────────────────────────────────────────────

    def is_active(self, nombre: str) -> bool:
        """Comprueba si el servicio ``nombre`` está corriendo en Runit.

        Ejecuta ``sv status <nombre>``. La salida contiene "run:" si el
        servicio está activo, o "down:" si está parado.

        Args:
            nombre: Nombre del servicio (``"nginx"``, ``"sshd"``…).

        Returns:
            ``True`` si la salida contiene ``"run:"`` y el exit code es 0.
        """
        try:
            r = _run(["sv", "status", nombre])
        except InitError:
            # Si sv no existe o falla, asumimos inactivo.
            return False

        # ``sv status`` devuelve "run: nginx: (pid 1234) 100s" cuando corre.
        # El exit code puede ser 0 o 1 dependiendo de la versión; nos fiamos del texto.
        return r.returncode == 0 and "run:" in r.stdout

    # ── Acciones ──────────────────────────────────────────────────────────────

    def _ejecutar(self, nombre: str, accion: str) -> None:
        """Ejecuta ``sv <accion> <nombre>`` y lanza ``InitError`` si falla.

        Args:
            nombre: Nombre del servicio Runit.
            accion: Subcomando de sv: ``"up"``, ``"down"``, ``"restart"``.

        Raises:
            InitError: Con ``no_existe=True`` si el servicio no está supervisado.
        """
        r = _run(["sv", accion, nombre])

        if r.returncode != 0:
            texto = _texto(r).lower()

            # Runit reporta servicios no supervisados con estos mensajes.
            no_existe = (
                "unknown" in texto
                or "no such service" in texto
                or "unable to open" in texto
            )

            raise InitError(
                f"sv {accion} {nombre}: {_texto(r)}",
                no_existe=no_existe,
            )

    def iniciar(self, nombre: str) -> None:
        """Inicia el servicio ``nombre`` con ``sv up <nombre>``.

        En Runit, ``up`` ordena al supervisor que levante el proceso si está parado.
        """
        self._ejecutar(nombre, "up")

    def detener(self, nombre: str) -> None:
        """Detiene el servicio ``nombre`` con ``sv down <nombre>``.

        ``down`` ordena al supervisor que baje el proceso y no lo reinicie.
        """
        self._ejecutar(nombre, "down")

    def reiniciar(self, nombre: str) -> None:
        """Reinicia el servicio ``nombre`` con ``sv restart <nombre>``.

        ``restart`` envía TERM al proceso y lo vuelve a levantar.
        """
        self._ejecutar(nombre, "restart")

    # ── Logs ──────────────────────────────────────────────────────────────────

    def log_lines(self, nombre: str, lines: int = 100) -> str:
        """Devuelve las últimas ``lines`` líneas del log del servicio.

        Runit usa ``svlogd`` que escribe logs en ``/var/log/<nombre>/current``.
        Los timestamps están en formato TAI64N; este método los simplifica.

        Args:
            nombre: Nombre del servicio.
            lines:  Número máximo de líneas a devolver.

        Returns:
            Texto con los logs decodificados, o mensaje de log no disponible.

        Raises:
            InitError: Si el archivo de log existe pero no puede leerse.
        """
        # Ruta estándar del log de svlogd para este servicio.
        ruta_log = _LOG_BASE / nombre / "current"

        if not ruta_log.exists():
            # El servicio no usa svlogd o no ha generado logs todavía.
            return f"[log no encontrado en {ruta_log}; el servicio puede no usar svlogd]"

        try:
            # Leemos todo el archivo (svlogd rota automáticamente, así que
            # "current" contiene el log activo y no debería ser enorme).
            contenido = ruta_log.read_text(errors="replace").splitlines()

            # Tomamos las últimas ``lines`` líneas.
            ultimas = contenido[-max(1, lines):]

            # Decodificamos los timestamps TAI64N para mejorar legibilidad.
            return "\n".join(_decodificar_tai64n_linea(l) for l in ultimas)
        except PermissionError:
            raise InitError(
                f"sin permiso para leer {ruta_log}; ejecuta el agente como root",
                no_existe=False,
            )

    # ── Listado de servicios activos ──────────────────────────────────────────

    def servicios_activos(self) -> list[dict]:
        """Lista los servicios activos supervisados por Runit.

        Recorre el directorio de servicios (``/var/service/``) y consulta
        el estado de cada uno con ``sv status``.

        Returns:
            Lista de dicts con claves ``unidad`` y ``estado`` para los
            servicios que están en estado ``"run"``.

        Raises:
            InitError: Si no se encuentra ningún directorio de servicios Runit.
        """
        # Buscamos el directorio de servicios en las rutas conocidas.
        dir_servicios = _directorio_servicio()

        if dir_servicios is None:
            raise InitError(
                "No se encontró el directorio de servicios de Runit "
                f"(probado: {[str(d) for d in _SERVICE_DIRS]})"
            )

        resultados: list[dict] = []

        # Cada entrada en el directorio de servicios es un servicio supervisado.
        for entrada in sorted(dir_servicios.iterdir()):
            # Solo procesamos directorios (los servicios son directorios/symlinks).
            if not (entrada.is_dir() or entrada.is_symlink()):
                continue

            nombre_servicio = entrada.name  # El nombre del servicio es el nombre del directorio.

            try:
                r = _run(["sv", "status", nombre_servicio])
                # Si la salida contiene "run:" el servicio está activo.
                if r.returncode == 0 and "run:" in r.stdout:
                    resultados.append({
                        "unidad": nombre_servicio,  # Nombre del servicio Runit.
                        "estado": "run",            # Estado "run" en terminología Runit.
                    })
            except InitError:
                # Si no podemos consultar este servicio, lo saltamos silenciosamente.
                continue

        return resultados
