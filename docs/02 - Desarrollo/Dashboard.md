# 📊 Dashboard — ProjectLumina

> El centro de control de ProjectLumina.

---

## Base actual (panel conectado a la API)

El dashboard web consumida la **API REST de v0.1** (estados reales, sin datos falsos) y es **una sola página**: la navegación cambia de vista sin recargar (hash `#/resumen`, `#/servicios`) → [Frontend](Frontend.md) · [UI - Sistema de Diseno](UI%20-%20Sistema%20de%20Diseno.md) · [API](API.md).

### Vista Resumen (`/`)
- **Sidebar:** identidad y navegación.
- **Cabecera:** título, subtítulo de estado (número real de servicios en línea) y botón «actualizar estado».
- **Sección de servicios:** tarjetas reales con estado en vivo; tarjeta vacía a ancho completo si no hay nada registrado.
- **Registro de actividad:** eventos reales de la API (acciones, errores, estado del listado).

### Vista Servicios (`/#/servicios`)
- **Selector bots / webs:** pestañas con icono (🤖/🌐) y contador real por tipo («N bots · X en línea»).
- **Tarjetas por tipo:** nombre, unidad systemd/ruta, tipo, auto-inicio y botones iniciar/detener/reiniciar/logs (llaman a la API).
- **Estados vacíos por tipo:** ninguna bot/web registrada (si la API falla, se mantienen y se avisa en el registro).

- ✅ Estados vacíos sin datos falsos (si la API no responde, no se inventan datos).
- ✅ Micro-animaciones y respeto de `prefers-reduced-motion`.

> Cuando llegue el registro manual de servicios (v0.1), el botón «añadir servicio» dejará de avisar y abrirá un formulario.

---

## Organización principal

```text
ProjectLumina

├── 🤖 BOTS
├── 🌐 WEBS
└── 🖥️ SERVIDOR
```

Cada bot y cada web tendrá su propio apartado con controles para iniciar, detener, reiniciar y desplegar logs.

---

## Sección de BOTS

→ Ver [Bots](Bots.md)

```text
🤖 TelegramBot

Estado: 🟢 Online
PID: 2841
CPU: 1.8%
RAM: 72 MB

[ Iniciar ] [ Detener ] [ Reiniciar ] [ Logs ]
```

---

## Sección de WEBS

→ Ver [Webs](Webs.md)

```text
🌐 NetSent

Estado: 🟢 Online

[ Iniciar ] [ Detener ] [ Reiniciar ] [ Logs ]
```

---

## Sección de SERVIDOR

→ Ver [Servidor](Servidor.md)

```text
🖥️ SERVER

CPU       23%
RAM       41%
DISCO     52%
RED       ↓ 2.4 MB/s ↑ 800 KB/s
UPTIME    4 días
```

### Información del servidor

Aunque bots y webs son la prioridad, el dashboard también podrá mostrar:

- CPU.
- RAM.
- Disco.
- Temperatura.
- Uso de red.
- Uptime.
- Procesos.
- Servicios activos.

---

## Logs

Los logs de bots y webs se mostrarán en el dashboard mediante un botón específico.

- Formato **desplegable** para no saturar el dashboard.

```text
+--------------------------------+
| Logs - TelegramBot          X |
+--------------------------------+
| 15:01 Bot iniciado             |
| 15:02 Conectado                |
| 15:14 Error de conexión        |
| 15:14 Reiniciando...           |
| 15:15 Bot iniciado             |
+--------------------------------+
```

→ Observabilidad según [Principios Tecnicos](../01%20-%20Planificacion/Principios%20Tecnicos.md).

---

## Relacionado

- [Frontend](Frontend.md) · Implementa el dashboard.
- [Bots](Bots.md) · Gestión de bots.
- [Webs](Webs.md) · Gestión de webs.
- [Servidor](Servidor.md) · Métricas del servidor.
- [API](API.md) · Datos que consume.
- [Backend](Backend.md) · Lógica detrás del dashboard.
- [Inicio](../00%20-%20Inicio/Inicio.md)
