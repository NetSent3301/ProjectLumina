# 🏗️ Arquitectura — ProjectLumina

> Arquitectura del MVP y evolución hacia etapas futuras.

---

## Arquitectura del MVP

La arquitectura preferida para el MVP es **simple**: sin agente.

```mermaid
flowchart TD
    A[💻 Web / iPhone] --> B[⚙️ Backend de ProjectLumina]
    B --> C[🐧 Debian 13]
    C --> D[Ejecuta acciones]
    D --> E1[🤖 Bot]
    D --> E2[🌐 Web]
    D --> E3[🛠️ Servicio]
    D --> E4[🖥️ Sistema]
```

### Forma simplificada

```
Web → Backend Lumina → Debian
```

---

## Ejemplo de flujo

```mermaid
sequenceDiagram
    participant U as Usuario
    participant B as Backend Lumina
    participant D as Debian
    participant Bot as Bot

    U->>B: Pulsa [ Reiniciar Bot ]
    B->>D: Ejecuta la operación
    D->>Bot: Reinicia
    Bot-->>D: Bot reiniciado
    D-->>B: Comprueba estado
    B-->>U: Dashboard: 🟢 ONLINE
```

---

## Agente Lumina

Se consideró utilizar un agente independiente:

```text
Web → Backend → Agente Lumina → Servidor
```

- **Para el MVP NO se utilizará agente.** Se mantiene arquitectura sencilla.
- El agente queda para una **etapa posterior**, especialmente cuando se administren **múltiples servidores**.

→ Ver etapas futuras abajo.

---

## Comunicación

- **Frontend ↔ Backend:** API REST → [[API]].
- WebSockets podrán incorporarse posteriormente para datos en tiempo real.

---

## Arquitectura futura

### Etapa intermedia
```mermaid
flowchart LR
    A[Web] --> B[Backend Lumina]
    B --> C[Administrador del sistema]
    C --> E[Bots / Webs / Servicios]
```

### Etapa avanzada (multi-servidor con agentes)
```mermaid
flowchart TD
    A[Web / iOS / Android] --> B[Backend Lumina]
    B --> A1[Agent 1]
    B --> A2[Agent 2]
    A1 --> S1[Server 1]
    A2 --> S2[Server 2]
```

### Etapa de plataforma (control plane)
```mermaid
flowchart TD
    P[ProjectLumina] --> CP[Backend / Control Plane]
    CP --> SA[Server A]
    CP --> SB[Server B]
    CP --> SC[Server C]
    SA --> GA[Agent]
    SB --> GB[Agent]
    SC --> GC[Agent]
    GA --> BA[Bots/Webs]
    GB --> BB[Bots/Webs]
    GC --> BC[Bots/Webs]
```

---

## Estructura del código (propuesta)

```text
ProjectLumina/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── app/
│   ├── main.py
│   ├── api/          → [[API]]
│   ├── services/     → [[Bots]] · [[Webs]]
│   ├── models/       → [[Base de Datos]]
│   ├── system/       → [[Servidor]] · [[Control Remoto]]
│   └── config/       → [[Configuracion de Bots]]
│
├── web/
│   ├── templates/    → [[Frontend]]
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── components/
│
├── data/
│   └── lumina.db     → [[Base de Datos]]
│
├── logs/             → [[Dashboard#Logs]]
│
├── tests/            → Ver [[Tareas#Testing]]
│
└── docs/             → Este mapa
```

> ⚠️ La estructura exacta podrá cambiar al implementar el proyecto.

---

## Relacionado

- [[Requisitos]] · Qué debe cumplir.
- [[Backend]] · Lógica del lado servidor.
- [[Frontend]] · Interfaz de usuario.
- [[API]] · Comunicación.
- [[Base de Datos]] · Almacenamiento.
- [[Servidor]] · Donde se ejecuta.
- [[Control Remoto]] · Ejecución de acciones.
- [Ver planificación completa](ProjectLumina_Planificacion)
