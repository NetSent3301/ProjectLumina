"""Backend de init system: **OpenRC**.

OpenRC es el gestor de arranque que usan Alpine Linux, Gentoo y Artix (entre
otros). En lugar de ``systemctl`` usa ``rc-service`` para gestionar servicios
individuales y ``rc-status`` para listar el estado global.

Diferencias clave respecto a systemd:
    * No hay ``journalctl``. Los logs van al syslog del sistema
      (``/var/log/messages`` en Alpine) y, si el servicio usa ``svlogd``
      (logger de runit), a ``/var/log/<nombre>/current``.
    * Los nombres de servicio no llevan sufijo (``.service``); son simples:
      ``"nginx"``, ``"sshd"``, etc.
    * ``rc-service`` devuelve exit 0 tanto para "started" como para algunos
      mensajes de estado; siempre parseamos el stdout para confirmar.

Referencias:
    https://wiki.alpinelinux.org/wiki/OpenRC
    https://github.com/OpenRC/openrc
"""

from __future__ import annotations  # Anotaciones de tipo como strings (PEP 563).

import shutil      # Para ``shutil.which``: verifica que el binario esté en PATH.
import subprocess  # Para ejecutar comandos y capturar su salida.
from pathlib import Path  # Para leer archivos de log de forma multiplataforma.

from .base import InitBackend, InitError  # Contrato abstracto y excepción base.
from .privilegios import PriviledgeError, ejecutar, es_root, escribir_archivo_privilegiado


# ─────────────────────────────────────────────────────────────────────────────
# Constantes
# ─────────────────────────────────────────────────────────────────────────────

#: Rutas donde OpenRC/svlogd puede almacenar logs de servicios.
#: Se comprueban en orden; se usa la primera que exista.
_SYSLOG_PATHS = [
    Path("/var/log/messages"),  # Alpine Linux (busybox syslog).
    Path("/var/log/syslog"),    # Gentoo y derivados con syslog-ng.
    Path("/var/log/everything/everything.log"),  # Algunas configs de metalog.
]

#: Timeout en segundos para comandos OpenRC. 15 s es generoso pero seguro.
_TIMEOUT = 15


# ─────────────────────────────────────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────────────────────────────────────

