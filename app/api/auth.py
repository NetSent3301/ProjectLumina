"""Autenticación MVP: token de API.

- Header `X-API-Key: <token>` o `Authorization: Bearer <token>`.
- Si `LUMINA_TOKEN` está vacío (dev local) la autenticación se desactiva.
- Con token configurado, sin token válido → 401.
"""

from typing import Optional

from fastapi import Header, HTTPException

from ..config import get_settings


def require_token(
    x_api_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
) -> None:
    esperado = get_settings().token
    if not esperado:
        # Sin token configurado: solo entorno de desarrollo local.
        return

    proporcionado = None
    if x_api_key:
        proporcionado = x_api_key
    elif authorization and authorization.lower().startswith("bearer "):
        proporcionado = authorization[7:]

    if not proporcionado or proporcionado != esperado:
        raise HTTPException(status_code=401, detail="token inválido o ausente")