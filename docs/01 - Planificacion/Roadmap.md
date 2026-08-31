# 🗺️ Roadmap — ProjectLumina

> Hoja de ruta del proyecto por versiones y etapas.

---

## Versiones

### v0.1 — Base funcional
> **Objetivo:** tener el primer centro de control funcionando.

- Backend.
- Frontend.
- API.
- Dashboard.
- Configuración de bots.
- Configuración de webs.
- Iniciar/detener/reiniciar.
- Estados.
- Logs.
- Métricas básicas.

→ Detalle en [v0.1](../05%20-%20Versiones/v0.1.md)

---

### v0.2 — Automatización
> **Objetivo:** que Lumina empiece a administrar por sí sola.

- Auto-start.
- Auto-restart.
- Detección de procesos caídos.
- Comprobación automática de webs.
- Reintentos.
- Configuración avanzada.
- Mejor manejo de servicios.

→ Detalle en [v0.2](../05%20-%20Versiones/v0.2.md)

---

### v0.3 — Sistema adaptable
> **Objetivo:** reducir la configuración manual.

- Detección de tipos.
- Detección de comandos.
- Detección de estructuras comunes.
- Adaptación de configuraciones.
- Plantillas genéricas cuando sean necesarias.

→ Detalle en [v0.3](../05%20-%20Versiones/v0.3.md)

---

### v0.4+ — Notificaciones
> **Objetivo:** informar al usuario cuando ocurran eventos importantes.

- Bot caído.
- Web caída.
- Reinicio automático.
- Error grave.
- Servidor fuera de línea.
- Alertas personalizadas.

→ Más en [Notificaciones](../02%20-%20Desarrollo/Notificaciones.md)

---

## Etapas futuras

### Futuro — Multi-servidor
> **Objetivo:** administrar múltiples servidores desde una sola instancia de Lumina.

- Aquí podría incorporarse el concepto de **agente** → [Arquitectura](Arquitectura.md).

### Futuro lejano — Plataforma
- Múltiples servidores.
- Servidores de terceros.
- Usuarios.
- Roles.
- Permisos avanzados.
- Aplicación iOS.
- Aplicación Android.
- Backend externo.
- Sistema de agentes.
- Despliegues.
- Automatizaciones avanzadas.

---

## Orden lógico de desarrollo

```text
v0.1 (funcional) → v0.2 (automatización) → v0.3 (adaptable)
→ v0.4+ (notificaciones) → multi-servidor → plataforma
```

Cada versión se apoya en la anterior y se publica según [Changelog](../06%20-%20Registro/Changelog.md) y el control de versiones [Git y GitHub](../02%20-%20Desarrollo/Git%20y%20GitHub.md).

---

## Relacionado

- [Vision](../00%20-%20Inicio/Vision.md) · Visión general.
- [Requisitos](Requisitos.md) · Requisitos por versión.
- [Tareas](Tareas.md) · Tareas a realizar.
- [Estado Actual](../00%20-%20Inicio/Estado%20Actual.md) · Dónde estamos.
- [Inicio](../00%20-%20Inicio/Inicio.md)
