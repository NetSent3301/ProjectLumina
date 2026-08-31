# ProjectLumina

> 🗄️ **Histórico** — Monolito original de planificación, conservado como referencia.

> Su contenido está dividido y mantenido en las notas del mapa actual → [Inicio](../00%20-%20Inicio/Inicio.md).

> Planificación general, visión y roadmap del proyecto.

## 1. Identidad

- **Nombre:** ProjectLumina
- **Estado:** Planificación
- **Versión inicial:** v0.1.0
- **Tipo:** Proyecto personal de programación, administración de servidores y redes.
- **Objetivo general:** crear un centro de control remoto para administrar servidores, bots, webs y servicios.

---

## 2. Idea general

ProjectLumina será un sistema de administración remota para una laptop vieja utilizada como servidor.

La primera versión será una aplicación web accesible desde la laptop principal y desde un iPhone. Desde ella se podrá consultar el estado del servidor y, principalmente, administrar bots y webs sin tener que ir físicamente al servidor.

La laptop servidor utilizará **Debian 13**.

La idea de "Lumina como el OS" significa que Lumina será la capa permanente de administración sobre Debian. Debian seguirá siendo el sistema operativo real.

---

## 3. Objetivos

### Objetivo principal

Poder administrar y controlar mi servidor remotamente desde diferentes dispositivos mediante una interfaz centralizada.

Especialmente:

- Administrar bots.
- Administrar webs.
- Iniciar, detener y reiniciar servicios.
- Consultar estados.
- Ejecutar acciones remotamente.
- Evitar tener que ir físicamente al servidor para iniciar o solucionar cosas.

### Objetivo secundario

Aprender programación, administración de servidores, redes y tecnologías relacionadas mientras construyo ProjectLumina y lo utilizo como parte de mi formación y futuro profesional.

---

## 4. Visión a largo plazo

ProjectLumina podría evolucionar hasta administrar múltiples servidores.

Primero estará destinado a mis propios servidores. En un futuro lejano, después de perfeccionar el sistema, podría llegar a administrar servidores de otras personas o clientes.

```text
                    PROJECTLUMINA
                         |
          +--------------+--------------+
          |              |              |
       Server 1       Server 2       Server 3
        Debian         Linux          Otros
          |
       Bots/Webs
```

La escalabilidad futura es importante, pero no debe complicar innecesariamente el MVP.

---

## 5. Filosofía del proyecto

ProjectLumina debe crecer junto con mis capacidades.

No se intentará construir todo desde el principio.

```text
Idea
  ↓
MVP sencillo
  ↓
Funcionamiento estable
  ↓
Mejoras
  ↓
Automatización
  ↓
Mayor seguridad
  ↓
Mayor compatibilidad
  ↓
Múltiples servidores
  ↓
Aplicaciones móviles
  ↓
Plataforma completa
```

Las funcionalidades podrán agregarse, modificarse o eliminarse según las necesidades y capacidades futuras.

---

## 6. Plataformas

### Primera etapa

ProjectLumina será una aplicación web accesible desde:

- Laptop principal.
- iPhone.

### Futuro

- Aplicación nativa para iPhone.
- Aplicación universal para Android y otros dispositivos.

La intención es que las interfaces futuras utilicen el mismo backend.

```text
                  Backend Lumina
                       |
             +---------+---------+
             |         |         |
            Web       iOS     Android
```

---

## 7. Servidor inicial

- **Hardware:** laptop vieja destinada a servidor.
- **Sistema operativo:** Debian 13.
- **Función:** ejecutar ProjectLumina, bots, webs y otros servicios.

La laptop debe poder permanecer encendida y disponible para administración remota.

---

## 8. Acceso remoto

Uno de los objetivos es poder acceder a ProjectLumina desde cualquier lugar del mundo mediante Internet, no solamente desde la misma red local.

```text
             INTERNET
                 |
       +---------+---------+
       |                   |
    Laptop              iPhone
       |                   |
       +---------+---------+
                 |
          ProjectLumina
                 |
                 v
          Debian 13 Server
```

Cuando se exponga a Internet deberán estudiarse y aplicarse correctamente:

- HTTPS.
- Autenticación.
- Autorización.
- Gestión de credenciales.
- Seguridad de APIs.
- Firewall.
- NAT y redes.
- Control de acceso.
- Protección contra accesos no autorizados.

