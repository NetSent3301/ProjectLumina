# 🌍 Redes — Investigación

> Investigación sobre redes, clave para el acceso remoto.

---

## Rol en el proyecto

Necesario para exponer [ProjectLumina a Internet](../03%20-%20Seguridad/Acceso%20Remoto.md) de forma segura.

---

## Temas a investigar

- [ ] **NAT** y port forwarding → exponer el servidor.
- [ ] **Firewall** (ufw, iptables/nftables) → protegen el acceso.
- [ ] DNS.
- [ ] VPN y túneles → alternativa segura al acceso directo.
- [ ] HTTPS y certificados → [Acceso Remoto](../03%20-%20Seguridad/Acceso%20Remoto.md).
- [ ] Direccionamiento IP y puertos.

---

## Aplicación al proyecto

```text
                INTERNET
                   |
                   |  HTTPS / API
           +-------+------+
           |  Router     |
           |  NAT/forward|
           +-------+------+
                   |
              Firewall
              (ufw/nft)
                   |
            Debian 13 Server
                   |
              ProjectLumina
            (backend + API)
                   |
       +-----------+-----------+
       |           |           |
    Bots       Webs       SSH remoto
```

- Ligado a [Acceso Remoto](../03%20-%20Seguridad/Acceso%20Remoto.md) y [API](../02%20-%20Desarrollo/API.md).
- Protección según [Principios Tecnicos](../01%20-%20Planificacion/Principios%20Tecnicos.md).

---

## Relacionado

- [Acceso Remoto](../03%20-%20Seguridad/Acceso%20Remoto.md) · Objetivo de red.
- [API](../02%20-%20Desarrollo/API.md) · Servicio expuesto.
- [SSH](SSH.md) · Acceso administrativo por red.
- [Debian](Debian.md) · Configuración de red.
- [Inicio](../00%20-%20Inicio/Inicio.md)
