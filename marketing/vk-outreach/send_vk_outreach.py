#!/usr/bin/env python3
"""
Рассылка ЛС в сообщества ВК (блок A кандидатов MyWay).

По умолчанию dry-run: только резолв групп и печать плана.
Реальная отправка: python send_vk_outreach.py --send

Нужен user-токен в .env (см. .env.example).
"""

from __future__ import annotations

import argparse
import csv
import os
import random
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Установите зависимости: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

DIR = Path(__file__).resolve().parent
API = "https://api.vk.com/method"
DEFAULT_DELAY = (35, 75)  # сек между отправками


def load_env(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def vk_call(method: str, token: str, version: str, **params) -> dict:
    data = {**params, "access_token": token, "v": version}
    r = requests.post(f"{API}/{method}", data=data, timeout=30)
    r.raise_for_status()
    body = r.json()
    if "error" in body:
        err = body["error"]
        code = err.get("error_code")
        msg = err.get("error_msg", "unknown")
        raise RuntimeError(f"VK API {code}: {msg}")
    return body["response"]


def resolve_group_id(token: str, version: str, screen_name: str) -> int:
    name = screen_name.strip().removeprefix("https://vk.com/").removeprefix("vk.com/")
    if name.startswith("club") and name[4:].isdigit():
        return int(name[4:])
    if name.startswith("public") and name[6:].isdigit():
        return int(name[6:])
    if name.isdigit():
        return int(name)
    info = vk_call("utils.resolveScreenName", token, version, screen_name=name)
    if not info or info.get("type") not in ("group", "page", "event"):
        raise RuntimeError(f"Не сообщество: {screen_name!r} → {info!r}")
    return int(info["object_id"])


def load_recipients(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if (row.get("enabled") or "").strip().lower() not in ("yes", "y", "1", "true"):
                continue
            rows.append(row)
    return rows


def append_log(path: Path, row: dict) -> None:
    new_file = not path.is_file()
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["ts", "id", "name", "screen_name", "group_id", "status", "detail"],
        )
        if new_file:
            w.writeheader()
        w.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description="VK outreach → сообщения сообществ")
    parser.add_argument("--send", action="store_true", help="Реально отправить (без флага — dry-run)")
    parser.add_argument("--csv", type=Path, default=DIR / "recipients_a.csv")
    parser.add_argument("--message", type=Path, default=DIR / "message.txt")
    parser.add_argument("--env", type=Path, default=DIR / ".env")
    parser.add_argument("--log", type=Path, default=DIR / "send_log.csv")
    parser.add_argument("--delay-min", type=float, default=DEFAULT_DELAY[0])
    parser.add_argument("--delay-max", type=float, default=DEFAULT_DELAY[1])
    parser.add_argument("--only", type=str, default="", help="Только id через запятую, напр. 1,3,7")
    args = parser.parse_args()

    load_env(args.env)
    token = os.environ.get("VK_TOKEN", "").strip()
    version = os.environ.get("VK_API_VERSION", "5.199").strip()

    if not token:
        print(
            "Нет VK_TOKEN. Скопируйте .env.example → .env и вставьте user-токен.",
            file=sys.stderr,
        )
        return 1

    if not args.message.is_file():
        print(f"Нет файла сообщения: {args.message}", file=sys.stderr)
        return 1
    message = args.message.read_text(encoding="utf-8").strip()
    if not message:
        print("message.txt пустой", file=sys.stderr)
        return 1

    recipients = load_recipients(args.csv)
    if args.only:
        allow = {x.strip() for x in args.only.split(",") if x.strip()}
        recipients = [r for r in recipients if r.get("id", "").strip() in allow]

    if not recipients:
        print("Нет получателей (проверьте enabled / --only)")
        return 1

    mode = "SEND" if args.send else "DRY-RUN"
    print(f"Режим: {mode}")
    print(f"Получателей: {len(recipients)}")
    print(f"Текст ({len(message)} символов):\n---\n{message}\n---\n")

    # Проверка токена
    me = vk_call("users.get", token, version)
    if not me:
        print("users.get пустой — проверьте токен", file=sys.stderr)
        return 1
    print(f"Отправитель: id{me[0]['id']} {me[0].get('first_name', '')} {me[0].get('last_name', '')}\n")

    for i, row in enumerate(recipients):
        name = row.get("name", "")
        screen = row.get("screen_name", "").strip()
        rid = row.get("id", "")
        print(f"[{i + 1}/{len(recipients)}] {name} ({screen}) …", end=" ", flush=True)

        try:
            group_id = resolve_group_id(token, version, screen)
            peer_id = -group_id
            print(f"group_id={group_id}", end="")

            if not args.send:
                print(" — dry-run OK")
                append_log(
                    args.log,
                    {
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "id": rid,
                        "name": name,
                        "screen_name": screen,
                        "group_id": group_id,
                        "status": "dry-run",
                        "detail": f"peer_id={peer_id}",
                    },
                )
            else:
                msg_id = vk_call(
                    "messages.send",
                    token,
                    version,
                    peer_id=peer_id,
                    message=message,
                    random_id=random.randint(1, 2_147_483_647),
                )
                print(f" — sent message_id={msg_id}")
                append_log(
                    args.log,
                    {
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "id": rid,
                        "name": name,
                        "screen_name": screen,
                        "group_id": group_id,
                        "status": "sent",
                        "detail": str(msg_id),
                    },
                )
                if i < len(recipients) - 1:
                    delay = random.uniform(args.delay_min, args.delay_max)
                    print(f"    пауза {delay:.0f} с …")
                    time.sleep(delay)

        except Exception as e:
            print(f" — ERROR: {e}")
            append_log(
                args.log,
                {
                    "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "id": rid,
                    "name": name,
                    "screen_name": screen,
                    "group_id": "",
                    "status": "error",
                    "detail": str(e),
                },
            )
            if args.send and i < len(recipients) - 1:
                time.sleep(random.uniform(args.delay_min, args.delay_max))

    print(f"\nЛог: {args.log}")
    if not args.send:
        print("Чтобы отправить: python send_vk_outreach.py --send")
    return 0


if __name__ == "__main__":
    sys.exit(main())
