# 🚀 Gestion Avanzada de Webs — ProjectLumina

> Despliegue y gestión avanzada de webs (futuro, no exigido en el MVP).

---

## Estado

**No será obligatorio para el MVP** → fuera del alcance en [[Requisitos#Fuera del MVP]].

Planificado para versiones posteriores → [[Roadmap]].

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

- **`git pull`** → actualizar código → [[Git y GitHub]].
- **Instalar dependencias** → gestión de paquetes → [[Debian]].
- **Reiniciar servicio** → systemd → [[systemd]].
- **Comprobar HTTP** → verificación de disponibilidad → [[Webs#Comprobación de disponibilidad]].

---

## Relacionado

- [[Webs]] · Gestión básica.
- [[systemd]] · Reinicio de servicios.
- [[Git y GitHub]] · Actualización de código.
- [[Servidor]] · Entorno de despliegue.
- [Ver planificación completa](ProjectLumina_Planificacion)
