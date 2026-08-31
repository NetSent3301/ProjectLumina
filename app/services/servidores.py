"""Lógica de negocio de servidores remotos (agentes Lumina).

Cada servidor registrado apunta a la API de otra instancia de Lumina;
su conexión se comprueba con una petición ligera a esa API remota.
"""

from datetime import datetime, timezone

import httpx
from fastapi import HTTPException
from sqlmodel import select

from ..db import Session, engine
from ..models.servidor import Servidor, ServidorCreate

_TIMEOUT = 3.0


def _normalizar_url(url: str) -> str:
    url = url.strip().rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url


def _chequear(s: Servidor) -> dict:
    """Estado en vivo de un servidor remoto (sin usar proxies)."""
    headers = {"X-API-Key": s.token} if s.token else {}
    try:
        respuesta = httpx.get(
            f"{_normalizar_url(s.url)}/api/servidor",
            headers=headers,
            timeout=_TIMEOUT,
            trust_env=False,
        )
        if respuesta.status_code == 200:
            alcanzable, detalle = True, "conectado"
        elif respuesta.status_code == 401:
            alcanzable, detalle = False, "token incorrecto (HTTP 401)"
        else:
            alcanzable, detalle = False, f"respuesta HTTP {respuesta.status_code}"
    except httpx.HTTPError:
        alcanzable, detalle = False, "sin acceso (¿API apagada o URL incorrecta?)"

    return {
        "id": s.id,
        "nombre": s.nombre,
        "url": s.url,
        "conexion": alcanzable,
        "detalle": detalle,
        "ultimo_check": datetime.now(timezone.utc).isoformat(),
    }


def listar() -> list[dict]:
    with Session(engine) as session:
        servidores = session.exec(select(Servidor)).all()
    return [_chequear(s) for s in servidores]


def crear(datos: ServidorCreate) -> dict:
    with Session(engine) as session:
        existente = session.exec(
            select(Servidor).where(Servidor.nombre == datos.nombre.strip())
        ).first()
        if existente:
            raise HTTPException(
                status_code=409, detail="ya existe un servidor con ese nombre"
            )
        servidor = Servidor(
            nombre=datos.nombre.strip(),
            url=_normalizar_url(datos.url),
            token=datos.token,
        )
        session.add(servidor)
        session.commit()
        session.refresh(servidor)
        creado = {"id": servidor.id, "nombre": servidor.nombre, "url": servidor.url}
    return {**creado, **_chequear(servidor)}


def eliminar(servidor_id: int) -> None:
    with Session(engine) as session:
        servidor = session.get(Servidor, servidor_id)
        if not servidor:
            raise HTTPException(status_code=404, detail="servidor no encontrado")
        session.delete(servidor)
        session.commit()


def resumen_conexion() -> dict:
    """Estado global de la conexión.

    El principal es esta misma API: si se logra preguntarle, se tiene
    acceso a él (el frontend no podría cargar datos si no).
    """
    remotos = listar()
    return {
        "principal": {"nombre": "este equipo", "alcanzable": True},
        "servidores": remotos,
        "conectado_a": sum(1 for s in remotos if s["conexion"]),
        "sin_acceso_a": sum(1 for s in remotos if not s["conexion"]),
        "total_remotos": len(remotos),
    }