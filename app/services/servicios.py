"""Lógica de negocio de servicios (bots y webs).

Une la base de datos (SQLModel) con la capa de sistema (systemd) y el
chequeo HTTP de webs. Devuelve dicts listos para la API.
"""

from datetime import datetime, timezone
from typing import Optional

import httpx
from fastapi import HTTPException
from sqlmodel import select

from ..db import engine, Session
from ..models.servicio import Servicio, ServicioCreate, ServicioUpdate, TipoServicio
from ..system import systemd

_MAX_LINES = 500


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _chequear_web(s: Servicio) -> str:
    """Estado de una web: online si responde bien su check_url."""
    if not s.check_url:
        return "offline"
    try:
        respuesta = httpx.get(s.check_url, timeout=8)
        return "online" if respuesta.status_code < 400 else "offline"
    except httpx.HTTPError:
        return "offline"


def _estado_actual(s: Servicio) -> str:
    """Estado en vivo: systemd (bots) o HTTP (webs con check_url)."""
    if s.tipo == TipoServicio.web:
        return _chequear_web(s)
    if s.servicio and systemd.is_active(s.servicio):
        return "online"
    return "offline"


def _publico(s: Servicio) -> dict:
    """Representación pública de un servicio con su estado en vivo."""
    return {
        "id": s.id,
        "tipo": s.tipo.value,
        "nombre": s.nombre,
        "ruta": s.ruta,
        "comando": s.comando,
        "servicio": s.servicio,
        "check_url": s.check_url,
        "auto_inicio": s.auto_inicio,
        "auto_reinicio": s.auto_reinicio,
        "estado": _estado_actual(s),
        "creado": s.creado.isoformat() if s.creado else None,
        "ultimo_estado": s.ultimo_estado,
        "ultimo_cambio": s.ultimo_cambio.isoformat() if s.ultimo_cambio else None,
    }


def _buscar(session: Session, servicio_id: int) -> Servicio:
    s = session.get(Servicio, servicio_id)
    if not s:
        raise HTTPException(status_code=404, detail="servicio no encontrado")
    return s


def listar(tipo: Optional[str] = None) -> list[dict]:
    with Session(engine) as session:
        consulta = select(Servicio)
        if tipo:
            try:
                consulta = consulta.where(Servicio.tipo == TipoServicio(tipo))
            except ValueError:
                raise HTTPException(
                    status_code=422, detail="tipo debe ser bot o web"
                )
        servicios = session.exec(consulta).all()
        return [_publico(s) for s in servicios]


def detalle(servicio_id: int) -> dict:
    with Session(engine) as session:
        return _publico(_buscar(session, servicio_id))


def crear(datos: ServicioCreate) -> dict:
    with Session(engine) as session:
        servicio = Servicio(**datos.model_dump())
        session.add(servicio)
        session.commit()
        session.refresh(servicio)
        return _publico(servicio)


def actualizar(servicio_id: int, cambios: ServicioUpdate) -> dict:
    with Session(engine) as session:
        servicio = _buscar(session, servicio_id)
        for campo, valor in cambios.model_dump(exclude_unset=True).items():
            setattr(servicio, campo, valor)
        session.add(servicio)
        session.commit()
        session.refresh(servicio)
        return _publico(servicio)


def eliminar(servicio_id: int) -> None:
    with Session(engine) as session:
        servicio = _buscar(session, servicio_id)
        session.delete(servicio)
        session.commit()


def _registrar_cambio(session: Session, servicio: Servicio, estado: Optional[str]):
    servicio.ultimo_estado = estado
    servicio.ultimo_cambio = _utcnow()
    session.add(servicio)
    session.commit()


def accion(servicio_id: int, operacion: str) -> dict:
    """Iniciar, detener o reiniciar un servicio (systemd)."""
    if operacion not in ("iniciar", "detener", "reiniciar"):
        raise HTTPException(status_code=422, detail="operación no válida")

    with Session(engine) as session:
        servicio = _buscar(session, servicio_id)
        unidad = servicio.servicio
        if not unidad:
            raise HTTPException(
                status_code=422,
                detail="este servicio no tiene unidad systemd configurada",
            )

        try:
            getattr(systemd, operacion)(unidad)
        except systemd.SystemdError as error:
            codigo = 404 if error.no_existe else 502
            raise HTTPException(status_code=codigo, detail=error.mensaje)

        estado = (
            "online"
            if systemd.is_active(unidad)
            else "offline"
        )
        _registrar_cambio(session, servicio, estado)
        return _publico(servicio)


def logs(servicio_id: int, lines: int = 100) -> dict:
    with Session(engine) as session:
        servicio = _buscar(session, servicio_id)
    unidad = servicio.servicio
    if not unidad:
        raise HTTPException(
            status_code=422, detail="este servicio no tiene unidad systemd configurada"
        )
    lines = max(1, min(lines, _MAX_LINES))
    try:
        contenido = systemd.log_lines(unidad, lines)
    except systemd.SystemdError as error:
        codigo = 404 if error.no_existe else 502
        raise HTTPException(status_code=codigo, detail=error.mensaje)
    return {"id": servicio_id, "unidad": unidad, "lines": lines, "log": contenido}