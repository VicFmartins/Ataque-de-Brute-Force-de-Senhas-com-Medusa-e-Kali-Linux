from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


def load_events(file_path: Path) -> list[dict]:
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def analyze(events: list[dict]) -> dict:
    failures_by_ip = defaultdict(int)
    users_by_ip = defaultdict(set)
    failures_by_ip_user = defaultdict(int)
    success_after_failures = []

    for event in events:
        ip = event["source_ip"]
        user = event["username"]
        result = event["result"]

        if result == "failure":
            failures_by_ip[ip] += 1
            users_by_ip[ip].add(user)
            failures_by_ip_user[(ip, user)] += 1
        elif result == "success" and failures_by_ip_user[(ip, user)] >= 3:
            success_after_failures.append({"ip": ip, "username": user})

    brute_force_candidates = [
        {"ip": ip, "username": user, "failures": count}
        for (ip, user), count in failures_by_ip_user.items()
        if count >= 4
    ]

    spraying_candidates = [
        {"ip": ip, "distinct_users": len(users), "failures": failures_by_ip[ip]}
        for ip, users in users_by_ip.items()
        if len(users) >= 4 and failures_by_ip[ip] >= 4
    ]

    high_failure_ips = [
        {"ip": ip, "failures": count}
        for ip, count in failures_by_ip.items()
        if count >= 3
    ]

    return {
        "total_events": len(events),
        "high_failure_ips": high_failure_ips,
        "brute_force_candidates": brute_force_candidates,
        "spraying_candidates": spraying_candidates,
        "success_after_failures": success_after_failures,
    }


def print_summary(summary: dict) -> None:
    print("Resumo de autenticacao")
    print(f"- Total de eventos: {summary['total_events']}")
    print(f"- IPs com alta taxa de falha: {len(summary['high_failure_ips'])}")
    print(f"- Usuarios alvo de spraying: {sum(item['distinct_users'] for item in summary['spraying_candidates'])}")
    print(f"- Possiveis brute force simples: {len(summary['brute_force_candidates'])}")
    print(f"- Possiveis password spraying: {len(summary['spraying_candidates'])}")

    if summary["brute_force_candidates"]:
        print("- Brute force suspeito:")
        for item in summary["brute_force_candidates"]:
            print(f"  * {item['ip']} -> {item['username']} | falhas: {item['failures']}")

    if summary["spraying_candidates"]:
        print("- Password spraying suspeito:")
        for item in summary["spraying_candidates"]:
            print(f"  * {item['ip']} | usuarios distintos: {item['distinct_users']} | falhas: {item['failures']}")

    if summary["success_after_failures"]:
        print("- Sucesso apos falhas repetidas:")
        for item in summary["success_after_failures"]:
            print(f"  * {item['ip']} -> {item['username']}")


def main() -> None:
    file_arg = sys.argv[1] if len(sys.argv) > 1 else "samples/auth_events.json"
    file_path = Path(file_arg)

    if not file_path.exists():
        raise SystemExit(f"Arquivo nao encontrado: {file_path}")

    summary = analyze(load_events(file_path))
    print_summary(summary)


if __name__ == "__main__":
    main()
