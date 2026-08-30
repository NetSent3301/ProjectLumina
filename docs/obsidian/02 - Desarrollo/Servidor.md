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

- **Servidor:** Debian 13 → [[Debian]].
- **Gestión de servicios:** systemd → [[systemd]].

ProjectLumina deberá poder **interactuar con servicios del sistema** de forma controlada y estable → [[Control Remoto]].

---

## Información mostrada

El dashboard podrá mostrar (→ [[Dashboard#Sección de SERVIDOR]]):

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
- Puntos de observabilidad → [[Principios Tecnicos#Observabilidad]].

---

## Relacionado

- [[Debian]] · Sistema operativo.
- [[systemd]] · Servicios.
- [[Dashboard]] · Muestra las métricas.
- [[Acceso Remoto]] · Acceso desde fuera.
- [[Control Remoto]] · Administración.
- [Ver planificación completa](ProjectLumina_Planificacion)
