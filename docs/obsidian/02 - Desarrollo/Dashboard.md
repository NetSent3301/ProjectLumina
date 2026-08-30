# 📊 Dashboard — ProjectLumina

> El centro de control de ProjectLumina.

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
