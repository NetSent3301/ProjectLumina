# ⚙️ Configuracion de Bots — ProjectLumina

> Cómo se define y almacena la configuración de cada bot.

---

## Concepto

Cada bot tendrá una **configuración almacenada** en la base de datos → [[Base de Datos]].

Esto permite que Lumina sepa **cómo administrar cada bot** sin que el usuario tenga que ir manualmente al servidor.

---

## Ejemplo de configuración

```text
Nombre: TelegramBot
Tipo: Python
Ruta: /home/bots/telegram
Comando: python bot.py
Auto-inicio: Sí
Auto-reinicio: Sí
```

---

## Campos (MVP)

En el MVP la configuración es explícita → [[Sistema Adaptable#MVP: configuración explícita]]:

- **Nombre** — Identificador.
- **Ruta** — Ubicación en el servidor.
- **Comando** — Cómo se inicia.
- **Tipo** — Tipo de proyecto (Python, Node, etc.).
- **Servicio** — Servicio systemd asociado (si aplica) → [[systemd]].

---

## Campos futuros

- Auto-inicio.
- Auto-reinicio → [[Auto Restart]].
- Variables de entorno.
- Configuración avanzada.
- Automatización adicional.

---

## Relacionado

- [[Bots]] · Gestión de bots.
- [[Base de Datos]] · Dónde se guarda.
- [[Sistema Adaptable]] · Hacia la detección automática.
- [[Backend]] · Lógica de configuración.
- [Ver planificación completa](ProjectLumina_Planificacion)
