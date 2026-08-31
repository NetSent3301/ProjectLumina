"""Lógica de negocio de servicios (bots y webs).

Une la base de datos (SQLModel) con la capa de init system (auto-detectada
por ``detector.get_backend()``) y el chequeo HTTP de webs.
Devuelve dicts listos para la API.

Cambio respecto a la versión anterior:
    Ya no importa ``systemd`` directamente. En su lugar llama a
    ``get_backend()`` para obtener el backend correcto según el init
    system del host (systemd, OpenRC, Runit o SysV).  Esto hace que el
    módulo funcione sin cambios en Alpine Linux, Void Linux, etc.
"""

from datetime import datetime, timezone  # Para timestamps UTC en los cambios de estado.
from typing import Optional              # Para campos opcionales en firmas de función.

import httpx           # Cliente HTTP para comprobar si las webs responden.
from fastapi import HTTPException  # Para devolver errores HTTP con código correcto.
from sqlmodel import select        # ORM de consultas SQLModel.

from ..db import engine, Session  # Motor de base de datos y sesión SQLModel.
from ..models.servicio import Servicio, ServicioCreate, ServicioUpdate, TipoServicio

# Importamos a través del __init__.py del módulo system, no desde systemd.py.
# Esto garantiza que se use el backend auto-detectado para el host actual.
from ..system import get_backend, InitError

#: Número máximo de líneas de log que se pueden solicitar en un request.
#: Límite de seguridad para evitar respuestas enormes.
_MAX_LINES = 500


# ─────────────────────────────────────────────────────────────────────────────
# Helpers privados
# ─────────────────────────────────────────────────────────────────────────────

def _utcnow() -> datetime:
    """Devuelve el timestamp actual en UTC con timezone aware.

    Se usa para registrar cuándo ocurrió el último cambio de estado.
    Devolver un datetime con timezone evita bugs de comparación naive vs aware.
    """
    return datetime.now(timezone.utc)


def _chequear_web(s: Servicio) -> str:
    """Determina el estado de una web haciendo una petición HTTP a su ``check_url``.

    Si el servicio no tiene ``check_url`` configurada, no podemos saber si
    está online y devolvemos ``"offline"`` como estado conservador.

    Args:
        s: El objeto ``Servicio`` de tipo ``web`` a comprobar.

    Returns:
        ``"online"`` si la URL responde con HTTP < 400, ``"offline"`` si no.
    """
    if not s.check_url:
        # Sin URL de chequeo no podemos determinar el estado; asumimos offline.
        return "offline"

    try:
        # Hacemos una petición GET con timeout de 8 segundos para no bloquear.
        respuesta = httpx.get(s.check_url, timeout=8)
        # Cualquier código < 400 se considera "online" (incluyendo redirects 3xx).
        return "online" if respuesta.status_code < 400 else "offline"
    except httpx.HTTPError:
        # Error de red, DNS, SSL, timeout… cualquier excepción httpx = offline.
        return "offline"


def _estado_actual(s: Servicio) -> str:
    """Determina el estado en tiempo real de un servicio.

    Para servicios de tipo ``web``: hace un chequeo HTTP.
    Para servicios de tipo ``bot``: consulta el init system del host.

    Args:
        s: El objeto ``Servicio`` cuyo estado queremos conocer.

    Returns:
        ``"online"`` si el servicio está activo, ``"offline"`` si no.
    """
    if s.tipo == TipoServicio.web:
        # Las webs se chequean por HTTP, no por el init system.
        return _chequear_web(s)

    # Para bots: usamos el backend auto-detectado del init system.
    # get_backend() devuelve el mismo objeto en llamadas subsiguientes (caché).
    if s.servicio and get_backend().is_active(s.servicio):
        return "online"

    return "offline"


def _publico(s: Servicio) -> dict:
    """Construye la representación pública de un servicio con su estado en vivo.

    Esta es la única función que convierte el modelo ORM a un dict plano
    que la API puede serializar a JSON. Centralizar aquí evita inconsistencias.

    Args:
        s: El objeto ``Servicio`` de la base de datos.

    Returns:
        Dict con todos los campos del servicio y su estado en tiempo real.
    """
    return {
        "id": s.id,                                              # Clave primaria.
        "tipo": s.tipo.value,                                    # "bot" o "web" (string).
        "nombre": s.nombre,                                      # Nombre legible del servicio.
        "ruta": s.ruta,                                          # Ruta del directorio del proyecto.
        "comando": s.comando,                                    # Comando de inicio manual.
        "servicio": s.servicio,                                  # Nombre en el init system.
        "check_url": s.check_url,                                # URL para health check (webs).
        "auto_inicio": s.auto_inicio,                            # Si debe iniciarse al arrancar.
        "auto_reinicio": s.auto_reinicio,                        # Si el init debe reiniciarlo al caer.
        "estado": _estado_actual(s),                             # Estado en vivo (online/offline).
        "creado": s.creado.isoformat() if s.creado else None,    # Timestamp de creación (ISO 8601).
        "ultimo_estado": s.ultimo_estado,                        # Último estado registrado en DB.
        "ultimo_cambio": s.ultimo_cambio.isoformat() if s.ultimo_cambio else None,
    }


