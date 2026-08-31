"""Capa de sistema: interacción con systemd (systemctl + journalctl).

Es la única capa que ejecuta comandos del sistema operativo. Diseñada con
degradación elegante: si systemctl no está disponible (p. ej. durante el
desarrollo local sin el servidor), lanza `SystemdError` clasificando si la
unidad no existe, para que la capa de servicios devuelva un HTTP correcto.
"""

import shutil
import subprocess


class SystemdError(RuntimeError):
    """Error al interactuar con systemd."""

    def __init__(self, mensaje: str, no_existe: bool = False):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.no_existe = no_existe


def _systemctl(*args) -> subprocess.CompletedProcess:
    if shutil.which("systemctl") is None:
        raise SystemdError("systemctl no está disponible en este sistema")
    try:
        return subprocess.run(
            ["systemctl", *args], capture_output=True, text=True, timeout=15
        )
    except subprocess.TimeoutExpired:
        raise SystemdError("systemctl tardó demasiado") from None


def _journalctl(*args) -> subprocess.CompletedProcess:
    if shutil.which("journalctl") is None:
        raise SystemdError("journalctl no está disponible en este sistema")
    try:
        return subprocess.run(
            ["journalctl", *args], capture_output=True, text=True, timeout=15
        )
    except subprocess.TimeoutExpired:
        raise SystemdError("journalctl tardó demasiado") from None


def _resultado(r: subprocess.CompletedProcess) -> str:
    return (r.stderr or r.stdout or "").strip()


def is_active(nombre: str) -> bool:
    """Devuelve si la unidad systemd está activa."""
    try:
        r = _systemctl("is-active", nombre)
    except SystemdError:
        return False
    return r.returncode == 0 and r.stdout.strip() == "active"


def _ejecutar(nombre: str, accion: str) -> None:
    r = _systemctl(accion, nombre)
    if r.returncode != 0:
        texto = _resultado(r).lower()
        no_existe = (
            "not found" in texto
            or "could not be found" in texto
            or "failed to get unit" in texto
        )
        raise SystemdError(
            f"systemctl {accion} {nombre}: {_resultado(r)}",
            no_existe=no_existe,
        )


def iniciar(nombre: str) -> None:
    _ejecutar(nombre, "start")


def detener(nombre: str) -> None:
    _ejecutar(nombre, "stop")


def reiniciar(nombre: str) -> None:
    _ejecutar(nombre, "restart")


def log_lines(nombre: str, lines: int = 100) -> str:
    """Últimas líneas del log de la unidad (journalctl)."""
    r = _journalctl("-u", nombre, "-n", str(max(1, lines)), "--no-pager")
    if r.returncode != 0:
        texto = _resultado(r).lower()
        no_existe = (
            "not found" in texto
            or "could not be found" in texto
            or "failed to get unit" in texto
        )
        raise SystemdError(
            f"journalctl {nombre}: {_resultado(r)}",
            no_existe=no_existe,
        )
    return r.stdout


def servicios_activos() -> list[dict]:
    """Unidades systemd de tipo servicio que están activas."""
    r = _systemctl("list-units", "--type=service", "--state=running", "--no-legend")
    if r.returncode != 0:
        raise SystemdError(f"list-units: {_resultado(r)}")
    resultados = []
    for linea in r.stdout.splitlines():
        partes = linea.split()
        if partes:
            resultados.append(
                {"unidad": partes[0], "carga": partes[1], "estado": partes[2]}
            )
    return resultados