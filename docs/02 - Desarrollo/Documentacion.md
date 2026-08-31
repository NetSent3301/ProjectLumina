# 📚 Documentacion — ProjectLumina

> Gestión de la documentación del proyecto.

---

## Estructura

La documentación es **una única fuente** en `docs/`: funciona a la vez como **vault de Obsidian** (se abre esta carpeta como vault) y como **documentación legible en GitHub**.

```text
docs/
├── README.md          ← índice general
├── 00 - Inicio        ← visión, objetivos, estado actual
├── 01 - Planificacion ← requisitos, arquitectura, roadmap, tareas
├── 02 - Desarrollo    ← backend, frontend, API, dashboard, bots, webs…
├── 03 - Seguridad     ← acceso remoto, autenticación, permisos
├── 04 - Investigacion ← Debian, Linux, redes, SSH, systemd
├── 05 - Versiones     ← v0.1 · v0.2 · v0.3
└── 06 - Registro      ← changelog, errores, decisiones, implementación
```

→ [Inicio](../00%20-%20Inicio/Inicio.md) · [README general](../README.md).

---

## Técnica "carpeta cero" (Index)

Cada carpeta usa un número de orden:

```text
00 - Inicio
01 - Planificacion
02 - Desarrollo
03 - Seguridad
04 - Investigacion
05 - Versiones
06 - Registro
```

> Los prefijos numéricos mantienen el orden en Obsidian.

---

## Buenas prácticas

- Usar **enlaces relativos** (`[Nota](ruta.md)`) para conectar ideas → renderizan bien en **GitHub** y en **Obsidian**, y alimentan el grafo.
- Mantener una nota **índice** por carpeta.
- Registrar cambios en [Changelog](../06%20-%20Registro/Changelog.md) · [Errores](../06%20-%20Registro/Errores.md) · [Decisiones](../06%20-%20Registro/Decisiones.md).

---

## Relacionado

- [Inicio](../00%20-%20Inicio/Inicio.md) · Mapa central.
- [Changelog](../06%20-%20Registro/Changelog.md) · Registro de cambios.
- [Decisiones](../06%20-%20Registro/Decisiones.md) · Decisiones registradas.
- [Git y GitHub](Git%20y%20GitHub.md) · Versión de la documentación.
- [Inicio](../00%20-%20Inicio/Inicio.md)
