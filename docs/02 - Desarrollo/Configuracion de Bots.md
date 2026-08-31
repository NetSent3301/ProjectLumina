# ⚙️ Configuracion de Bots — ProjectLumina

> Cómo se define y almacena la configuración de cada bot.

---

## Concepto

Cada bot tendrá una **configuración almacenada** en la base de datos → [Base de Datos](Base%20de%20Datos.md).

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

En el MVP la configuración es explícita → [Sistema Adaptable](Sistema%20Adaptable.md):

- **Nombre** — Identificador.
- **Ruta** — Ubicación en el servidor.
- **Comando** — Cómo se inicia.
- **Tipo** — Tipo de proyecto (Python, Node, etc.).
- **Servicio** — Servicio systemd asociado (si aplica) → [systemd](../04%20-%20Investigacion/systemd.md).

---

## Campos futuros

- Auto-inicio.
- Auto-reinicio → [Auto Restart](Auto%20Restart.md).
- Variables de entorno.
- Configuración avanzada.
- Automatización adicional.

---

## Relacionado

- [Bots](Bots.md) · Gestión de bots.
- [Base de Datos](Base%20de%20Datos.md) · Dónde se guarda.
- [Sistema Adaptable](Sistema%20Adaptable.md) · Hacia la detección automática.
- [Backend](Backend.md) · Lógica de configuración.
- [Inicio](../00%20-%20Inicio/Inicio.md)