def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    """Ejecuta un comando de OpenRC y captura su salida.

    Args:
        cmd: Lista de tokens del comando (sin shell).

    Returns:
        ``CompletedProcess`` con ``stdout``, ``stderr`` y ``returncode``.

    Raises:
        InitError: Si el binario no existe en PATH o el comando supera timeout.
    """
    # Verificamos que el binario exista antes de intentar ejecutarlo.
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

    Prefiere stderr (donde van los errores de rc-service) y cae a stdout.

    Args:
        r: Resultado del proceso a examinar.

    Returns:
        Texto limpio sin espacios al inicio/final.
    """
    return (r.stderr or r.stdout or "").strip()


def _leer_syslog_filtrado(nombre: str, lines: int) -> str:
    """Lee las últimas líneas del syslog que mencionen el servicio ``nombre``.

    Busca en las rutas de syslog conocidas (``_SYSLOG_PATHS``) la primera que
    exista y filtra las líneas que contengan el nombre del servicio.

    Args:
        nombre: Nombre del servicio a buscar en los logs.
        lines:  Número máximo de líneas a devolver.

    Returns:
        Bloque de texto con las líneas relevantes, o un mensaje indicando
        que no se encontraron logs.
    """
    for ruta in _SYSLOG_PATHS:
        if not ruta.exists():
            continue  # Esta ruta no existe en este sistema; probamos la siguiente.

        try:
            # Leemos el archivo completo. Para archivos grandes esto puede ser
            # lento, pero es la única forma portable sin ``tail`` externo.
            contenido = ruta.read_text(errors="replace").splitlines()

            # Filtramos solo las líneas que mencionan el nombre del servicio.
            # La comparación es case-insensitive para mayor robustez.
            nombre_lower = nombre.lower()
            filtradas = [l for l in contenido if nombre_lower in l.lower()]

            # Tomamos las últimas ``lines`` líneas del filtrado.
            return "\n".join(filtradas[-lines:]) if filtradas else f"[sin entradas de '{nombre}' en {ruta}]"
        except PermissionError:
            # El proceso no tiene permisos para leer el syslog; lo indicamos claramente.
            return f"[sin permiso para leer {ruta}; ejecuta el agente como root]"

    # Ninguna ruta de syslog encontrada.
    return "[syslog no encontrado; logs no disponibles para este backend]"


# ─────────────────────────────────────────────────────────────────────────────
# Backend
# ─────────────────────────────────────────────────────────────────────────────

class OpenRCBackend(InitBackend):
    """Backend que controla servicios a través de ``rc-service`` y ``rc-status``.

    Compatible con Alpine Linux, Gentoo, Artix (OpenRC) y cualquier sistema
    que tenga OpenRC instalado como init principal.

    Los nombres de servicio NO llevan sufijo. Por convención en OpenRC se usa
    el nombre simple (``"nginx"``, ``"sshd"``, ``"crond"``).
    """

    # ── Información del backend ───────────────────────────────────────────────

    def nombre(self) -> str:
        """Devuelve el identificador del backend: ``"openrc"``."""
        return "openrc"

    def disponible(self) -> bool:
        """Devuelve ``True`` si ``rc-service`` está en PATH.

        ``rc-service`` es el comando principal de OpenRC; si existe asumimos
        que el sistema corre OpenRC.
        """
        return shutil.which("rc-service") is not None

    def info(self) -> dict:
        """Retorna metadatos del backend para el endpoint ``GET /api/init``.

        Intenta obtener la versión de OpenRC con ``rc-service --version``.
        """
        version: str | None = None

        try:
            # OpenRC imprime su versión en stderr cuando se pasa --version.
            r = _run(["rc-service", "--version"])
            salida = (r.stdout or r.stderr or "").strip()
            if salida:
                # La salida suele ser "rc-service (OpenRC) 0.54.2" o similar.
                partes = salida.split()
                # Buscamos el token que luce como número de versión.
                for token in partes:
                    if token[0].isdigit():
                        version = token
                        break
        except InitError:
            pass  # No pudimos obtener la versión; dejamos None.

        return {
            "backend": self.nombre(),  # "openrc"
            "version": version,        # Versión de OpenRC o None.
            "pid1": "openrc-init",     # En Alpine con OpenRC, PID 1 es openrc-init.
        }

    # ── Estado de un servicio ─────────────────────────────────────────────────

    def is_active(self, nombre: str) -> bool:
        """Comprueba si el servicio ``nombre`` está activo en OpenRC.

        Ejecuta ``rc-service <nombre> status``. El exit code 0 significa
        que el servicio está corriendo; cualquier otro valor indica que no.

        Args:
            nombre: Nombre simple del servicio (``"nginx"``, ``"sshd"``…).

        Returns:
            ``True`` si el servicio está activo (exit 0), ``False`` si no.
        """
        try:
            r = _run(["rc-service", nombre, "status"])
        except InitError:
            # Si rc-service no existe o falla, asumimos inactivo.
            return False
        # Exit code 0 = servicio corriendo; cualquier otro = parado/error.
        return r.returncode == 0

    # ── Acciones ──────────────────────────────────────────────────────────────

    def _ejecutar(self, nombre: str, accion: str) -> None:
        """Ejecuta ``rc-service <nombre> <accion>`` y maneja errores.

        Args:
            nombre: Nombre del servicio OpenRC.
            accion: Subcomando: ``"start"``, ``"stop"``, ``"restart"``.

        Raises:
            InitError: Con ``no_existe=True`` si el servicio no está registrado.
        """
        r = _run(["rc-service", nombre, accion])

        if r.returncode != 0:
            texto = _texto(r).lower()

            # OpenRC reporta servicios inexistentes con estos mensajes.
            no_existe = (
                "does not exist" in texto
                or "unknown service" in texto
                or "no such" in texto
            )

            raise InitError(
                f"rc-service {nombre} {accion}: {_texto(r)}",
                no_existe=no_existe,
            )

    def iniciar(self, nombre: str) -> None:
        """Inicia el servicio ``nombre`` con ``rc-service <nombre> start``."""
        self._ejecutar(nombre, "start")

    def detener(self, nombre: str) -> None:
        """Detiene el servicio ``nombre`` con ``rc-service <nombre> stop``."""
        self._ejecutar(nombre, "stop")

    def reiniciar(self, nombre: str) -> None:
        """Reinicia el servicio ``nombre`` con ``rc-service <nombre> restart``."""
        self._ejecutar(nombre, "restart")

    # ── Logs ──────────────────────────────────────────────────────────────────

    def log_lines(self, nombre: str, lines: int = 100) -> str:
        """Devuelve las últimas ``lines`` líneas de log del servicio.

        Estrategia (en orden de preferencia):
            1. ``/var/log/<nombre>/current`` — si el servicio usa svlogd/runit.
            2. Syslog del sistema filtrado por nombre del servicio.

        Args:
            nombre: Nombre del servicio.
            lines:  Número máximo de líneas a devolver.

        Returns:
            Texto con los logs o un mensaje indicando que no están disponibles.
        """
        # ── Opción 1: log dedicado via svlogd ────────────────────────────────
        # Algunos servicios en OpenRC/Gentoo usan svlogd para escribir a
        # /var/log/<nombre>/current (formato de runit logger).
        log_svlogd = Path(f"/var/log/{nombre}/current")
        if log_svlogd.exists():
            try:
                contenido = log_svlogd.read_text(errors="replace").splitlines()
                # Tomamos las últimas ``lines`` líneas del archivo.
                return "\n".join(contenido[-lines:])
            except PermissionError:
                # No tenemos permiso; continuamos con el fallback.
                pass

        # ── Opción 2: syslog filtrado ─────────────────────────────────────────
        # OpenRC no tiene journalctl; el fallback es buscar en syslog.
        return _leer_syslog_filtrado(nombre, lines)

    # ── Listado de servicios activos ──────────────────────────────────────────

    def servicios_activos(self) -> list[dict]:
        """Lista los servicios que están corriendo según OpenRC.

        Usa ``rc-status --all --nocolor`` para obtener el estado de todos
        los servicios sin escape de colores ANSI que compliquen el parsing.

        Returns:
            Lista de dicts con claves ``unidad`` y ``estado``.

        Raises:
            InitError: Si ``rc-status`` falla.
        """
        # --all    → incluye servicios de todos los runlevels.
        # --nocolor → sin colores ANSI para facilitar el parsing de texto.
        r = _run(["rc-status", "--all", "--nocolor"])

        if r.returncode != 0:
            raise InitError(f"rc-status falló: {_texto(r)}")

        resultados: list[dict] = []

        for linea in r.stdout.splitlines():
            # rc-status imprime líneas como:
            #   " * nginx                     [ started ]"
            #   " * crond                     [ started ]"
            # Las líneas de runlevel comienzan sin espacios o con "Runlevel: ".
            linea_strip = linea.strip()

            # Ignoramos líneas de cabecera (runlevel, separadores vacíos).
            if not linea_strip or linea_strip.startswith("Runlevel:"):
                continue

            # Removemos el "*" inicial que OpenRC pone delante de cada servicio.
            if linea_strip.startswith("*"):
                linea_strip = linea_strip[1:].strip()

            # Separamos por "[ ... ]" para extraer nombre y estado.
            if "[" in linea_strip and "]" in linea_strip:
                # La parte izquierda del "[" es el nombre del servicio.
                nombre_servicio = linea_strip[:linea_strip.index("[")].strip()
                # La parte entre "[" y "]" es el estado.
                estado = linea_strip[linea_strip.index("[") + 1:linea_strip.index("]")].strip()

                # Solo incluimos servicios que estén "started" (activos).
                if estado == "started" and nombre_servicio:
                    resultados.append({
                        "unidad": nombre_servicio,  # Nombre del servicio OpenRC.
                        "estado": estado,           # "started" en OpenRC.
                    })

        return resultados

    # ── Creación y gestión de unidades (v0.2) ─────────────────────────────────

    def soporta_crear_unidades(self) -> bool:
        """OpenRC sí permite crear servicios (init scripts en /etc/init.d)."""
        return True

    @property
    def _dir_init_d(self) -> str:
        """Directorio donde residen los scripts de servicio de OpenRC."""
        return "/etc/init.d"

    def _nombre_archivo(self, nombre: str) -> str:
        """Normaliza el nombre del servicio OpenRC (sin .service, sin guiones raros)."""
        nombre = nombre.strip()
        # OpenRC no usa la extensión .service.
        if nombre.endswith(".service"):
            nombre = nombre[: -len(".service")]
        if not nombre:
            nombre = "lumina-service"
        return nombre

    def _escribir_script(self, nombre: str, contenido: str) -> None:
        """Escribe el init script en ``/etc/init.d`` y lo hace ejecutable (con sudo)."""
        ruta = f"{self._dir_init_d}/{nombre}"

        try:
            # Escritura segura vía archivo temporal + sudo install (evita que
            # la contraseña de sudo corrompa el contenido del script).
            escribir_archivo_privilegiado(
                ruta, contenido, modo="0755", propietario="root", grupo="root"
            )
        except PriviledgeError as error:
            raise InitError(f"no se pudo escribir el servicio '{nombre}': {error}")

        # Los scripts de OpenRC deben ser ejecutables (0755 ya lo garantiza
        # vía install), pero lo reforzamos por compatibilidad con sistemas
        # donde el directorio esté montado con opciones restrictivas.
        try:
            r = ejecutar(["chmod", "+x", ruta], timeout=10)
        except PriviledgeError as error:
            raise InitError(f"no se pudo hacer ejecutable '{nombre}': {error}")
        if r.returncode != 0:
            raise InitError(f"chmod falló para '{nombre}': {_texto(r)}")

    def _que_supervise_duemon(self) -> bool:
        """Indica si OpenRC soporta ``supervise-daemon`` (auto-reinicio)."""
        # supervise-daemon existe desde OpenRC 0.17 (presente en Alpine 3.x moderno).
        return shutil.which("supervise-daemon") is not None

    def daemon_reload(self) -> None:
        """OpenRC no necesita recarga tras crear scripts de init."""
        return  # No-op: los init scripts se leen directamente.

    def habilitar(self, nombre: str, activo: bool = True) -> None:
        """Habilita (``rc-update add``) o deshabilita (``rc-update del``) el servicio."""
        accion = "add" if activo else "del"
        try:
            r = ejecutar(["rc-update", accion, nombre, "default"], timeout=30)
        except PriviledgeError as error:
            raise InitError(f"rc-update {accion} {nombre}: {error}")
        if r.returncode != 0:
            raise InitError(f"rc-update {accion} {nombre}: {_texto(r)}")

    def crear_unidad(
        self,
        nombre: str,
        *,
        comando: str,
        ruta: str,
        usuario: Optional[str] = None,
        entorno: Optional[dict] = None,
        auto_inicio: bool = False,
        auto_reinicio: bool = False,
        descripcion: str = "",
    ) -> str:
        """Crea un servicio OpenRC: init script + (opcional) rc-update add.

        Genera un script compatible con OpenRC moderno usando
        ``start-stop-daemon`` (o ``supervise-daemon`` cuando se pide
        auto-reinicio, para que el proceso se re-arranque al caer).
        """
        nombre_s = self._nombre_archivo(nombre)
        ruta_abs = Path(ruta or "~").expanduser() or Path.home()
        usuario_target = usuario or ("" if es_root() else __import__("getpass").getuser())

        # Construimos el comando en dos partes: binario + argumentos.
        programa, *argumentos = (comando or "true").split()

        lineas = ["#!/sbin/openrc-run", f"name=\"{descripcion or nombre_s}\""]

        if self._que_supervise_duemon() and auto_reinicio:
            # supervise-daemon añade respawn para auto-reinicio automático.
            lineas += [
                "supervisor=supervise-daemon",
                f"command=\"{programa}\"",
                f"command_args=\"{' '.join(argumentos)}\"",
                f"directory=\"{ruta_abs}\"",
                "supervise_daemon_args=\"--respawn --respawn-delay 3\"",
            ]
        else:
            lineas += [
                f"command=\"{programa}\"",
                f"command_args=\"{' '.join(argumentos)}\"",
                f"directory=\"{ruta_abs}\"",
            ]

        if usuario_target:
            lineas.append(f"command_user=\"{usuario_target}\"")

        # Variables de entorno extra.
        entorno = entorno or {}
        if entorno:
            env = " ".join(f"{k}=\"{v}\"" for k, v in entorno.items())
            lineas.append(f'export {env}')

        lineas.append("")
        contenido = "\n".join(lineas) + "\n"

        self._escribir_script(nombre_s, contenido)

        if auto_inicio:
            self.habilitar(nombre_s, activo=True)

        return nombre_s
