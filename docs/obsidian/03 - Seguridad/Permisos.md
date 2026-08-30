# 🛡️ Permisos — ProjectLumina

> Control de qué puede hacer cada usuario, servidor o dispositivo.

---

## Contexto

Aunque no haya multiusuario inicialmente, las **operaciones remotas son sensibles** → [[Acceso Remoto]] · [[Control Remoto]].

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

> Toda capacidad de **ejecución remota** debe tratarse como una **operación privilegiada** → [[Principios Tecnicos#Seguridad]].

---

## Relacionado

- [[Autenticacion]] · Identidad del usuario.
- [[Usuarios]] · Modelo de usuarios.
- [[Acceso Remoto]] · Exposición.
- [[Control Remoto]] · Capacidad a proteger.
- [Ver planificación completa](ProjectLumina_Planificacion)