def _buscar(session: Session, servicio_id: int) -> Servicio:
    """Busca un servicio en la base de datos por ID o lanza HTTP 404.

    Args:
        session:     Sesión SQLModel activa.
        servicio_id: ID del servicio a buscar.

    Returns:
        El objeto ``Servicio`` encontrado.

    Raises:
        HTTPException: Con status 404 si el servicio no existe en la DB.
    """
    s = session.get(Servicio, servicio_id)
    if not s:
        raise HTTPException(status_code=404, detail="servicio no encontrado")
    return s


# ─────────────────────────────────────────────────────────────────────────────
# CRUD público
# ─────────────────────────────────────────────────────────────────────────────

def listar(tipo: Optional[str] = None) -> list[dict]:
    """Devuelve todos los servicios registrados, opcionalmente filtrados por tipo.

    Args:
        tipo: ``"bot"`` o ``"web"`` para filtrar. ``None`` devuelve todos.

    Returns:
        Lista de representaciones públicas de los servicios.

    Raises:
        HTTPException: Con status 422 si ``tipo`` tiene un valor no válido.
    """
    with Session(engine) as session:
        consulta = select(Servicio)

        if tipo:
            try:
                # Convertimos el string a enum; si el valor no existe, ValueError.
                consulta = consulta.where(Servicio.tipo == TipoServicio(tipo))
            except ValueError:
                raise HTTPException(
                    status_code=422, detail="tipo debe ser 'bot' o 'web'"
                )

        servicios = session.exec(consulta).all()
        # Construimos el dict público para cada servicio (incluye estado en vivo).
        return [_publico(s) for s in servicios]


def detalle(servicio_id: int) -> dict:
    """Devuelve los detalles completos de un servicio por su ID.

    Args:
        servicio_id: ID del servicio.

    Returns:
        Representación pública del servicio.

    Raises:
        HTTPException: Con status 404 si no existe.
    """
    with Session(engine) as session:
        return _publico(_buscar(session, servicio_id))


def crear(datos: ServicioCreate) -> dict:
    """Registra un nuevo servicio en la base de datos.

    Args:
        datos: Datos validados del nuevo servicio (nombre, tipo, etc.).

    Returns:
        Representación pública del servicio recién creado.

    Raises:
        HTTPException: Con status 409 si ya existe un servicio con ese nombre.
    """
    with Session(engine) as session:
        # Comprobamos unicidad del nombre antes de insertar.
        existente = session.exec(
            select(Servicio).where(Servicio.nombre == datos.nombre)
        ).first()

        if existente:
            raise HTTPException(
                status_code=409,
                detail="ya existe un servicio con ese nombre",
            )

        # Creamos el objeto ORM desde el dict de datos validados.
        servicio = Servicio(**datos.model_dump())
        session.add(servicio)
        session.commit()
        session.refresh(servicio)  # Recargamos para obtener el ID autogenerado.
        return _publico(servicio)


def actualizar(servicio_id: int, cambios: ServicioUpdate) -> dict:
    """Actualiza los campos editables de un servicio existente.

    Solo actualiza los campos presentes en ``cambios`` (PATCH semántico).
    Los campos no presentes en el request no se modifican.

    Args:
        servicio_id: ID del servicio a actualizar.
        cambios:     Campos a modificar (todos opcionales).

    Returns:
        Representación pública del servicio actualizado.

    Raises:
        HTTPException: Con status 404 si el servicio no existe.
    """
    with Session(engine) as session:
        servicio = _buscar(session, servicio_id)

        # exclude_unset=True → solo los campos incluidos en el request JSON.
        for campo, valor in cambios.model_dump(exclude_unset=True).items():
            setattr(servicio, campo, valor)  # Actualizamos cada campo en el objeto ORM.

        session.add(servicio)
        session.commit()
        session.refresh(servicio)
        return _publico(servicio)


def eliminar(servicio_id: int) -> None:
    """Elimina permanentemente un servicio de la base de datos.

    No detiene el servicio en el init system; solo borra el registro en DB.

    Args:
        servicio_id: ID del servicio a eliminar.

    Raises:
        HTTPException: Con status 404 si el servicio no existe.
    """
    with Session(engine) as session:
        servicio = _buscar(session, servicio_id)
        session.delete(servicio)
        session.commit()


