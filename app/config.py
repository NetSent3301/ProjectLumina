"""Configuración de ProjectLumina (variables con prefijo LUMINA_).
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """Variables de configuración (prefijo LUMINA_)."""

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_prefix="LUMINA_",
        extra="ignore",
    )

    # Escucha y red.
    host: str = "127.0.0.1"
    port: int = 8000

    # Seguridad: token de API. Vacío = autenticación desactivada (solo local/dev).
    token: str = ""

    # Almacenamiento.
    db: str = str(ROOT / "data" / "lumina.db")
    logs: str = str(ROOT / "logs")

    # Depuración.
    debug: bool = False


def get_settings() -> Settings:
    """Devuelve la configuración actual.

    No se cachea a propósito: así los tests pueden cambiar variables de
    entorno sin dependencias de orden de importación.
    """
    return Settings()