La ejecución remota de comandos será una capacidad sensible y deberá protegerse correctamente.

---

## 9. Arquitectura inicial

La arquitectura preferida para el MVP es:

```text
Web / iPhone
      |
      v
Backend de ProjectLumina
      |
      v
Debian 13
      |
      v
Ejecuta acciones
      |
      +---- Bot
      |
      +---- Web
      |
      +---- Servicio
      |
      +---- Sistema
```

Ejemplo:

```text
Usuario pulsa:
[ Reiniciar Bot ]

       ↓

Backend Lumina

       ↓

Debian ejecuta la operación

       ↓

Bot reiniciado

       ↓

Lumina comprueba el estado

       ↓

Dashboard: 🟢 ONLINE
```

---

## 10. Agente Lumina

Se consideró utilizar un agente independiente:

```text
Web
 ↓
Backend
 ↓
Agente Lumina
 ↓
Servidor
```

Para el MVP **no se utilizará agente**. Se mantendrá una arquitectura sencilla:

```text
Web
 ↓
Backend Lumina
 ↓
Debian
```

El agente queda para una etapa posterior, especialmente cuando se administren múltiples servidores.

---

## 11. Backend

Tecnologías propuestas:

- Python.
- Flask o FastAPI.

El backend será responsable de:

- Recibir solicitudes del frontend.
- Consultar el estado del servidor.
- Gestionar bots.
- Gestionar webs.
- Gestionar servicios.
- Ejecutar acciones administrativas.
- Devolver resultados al frontend.
- Gestionar configuraciones.
- Mantener separada la lógica de administración de la interfaz.

La elección final entre Flask y FastAPI se hará al comenzar la implementación.

---

## 12. Frontend

Tecnologías propuestas:

- HTML.
- CSS.
- JavaScript.

La primera interfaz será web y debe ser usable desde laptop y iPhone.

---

## 13. API

La comunicación inicial utilizará una API REST.

```text
Frontend
   |
   | HTTP
   v
REST API
   |
   v
Backend
   |
   v
Servidor
```

WebSockets podrán incorporarse posteriormente cuando se necesite información en tiempo real.

---

## 14. Base de datos

Inicialmente se utilizará **SQLite**.

Podrá almacenar configuraciones como:

- Bots.
- Webs.
- Rutas.
- Comandos.
- Opciones de automatización.
- Estados.
- Configuración de servicios.

Si el proyecto crece considerablemente se podrá migrar a PostgreSQL.

---

## 15. Sistema y procesos

Servidor:

- Debian 13.

Gestión de servicios:

- systemd.

ProjectLumina deberá poder interactuar con servicios del sistema de forma controlada y estable.

---

## 16. Git y GitHub

El proyecto utilizará:

- Git.
- GitHub.

Se recomienda mantener versiones como:

```text
v0.1.0
v0.2.0
v0.3.0
```

También habrá un `CHANGELOG.md`.

---

# 17. Bot Manager

Una de las funciones centrales de ProjectLumina será administrar bots remotamente.

El objetivo es no tener que entrar físicamente al servidor para iniciar, detener o solucionar un bot.

Ejemplo:

```text
🤖 TelegramBot

Estado: 🟢 Online
PID: 2841
CPU: 1.8%
RAM: 72 MB

[ Iniciar ]
[ Detener ]
[ Reiniciar ]
[ Logs ]
```

---

## 18. Configuración de bots

Cada bot tendrá una configuración almacenada.

Ejemplo:

```text
Nombre: TelegramBot
Tipo: Python
Ruta: /home/bots/telegram
Comando: python bot.py
Auto-inicio: Sí
Auto-reinicio: Sí
```

Esto permitirá que Lumina sepa cómo administrar cada bot sin que el usuario tenga que ir manualmente al servidor.

---

## 19. Acciones de bots

Se contemplan:

- Iniciar.
- Detener.
- Reiniciar.
- Consultar estado.
- Ver logs.
- Detectar si está activo.
- Detectar si se cayó.

Posteriormente:

- Auto-inicio.
- Auto-reinicio.
- Variables de entorno.
- Configuración avanzada.
- Automatización adicional.

---

## 20. Auto-restart

ProjectLumina deberá poder detectar cuando un bot se cae y tratar de reiniciarlo automáticamente.

