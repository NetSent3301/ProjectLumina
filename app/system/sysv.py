"""Backend de init system: **SysV** (System V init / init.d).

.. warning::
    **Backend experimental.** SysV es el init system más antiguo y su
    comportamiento varía significativamente entre distribuciones. Este backend
    funciona como mejor puede (best-effort) pero puede tener limitaciones
    en distros con implementaciones muy específicas de ``service`` o
    ``/etc/init.d/``.

SysV init fue el gestor de arranque estándar de Unix System V y dominó
Linux durante décadas. Hoy se encuentra principalmente en:
    * RHEL 6 / CentOS 6 (y clones)
    * Devuan (fork sin systemd de Debian)
    * Algunos sistemas embebidos
    * MX Linux (usa SysV por defecto)

Comandos usados:
    * ``service <nombre> start/stop/restart/status``
    * ``service --status-all`` (para listar servicios, si está disponible)
    * ``/etc/init.d/<nombre>`` (fallback cuando ``service`` no existe)

Referencias:
    https://wiki.debian.org/SysVinit
    https://www.devuan.org/
"""

from __future__ import annotations  # Anotaciones de tipo como strings (PEP 563).

import shutil      # Para verificar binarios en PATH con ``shutil.which``.
import subprocess  # Para ejecutar comandos de SysV y capturar su salida.
from pathlib import Path  # Para trabajar con rutas de ``/etc/init.d/``.

from .base import InitBackend, InitError  # Contrato abstracto y excepción base.


# ─────────────────────────────────────────────────────────────────────────────
# Constantes
# ─────────────────────────────────────────────────────────────────────────────

#: Directorio donde SysV guarda los scripts de inicio de servicios.
_INITD_DIR = Path("/etc/init.d")

#: Rutas de syslog donde buscar logs cuando no hay herramienta de journal.
_SYSLOG_PATHS = [
    Path("/var/log/syslog"),    # Debian/Ubuntu sin systemd.
    Path("/var/log/messages"),  # RHEL/CentOS/OpenSUSE.
    Path("/var/log/daemon.log"),  # Algunos sistemas con syslog-ng.
]

#: Timeout en segundos para los comandos de SysV.
_TIMEOUT = 20  # SysV puede tardar más que otros; 20 s es seguro.


# ─────────────────────────────────────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────────────────────────────────────

