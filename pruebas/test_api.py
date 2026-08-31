# Tests de la API REST de v0.1 (auth, CRUD de servicios y acciones).
# El token y la base de datos temporal se configuran en conftest.py.
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

HEADERS = {"X-API-Key": "tokentest"}


def test_api_requiere_token():
    assert client.get("/api/servicios").status_code == 401
    assert client.post("/api/servicios", json={}).status_code == 401


def test_crud_con_token():
    # Empieza vacía.
    assert client.get("/api/servicios", headers=HEADERS).json() == []

    # Crear un bot.
    r = client.post(
        "/api/servicios",
        json={
            "tipo": "bot",
            "nombre": "mini",
            "ruta": "/home/u/bots",
            "comando": "python bot.py",
            "servicio": "mini.service",
        },
        headers=HEADERS,
    )
    assert r.status_code == 201
    creado = r.json()
    sid = creado["id"]
    assert creado["tipo"] == "bot"
    assert "estado" in creado

    # Listar por tipo.
    lista = client.get("/api/servicios?tipo=bot", headers=HEADERS).json()
    assert len(lista) == 1 and lista[0]["nombre"] == "mini"

    # Detalle.
    det = client.get(f"/api/servicios/{sid}", headers=HEADERS)
    assert det.status_code == 200
    assert det.json()["id"] == sid

    # Editar (PATCH).
    p = client.patch(
        f"/api/servicios/{sid}", json={"nombre": "mini2"}, headers=HEADERS
    )
    assert p.status_code == 200
    assert p.json()["nombre"] == "mini2"

    # Tipo inválido al listar → 422.
    assert client.get("/api/servicios?tipo=xyz", headers=HEADERS).status_code == 422

    # Acción contra unit inexistente (o sin systemctl) → error controlado.
    reinicio = client.post(f"/api/servicios/{sid}/reiniciar", headers=HEADERS)
    assert reinicio.status_code in (404, 502)

    # Logs: journalctl no falla por unidad inexistente → log vacío.
    logs = client.get(f"/api/servicios/{sid}/logs", headers=HEADERS)
    assert logs.status_code == 200
    assert logs.json()["log"].strip() in ("", "-- No entries --")

    # Eliminar.
    assert client.delete(f"/api/servicios/{sid}", headers=HEADERS).status_code == 204
    assert client.get("/api/servicios", headers=HEADERS).json() == []

    # Detalle de un id inexistente → 404.
    assert client.get(f"/api/servicios/{sid}", headers=HEADERS).status_code == 404


def test_web_con_check_url():
    r = client.post(
        "/api/servicios",
        json={
            "tipo": "web",
            "nombre": "sitioweb",
            "servicio": "sitioweb.service",
            "check_url": "http://127.0.0.1:1/",
        },
        headers=HEADERS,
    )
    assert r.status_code == 201
    sid = r.json()["id"]
    # URL inalcanzable → offline, pero petición responde.
    det = client.get(f"/api/servicios/{sid}", headers=HEADERS).json()
    assert det["estado"] == "offline"
    client.delete(f"/api/servicios/{sid}", headers=HEADERS)


def test_nombre_duplicado_rechazado():
    datos = {"tipo": "bot", "nombre": "unico"}
    assert client.post("/api/servicios", json=datos, headers=HEADERS).status_code == 201

    duplicado = client.post("/api/servicios", json=datos, headers=HEADERS)
    assert duplicado.status_code == 409
    assert duplicado.json()["detail"] == "ya existe un servicio con ese nombre"
    assert len(client.get("/api/servicios", headers=HEADERS).json()) == 1

    sid = client.get("/api/servicios", headers=HEADERS).json()[0]["id"]
    client.delete(f"/api/servicios/{sid}", headers=HEADERS)


def test_servidores_y_conexion():
    # Sin remotos: el principal (esta API) siempre es alcanzable.
    assert client.get("/api/servidores", headers=HEADERS).json() == []
    conexion = client.get("/api/conexion", headers=HEADERS).json()
    assert conexion["principal"]["alcanzable"] is True
    assert conexion["total_remotos"] == 0

    # Registro de un agente inalcanzable (nada escucha en ese puerto).
    r = client.post(
        "/api/servidores",
        json={"nombre": "pi", "url": "http://127.0.0.1:1"},
        headers=HEADERS,
    )
    assert r.status_code == 201
    sid = r.json()["id"]
    assert r.json()["conexion"] is False

    # Duplicado rechazado.
    duplicado = client.post(
        "/api/servidores",
        json={"nombre": "pi", "url": "http://127.0.0.1:2"},
        headers=HEADERS,
    )
    assert duplicado.status_code == 409

    # El listado refleja su conexión y el resumen global los cuenta.
    lista = client.get("/api/servidores", headers=HEADERS).json()
    assert len(lista) == 1
    assert lista[0]["conexion"] is False
    assert lista[0]["detalle"].startswith("sin acceso")

    conexion = client.get("/api/conexion", headers=HEADERS).json()
    assert conexion["total_remotos"] == 1
    assert conexion["sin_acceso_a"] == 1
    assert conexion["conectado_a"] == 0

    # Eliminar (y 404 si ya no existe).
    assert client.delete(f"/api/servidores/{sid}", headers=HEADERS).status_code == 204
    assert client.get("/api/servidores", headers=HEADERS).json() == []
    assert client.delete(f"/api/servidores/{sid}", headers=HEADERS).status_code == 404