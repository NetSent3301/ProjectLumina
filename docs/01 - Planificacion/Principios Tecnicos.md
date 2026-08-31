# ⚖️ Principios Técnicos — ProjectLumina

> Principios de diseño que guían todas las decisiones del proyecto.

---

## Modularidad

Cada parte debería poder **modificarse sin destruir todo el proyecto**.

- Backend, frontend, API, bots y webs como módulos separados → [Arquitectura](Arquitectura.md).
- Separar la lógica de administración de la interfaz → [Backend](../02%20-%20Desarrollo/Backend.md).

---

## Simplicidad inicial

**No implementar sistemas complejos antes de necesitarlos.**

- No usar agente en el MVP → [Arquitectura](Arquitectura.md).
- SQLite en lugar de PostgreSQL al inicio → [Base de Datos](../02%20-%20Desarrollo/Base%20de%20Datos.md).
- REST en lugar de WebSockets al inicio → [API](../02%20-%20Desarrollo/API.md).
- Sin sistema de usuarios en el MVP → [Usuarios](../03%20-%20Seguridad/Usuarios.md).

---

## Seguridad

> Toda capacidad de ejecución remota debe tratarse como una **operación privilegiada**.

- → [Permisos](../03%20-%20Seguridad/Permisos.md) · [Acceso Remoto](../03%20-%20Seguridad/Acceso%20Remoto.md) · [Autenticacion](../03%20-%20Seguridad/Autenticacion.md)
- La ejecución remota de comandos es sensible y debe protegerse → [Control Remoto](../02%20-%20Desarrollo/Control%20Remoto.md).

---

## Automatización

Las **tareas repetitivas** deberían poder automatizarse.

- Auto-start y auto-restart → [Auto Restart](../02%20-%20Desarrollo/Auto%20Restart.md).
- Comprobación automática de webs → [Webs](../02%20-%20Desarrollo/Webs.md).
- Detección de procesos caídos → [v0.2](../05%20-%20Versiones/v0.2.md).

---

## Observabilidad

Lumina debe poder **informar qué está ocurriendo** mediante estados y logs.

- Estados de bots/webs → [Dashboard](../02%20-%20Desarrollo/Dashboard.md).
- Logs desplegables → [Dashboard](../02%20-%20Desarrollo/Dashboard.md).
- Métricas del servidor → [Servidor](../02%20-%20Desarrollo/Servidor.md).

---

## Escalabilidad progresiva

El sistema debe poder **crecer sin diseñar desde el principio** una infraestructura gigantesca.

- De un servidor a múltiples → [Roadmap](Roadmap.md).
- De web a apps móviles → [Vision](../00%20-%20Inicio/Vision.md).

---

## Aprendizaje

ProjectLumina también es una **herramienta de aprendizaje** en:

- Python.
- Backend.
- APIs.
- Linux.
- Redes.
- Servidores.
- Procesos.
- Seguridad.
- Desarrollo web.
- Automatización.

→ Ver [Objetivos](../00%20-%20Inicio/Objetivos.md) y carpetas de [investigación](../00%20-%20Inicio/Inicio.md).

---

## Relacionado

- [Vision](../00%20-%20Inicio/Vision.md) · Filosofía general.
- [Requisitos](Requisitos.md) · Criterios de calidad.
- [Decisiones](../06%20-%20Registro/Decisiones.md) · Decisiones basadas en estos principios.
- [Inicio](../00%20-%20Inicio/Inicio.md)
