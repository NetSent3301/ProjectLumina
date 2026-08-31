# Dashboard — ProjectLumina

El **dashboard** será el centro de control de ProjectLumina.

## Base actual (maqueta)

El dashboard web implementado es una **maqueta con estados vacíos** (sin datos falsos) y **una sola página**: la navegación cambia de vista sin recargar (hash `#/resumen`, `#/servicios`). Estructura:

### Vista Resumen (`/`)
- **Sidebar**: identidad y navegación.
- **Cabecera**: título, subtítulo de estado ("sin servicios registrados") y botón "actualizar estado".
- **Sección de servicios**: tarjeta vacía a ancho completo ("conectar un servicio", disponible en v0.1).
- **Registro de actividad**: lista de eventos con tiempo y nivel (ok/warn), con estado vacío "sin actividad todavía".

### Vista Servicios (`/#/servicios`)
- **Selector bots / webs**: pestañas con icono y contador por tipo ("0 bots").
- **Estados vacíos por tipo**: ninguna bot/web registrada, con chip "disponible en v0.1".
- Botón "añadir servicio" en la cabecera (aviso de que llega en v0.1).

Micro-animaciones: entrada escalonada al cargar, elevaciones al hover, flotación del estado vacío y animación de entradas del registro; todo respeta `prefers-reduced-motion` → [frontend.md](frontend.md).

> Cuando haya datos reales, cada bot y web tendrá su apartado con controles para iniciar, detener, reiniciar y desplegar logs.

## Organización principal

```
ProjectLumina

├── 🤖 BOTS
├── 🌐 WEBS
└── 🖥️ SERVIDOR
```

Cada bot y cada web tendrá su propio apartado con controles para iniciar, detener, reiniciar y desplegar logs.

## Sección BOTS

```
🤖 TelegramBot

Estado: 🟢 Online
PID: 2841
CPU: 1.8%
RAM: 72 MB

[ Iniciar ] [ Detener ] [ Reiniciar ] [ Logs ]
```

→ Detalle en [bots.md](bots.md).

## Sección WEBS

```
🌐 NetSent

Estado: 🟢 Online

[ Iniciar ] [ Detener ] [ Reiniciar ] [ Logs ]
```

→ Detalle en [webs.md](webs.md).

## Sección SERVIDOR

```
🖥️ SERVER

CPU       23%
RAM       41%
DISCO     52%
RED       ↓ 2.4 MB/s ↑ 800 KB/s
UPTIME    4 días
```

### Información del servidor

Aunque bots y webs son la prioridad, el dashboard también puede mostrar:

- CPU.
- RAM.
- Disco.
- Temperatura.
- Uso de red.
- Uptime.
- Procesos.
- Servicios activos.

## Logs

Los logs de bots y webs se mostrarán en el dashboard mediante un botón específico, en formato **desplegable** para no saturar la vista.

```
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

---

Volver a [desarrollo](README.md).