# ─────────────────────────────────────────────────────────────────────────────
# Control de estado (start / stop / restart)
# ─────────────────────────────────────────────────────────────────────────────

def _registrar_cambio(session: Session, servicio: Servicio, estado: Optional[str]) -> None:
    """Guarda en la base de datos el último estado conocido y su timestamp.

    Se llama después de cada operación exitosa sobre el init system.

    Args:
        session:  Sesión SQLModel activa.
        servicio: El objeto Servicio cuyo estado cambió.
        estado:   El nuevo estado (``"online"`` / ``"offline"``).
    """
    servicio.ultimo_estado = estado       # Guardamos el estado textual.
    servicio.ultimo_cambio = _utcnow()    # Timestamp del cambio.
    session.add(servicio)
    session.commit()


def accion(servicio_id: int, operacion: str) -> dict:
    """Ejecuta una acción de control sobre un servicio: iniciar, detener o reiniciar.

    Delega en el backend de init system auto-detectado para el host.
    Después de la operación, consulta el estado real y lo persiste en DB.

    Args:
        servicio_id: ID del servicio en la base de datos.
        operacion:   ``"iniciar"``, ``"detener"`` o ``"reiniciar"``.

    Returns:
        Representación pública del servicio con el estado actualizado.

    Raises:
        HTTPException: 422 si la operación no es válida o no hay unidad configurada.
        HTTPException: 404 si el servicio no existe en el init system.
        HTTPException: 502 si el init system devuelve un error.
    """
    # Validamos la operación antes de tocar la base de datos.
    if operacion not in ("iniciar", "detener", "reiniciar"):
        raise HTTPException(status_code=422, detail="operación no válida")

    with Session(engine) as session:
        servicio = _buscar(session, servicio_id)
        unidad = servicio.servicio  # Nombre de la unidad en el init system.

        if not unidad:
            # El servicio no tiene nombre de unidad configurado; no podemos controlarlo.
            raise HTTPException(
                status_code=422,
                detail="este servicio no tiene unidad de init configurada",
            )

        backend = get_backend()  # Obtiene el backend cacheado (systemd, OpenRC, etc.).

        try:
            # ``getattr`` nos permite llamar backend.iniciar / backend.detener / backend.reiniciar
            # sin un switch-case, usando la operación como nombre de método.
            getattr(backend, operacion)(unidad)
        except InitError as error:
            # 404 si la unidad no existe en el init system; 502 para otros errores.
            codigo = 404 if error.no_existe else 502
            raise HTTPException(status_code=codigo, detail=error.mensaje)

        # Después de la operación, consultamos el estado real para persistirlo.
        estado = "online" if backend.is_active(unidad) else "offline"
        _registrar_cambio(session, servicio, estado)

        return _publico(servicio)


# ─────────────────────────────────────────────────────────────────────────────
# Logs
# ─────────────────────────────────────────────────────────────────────────────

def logs(servicio_id: int, lines: int = 100) -> dict:
    """Devuelve las últimas líneas de log del servicio.

    Delega en el backend de init system para obtener los logs. El mecanismo
    varía por backend: journalctl (systemd), syslog filtrado (OpenRC/SysV),
    o svlogd (Runit/OpenRC).

    Args:
        servicio_id: ID del servicio.
        lines:       Número de líneas a devolver (clamped a 1-500).

    Returns:
        Dict con ``id``, ``unidad``, ``lines``, ``backend`` y ``log``.

    Raises:
        HTTPException: 422 si el servicio no tiene unidad configurada.
        HTTPException: 404 si la unidad no existe en el init system.
        HTTPException: 502 si el backend falla al obtener los logs.
    """
    with Session(engine) as session:
        servicio = _buscar(session, servicio_id)

    unidad = servicio.servicio
    if not unidad:
        raise HTTPException(
            status_code=422, detail="este servicio no tiene unidad de init configurada"
        )

    # Aplicamos el clamp para evitar requests de logs extremadamente grandes.
    lines = max(1, min(lines, _MAX_LINES))

    backend = get_backend()  # Backend auto-detectado del host.

    try:
        contenido = backend.log_lines(unidad, lines)
    except InitError as error:
        codigo = 404 if error.no_existe else 502
        raise HTTPException(status_code=codigo, detail=error.mensaje)

    return {
        "id": servicio_id,        # ID del servicio en DB.
        "unidad": unidad,         # Nombre de la unidad en el init system.
        "lines": lines,           # Número de líneas solicitadas.
        "backend": backend.nombre(),  # Nombre del backend usado (p. ej. "openrc").
        "log": contenido,         # Texto del log.
    }