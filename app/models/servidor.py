"""Modelo de datos: tabla `servidores` (agentes Lumina remotos).

El servidor principal es la máquina donde corre este panel; los
servidores registrados aquí son otras instancias de Lumina a las que
se consulta su API (ver docs/desarrollo/api.md).
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Servidor(SQLModel, table=True):
    __tablename__ = "servidores"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    url: str
    token: str = ""
    creado: datetime = Field(default_factory=_utcnow)


class ServidorCreate(SQLModel):
    """Datos para registrar un agente Lumina remoto."""

    nombre: str
    url: str
    token: str = ""