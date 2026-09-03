"""Ejecución de comandos privilegiados (root) de forma segura y configurable.

Este módulo centraliza cómo el panel obtiene privilegios para operaciones
que tocan el sistema (crear unidades systemd, escribir en /etc, abrir una
terminal…).

Política:
    * Nunca se hardcodea una contraseña en el código.  La contraseña de
      sudo, si se usa, proviene de la variable de entorno / .env
      ``LUMINA_SUDO_PASSWORD`` (gitignored).
    * Por defecto se intenta ``sudo -n`` (no interactivo, sin prompt): si el
      usuario del panel ya tiene permisos sin contraseña (regla sudoers),
      funciona sin llevar contraseña en memoria.
    * Si ``LUMINA_SUDO_PASSWORD`` está definida, se usa ``sudo -S``
      alimentando la contraseña por stdin.
    * Si el backend corre como root (p. ej. agente Docker ``--privileged``),
      no se antepone sudo en absoluto.

La función ``ejecutar`` sustituye a los ``subprocess.run`` directos para
comandos privilegiados y lanza ``SystemError`` con mensajes claros si no se
disponen de los privilegios necesarios.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from typing import Optional

from ..config import get_settings


class PriviledgeError(RuntimeError):
    """Error al ejecutar un comando privilegiado (permisos, fallo, timeout)."""


def es_root() -> bool:
    """Devuelve ``True`` si el proceso actual corre como root (uid 0)."""
    try:
        return os.geteuid() == 0
    except AttributeError:
        # Plataformas sin geteuid (Windows) → no root.
        return False


def sudo_disponible() -> bool:
    """Devuelve ``True`` si ``sudo`` existe en el sistema."""
    import shutil
    return shutil.which("sudo") is not None


def _prefijo_sudo() -> list[str]:
    """Construye el prefijo sudo adecuado según el entorno de ejecución.

    * Si corremos como root → sin sudo.
    * Si hay contraseña configurada → ``sudo -S -p ''`` (la alimenta quien
      llame pasándola por stdin).
    * Si no hay contraseña → ``sudo -n`` (no interactivo; exige regla sudoers).

    Returns:
        Lista con el comando prefijo (vacía si ya somos root).
    """
    if not _necesita_sudo():
        return []

    settings = get_settings()

    if settings.sudo_password:
        # -S lee la contraseña de stdin; -p '' evita el prompt al stderr.
        return ["sudo", "-S", "-p", ""]

    # Sin contraseña configurada: no interactivo, dependerá de visudo.
    return ["sudo", "-n"]


def _necesita_sudo() -> bool:
    """Indica si hay que elevar privilegios (no somos root)."""
    return not es_root()


def ejecutar(
    cmd: list[str],
    *,
    timeout: int = 30,
    stdin_texto: Optional[str] = None,
    cwd: Optional[str] = None,
    como_servicio: bool = False,
) -> subprocess.CompletedProcess:
    """Ejecuta un comando, elevando privilegios con sudo si hace falta.

    Args:
        cmd:          Comando a ejecutar (sin shell).
        timeout:      Segundos máximos de espera.
        stdin_texto:  Texto a enviar por stdin (si ``sudo -S`` lo requiere).
        cwd:          Directorio de trabajo del comando.
        como_servicio:``True`` si este comando forma parte de una operación
                      de gestión de servicios (permite loggear contexto).

    Returns:
        El ``CompletedProcess``.

    Raises:
        PriviledgeError: Si el comando no existe, supera el timeout o falla
                         por permisos.
    """
    import shutil

    if shutil.which(cmd[0]) is None:
        # Para comandos bajo sudo, comprobamos el binario directamente.
        if not _necesita_sudo() or shutil.which("sudo") is None:
            raise PriviledgeError(
                f"'{cmd[0]}' no está disponible en este sistema"
            )

    prefijo = _prefijo_sudo()
    completo = prefijo + cmd

    # ``stdin_texto`` que se entrega al proceso. Si usamos ``sudo -S``, la
    # primera línea del stdin es la contraseña de sudo y el resto (si lo hay)
    # queda disponible para el comando objetivo (p. ej. ``tee`` que escribirá
    # el contenido del archivo).  Si no hay sudo, todo ``stdin_texto`` va al
    # comando directamente.
    entrada: Optional[str] = stdin_texto
    if prefijo and prefijo[:1] == ["sudo"] and "-S" in prefijo:
        settings = get_settings()
        base_entrada = settings.sudo_password + "\n"
        entrada = base_entrada + (stdin_texto or "")

    try:
        return subprocess.run(
            completo,
            capture_output=True,
            text=True,
            timeout=timeout,
            input=entrada,
            cwd=cwd,
        )
    except subprocess.TimeoutExpired:
        raise PriviledgeError(
            f"comando '{' '.join(cmd)}' tardó demasiado (timeout={timeout}s)"
        ) from None


def verificar_privilegios() -> None:
    """Comprueba si el panel puede ejecutar comandos privilegiados.

    Lanza ``PriviledgeError`` con un mensaje claro si no es posible, para
    que la UI pueda informar al usuario antes de fallar la operación.

    Raises:
        PriviledgeError: Si no hay forma de obtener root.
    """
    if es_root():
        return

    if not sudo_disponible():
        raise PriviledgeError(
            "no hay 'sudo' disponible y el panel no corre como root: "
            "no se pueden ejecutar operaciones privilegiadas"
        )

    # Probamos un sudo no interactivo con ``true``.
    r = ejecutar(["true"], timeout=10)
    if r.returncode != 0:
        raise PriviledgeError(
            "no se pudieron obtener privilegios (sudo): "
            "configura una regla visudo para el usuario del panel o "
            "define LUMINA_SUDO_PASSWORD en el entorno (ver docs). "
            f"salida: {(r.stderr or r.stdout or '').strip()}"
        )


def escribir_archivo_privilegiado(ruta: str, contenido: str,
                                  *, modo: str = "0644",
                                  propietario: str = "root",
                                  grupo: str = "root") -> None:
    """Escribe un archivo con privilegios de root sin mezclar contraseña y contenido.

    Estrategia **segura frente al bug del stdin compartido** de ``sudo -S``:
    escribir el contenido a un archivo temporal (como el usuario del panel,
    sin sudo) y después elevarlo al destino con ``sudo install``.  Así el
    contenido viaja en un archivo y sudo solo recibe la contraseña, sin
    ningún riesgo de que se corrompan entre sí.

    Args:
        ruta:        Ruta destino del archivo.
        contenido:   Contenido de texto a escribir.
        modo:        Permisos en octal (string), p. ej. ``"0644"``.
        propietario: Usuario propietario del archivo.
        grupo:       Grupo propietario del archivo.

    Raises:
        PriviledgeError: Si falla la escritura o la elevación de permisos.
    """
    if es_root():
        # Ya somos root: escribimos directamente.
        os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
        with open(ruta, "w") as f:
            f.write(contenido)
        os.chmod(ruta, int(modo, 8))
        return

    # 1) Escribimos el archivo temporal como usuario normal.
    fd, tmp = tempfile.mkstemp(prefix="lumina-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(contenido)

        # 2) Elevamos: sudo install -o <owner> -g <group> -m <modo> tmp -> ruta.
        r = ejecutar(
            ["install", "-o", propietario, "-g", grupo, "-m", modo, tmp, ruta],
            timeout=20,
        )
        if r.returncode != 0:
            raise PriviledgeError(
                f"no se pudo instalar '{ruta}': "
                f"{(r.stderr or r.stdout or '').strip()}"
            )
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass
