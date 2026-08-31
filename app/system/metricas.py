"""Métricas del sistema (psutil): CPU, RAM, disco, red, uptime y procesos.
"""

import time

import psutil


def sistema() -> dict:
    """Resumen de estado del servidor."""
    vms = psutil.virtual_memory()
    disco = psutil.disk_usage("/")
    nic = psutil.net_io_counters()
    return {
        "cpu": psutil.cpu_percent(interval=0.15),
        "ram": {
            "total": vms.total,
            "usado": vms.used,
            "porcentaje": vms.percent,
        },
        "disco": {
            "total": disco.total,
            "usado": disco.used,
            "porcentaje": disco.percent,
        },
        "red": {
            "recibidos": nic.bytes_recv,
            "enviados": nic.bytes_sent,
        },
        "uptime_seg": int(time.time() - psutil.boot_time()),
        "procesos": len(psutil.pids()),
    }


def procesos(limite: int = 20) -> list[dict]:
    """Primeros procesos por uso de CPU."""
    lista = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            info = p.info
            if info["name"] is not None:
                lista.append(
                    {
                        "pid": info["pid"],
                        "nombre": info["name"],
                        "cpu": round(info["cpu_percent"] or 0, 1),
                        "memoria": round(info["memory_percent"] or 0, 1),
                    }
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    lista.sort(key=lambda p: p["cpu"], reverse=True)
    return lista[:max(1, limite)]