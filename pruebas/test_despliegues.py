"""Tests de la lógica de despliegue de bots (v0.2).

Se prueban las partes deterministas (auto-detección de comando y clipping de
nombres) sin ejecutar comandos reales del sistema, para no tocar systemd ni
requerir privilegios en los tests.
"""

from pathlib import Path


_raiz = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(_raiz))

from app.services.despliegues import _autodetect_tipo  # noqa: E402


def _repos_con(archivos: dict) -> Path:
    import tempfile
    d = Path(tempfile.mkdtemp(prefix="repo_test_"))
    for nombre, contenido in archivos.items():
        p = d / nombre
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(contenido)
    return d


def test_autodetect_main_py():
    d = _repos_con({"main.py": "print('hola')"})
    tipo, cmd = _autodetect_tipo("", d)
    assert tipo == "bot"
    assert cmd == "python3 main.py"


def test_autodetect_requirements():
    d = _repos_con({"main.py": "x", "requirements.txt": "requests\n"})
    tipo, cmd = _autodetect_tipo("", d)
    assert (tipo, cmd) == ("bot", "python3 main.py")


def test_autodetect_node_start():
    import json
    d = _repos_con({"package.json": json.dumps({"scripts": {"start": "node bot.js"}})})
    tipo, cmd = _autodetect_tipo("", d)
    assert cmd == "node bot.js"


def test_autodetect_node_sin_start():
    import json
    d = _repos_con({"package.json": json.dumps({})})
    tipo, cmd = _autodetect_tipo("", d)
    assert cmd == "node ."


def test_autodetect_go():
    d = _repos_con({"go.mod": "module x"})
    tipo, cmd = _autodetect_tipo("", d)
    assert cmd == "go run ."


def test_autodetect_vacio_sin_comando():
    d = _repos_con({"README.md": "sin codigo"})
    tipo, cmd = _autodetect_tipo("", d)
    assert cmd == ""