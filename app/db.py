"""Acceso a la base de datos SQLite (SQLModel).

El motor se crea a partir de la configuración (LUMINA_DB). Las tablas se
crean en `init_db()`, que se llama al construir la aplicación.
"""

from pathlib import Path

from sqlmodel import SQLModel, Session, create_engine

from .config import get_settings


def _engine():
    cfg = get_settings()
    db_path = Path(cfg.db)
    if db_path.suffix in (".db", ".sqlite", ".sqlite3"):
        db_path.parent.mkdir(parents=True, exist_ok=True)
    url = f"sqlite:///{db_path}"
    return create_engine(url, connect_args={"check_same_thread": False})


engine = _engine()


def init_db():
    """Crea las tablas si no existen (idempotente)."""
    from . import models  # noqa: F401  (registra los modelos en SQLModel.metadata)

    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependencia que entrega una sesión de base de datos."""
    with Session(engine) as session:
        yield session