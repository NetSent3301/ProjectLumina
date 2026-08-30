#!/usr/bin/env bash
# ProjectLumina - Arranca el proyecto con un solo comando.
# Uso:  bash run.sh
set -e

# 1) Crear el entorno virtual si no existe
if [ ! -d ".venv" ]; then
  echo "Creando entorno virtual (.venv)..."
  python3 -m venv .venv
fi

# 2) Activar y asegurar dependencias
source .venv/bin/activate
echo "Instalando dependencias..."
pip install --quiet -r requirements.txt

# 3) Arrancar el servidor
echo "Arrancando ProjectLumina en http://127.0.0.1:8000"
uvicorn lumina:app --reload
