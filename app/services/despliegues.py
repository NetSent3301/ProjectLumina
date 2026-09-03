"""Lógica de negocio de despliegue de bots desde repositorios git.

Une el sistema de archivos (git clone/install), la capa de init system
(crear unidad) y la base de datos (registrar el servicio). El resultado es
un "asistente" que con solo nombre + URL del repo deja el bot corriendo.

Seguridad:
    * El ``token`` del repositorio (privado) se usa solo en el momento del
      clon y **no se persiste**.
    * Toda la creación de unidades requiere privilegios vía sudo.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Optional

import httpx
from fastapi import HTTPException
from sqlmodel import select

from ..config import get_settings
from ..db import engine, Session
from ..models.despliegue import DespliegueGit
from ..models.servicio import Servicio, TipoServicio
from ..system import get_backend, InitError
from ..system.privilegios import PriviledgeError, ejecutar, verificar_privilegios

#: Carpetas por defecto donde se alojan los bots desplegados.
_DEFECTO_BASE = "~/bots"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers privados
# ─────────────────────────────────────────────────────────────────────────────

def _autodetect_tipo(repo_url: str, ruta: Path) -> str:
    """Determina el lenguaje/comando del proyecto según los archivos presentes.

    Returns:
        Tuple con (tipo_servicio, comando_por_defecto).
        tipo: ``"bot"`` o ``"web"``; comando: recomendado o "".
    """
    if (ruta / "requirements.txt").exists() or (ruta / "pyproject.toml").exists():
        return "bot", "python3 main.py"
    if (ruta / "package.json").exists():
        # No sabemos si es una API (web) o un bot JS; asumimos bot por defecto.
        return "bot", "node ."
    if (ruta / "go.mod").exists():
        return "bot", "go run ."
    return "bot", ""


def _clonar(repo_url: str, destino: Path, token: str) -> None:
    """Clona el repositorio en ``destino``, soportando repos privados con token.

    Raises:
        HTTPException: 502 si el clon falla, 409 si el destino ya existe.
    """
    if destino.exists():
        raise HTTPException(
            status_code=409,
            detail=f"el destino '{destino}' ya existe. elige otra ruta o elimínalo.",
        )

    destino.parent.mkdir(parents=True, exist_ok=True)

    # Para repos privados usamos el token embebido en la URL (https).
    if token and repo_url.startswith("https://"):
        repo_url_clon = repo_url.replace(
            "https://", f"https://x-access-token:{token}@", 1
        )
    else:
        repo_url_clon = repo_url

    try:
        r = subprocess.run(
            ["git", "clone", "--depth", "1", repo_url_clon, str(destino)],
            capture_output=True,
            text=True,
            timeout=180,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=502, detail="'git' no está instalado en este servidor")
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=502, detail="el clon tardó demasiado (timeout=180s)")

    if r.returncode != 0:
        mensaje = (r.stderr or r.stdout or "").strip()
        if "could not read Username" in mensaje or "Authentication failed" in mensaje:
            raise HTTPException(
                status_code=502,
                detail="no se pudo autenticar contra el repositorio. comprueba el token/permisos.",
            )
        raise HTTPException(status_code=502, detail=f"git clone falló: {mensaje}")


def _instalar_deps(ruta: Path, tipo_servicio: str) -> None:
    """Instala las dependencias del proyecto detectadas en la carpeta."""
    pip = shutil.which("pip3") or shutil.which("pip")
    if pip:
        req = ruta / "requirements.txt"
        if req.exists():
            subprocess.run(
                [pip, "install", "-r", str(req)],
                capture_output=True,
                text=True,
                timeout=300,
            )
            return

    # Node/package.json
    if (ruta / "package.json").exists():
        npm = shutil.which("npm")
        if npm:
            subprocess.run(
                [npm, "install"],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(ruta),
            )


# ─────────────────────────────────────────────────────────────────────────────
# Despliegue
# ─────────────────────────────────────────────────────────────────────────────

def desplegar(datos: DespliegueGit) -> dict:
    """Despliega un bot desde git y lo deja corriendo como servicio.

    El flujo completo:
        1. Autentica/verifica la capacidad privilegiada (sudo).
        2. Clona el repositorio en la ruta destino.
        3. Detecta lenguaje y comando por defecto.
        4. Instala dependencias (opcional).
        5. Crea la unidad systemd (con auto-inicio/reinicio reales).
        6. Registra el servicio en la base de datos.
        7. Inicia la unidad.

    Returns:
        Dict con el servicio registrado (de ``servicios._publico``).

    Raises:
        HTTPException: 409 si el nombre o destino ya existen; 502 en fallos.
    """
    from . import servicios as servi_svcs  # import tardío para evitar circular.

    # 1) Capacidad privilegiada.
    try:
        verificar_privilegios()
    except PriviledgeError as error:
        raise HTTPException(status_code=403, detail=str(error))

    # 2) Resolver ruta destino.
    ruta_orig = datos.ruta or f"{_DEFECTO_BASE}/{datos.nombre}"
    ruta = Path(ruta_orig).expanduser()

    # 3) Clonar.
    _clonar(datos.repo_url, ruta, datos.token)

    try:
        # 4) Auto-detección de tipo/comando.
        tipo_val, comando_default = _autodetect_tipo(datos.repo_url, ruta)
        comando = datos.comando.strip() or comando_default

        # 5) Instalar dependencias.
        if datos.instalar_deps:
            _instalar_deps(ruta, tipo_val)

        # 6) Crear unidad systemd.
        unidad = _crear_unidad(datos, ruta, comando)

        # 7) Registrar en DB.
        servicio = _registrar_servicio(datos, ruta, comando, unidad)

        # 8) Iniciar la unidad.
        try:
            get_backend().iniciar(unidad)
            servicio["estado"] = "online"
        except InitError:
            servicio["estado"] = "offline"

        servicio["unidad_creada"] = True
        return servicio
    except HTTPException:
        # Si algo falla a mitad, intentamos limpiar el clon para no dejar basura.
        shutil.rmtree(ruta, ignore_errors=True)
        raise


def _crear_unidad(datos: DespliegueGit, ruta: Path, comando: str) -> str:
    """Crea la unidad systemd para el bot desplegado.

    Returns:
        El nombre de la unidad creada (con extensión).
    """
    backend = get_backend()

    if not backend.soporta_crear_unidades():
        raise HTTPException(
            status_code=422,
            detail=f"el init system '{backend.nombre()}' no soporta crear unidades.",
        )

    nombre_unidad = datos.nombre.lower().replace(" ", "-")
    if not nombre_unidad:
        nombre_unidad = "lumina-bot"

    try:
        return backend.crear_unidad(
            nombre_unidad,
            comando=comando or "sleep infinity",
            ruta=str(ruta),
            auto_inicio=datos.auto_inicio,
            auto_reinicio=datos.auto_reinicio,
            descripcion=f"Bot {datos.nombre} desplegado por ProjectLumina",
        )
    except InitError as error:
        raise HTTPException(status_code=502, detail=error.mensaje)


def _registrar_servicio(datos: DespliegueGit, ruta: Path, comando: str, unidad: str) -> dict:
    """Registra el bot como servicio en la base de datos.

    Returns:
        Representación pública del servicio recién creado.
    """
    with Session(engine) as session:
        existente = session.exec(
            select(Servicio).where(Servicio.nombre == datos.nombre)
        ).first()
        if existente:
            raise HTTPException(
                status_code=409,
                detail="ya existe un servicio con ese nombre",
            )

        tipo = TipoServicio.bot  # Por ahora los despliegues git son bot.

        servicio = Servicio(
            tipo=tipo,
            nombre=datos.nombre,
            ruta=str(ruta),
            comando=comando,
            servicio=unidad,
            auto_inicio=datos.auto_inicio,
            auto_reinicio=datos.auto_reinicio,
        )
        session.add(servicio)
        session.commit()
        session.refresh(servicio)

        from .servicios import _publico  # import tardío para evitar circular.
        return _publico(servicio)
