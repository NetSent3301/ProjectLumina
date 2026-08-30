# 🌍 Redes — Investigación

> Investigación sobre redes, clave para el acceso remoto.

---

## Rol en el proyecto

Necesario para exponer [[Acceso Remoto|ProjectLumina a Internet]] de forma segura.

---

## Temas a investigar

- [ ] **NAT** y port forwarding → exponer el servidor.
- [ ] **Firewall** (ufw, iptables/nftables) → protegen el acceso.
- [ ] DNS.
- [ ] VPN y túneles → alternativa segura al acceso directo.
- [ ] HTTPS y certificados → [[Acceso Remoto#Medidas de seguridad]].
- [ ] Direccionamiento IP y puertos.

---

## Aplicación al proyecto

```text
Internet → NAT/Firewall → Servidor Debian → ProjectLumina
```

- Ligado a [[Acceso Remoto]] y [[API]].
- Protección según [[Principios Tecnicos#Seguridad]].

---

## Relacionado

- [[Acceso Remoto]] · Objetivo de red.
- [[API]] · Servicio expuesto.
- [[SSH]] · Acceso administrativo por red.
- [[Debian]] · Configuración de red.
- [Ver planificación completa](ProjectLumina_Planificacion)
