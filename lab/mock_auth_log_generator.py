from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path


OUTPUT_FILE = Path("samples/auth_events.json")


def build_events() -> list[dict]:
    start = datetime(2026, 3, 22, 9, 0, 0)
    return [
        {
            "timestamp": (start + timedelta(seconds=0)).isoformat(),
            "source_ip": "203.0.113.10",
            "username": "admin",
            "result": "failure",
            "service": "ssh"
        },
        {
            "timestamp": (start + timedelta(seconds=5)).isoformat(),
            "source_ip": "203.0.113.10",
            "username": "admin",
            "result": "failure",
            "service": "ssh"
        },
        {
            "timestamp": (start + timedelta(seconds=11)).isoformat(),
            "source_ip": "203.0.113.10",
            "username": "admin",
            "result": "failure",
            "service": "ssh"
        },
        {
            "timestamp": (start + timedelta(seconds=17)).isoformat(),
            "source_ip": "203.0.113.10",
            "username": "admin",
            "result": "success",
            "service": "ssh"
        },
        {
            "timestamp": (start + timedelta(minutes=1)).isoformat(),
            "source_ip": "198.51.100.25",
            "username": "financeiro",
            "result": "failure",
            "service": "vpn"
        },
        {
            "timestamp": (start + timedelta(minutes=1, seconds=10)).isoformat(),
            "source_ip": "198.51.100.25",
            "username": "rh",
            "result": "failure",
            "service": "vpn"
        },
        {
            "timestamp": (start + timedelta(minutes=1, seconds=20)).isoformat(),
            "source_ip": "198.51.100.25",
            "username": "compras",
            "result": "failure",
            "service": "vpn"
        },
        {
            "timestamp": (start + timedelta(minutes=1, seconds=30)).isoformat(),
            "source_ip": "198.51.100.25",
            "username": "diretoria",
            "result": "failure",
            "service": "vpn"
        },
        {
            "timestamp": (start + timedelta(minutes=3)).isoformat(),
            "source_ip": "192.0.2.50",
            "username": "joao",
            "result": "success",
            "service": "web"
        },
        {
            "timestamp": (start + timedelta(minutes=4)).isoformat(),
            "source_ip": "192.0.2.51",
            "username": "maria",
            "result": "failure",
            "service": "web"
        },
        {
            "timestamp": (start + timedelta(minutes=4, seconds=5)).isoformat(),
            "source_ip": "192.0.2.51",
            "username": "maria",
            "result": "failure",
            "service": "web"
        },
        {
            "timestamp": (start + timedelta(minutes=4, seconds=10)).isoformat(),
            "source_ip": "192.0.2.51",
            "username": "maria",
            "result": "failure",
            "service": "web"
        },
        {
            "timestamp": (start + timedelta(minutes=4, seconds=15)).isoformat(),
            "source_ip": "192.0.2.51",
            "username": "maria",
            "result": "failure",
            "service": "web"
        },
        {
            "timestamp": (start + timedelta(minutes=5)).isoformat(),
            "source_ip": "192.0.2.52",
            "username": "suporte",
            "result": "success",
            "service": "rdp"
        },
    ]


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    events = build_events()

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(events, file, indent=2, ensure_ascii=False)

    print("Arquivo gerado com sucesso:")
    print(OUTPUT_FILE)
    print(f"Total de eventos simulados: {len(events)}")


if __name__ == "__main__":
    main()
