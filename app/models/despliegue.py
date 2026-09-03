"""Modelo de datos para el despliegue de bots desde un repositorio git.

Representa la petición de desplegar un bot: de dónde se clona el código,
a dónde, y cómo se arranca (unidad systemd + auto-inicio/reinicio).
"""

from typing import Optional

from sqlmodel import SQLModel


class DespliegueGit(SQLModel):
    """Datos para desplegar un bot desde un repositorio git.

    Todos los comandos de despliegue se ejecutan como operaciones
    privilegiadas; el panel intenta elevarlas con sudo cuando no corre
    como root.  El ``token`` (para repos privados) solo viaja en la petición
    y no se persiste en la base de datos.
    """

    nombre: str                                    # Nombre legible del bot.
    repo_url: str                                  # URL git del repositorio (https/ssh).
    token: str = ""                                # Token para repos privados (no se guarda).
    ruta: Optional[str] = None                     # Carpeta destino (por defecto ~/bots/<nombre>).
    comando: str = ""                              # Comando de lanzamiento (auto-detectado si vacío).
    tipo: str = "bot"                              # "bot" (o "web" en el futuro).
    auto_inicio: bool = False                      # Habilitar al boot.
    auto_reinicio: bool = False                    # Reiniciar al caer.
    instalar_deps: bool = True                     # Instalar requirements.txt / package.json.