def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    """Ejecuta un comando de SysV y captura su salida.

    Args:
        cmd: Lista de tokens del comando (sin shell).

    Returns:
        ``CompletedProcess`` con ``stdout``, ``stderr`` y ``returncode``.

    Raises:
        InitError: Si el binario no existe en PATH o supera el timeout.
    """
    # Verificamos que el primer token (el binario) exista en PATH.
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
        stderr o stdout, sin espacios al inicio/final.
    """
    return (r.stderr or r.stdout or "").strip()


def _cmd_servicio(nombre: str) -> list[str]:
    """Devuelve el comando base para gestionar el servicio ``nombre``.

    Prefiere ``service <nombre>`` si está disponible; cae a
    ``/etc/init.d/<nombre>`` como alternativa directa.

    Args:
        nombre: Nombre del servicio.

    Returns:
        Lista de strings que forman el prefijo del comando (sin la acción).

    Raises:
        InitError: Si ninguna de las dos opciones está disponible.
    """
    # Opción 1: el comando ``service`` (disponible en la mayoría de distros SysV).
    if shutil.which("service") is not None:
        return ["service", nombre]

    # Opción 2: el script directo en /etc/init.d/.
    script = _INITD_DIR / nombre
    if script.exists() and script.is_file():
        return [str(script)]  # Ejecutamos el script directamente.

    # Ninguna opción disponible.
    raise InitError(
        f"No se encontró 'service' ni el script '/etc/init.d/{nombre}'",
        no_existe=True,
    )


def _leer_syslog_filtrado(nombre: str, lines: int) -> str:
    """Lee las últimas líneas del syslog que mencionen el servicio ``nombre``.

    Args:
        nombre: Nombre del servicio a buscar en los logs.
        lines:  Número máximo de líneas a devolver.

    Returns:
        Texto con las líneas relevantes o un mensaje de error.
    """
    for ruta in _SYSLOG_PATHS:
        if not ruta.exists():
            continue  # Esta ruta no existe; probamos la siguiente.

        try:
            contenido = ruta.read_text(errors="replace").splitlines()
            # Filtramos líneas que mencionen el nombre del servicio (case-insensitive).
            nombre_lower = nombre.lower()
            filtradas = [l for l in contenido if nombre_lower in l.lower()]
            # Devolvemos las últimas ``lines`` coincidencias.
            return "\n".join(filtradas[-lines:]) if filtradas else f"[sin entradas de '{nombre}' en {ruta}]"
        except PermissionError:
            return f"[sin permiso para leer {ruta}; ejecuta el agente como root]"

    return "[syslog no encontrado; logs no disponibles para SysV en este sistema]"


# ─────────────────────────────────────────────────────────────────────────────
# Backend
# ─────────────────────────────────────────────────────────────────────────────

class SysVBackend(InitBackend):
    """Backend experimental que controla servicios con ``service`` o ``/etc/init.d/``.

    .. warning::
        Este backend es experimental. El comportamiento de ``service`` y los
        scripts de ``/etc/init.d/`` varía mucho entre distribuciones.
        No se garantiza compatibilidad con todos los sistemas SysV.

    Compatible con: Devuan, MX Linux, RHEL/CentOS 6, sistemas embebidos con SysV.
    """

    # ── Información del backend ───────────────────────────────────────────────

    def nombre(self) -> str:
        """Devuelve el identificador del backend: ``"sysv"``."""
        return "sysv"

    def disponible(self) -> bool:
        """Devuelve ``True`` si ``service`` está en PATH o ``/etc/init.d/`` existe.

        SysV está disponible si existe el comando ``service`` O si el directorio
        ``/etc/init.d/`` existe con al menos un script dentro.
        """
        # Comprobamos el comando service primero (más común).
        if shutil.which("service") is not None:
            return True

        # Fallback: verificamos que /etc/init.d/ exista y tenga contenido.
        return _INITD_DIR.exists() and any(_INITD_DIR.iterdir())

    def info(self) -> dict:
        """Retorna metadatos del backend para el endpoint ``GET /api/init``.

        SysV no tiene un comando de versión estándar; reportamos la existencia
        del comando ``service`` y el número de scripts en ``/etc/init.d/``.
        """
        # Contamos los scripts disponibles en /etc/init.d/ como indicador de salud.
        num_scripts: int = 0
        if _INITD_DIR.exists():
            # Contamos solo archivos ejecutables (que son los scripts de servicio).
            num_scripts = sum(1 for f in _INITD_DIR.iterdir() if f.is_file())

        return {
            "backend": self.nombre(),                           # "sysv"
            "version": None,                                   # SysV no reporta versión.
            "pid1": "init",                                    # PID 1 en SysV es el binario "init".
            "experimental": True,                              # Marcado explícitamente como experimental.
            "service_cmd": shutil.which("service") is not None,  # ¿Existe el comando service?
            "initd_scripts": num_scripts,                      # Número de scripts en /etc/init.d/.
        }

    # ── Estado de un servicio ─────────────────────────────────────────────────

    def is_active(self, nombre: str) -> bool:
        """Comprueba si el servicio ``nombre`` está activo según SysV.

        Ejecuta ``service <nombre> status`` o ``/etc/init.d/<nombre> status``.
        Un exit code 0 generalmente indica que el servicio está corriendo,
        aunque algunos scripts SysV no siguen esta convención.

        Args:
            nombre: Nombre del servicio (``"nginx"``, ``"ssh"``…).

        Returns:
            ``True`` si el exit code es 0, ``False`` en cualquier otro caso.
        """
        try:
            cmd = _cmd_servicio(nombre)  # Obtiene ["service", nombre] o ["/etc/init.d/nginx"].
            r = _run(cmd + ["status"])   # Añadimos la acción "status".
        except InitError:
            return False  # Si no podemos ejecutar el comando, asumimos inactivo.

        # En SysV, exit 0 = corriendo; exit 3 = parado; exit 1/2 = error.
        return r.returncode == 0

    # ── Acciones ──────────────────────────────────────────────────────────────

    def _ejecutar(self, nombre: str, accion: str) -> None:
        """Ejecuta una acción SysV sobre el servicio ``nombre``.

        Args:
            nombre: Nombre del servicio.
            accion: Acción a ejecutar: ``"start"``, ``"stop"``, ``"restart"``.

        Raises:
            InitError: Con ``no_existe=True`` si el servicio no está registrado.
        """
        cmd = _cmd_servicio(nombre)  # Puede lanzar InitError si no existe el servicio.
        r = _run(cmd + [accion])     # Ejecutamos cmd + ["start"/"stop"/"restart"].

        if r.returncode != 0:
            texto = _texto(r).lower()

            # Detectamos mensajes de "no existe" comunes en scripts SysV.
            no_existe = (
                "unrecognized service" in texto
                or "no such file" in texto
                or "not found" in texto
                or "unknown" in texto
            )

            raise InitError(
                f"service {nombre} {accion}: {_texto(r)}",
                no_existe=no_existe,
            )

    def iniciar(self, nombre: str) -> None:
        """Inicia el servicio ``nombre`` con ``service <nombre> start``."""
        self._ejecutar(nombre, "start")

    def detener(self, nombre: str) -> None:
        """Detiene el servicio ``nombre`` con ``service <nombre> stop``."""
        self._ejecutar(nombre, "stop")

    def reiniciar(self, nombre: str) -> None:
        """Reinicia el servicio ``nombre`` con ``service <nombre> restart``."""
        self._ejecutar(nombre, "restart")

    # ── Logs ──────────────────────────────────────────────────────────────────

    def log_lines(self, nombre: str, lines: int = 100) -> str:
        """Devuelve las últimas ``lines`` líneas de log del servicio.

        SysV no tiene un gestor de logs centralizado como journalctl.
        Esta implementación busca en las rutas de syslog conocidas y filtra
        las líneas que mencionen el nombre del servicio.

        Args:
            nombre: Nombre del servicio.
            lines:  Número máximo de líneas a devolver.

        Returns:
            Texto con los logs encontrados o mensaje de no disponibilidad.
        """
        return _leer_syslog_filtrado(nombre, lines)

    # ── Listado de servicios activos ──────────────────────────────────────────

    def servicios_activos(self) -> list[dict]:
        """Lista los servicios activos según SysV.

        Estrategia (en orden de preferencia):
            1. ``service --status-all`` si está disponible (Debian/Ubuntu SysV).
            2. Iterar ``/etc/init.d/`` y consultar cada script con ``status``.

        Returns:
            Lista de dicts con claves ``unidad`` y ``estado``.

        Raises:
            InitError: Si no se puede determinar la lista de servicios.
        """
        # ── Opción 1: service --status-all (Debian SysV) ─────────────────────
        if shutil.which("service") is not None:
            try:
                r = _run(["service", "--status-all"])
                # ``service --status-all`` imprime líneas como:
                #   " [ + ]  nginx"    → activo
                #   " [ - ]  apache2"  → inactivo
                #   " [ ? ]  ufw"      → estado desconocido
                if r.returncode == 0 or r.stdout:
                    resultados: list[dict] = []
                    for linea in (r.stdout or r.stderr or "").splitlines():
                        linea_strip = linea.strip()
                        # Solo procesamos líneas con el formato "[ X ] nombre".
                        if "[ + ]" in linea_strip:
                            # Extraemos el nombre del servicio: la parte después de "[ + ]".
                            nombre_svc = linea_strip.split("]", 1)[-1].strip()
                            if nombre_svc:
                                resultados.append({
                                    "unidad": nombre_svc,  # Nombre del servicio.
                                    "estado": "running",   # "+" en SysV Debian = corriendo.
                                })
                    return resultados
            except InitError:
                pass  # Si falla, continuamos con el método alternativo.

        # ── Opción 2: iterar /etc/init.d/ ────────────────────────────────────
        # Si service --status-all no funciona, consultamos cada script individualmente.
        if not _INITD_DIR.exists():
            raise InitError("Ni 'service --status-all' ni '/etc/init.d/' están disponibles")

        resultados = []
        for script in sorted(_INITD_DIR.iterdir()):
            # Solo procesamos scripts ejecutables (ignoramos README, etc.).
            if not script.is_file():
                continue

            nombre_svc = script.name

            # Ignoramos scripts especiales que no son servicios reales.
            if nombre_svc.startswith("rc") or nombre_svc.startswith("skeleton"):
                continue

            try:
                # Consultamos el estado de este servicio concreto.
                r = subprocess.run(
                    [str(script), "status"],
                    capture_output=True,
                    text=True,
                    timeout=5,  # Timeout corto para no bloquear en servicios lentos.
                )
                if r.returncode == 0:
                    resultados.append({
                        "unidad": nombre_svc,  # Nombre del script /etc/init.d/.
                        "estado": "running",   # Exit 0 = corriendo (convención SysV).
                    })
            except (subprocess.TimeoutExpired, PermissionError, FileNotFoundError):
                # Saltamos servicios que no responden o no tenemos permiso.
                continue

        return resultados
