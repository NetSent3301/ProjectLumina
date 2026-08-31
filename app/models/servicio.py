"""Modelo de datos: tabla única `servicios` (bots y webs).

Según la arquitectura definitiva del MVP y las decisiones del proyecto
([[Arquitectura]], [[Base de Datos]]).
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TipoServicio(str, Enum):
    bot = "bot"
    web = "web"


class Servicio(SQLModel, table=True):
    __tablename__ = "servicios"

    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: TipoServicio
    nombre: str
    ruta: str = ""
    comando: str = ""
    servicio: str = ""
    check_url: Optional[str] = None
    auto_inicio: bool = False
    auto_reinicio: bool = False
    creado: datetime = Field(default_factory=_utcnow)
    ultimo_estado: Optional[str] = None
    ultimo_cambio: Optional[datetime] = None


class ServicioCreate(SQLModel):
    """Datos para registrar un servicio."""

    tipo: TipoServicio
    nombre: str
    ruta: str = ""
    comando: str = ""
    servicio: str = ""
    check_url: Optional[str] = None
    auto_inicio: bool = False
    auto_reinicio: bool = False


class ServicioUpdate(SQLModel):
    """Datos editables de un servicio (todos opcionales)."""

    nombre: Optional[str] = None
    ruta: Optional[str] = None
    comando: Optional[str] = None
    servicio: Optional[str] = None
    check_url: Optional[str] = None
    auto_inicio: Optional[bool] = None
    auto_reinicio: Optional[bool] = None