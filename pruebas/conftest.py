"""Configuración de entorno para los tests.

Se ejecuta antes que cualquier test: apunta la base de datos a un archivo
temporal y define un token de API, para no tocar `data/lumina.db` real ni
dejar la API sin autenticar.
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

_tmp = tempfile.mkdtemp(prefix="lumina_test_")
os.environ.setdefault("LUMINA_DB", str(Path(_tmp) / "test.db"))
os.environ.setdefault("LUMINA_TOKEN", "tokentest")