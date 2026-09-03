"""Endpoints de actualizaciones: chequeo de releases en GitHub.

Compara la versión actual con la última release/tag en GitHub y notifica
si hay una actualización disponible.
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..config import get_settings
from ..api.auth import require_token

# ─────────────────────────────────────────────────────────────────────────────
# Configuración y constantes
# ─────────────────────────────────────────────────────────────────────────────

log = logging.getLogger("lumina.update")

# Archivo para persistir el estado de actualizaciones entre reinicios
UPDATE_STATE_FILE = Path(__file__).resolve().parents[2] / "data" / "update_state.json"

# Versión actual de la aplicación (hardcoded; en producción podría venir de pyproject.toml)
CURRENT_VERSION = "0.1.1"

# Cache en memoria del último chequeo
_update_cache: dict | None = None
_last_check: float = 0


# ─────────────────────────────────────────────────────────────────────────────
# Modelos Pydantic
# ─────────────────────────────────────────────────────────────────────────────

class UpdateInfo(BaseModel):
    """Información de actualización disponible."""
    hay_actualizacion: bool
    version_actual: str
    version_nueva: Optional[str] = None
    release_url: Optional[str] = None
    release_notes: Optional[str] = None
    publicado_en: Optional[str] = None
    ultimo_chequeo: str
    proximo_chequeo: Optional[str] = None


class UpdateState(BaseModel):
    """Estado persistido de actualizaciones."""
    ultima_version_vista: str = CURRENT_VERSION
    ultima_notificacion: Optional[str] = None
    dismiss_hasta: Optional[str] = None  # ISO timestamp hasta cuándo no molestar


class DismissRequest(BaseModel):
    """Cuerpo de la petición para descartar una actualización."""
    version: str
    horas: int = 24


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades de persistencia
# ─────────────────────────────────────────────────────────────────────────────

def _cargar_estado() -> UpdateState:
    """Carga el estado persistido desde disco."""
    if UPDATE_STATE_FILE.exists():
        try:
            data = json.loads(UPDATE_STATE_FILE.read_text())
            return UpdateState(**data)
        except Exception:
            pass
    return UpdateState()


def _guardar_estado(estado: UpdateState) -> None:
    """Guarda el estado persistido en disco."""
    UPDATE_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    UPDATE_STATE_FILE.write_text(estado.model_dump_json(indent=2))


# ─────────────────────────────────────────────────────────────────────────────
# Lógica de chequeo GitHub
# ─────────────────────────────────────────────────────────────────────────────

async def _obtener_latest_release_github(repo: str, token: str = "") -> dict | None:
    """Obtiene la última release de GitHub (no prerelease, no draft)."""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ProjectLumina/UpdateChecker"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 404:
                # No hay releases; intentar con tags
                return await _obtener_latest_tag_github(repo, token)
            resp.raise_for_status()
            data = resp.json()
            if data.get("draft") or data.get("prerelease"):
                return await _obtener_latest_tag_github(repo, token)
            return data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                log.warning("Rate limit GitHub API (403). ¿Configuraste LUMINA_GITHUB_TOKEN?")
            raise
        except Exception as e:
            log.error(f"Error consultando GitHub releases: {e}")
            return None


async def _obtener_latest_tag_github(repo: str, token: str = "") -> dict | None:
    """Fallback: obtiene el último tag (semver) si no hay releases."""
    url = f"https://api.github.com/repos/{repo}/tags"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ProjectLumina/UpdateChecker"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(url, headers=headers, params={"per_page": 10})
            resp.raise_for_status()
            tags = resp.json()
            if not tags:
                return None
            # Filtrar tags semver válidos (vX.Y.Z o X.Y.Z)
            import re
            semver_re = re.compile(r"^v?\d+\.\d+\.\d+(-.+)?$")
            validos = [t for t in tags if semver_re.match(t["name"])]
            if not validos:
                return None
            # El primer tag suele ser el más reciente en la API
            tag = validos[0]
            # Obtener info del commit/tag para fecha y mensaje
            tag_url = f"https://api.github.com/repos/{repo}/git/ref/tags/{tag['name']}"
            tag_resp = await client.get(tag_url, headers=headers)
            tag_resp.raise_for_status()
            tag_data = tag_resp.json()
            return {
                "tag_name": tag["name"],
                "name": f"Release {tag['name']}",
                "html_url": f"https://github.com/{repo}/releases/tag/{tag['name']}",
                "body": f"Tag {tag['name']} detectado (sin release formal)",
                "published_at": tag_data.get("object", {}).get("date") or tag_data.get("tagger", {}).get("date"),
            }
        except Exception as e:
            log.error(f"Error consultando GitHub tags: {e}")
            return None


def _comparar_versiones(actual: str, nueva: str) -> bool:
    """Compara versiones semver simples. Devuelve True si nueva > actual."""
    def parse(v: str) -> tuple[int, ...]:
        v = v.lstrip("v")
        parts = v.split(".")
        nums = []
        for p in parts:
            # Manejar prerelease: 1.0.0-beta -> 1,0,0
            num_part = p.split("-")[0]
            try:
                nums.append(int(num_part))
            except ValueError:
                nums.append(0)
        return tuple(nums)
    return parse(nueva) > parse(actual)


async def chequear_actualizacion(forzar: bool = False) -> UpdateInfo:
    """Chequea si hay actualización disponible en GitHub.

    Args:
        forzar: Ignora el cache y fuerza chequeo inmediato.

    Returns:
        UpdateInfo con el resultado.
    """
    global _update_cache, _last_check

    settings = get_settings()
    ahora = time.time()
    intervalo_seg = settings.update_check_interval_hours * 3600

    # Usar cache si no ha pasado el intervalo y no se fuerza
    if not forzar and _update_cache and (ahora - _last_check) < intervalo_seg:
        cache = _update_cache.copy()
        cache["proximo_chequeo"] = datetime.fromtimestamp(_last_check + intervalo_seg).isoformat()
        return UpdateInfo(**cache)

    # Cargar estado persistido
    estado = _cargar_estado()

    # Verificar si hay una versión "dismissed" pendiente
    if estado.dismiss_hasta:
        try:
            dismiss_dt = datetime.fromisoformat(estado.dismiss_hasta)
            if datetime.now() < dismiss_dt:
                # Usuario dismissó esta versión; no notificar hasta que pase el tiempo
                return UpdateInfo(
                    hay_actualizacion=False,
                    version_actual=CURRENT_VERSION,
                    ultimo_chequeo=datetime.now().isoformat(),
                    proximo_chequeo=datetime.fromtimestamp(ahora + intervalo_seg).isoformat(),
                )
        except Exception:
            pass

    # Consultar GitHub
    release = await _obtener_latest_release_github(settings.github_repo, settings.github_token)

    hay_actualizacion = False
    version_nueva = None
    release_url = None
    release_notes = None
    publicado_en = None

    if release:
        version_nueva = release.get("tag_name", "").lstrip("v")
        if version_nueva and _comparar_versiones(CURRENT_VERSION, version_nueva):
            hay_actualizacion = True
            release_url = release.get("html_url")
            release_notes = release.get("body")
            publicado_en = release.get("published_at")

    # Actualizar cache
    resultado = {
        "hay_actualizacion": hay_actualizacion,
        "version_actual": CURRENT_VERSION,
        "version_nueva": version_nueva,
        "release_url": release_url,
        "release_notes": release_notes,
        "publicado_en": publicado_en,
        "ultimo_chequeo": datetime.now().isoformat(),
        "proximo_chequeo": datetime.fromtimestamp(ahora + intervalo_seg).isoformat(),
    }
    _update_cache = resultado
    _last_check = ahora

    # Si hay actualización y notificaciones activadas, actualizar estado persistido
    if hay_actualizacion and settings.update_notify_enabled:
        estado.ultima_version_vista = version_nueva or CURRENT_VERSION
        estado.ultima_notificacion = datetime.now().isoformat()
        _guardar_estado(estado)

    return UpdateInfo(**resultado)


def dismiss_actualizacion(version: str, horas: int = 24) -> None:
    """Marca una versión como 'no molestar' por N horas."""
    estado = _cargar_estado()
    estado.dismiss_hasta = (datetime.now() + timedelta(hours=horas)).isoformat()
    estado.ultima_version_vista = version
    _guardar_estado(estado)


# ─────────────────────────────────────────────────────────────────────────────
# Router FastAPI
# ─────────────────────────────────────────────────────────────────────────────

router = APIRouter(prefix="/api", tags=["update"])


@router.get("/update", response_model=UpdateInfo)
async def get_update_info(request: Request, forzar: bool = False):
    """Obtiene información de actualización disponible.

    No requiere token (es de solo lectura informativo).
    """
    return await chequear_actualizacion(forzar=forzar)


@router.post("/update/dismiss")
async def dismiss_update(datos: DismissRequest, _: None = Depends(require_token)):
    """Descarta la notificación de actualización por N horas (requiere token)."""
    dismiss_actualizacion(datos.version, datos.horas)
    return {"ok": True, "dismiss_hasta": (datetime.now() + timedelta(hours=datos.horas)).isoformat()}


@router.post("/update/check")
async def force_update_check(_: None = Depends(require_token)):
    """Fuerza un chequeo inmediato de actualizaciones (requiere token)."""
    return await chequear_actualizacion(forzar=True)