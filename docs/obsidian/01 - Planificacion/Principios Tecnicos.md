# ⚖️ Principios Técnicos — ProjectLumina

> Principios de diseño que guían todas las decisiones del proyecto.

---

## Modularidad

Cada parte debería poder **modificarse sin destruir todo el proyecto**.

- Backend, frontend, API, bots y webs como módulos separados → [[Arquitectura]].
- Separar la lógica de administración de la interfaz → [[Backend#Responsabilidades]].

---

## Simplicidad inicial

**No implementar sistemas complejos antes de necesitarlos.**

- No usar agente en el MVP → [[Arquitectura#Agente Lumina]].
- SQLite en lugar de PostgreSQL al inicio → [[Base de Datos]].
- REST en lugar de WebSockets al inicio → [[API]].
- Sin sistema de usuarios en el MVP → [[Usuarios]].

---

## Seguridad

> Toda capacidad de ejecución remota debe tratarse como una **operación privilegiada**.

- → [[Permisos]] · [[Acceso Remoto]] · [[Autenticacion]]
- La ejecución remota de comandos es sensible y debe protegerse → [[Control Remoto]].

---

## Automatización

Las **tareas repetitivas** deberían poder automatizarse.

- Auto-start y auto-restart → [[Auto Restart]].
- Comprobación automática de webs → [[Webs]].
- Detección de procesos caídos → [[v0.2]].

---

## Observabilidad

Lumina debe poder **informar qué está ocurriendo** mediante estados y logs.

- Estados de bots/webs → [[Dashboard]].
- Logs desplegables → [[Dashboard#Logs]].
- Métricas del servidor → [[Servidor#Información mostrada]].

---

## Escalabilidad progresiva

El sistema debe poder **crecer sin diseñar desde el principio** una infraestructura gigantesca.

- De un servidor a múltiples → [[Roadmap#Etapas futuras]].
- De web a apps móviles → [[Vision#Plataformas]].

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

→ Ver [[Objetivos#Objetivo secundario]] y carpetas de [[Inicio#📚 Investigación|investigación]].

---

## Relacionado

- [[Vision#Filosofía del proyecto]] · Filosofía general.
- [[Requisitos#Requisitos no funcionales]] · Criterios de calidad.
- [[Decisiones]] · Decisiones basadas en estos principios.
- [Ver planificación completa](ProjectLumina_Planificacion)