```text
Bot 🟢
  ↓
Bot se cae ❌
  ↓
Lumina detecta el fallo
  ↓
Espera configurada
  ↓
Lumina intenta reiniciar
  ↓
Bot 🟢
```

Configuración futura posible:

```text
Auto-restart: Sí
Intentos máximos: 5
Espera entre intentos: 10 segundos
```

---

# 21. Logs

Los bots y webs tendrán logs accesibles desde el dashboard mediante un botón específico.

Ejemplo:

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

Los logs se mostrarán de forma desplegable para no saturar el dashboard.

---

# 22. Web Manager

Las webs tendrán una gestión similar a los bots.

ProjectLumina podrá:

- Ver estado.
- Iniciar.
- Detener.
- Reiniciar.
- Consultar logs.
- Comprobar disponibilidad.
- Administrar el servicio asociado.
- Eventualmente desplegar actualizaciones.

Ejemplo:

```text
🌐 NetSent

Estado: 🟢 Online

[ Iniciar ]
[ Detener ]
[ Reiniciar ]
[ Logs ]
```

---

## 23. Gestión avanzada de webs

En versiones posteriores se podrá implementar un flujo de despliegue:

```text
Actualizar web
      ↓
git pull
      ↓
Instalar dependencias
      ↓
Ejecutar procesos necesarios
      ↓
Reiniciar servicio
      ↓
Comprobar HTTP
      ↓
🟢 Online
```

Esto no será obligatorio para el MVP.

---

# 24. Sistema adaptable

Una idea importante es que Lumina no dependa de una plantilla específica para cada bot o web.

La visión futura es que pueda determinar cómo gestionar diferentes tipos de proyectos sin requerir una configuración manual completamente diferente para cada uno.

### MVP

Configuración explícita:

```text
Nombre
Ruta
Comando
Tipo
Servicio
```

### Versión posterior

```text
Bot/Web
   ↓
Lumina detecta o interpreta
cómo gestionarlo
   ↓
Gestión automática
```

Esta funcionalidad es avanzada, pero se considera importante y deberá llegar relativamente pronto después del MVP.

---

# 25. Dashboard

El dashboard será el centro de control de ProjectLumina.

Organización principal:

```text
ProjectLumina

├── 🤖 BOTS
├── 🌐 WEBS
└── 🖥️ SERVIDOR
```

Cada bot y cada web tendrá su propio apartado con controles para iniciar, detener, reiniciar y desplegar logs.

---

## 26. Información del servidor

Aunque bots y webs son la prioridad, el dashboard también podrá mostrar:

- CPU.
- RAM.
- Disco.
- Temperatura.
- Uso de red.
- Uptime.
- Procesos.
- Servicios activos.

Ejemplo:

```text
🖥️ SERVER

CPU       23%
RAM       41%
DISCO     52%
RED       ↓ 2.4 MB/s ↑ 800 KB/s
UPTIME    4 días
```

Esta información sirve como soporte para la administración.

---

# 27. Control remoto general

La visión de ProjectLumina incluye acceso remoto amplio al servidor.

Se contempla poder ejecutar comandos y acciones administrativas.

Ejemplos conceptuales:

```text
systemctl restart nginx
systemctl stop bot
git pull
python bot.py
```

También se contempla administrar:

- Procesos.
- Servicios.
- Bots.
- Webs.
- SSH.
- Sistema.

Esta capacidad deberá implementarse con especial atención a la seguridad.

---

# 28. SSH

La gestión de SSH forma parte de la visión del proyecto.

Se contempla:

- Crear conexiones SSH.
- Cerrar conexiones.
- Gestionar conexiones existentes.

Las capacidades exactas se definirán durante la implementación.

---

# 29. Usuarios

## MVP

No habrá sistema de usuarios.

ProjectLumina será una herramienta personal destinada al propietario del servidor.

## Futuro

Podrán incorporarse:

- Login.
- Autenticación.
- Usuarios.
- Roles.
- Permisos.
- Dispositivos autorizados.

Esto será especialmente importante cuando el proyecto llegue a administrar servidores de terceros.

---

# 30. Permisos y seguridad

Aunque no haya multiusuario inicialmente, las operaciones remotas son sensibles.

En versiones futuras el sistema podrá tener permisos configurables por servidor, dispositivo o usuario.

Ejemplo:

```text
Servidor: Debian-01

Permisos:
✓ Ver métricas
✓ Ver procesos
✓ Reiniciar servicios
✓ Administrar bots
✓ Ejecutar comandos
✗ Modificar usuarios
✗ Apagar servidor
```

