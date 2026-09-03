"""Backend de init system: **systemd**.

Implementa ``InitBackend`` usando ``systemctl`` (para gestión de servicios)
y ``journalctl`` (para obtener logs). Es el backend predeterminado en la
gran mayoría de distribuciones Linux modernas (Debian, Ubuntu, Arch, Fedora…).

Degradación elegante:
    Si ``systemctl`` no está en PATH (p. ej. en desarrollo local), los métodos
    lanzan ``InitError`` con un mensaje claro en lugar de crashear con
    ``FileNotFoundError``.

Compatibilidad:
    La excepción ``SystemdError`` se mantiene como alias de ``InitError``
    para no romper código externo que ya la importe directamente.
"""

from __future__ import annotations  # Permite usar nombres de tipos en anotaciones antes de definirlos.

import os
import shutil      # Para ``shutil.which``: verifica si un binario existe en PATH.
import subprocess  # Para ejecutar comandos del sistema y capturar su salida.

from .base import InitBackend, InitError  # Contrato abstracto e excepción base.
from .privilegios import PriviledgeError, ejecutar, es_root


# ─────────────────────────────────────────────────────────────────────────────
# Alias de compatibilidad
# ─────────────────────────────────────────────────────────────────────────────

#: Alias de ``InitError`` para no romper código que ya importe ``SystemdError``.
SystemdError = InitError


# ─────────────────────────────────────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────────────────────────────────────

def _run(cmd: list[str], timeout: int = 15) -> subprocess.CompletedProcess:
    """Ejecuta un comando y captura stdout/stderr.

    Args:
        cmd:     Lista de strings que forman el comando (sin shell).
        timeout: Segundos máximos de espera antes de abortar.

    Returns:
        El ``CompletedProcess`` con ``stdout``, ``stderr`` y ``returncode``.

    Raises:
        InitError: Si el comando no existe en PATH o supera el timeout.
    """
    # Verificamos que el binario principal (primer elemento) exista en PATH.
    if shutil.which(cmd[0]) is None:
        raise InitError(f"'{cmd[0]}' no está disponible en este sistema")

    try:
        # capture_output=True → captura stdout y stderr por separado.
        # text=True           → decodifica bytes a str con el encoding del sistema.
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        # El init system tardó más de lo aceptable; lo reportamos como error.
        raise InitError(f"'{cmd[0]}' tardó demasiado (timeout={timeout}s)") from None


def _texto(r: subprocess.CompletedProcess) -> str:
    """Extrae el texto de salida de un proceso: prefiere stderr, cae a stdout.

    En systemd los errores suelen ir a stderr; el output normal va a stdout.
    Esta función normaliza eso para los mensajes de error.

    Args:
        r: Resultado del proceso.

    Returns:
        Texto de stderr o stdout, sin espacios al inicio/final.
    """
    # Si stderr tiene contenido lo usamos; si no, usamos stdout; si no hay nada, "".
    return (r.stderr or r.stdout or "").strip()


# ─────────────────────────────────────────────────────────────────────────────
# Backend
# ─────────────────────────────────────────────────────────────────────────────

