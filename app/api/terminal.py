"""Endpoint WebSocket de terminal interactiva.

La terminal se conecta como el usuario del panel (no root) por defecto, y
queda protegida por el token de API.  El token se pasa por query string
(``?token=...``) porque los navegadores no pueden fijar cabeceras en un
WebSocket.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..config import get_settings
from ..services import terminal

router = APIRouter()


@router.websocket("/api/terminal")
async def terminal_ws(websocket: WebSocket):
    """Sesión WebSocket que abre un shell interactivo en el servidor.

    Autenticación: verifica ``?token=...`` contra ``LUMINA_TOKEN``.
    Si ``LUMINA_TOKEN`` está vacío, no se exige (solo desarrollo local).
    """
    settings = get_settings()
    token_esperado = settings.token

    # Se exige token solo si el servidor tiene uno configurado.
    query_token = websocket.query_params.get("token", "")
    if token_esperado and query_token != token_esperado:
        await websocket.close(code=4401, reason="no autorizado")
        return

    await websocket.accept()

    # cwd opcional: permite iniciar el shell en una ruta concreta del servicio.
    cwd = websocket.query_params.get("cwd")
    if cwd and not cwd.startswith("/"):
        cwd = None

    try:
        await terminal.emparejar(websocket, cwd=cwd)
    except WebSocketDisconnect:
        pass
    except Exception:  # noqa: BLE001 - cualquier error en la sesión termina el socket
        try:
            await websocket.close(code=1011, reason="error en terminal")
        except Exception:
            pass
