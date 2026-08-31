# 🛡️ Permisos — ProjectLumina

> Control de qué puede hacer cada usuario, servidor o dispositivo.

---

## Contexto

Aunque no haya multiusuario inicialmente, las **operaciones remotas son sensibles** → [Acceso Remoto](Acceso%20Remoto.md) · [Control Remoto](../02%20-%20Desarrollo/Control%20Remoto.md).

En versiones futuras el sistema podrá tener **permisos configurables** por:

- Servidor.
- Dispositivo.
- Usuario.

---

## Ejemplo

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

## Principio de seguridad

> Toda capacidad de **ejecución remota** debe tratarse como una **operación privilegiada** → [Principios Tecnicos](../01%20-%20Planificacion/Principios%20Tecnicos.md).

---

## Relacionado

- [Autenticacion](Autenticacion.md) · Identidad del usuario.
- [Usuarios](Usuarios.md) · Modelo de usuarios.
- [Acceso Remoto](Acceso%20Remoto.md) · Exposición.
- [Control Remoto](../02%20-%20Desarrollo/Control%20Remoto.md) · Capacidad a proteger.
- [Inicio](../00%20-%20Inicio/Inicio.md)
