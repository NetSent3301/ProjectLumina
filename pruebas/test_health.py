# Test simple del endpoint /api/health.
# Uso:  .venv/bin/pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Permitir importar lumina.py desde la raíz del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lumina import app

client = TestClient(app)


def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
