# 📊 Dashboard — ProjectLumina

> El centro de control de ProjectLumina.

---

## Base actual (maqueta)

El dashboard web implementado es una **maqueta con estados vacíos** (sin datos falsos) y **una sola página**: la navegación cambia de vista sin recargar (hash `#/resumen`, `#/servicios`) → [[Frontend#Estado actual]] · [[UI - Sistema de Diseno]].

### Vista Resumen (`/`)
- **Sidebar:** identidad y navegación.
- **Cabecera:** título, subtítulo de estado («sin servicios registrados») y botón «actualizar estado».
- **Sección de servicios:** tarjeta vacía a ancho completo («conectar un servicio», disponible en v0.1).
- **Registro de actividad:** lista de eventos con tiempo y nivel (ok/warn), con estado vacío «sin actividad todavía».

### Vista Servicios (`/#/servicios`)
- **Selector bots / webs:** pestañas con icono (🤖/🌐) y contador por tipo.
- **Estados vacíos por tipo:** ninguna bot/web registrada, con chip «disponible en v0.1».
- Botón «añadir servicio» en la cabecera (aviso de que llega en v0.1).

- ✅ Estados vacíos (sin datos falsos).
- ✅ Micro-animaciones y respeto de `prefers-reduced-motion`.

> Cuando haya datos reales, cada bot y web tendrá su apartado con controles para iniciar, detener, reiniciar y desplegar logs (más abajo).

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

→ Ver [[Bots]]

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

→ Ver [[Webs]]

```text
🌐 NetSent

Estado: 🟢 Online

[ Iniciar ] [ Detener ] [ Reiniciar ] [ Logs ]
```

---

## Sección de SERVIDOR

→ Ver [[Servidor]]

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

→ Observabilidad según [[Principios Tecnicos#Observabilidad]].

---

## Relacionado

- [[Frontend]] · Implementa el dashboard.
- [[Bots]] · Gestión de bots.
- [[Webs]] · Gestión de webs.
- [[Servidor]] · Métricas del servidor.
- [[API]] · Datos que consume.
- [[Backend]] · Lógica detrás del dashboard.
- [Ver planificación completa](ProjectLumina_Planificacion)