---

# 31. Notificaciones

Las notificaciones serán una funcionalidad futura, no del MVP.

Ejemplo:

```text
🚨 ProjectLumina

TelegramBot se cayó.

Lumina intentó reiniciarlo.

Estado actual:
🟢 Online
```

Posibles canales futuros:

- Telegram.
- Discord.
- Email.
- Otros.

---

# 32. MVP: ProjectLumina v0.1

Objetivo:

> Crear una aplicación web funcional que permita conectarse al servidor Debian 13, consultar información básica y administrar bots y webs.

Debe incluir:

1. Backend.
2. Frontend web.
3. API.
4. Dashboard.
5. Configuración de bots.
6. Configuración de webs.
7. Iniciar/detener/reiniciar.
8. Estados.
9. Logs.
10. Información básica del servidor.
11. Manejo de errores.
12. Seguridad básica.

---

# 33. Prioridades del MVP

```text
1. Backend funcionando
2. Comunicación frontend ↔ backend
3. Identificación de bots/webs
4. Estado de bots/webs
5. Iniciar/detener/reiniciar
6. Logs
7. Información básica del servidor
8. Manejo de errores
9. Seguridad básica
10. Estabilización
```

---

# 34. Roadmap

## v0.1 - Base funcional

Objetivo: tener el primer centro de control funcionando.

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

## v0.2 - Automatización

Objetivo: hacer que Lumina empiece a administrar por sí sola.

Posibles características:

- Auto-start.
- Auto-restart.
- Detección de procesos caídos.
- Comprobación automática de webs.
- Reintentos.
- Configuración avanzada.
- Mejor manejo de servicios.

## v0.3 - Sistema adaptable

Objetivo: reducir la configuración manual.

Posibles características:

- Detección de tipos.
- Detección de comandos.
- Detección de estructuras comunes.
- Adaptación de configuraciones.
- Plantillas genéricas cuando sean necesarias.

## v0.4+ - Notificaciones

Objetivo: informar al usuario cuando ocurran eventos importantes.

Posibles características:

- Bot caído.
- Web caída.
- Reinicio automático.
- Error grave.
- Servidor fuera de línea.
- Alertas personalizadas.

## Futuro - Multi-servidor

Objetivo: administrar múltiples servidores desde una sola instancia de Lumina.

Aquí podría incorporarse el concepto de agente.

## Futuro lejano - Plataforma

Posibles características:

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

# 35. Arquitectura futura

## Etapa inicial

```text
Web
 ↓
Backend Lumina
 ↓
Debian
```

## Etapa intermedia

```text
Web
 ↓
Backend Lumina
 ↓
Administrador del sistema
 ↓
Bots / Webs / Servicios
```

## Etapa avanzada

```text
Web / iOS / Android
          |
          v
    Backend Lumina
          |
    +-----+-----+
    |           |
 Agent 1     Agent 2
    |           |
Server 1     Server 2
```

## Etapa de plataforma

```text
                         ProjectLumina
                              |
                    Backend / Control Plane
                              |
          +-------------------+-------------------+
          |                   |                   |
       Server A            Server B            Server C
          |                   |                   |
       Agent                 Agent               Agent
          |                   |                   |
       Bots/Webs           Bots/Webs           Bots/Webs
```

---

# 36. Posible estructura del código

```text
ProjectLumina/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── app/
│   ├── main.py
│   ├── api/
│   ├── services/
│   ├── models/
│   ├── system/
│   └── config/
│
├── web/
│   ├── templates/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── components/
│
├── data/
│   └── lumina.db
│
├── logs/
│
├── tests/
│
└── docs/
```

La estructura exacta podrá cambiar al implementar el proyecto.

---

# 37. Estructura recomendada para Obsidian

