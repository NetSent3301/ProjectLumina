# Test simple del endpoint /api/health (no requiere token).
# Uso:  .venv/bin/pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_frontend_raiz():
    res = client.get("/")
    assert res.status_code == 200
    assert "Lumina" in res.text


def test_estaticos_y_atajos():
    assert client.get("/static/css/style.css").status_code == 200
    assert (
        client.get("/servicios", follow_redirects=False).status_code == 307
    )