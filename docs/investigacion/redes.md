# Redes — Investigación

> Notas sobre redes, clave para exponer el acceso remoto a ProjectLumina por Internet.

## Rol en el proyecto

Las redes son la base para **exponer el acceso remoto a Internet** de forma segura: conexión al servidor, publicación de la API, acceso desde cualquier lugar y protección del tráfico.

Ver también [seguridad](../seguridad.md) y [API](../desarrollo/api.md).

## Temas a investigar

- [ ] NAT y port forwarding.
- [ ] Firewall: ufw / iptables / nftables.
- [ ] DNS.
- [ ] VPN y túneles.
- [ ] HTTPS y certificados.
- [ ] IP y puertos.

## Aplicación al proyecto

```
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

## Relación con el proyecto

- Exposición segura a Internet → [seguridad](../seguridad.md).
- Publicación de la API → [API](../desarrollo/api.md).
- Servidor y servicios detrás de la red → [servidor](../desarrollo/servidor.md).
- Túneles y administración remota → [SSH](ssh.md).

---

Volver a [investigación](README.md).