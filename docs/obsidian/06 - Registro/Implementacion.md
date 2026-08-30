# 🛠️ Implementación — ProjectLumina

> Estado actual de la base del proyecto y qué queda pendiente.

---

## Estado

La **base inicial** del proyecto ya está montada y **funciona localmente** (sin necesidad del servidor).

Corresponde a la fase "Preparar el terreno", previa al desarrollo real de [[v0.1]].

---

## Qué está hecho

- ✅ Repositorio **Git** inicializado (rama `main`).
- ✅ Entorno virtual (`.venv`) y dependencias: **FastAPI**, Uvicorn, pytest, httpx.
- ✅ **`lumina.py`** — backend mínimo en un único archivo.
  - ✅ Servidor que arranca.
  - ✅ Endpoint `GET /api/health` de verificación → [[API]].
  - ✅ Sirve la página `web/index.html` en la raíz `/` → [[Frontend]].
- ✅ Frontend mínimo (`web/index.html`) que comprueba la conexión con el backend → [[Frontend]].
- ✅ Script de arranque `scripts/run.sh` → un solo comando para lanzar todo.
- ✅ Test básico del endpoint → [[Dashboard#Testing]].
- ✅ Backend con **FastAPI** → [[Decisiones#Backend con FastAPI]].

---

## Cómo ejecutarlo

```bash
bash scripts/run.sh
```

- Web: http://127.0.0.1:8000/
- API de prueba: http://127.0.0.1:8000/api/health

---

## Pendiente (para [[v0.1]])

> Requiere acceso al servidor Debian 13 → [[Servidor]].

- ❌ Gestión real de bots (iniciar/detener/reiniciar/estados/logs) → [[Bots]] · [[Acciones de Bots]].
- ❌ Gestión real de webs → [[Webs]].
- ❌ Métricas del servidor (CPU/RAM/disco/red) → [[Servidor#Información mostrada]].
- ❌ Base de datos y modelos → [[Base de Datos]].
- ❌ Seguridad y exposición a Internet → [[Acceso Remoto]] · [[Autenticacion]].
- ❌ Separar `lumina.py` en módulos → [[Arquitectura#Estructura del código]] (cuando crezca).

---

## Relacionado

- [[Estado Actual]] · En qué fase estamos.
- [[v0.1]] · Próximo entregable.
- [[Decisiones]] · Por qué FastAPI.
- [[Git y GitHub]] · Control de versiones.
- [Ver planificación completa](ProjectLumina_Planificacion)
