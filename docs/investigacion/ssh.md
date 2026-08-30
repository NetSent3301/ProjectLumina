# SSH — Investigación

> Notas sobre SSH, base de la administración remota del servidor.

## Rol en el proyecto

La **gestión de SSH** forma parte de la visión de ProjectLumina: permitir **control remoto** seguro del servidor. SSH es el canal clásico y confiable para administrar el sistema sin acceso físico.

Ver también [control remoto](../desarrollo/control-remoto.md).

## Funciones contempladas

- [ ] Crear conexiones SSH.
- [ ] Cerrar conexiones.
- [ ] Gestionar conexiones activas.
- [ ] Ver estado de la conexión.
- [ ] Capacidades por definir durante la implementación.

## Temas a investigar

- [ ] Configuración de `sshd`.
- [ ] Autenticación por claves.
- [ ] Seguridad de SSH.
- [ ] Túneles SSH.
- [ ] Uso de SSH desde el backend.

## Nota de seguridad

> SSH otorga **acceso privilegiado** al servidor. Es una de las capacidades más sensibles del proyecto y debe protegerse con especial atención.

- Protección general → [seguridad](../seguridad.md).
- Ejecución remota → [control remoto](../desarrollo/control-remoto.md).
- Integración con el sistema → [backend](../desarrollo/backend.md).

---

Volver a [investigación](README.md).