# 🧩 Sistema Adaptable — ProjectLumina

> Detección e interpretación automática de cómo gestionar bots y webs.

---

## Idea

Una idea importante es que Lumina **no dependa de una plantilla específica** para cada bot o web.

La visión futura es que pueda **determinar cómo gestionar diferentes tipos de proyectos** sin requerir una configuración manual completamente diferente para cada uno.

---

## MVP: configuración explícita

En el MVP la configuración es **explícita y manual**:

```text
Nombre
Ruta
Comando
Tipo
Servicio
```

→ Ver [[Configuracion de Bots]].

---

## Versión posterior: detección automática

```text
Bot/Web
   ↓
Lumina detecta o interpreta
cómo gestionarlo
   ↓
Gestión automática
```

- Detección de tipos.
- Detección de comandos.
- Detección de estructuras comunes.
- Adaptación de configuraciones.
- Plantillas genéricas cuando sean necesarias.

---

## Estado

Esta funcionalidad es **avanzada**, pero se considera **importante** y deberá llegar **relativamente pronto después del MVP** → [[v0.3]].

---

## Relacionado

- [[Bots]] · [[Webs]] · Objetos gestionados.
- [[v0.3]] · Versión donde se implementa.
- [[Configuracion de Bots]] · Configuración actual.
- [[Roadmap]] · Planificación.
- [Ver planificación completa](ProjectLumina_Planificacion)
