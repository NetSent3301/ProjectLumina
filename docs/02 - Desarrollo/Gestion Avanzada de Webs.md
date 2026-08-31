# 🚀 Gestion Avanzada de Webs — ProjectLumina

> Despliegue y gestión avanzada de webs (futuro, no exigido en el MVP).

---

## Estado

**No será obligatorio para el MVP** → fuera del alcance en [Requisitos](../01%20-%20Planificacion/Requisitos.md).

Planificado para versiones posteriores → [Roadmap](../01%20-%20Planificacion/Roadmap.md).

---

## Flujo de despliegue propuesto

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

---

## Componentes del flujo

- **`git pull`** → actualizar código → [Git y GitHub](Git%20y%20GitHub.md).
- **Instalar dependencias** → gestión de paquetes → [Debian](../04%20-%20Investigacion/Debian.md).
- **Reiniciar servicio** → systemd → [systemd](../04%20-%20Investigacion/systemd.md).
- **Comprobar HTTP** → verificación de disponibilidad → [Webs](Webs.md).

---

## Relacionado

- [Webs](Webs.md) · Gestión básica.
- [systemd](../04%20-%20Investigacion/systemd.md) · Reinicio de servicios.
- [Git y GitHub](Git%20y%20GitHub.md) · Actualización de código.
- [Servidor](Servidor.md) · Entorno de despliegue.
- [Inicio](../00%20-%20Inicio/Inicio.md)
