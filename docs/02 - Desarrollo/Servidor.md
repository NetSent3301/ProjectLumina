# 🖥️ Servidor — ProjectLumina

> Laptop servidor donde se ejecuta ProjectLumina, bots, webs y servicios.

---

## Servidor inicial

| Aspecto | Valor |
|---------|-------|
| **Hardware** | Laptop vieja destinada a servidor |
| **Sistema operativo** | Debian 13 |
| **Función** | Ejecutar ProjectLumina, bots, webs y otros servicios |

La laptop debe poder **permanecer encendida y disponible** para administración remota.

---

## Sistema y procesos

- **Servidor:** Debian 13 → [Debian](../04%20-%20Investigacion/Debian.md).
- **Gestión de servicios:** systemd → [systemd](../04%20-%20Investigacion/systemd.md).

ProjectLumina deberá poder **interactuar con servicios del sistema** de forma controlada y estable → [Control Remoto](Control%20Remoto.md).

---

## Información mostrada

El dashboard podrá mostrar (→ [Dashboard](Dashboard.md)):

- ✅ CPU.
- ✅ RAM.
- ✅ Disco.
- ✅ Temperatura.
- ✅ Uso de red.
- ✅ Uptime.
- ✅ Procesos.
- ✅ Servicios activos.

```text
🖥️ SERVER

CPU       23%
RAM       41%
DISCO     52%
RED       ↓ 2.4 MB/s ↑ 800 KB/s
UPTIME    4 días
```

---

## Monitorización

- Sirve como **soporte para la administración**.
- Puntos de observabilidad → [Principios Tecnicos](../01%20-%20Planificacion/Principios%20Tecnicos.md).

---

## Relacionado

- [Debian](../04%20-%20Investigacion/Debian.md) · Sistema operativo.
- [systemd](../04%20-%20Investigacion/systemd.md) · Servicios.
- [Dashboard](Dashboard.md) · Muestra las métricas.
- [Acceso Remoto](../03%20-%20Seguridad/Acceso%20Remoto.md) · Acceso desde fuera.
- [Control Remoto](Control%20Remoto.md) · Administración.
- [Inicio](../00%20-%20Inicio/Inicio.md)