```text
ProjectLumina/
│
├── 00 - Inicio/
│   ├── Inicio.md
│   ├── Vision.md
│   └── Objetivos.md
│
├── 01 - Planificacion/
│   ├── Roadmap.md
│   ├── Requisitos.md
│   ├── Arquitectura.md
│   └── Tareas.md
│
├── 02 - Desarrollo/
│   ├── Backend.md
│   ├── Frontend.md
│   ├── API.md
│   ├── Bots.md
│   ├── Webs.md
│   └── Servidor.md
│
├── 03 - Seguridad/
│   ├── Autenticacion.md
│   ├── Permisos.md
│   └── Acceso_Remoto.md
│
├── 04 - Investigacion/
│   ├── Debian.md
│   ├── Linux.md
│   ├── Redes.md
│   ├── SSH.md
│   └── systemd.md
│
├── 05 - Versiones/
│   ├── v0.1.md
│   ├── v0.2.md
│   └── v0.3.md
│
└── 06 - Registro/
    ├── Changelog.md
    ├── Errores.md
    └── Decisiones.md
```

---

# 38. Principios técnicos

## Modularidad

Cada parte debería poder modificarse sin destruir todo el proyecto.

## Simplicidad inicial

No implementar sistemas complejos antes de necesitarlos.

## Seguridad

Toda capacidad de ejecución remota debe tratarse como una operación privilegiada.

## Automatización

Las tareas repetitivas deberían poder automatizarse.

## Observabilidad

Lumina debe poder informar qué está ocurriendo mediante estados y logs.

## Escalabilidad progresiva

El sistema debe poder crecer sin diseñar desde el principio una infraestructura gigantesca.

## Aprendizaje

ProjectLumina también es una herramienta de aprendizaje en:

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

---

# 39. Funcionalidades confirmadas

- [x] Administración remota.
- [x] Dashboard web.
- [x] Soporte inicial para laptop y iPhone mediante web.
- [x] Servidor inicial con Debian 13.
- [x] Gestión de bots.
- [x] Gestión de webs.
- [x] Iniciar bots/webs.
- [x] Detener bots/webs.
- [x] Reiniciar bots/webs.
- [x] Consulta de estados.
- [x] Logs desplegables.
- [x] Auto-restart como funcionalidad importante.
- [x] Información del servidor.
- [x] Ejecución remota de acciones.
- [x] Configuración por bot/web.
- [x] Acceso remoto por Internet como objetivo.
- [x] Evolución futura hacia múltiples servidores.
- [x] Posible administración futura de servidores de terceros.

---

# 40. Funcionalidades futuras

- [ ] Sistema adaptable para bots/webs.
- [ ] Detección automática de configuración.
- [ ] Notificaciones.
- [ ] Aplicación nativa para iPhone.
- [ ] Aplicación universal para Android/otros dispositivos.
- [ ] Agente Lumina.
- [ ] Múltiples servidores.
- [ ] Usuarios.
- [ ] Roles.
- [ ] Permisos avanzados.
- [ ] Backend alojado externamente.
- [ ] Deploy automático.
- [ ] Automatizaciones avanzadas.

---

# 41. Fuera del MVP

Inicialmente NO se priorizará:

- Aplicación nativa para iPhone.
- Aplicación Android.
- Multiusuario.
- Administración de servidores de terceros.
- Agente distribuido.
- Sistema inteligente completamente adaptable.
- Notificaciones avanzadas.
- Infraestructura externa compleja.
- Arquitectura para miles de servidores.

---

# 42. Definición final

> **ProjectLumina es una plataforma personal de administración remota de servidores, bots, webs y servicios.**
>
> Su primera versión estará instalada sobre una laptop con Debian 13 y será accesible mediante una interfaz web desde una laptop y un iPhone.
>
> El objetivo principal es permitir administrar bots y webs remotamente, incluyendo iniciar, detener, reiniciar, consultar estados y visualizar logs, además de monitorizar el servidor.
>
> Lumina evolucionará progresivamente hacia una plataforma automatizada capaz de detectar fallos, reiniciar servicios, gestionar diferentes tipos de proyectos y eventualmente administrar múltiples servidores.
>
> A largo plazo podrá incorporar agentes, aplicaciones móviles, usuarios, permisos y soporte para servidores de terceros.

---

# 43. Estado actual

**Fase actual:** planificación.

Siguiente camino:

```text
PLANIFICACIÓN
     ↓
REQUISITOS TÉCNICOS
     ↓
ARQUITECTURA DEFINITIVA DEL MVP
     ↓
ESTRUCTURA DEL REPOSITORIO
     ↓
DESARROLLO v0.1.0
     ↓
TESTING
     ↓
DEPLOY
```

## Objetivo inmediato

> **Conseguir que ProjectLumina pueda administrar correctamente un bot y una web desde un dashboard web.**

A partir de ahí se construirá el resto del sistema.
