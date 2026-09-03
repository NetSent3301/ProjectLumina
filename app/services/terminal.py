"""Terminal interactiva: puente entre un WebSocket y un shell del sistema.

Abre una pseudo-terminal (PTY) corriendo ``bash`` (o el shell configurado)
como el usuario del panel, y conecta su entrada/salida con un cliente
WebSocket.  Permite administrar el servidor desde el navegador de forma
interactiva (como un SSH local).

Seguridad:
    * Por defecto el shell se lanza como el **usuario del panel** (no root):
      es más seguro que dar acceso root total desde la UI.
    * El WebSocket está protegido por el mismo token que el resto de la API.
"""

from __future__ import annotations

import asyncio
import os
import pty
import selectors
import subprocess

#: Lista de shells que admitimos. El primero que exista se usa.
_SHELLS = ["/bin/bash", "/bin/sh"]

#: Comando con el que se lanza el shell interactivo.
def _shell_command() -> list[str]:
    for shell in _SHELLS:
        if os.path.exists(shell):
            return [shell, "-l"]
    return ["/bin/sh"]


class PTYProceso:
    """Maneja un proceso con pseudo-terminal para conectar a un WebSocket.

    Encapsula la creación de la PTY y el puente bidireccional de bytes
    entre el proceso y un buffer que el endpoint WebSocket lee/escribe.
    """

    def __init__(self, cwd: str | None = None) -> None:
        # Abrimos dos fds: maestro (lo lee/usa Python) y esclavo (lo usa bash).
        self._master_fd, _slave_fd = pty.openpty()
        self._selector = selectors.DefaultSelector()
        self._selector.register(self._master_fd, selectors.EVENT_READ)
        self._rupted = False

        env = {**os.environ, "TERM": "xterm-256color"}
        cmd = _shell_command()

        self._proc = subprocess.Popen(
            cmd,
            stdin=_slave_fd,
            stdout=_slave_fd,
            stderr=_slave_fd,
            env=env,
            close_fds=True,
            cwd=cwd or os.path.expanduser("~"),
        )
        os.close(_slave_fd)

    def lectura_disponible(self) -> bool:
        """Indica si hay bytes listos para leer de la PTY."""
        return bool(self._selector.select(timeout=0))

    def leer(self) -> bytes:
        """Lee los bytes disponibles de la PTY (salida del shell).

        El fd maestro de una PTY es **bloqueante**: esta llamada no retorna
        hasta que haya datos o se cierre el canal.  Por eso se invoca desde
        un executor para no bloquear el loop de eventos.

        Returns:
            Bytes leídos (puede ser ``b""`` si se cerró el canal = fin).
        """
        data = os.read(self._master_fd, 65536)
        return data

    def escribir(self, datos: bytes) -> None:
        """Escribe bytes hacia la PTY (entrada del usuario desde el terminal)."""
        os.write(self._master_fd, datos)

    def cerrar(self) -> None:
        """Cierra la PTY y termina el proceso si sigue vivo."""
        if self._rupted:
            return
        self._rupted = True
        try:
            self._selector.unregister(self._master_fd)
        except Exception:
            pass
        try:
            self._selector.close()
        except Exception:
            pass
        try:
            os.close(self._master_fd)
        except OSError:
            pass
        if self._proc.poll() is None:
            try:
                self._proc.terminate()
            except Exception:
                pass

    @property
    def proceso_vivo(self) -> bool:
        return self._proc.poll() is None


async def emparejar(websocket, cwd: str | None = None) -> None:
    """Puente el WebSocket con un shell PTY, sirviendo un terminal interactivo.

    El endpoint WebSocket llama a esta función tras autenticar.  Bucle:
        * Envía la salida del proceso al WebSocket (base64).
        * Recibe entrada del cliente y la escribe en la PTY.
        * Termina cuando el cliente cierra o el proceso muere.

    Args:
        websocket: Websocket conectado (la sesión ya está aceptada).
        cwd:       Directorio de trabajo inicial del shell (None → home).
    """
    pty_proc = PTYProceso(cwd=cwd)
    loop = asyncio.get_running_loop()

    async def _leer_proceso():
        # Lee la salida del proceso de forma bloqueante en un executor
        # (el master fd es bloqueante) y la reenvía al cliente.
        while pty_proc.proceso_vivo and not pty_proc._rupted:
            try:
                data = await loop.run_in_executor(None, pty_proc.leer)
            except OSError:
                break
            if not data:
                break
            if not pty_proc.proceso_vivo and not data:
                break
            import base64
            try:
                await websocket.send_text("out:" + base64.b64encode(data).decode())
            except Exception:
                break
        # El proceso terminó: avisamos al cliente para que cierre el terminal.
        try:
            await websocket.send_text("bye")
        except Exception:
            pass

    try:
        tarea_lectura = asyncio.create_task(_leer_proceso())

        # Bucle principal: espera mensajes del cliente (entrada de teclado).
        while pty_proc.proceso_vivo:
            mensaje = await websocket.receive_text()
            if mensaje.startswith("in:"):
                import base64
                datos = base64.b64decode(mensaje[3:])
                await loop.run_in_executor(None, pty_proc.escribir, datos)
            elif mensaje == "ctrl-c":
                pty_proc.escribir(b"\x03")

        tarea_lectura.cancel()
    finally:
        pty_proc.cerrar()