class SystemdBackend(InitBackend):
    """Backend que controla servicios a través de ``systemctl`` y ``journalctl``.

    No mantiene estado interno; cada llamada ejecuta el comando en el momento.
    Esto significa que es seguro reusar la misma instancia de forma concurrente.
    """

    # ── Información del backend ───────────────────────────────────────────────

    def nombre(self) -> str:
        """Devuelve el identificador del backend: ``"systemd"``."""
        return "systemd"

    def disponible(self) -> bool:
        """Devuelve ``True`` si ``systemctl`` existe en PATH.

        El detector usa este método para saber si systemd está presente.
        """
        # shutil.which devuelve la ruta completa si existe, o None si no.
        return shutil.which("systemctl") is not None

    def info(self) -> dict:
        """Retorna metadatos del backend para el endpoint ``GET /api/init``.

        Intenta obtener la versión de systemd con ``systemctl --version``.
        Si falla (p. ej. sin privilegios), devuelve ``version=None``.
        """
        version: str | None = None  # Valor por defecto si no podemos leer la versión.

        try:
            # ``systemctl --version`` devuelve algo como "systemd 255 (255-..."
            r = _run(["systemctl", "--version"])
            if r.returncode == 0 and r.stdout:
                # Tomamos la primera línea y el segundo token ("255").
                version = r.stdout.splitlines()[0].split()[1]
        except InitError:
            pass  # Si el comando falla simplemente dejamos version=None.

        return {
            "backend": self.nombre(),  # "systemd"
            "version": version,        # Versión numérica o None.
            "pid1": "systemd",         # En sistemas con systemd, PID 1 siempre es systemd.
        }

    # ── Estado de un servicio ─────────────────────────────────────────────────

    def is_active(self, nombre: str) -> bool:
        """Comprueba si la unidad ``nombre`` está activa según systemd.

        Usa ``systemctl is-active <nombre>`` que devuelve exit 0 y escribe
        "active" a stdout cuando la unidad está corriendo.

        Args:
            nombre: Nombre de la unidad (p. ej. ``"nginx.service"``).

        Returns:
            ``True`` solo si el exit code es 0 y stdout == "active".
        """
        try:
            r = _run(["systemctl", "is-active", nombre])
        except InitError:
            # Si systemctl no está disponible asumimos "no activo".
            return False
        # Doble comprobación: exit 0 Y texto "active" para evitar falsos positivos.
        return r.returncode == 0 and r.stdout.strip() == "active"

    # ── Acciones ──────────────────────────────────────────────────────────────

    def _ejecutar(self, nombre: str, accion: str) -> None:
        """Ejecuta ``systemctl <accion> <nombre>`` y lanza ``InitError`` si falla.

        Args:
            nombre: Nombre de la unidad systemd.
            accion: Subcomando de systemctl: ``"start"``, ``"stop"``, ``"restart"``.

        Raises:
            InitError: Con ``no_existe=True`` si la unidad no está registrada.
        """
        # Ejecutamos el comando real.
        r = _run(["systemctl", accion, nombre])

        if r.returncode != 0:
            # Normalizamos el texto de error a minúsculas para la búsqueda de palabras clave.
            texto = _texto(r).lower()

            # Detectamos si el error es "no existe" buscando mensajes conocidos de systemd.
            no_existe = (
                "not found" in texto
                or "could not be found" in texto
                or "failed to get unit" in texto
            )

            # Lanzamos con el texto original (sin lower) para que el usuario lo vea legible.
            raise InitError(
                f"systemctl {accion} {nombre}: {_texto(r)}",
                no_existe=no_existe,
            )

    def iniciar(self, nombre: str) -> None:
        """Inicia la unidad systemd ``nombre`` con ``systemctl start``."""
        self._ejecutar(nombre, "start")

    def detener(self, nombre: str) -> None:
        """Detiene la unidad systemd ``nombre`` con ``systemctl stop``."""
        self._ejecutar(nombre, "stop")

    def reiniciar(self, nombre: str) -> None:
        """Reinicia la unidad systemd ``nombre`` con ``systemctl restart``."""
        self._ejecutar(nombre, "restart")

    # ── Logs ──────────────────────────────────────────────────────────────────

    def log_lines(self, nombre: str, lines: int = 100) -> str:
        """Devuelve las últimas ``lines`` líneas del journal de la unidad.

        Usa ``journalctl -u <nombre> -n <lines> --no-pager`` para obtener
        los logs sin que journalctl intente paginar la salida.

        Args:
            nombre: Nombre de la unidad (p. ej. ``"sshd.service"``).
            lines:  Número de líneas a retornar.

        Returns:
            Texto con los logs, posiblemente vacío.

        Raises:
            InitError: Si journalctl falla o no existe.
        """
        # max(1, lines) evita pasar 0 o negativos a journalctl.
        r = _run(["journalctl", "-u", nombre, "-n", str(max(1, lines)), "--no-pager"])

        if r.returncode != 0:
            texto = _texto(r).lower()
            no_existe = (
                "not found" in texto
                or "could not be found" in texto
                or "failed to get unit" in texto
            )
            raise InitError(
                f"journalctl {nombre}: {_texto(r)}",
                no_existe=no_existe,
            )

        # Devolvemos el stdout tal cual; la capa de servicio decide cómo usarlo.
        return r.stdout

    # ── Listado ───────────────────────────────────────────────────────────────

    def servicios_activos(self) -> list[dict]:
        """Lista todas las unidades de tipo ``service`` con estado ``running``.

        Usa ``systemctl list-units --type=service --state=running --no-legend``
        para obtener solo los servicios activos sin la cabecera decorativa.

        Returns:
            Lista de dicts con claves ``unidad``, ``carga`` y ``estado``.

        Raises:
            InitError: Si systemctl falla.
        """
        # --no-legend elimina la cabecera y el pie de la tabla de systemctl.
        r = _run(["systemctl", "list-units", "--type=service", "--state=running", "--no-legend"])

        if r.returncode != 0:
            raise InitError(f"list-units falló: {_texto(r)}")

        resultados: list[dict] = []

        for linea in r.stdout.splitlines():
            # Cada línea tiene la forma: "nginx.service loaded active running NGINX server"
            partes = linea.split()
            if partes:  # Ignoramos líneas vacías.
                resultados.append({
                    "unidad": partes[0],                          # Nombre de la unidad.
                    "carga": partes[1] if len(partes) > 1 else "",  # Estado de carga (loaded…).
                    "estado": partes[2] if len(partes) > 2 else "",  # Estado de activación.
                })

        return resultados

    # ── Creación y gestión de unidades (v0.2) ─────────────────────────────────

    def soporta_crear_unidades(self) -> bool:
        """systemd sí permite crear unidades de servicio."""
        return True

    @property
    def _dir_unidades(self) -> str:
        """Directorio donde systemd lee los archivos .service del administrador."""
        return "/etc/systemd/system"

    def _nombre_archivo(self, nombre: str) -> str:
        """Normaliza el nombre de la unidad asegurando la extensión ``.service``."""
        nombre = nombre.strip()
        if not nombre.endswith(".service"):
            nombre += ".service"
        return nombre

    def _escribir_unidad(self, nombre_archivo: str, contenido: str) -> None:
        """Escribe el archivo de unidad en ``/etc/systemd/system`` con sudo si hace falta.

        Usa ``tee`` para respetar redirección y permisos vía ``sudo``.
        """
        ruta = os.path.join(self._dir_unidades, nombre_archivo)

        try:
            # Escribimos usando un comando que acepte el contenido por stdin.
            r = ejecutar(
                ["tee", ruta],
                stdin_texto=contenido,
                timeout=15,
            )
        except PriviledgeError as error:
            raise InitError(
                f"no se pudo escribir la unidad '{nombre_archivo}': {error}",
                no_existe=False,
            ) from None

        if r.returncode != 0:
            raise InitError(
                f"no se pudo escribir la unidad '{nombre_archivo}': "
                f"{_texto(r)}"
            )

    def daemon_reload(self) -> None:
        """Recarga la configuración de systemd tras crear/editar unidades."""
        try:
            r = ejecutar(["systemctl", "daemon-reload"], timeout=30)
        except PriviledgeError as error:
            raise InitError(f"daemon-reload falló: {error}") from None

        if r.returncode != 0:
            raise InitError(f"daemon-reload falló: {_texto(r)}")

    def habilitar(self, nombre: str, activo: bool = True) -> None:
        """Habilita (``enable``) o deshabilita (``disable``) el arranque al boot."""
        accion = "enable" if activo else "disable"
        try:
            r = ejecutar(["systemctl", accion, nombre], timeout=30)
        except PriviledgeError as error:
            raise InitError(f"systemctl {accion} {nombre}: {error}") from None

        if r.returncode != 0:
            raise InitError(f"systemctl {accion} {nombre}: {_texto(r)}")

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
        """Genera, instala y (opcionalmente) habilita una unidad systemd.

        El contenido del archivo ``.service`` se construye a partir de los
        parámetros y se escribe en ``/etc/systemd/system``.  Tras escribirlo
        se ejecuta ``daemon-reload`` y, si se pide, ``enable``.
        """
        nombre_archivo = self._nombre_archivo(nombre)
        unidad = os.path.basename(nombre_archivo)

        # Usuario del sistema: por defecto el que corre el panel.
        if usuario is None and not es_root():
            import getpass
            usuario = getpass.getuser()
        usuario_target = usuario or ""

        lineas = ["[Unit]"]
        lineas.append(f"Description={descripcion or unidad}")

        # Configuración de reinicio automático (Restart= on-failure).
        restart = "on-failure" if auto_reinicio else "no"
        restart_sec = "3" if auto_reinicio else ""

        lineas.append("")
        lineas.append("[Service]")
        if usuario_target:
            lineas.append(f"User={usuario_target}")
        lineas.append(f"WorkingDirectory={ruta}")
        lineas.append(f"ExecStart={comando}")
        lineas.append(f"Restart={restart}")
        if restart_sec:
            lineas.append(f"RestartSec={restart_sec}")

        # Variables de entorno extra que la unidad debe recibir.
        entorno = entorno or {}
        if entorno:
            for clave, valor in entorno.items():
                lineas.append(f"Environment={clave}={valor}")

        lineas.append("")
        lineas.append("[Install]")
        lineas.append("WantedBy=multi-user.target")
        contenido = "\n".join(lineas) + "\n"

        # 1) Escribir la unidad.
        self._escribir_unidad(nombre_archivo, contenido)

        # 2) Recargar para que systemd conozca la nueva unidad.
        self.daemon_reload()

        # 3) Habilitar arranque al boot si se solicita.
        if auto_inicio:
            self.habilitar(unidad, activo=True)

        return unidad
# ─────────────────────────────────────────────────────────────────────────────
# El código anterior a la refactorización importaba funciones sueltas de este
# módulo (p. ej. ``from ..system import systemd; systemd.is_active(...)``).
# Mantenemos esas funciones como thin wrappers sobre el backend para no romper
# nada.  Los módulos nuevos deben usar ``get_backend()`` del detector.

_backend = SystemdBackend()  # Instancia singleton usada por los wrappers legados.


def is_active(nombre: str) -> bool:
    """[Legado] Comprueba si la unidad systemd está activa. Usa ``SystemdBackend``."""
    return _backend.is_active(nombre)


def iniciar(nombre: str) -> None:
    """[Legado] Inicia una unidad systemd. Usa ``SystemdBackend``."""
    _backend.iniciar(nombre)


def detener(nombre: str) -> None:
    """[Legado] Detiene una unidad systemd. Usa ``SystemdBackend``."""
    _backend.detener(nombre)


def reiniciar(nombre: str) -> None:
    """[Legado] Reinicia una unidad systemd. Usa ``SystemdBackend``."""
    _backend.reiniciar(nombre)


def log_lines(nombre: str, lines: int = 100) -> str:
    """[Legado] Devuelve logs de journalctl. Usa ``SystemdBackend``."""
    return _backend.log_lines(nombre, lines)


def servicios_activos() -> list[dict]:
    """[Legado] Lista servicios systemd activos. Usa ``SystemdBackend``."""
    return _backend.servicios_activos()