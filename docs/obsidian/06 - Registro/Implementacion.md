# 🛠️ Implementación — ProjectLumina

> Estado actual de la base del proyecto y qué queda pendiente.

---

## Estado

La **base inicial** del proyecto está montada y **funciona localmente** (sin el servidor), y el **dashboard web está en maqueta** con estados vacíos.

Corresponde a la fase "Preparar el terreno", previa al desarrollo real de [[v0.1]].

---

## Qué está hecho

- ✅ Repositorio **Git** inicializado (rama `main`).
- ✅ Entorno virtual (`.venv`) y dependencias: **FastAPI**, Uvicorn, pytest, httpx.
- ✅ **`lumina.py`** — backend mínimo.
  - ✅ Servidor que arranca.
  - ✅ Endpoint `GET /api/health` de verificación → [[API]].
  - ✅ Sirve el panel en `/` con cambio de vista sin recargar (hash `#/resumen`, `#/servicios`); `/servicios` redirige a `/#/servicios`.
  - ✅ Archivos estáticos montados en `/static` (`StaticFiles`) → [[Decisiones#Sirviendo estáticos con StaticFiles]] · [[Errores#CSS y JS del dashboard no cargaban]].
- ✅ **Frontend reorganizado**: `web/templates/` + `web/static/` (css, js, assets).
- ✅ **Dashboard en maqueta** con estados vacíos (sin datos falsos) → [[Dashboard#Base actual]] · [[UI - Sistema de Diseno]]:
  - ✅ Una sola página con vistas **resumen** (`/`) y **servicios** (`/#/servicios`), sin recargas.
  - ✅ Vista servicios con selector bots/webs (pestañas 🤖/🌐) → [[Bots]] · [[Webs]].
  - ✅ Cabecera de estado y tarjetas vacías con chip "disponible en v0.1".
  - ✅ Registro de actividad con estado vacío (solo en resumen).
  - ✅ Micro-animaciones (entrada escalonada, hover, flotación, registro) y respeto de `prefers-reduced-motion` → [[Frontend#Diseño y animaciones]].
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
- ❌ Conectar el dashboard a datos reales (reemplazar los estados vacíos) → [[Frontend#Base actual]].

---

## Relacionado

- [[Estado Actual]] · En qué fase estamos.
- [[v0.1]] · Próximo entregable.
- [[Decisiones]] · Por qué FastAPI y cómo se sirven los estáticos.
- [[Changelog]] · Registro de cambios recientes.
- [[UI - Sistema de Diseno]] · Identidad visual del dashboard.
- [[Git y GitHub]] · Control de versiones.
- [Ver planificación completa](ProjectLumina_Planificacion)
