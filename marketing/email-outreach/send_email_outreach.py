#!/usr/bin/env python3
"""
Рассылка писем блока A с домена myway-line.ru через SMTP.

По умолчанию dry-run: печать плана без отправки.
Реальная отправка: python send_email_outreach.py --send

Секреты — в .env (см. .env.example). Нужны SPF/DKIM/DMARC на домене.
"""

from __future__ import annotations

import argparse
import csv
import os
import random
import smtplib
import ssl
import sys
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid
from pathlib import Path
from string import Formatter

DIR = Path(__file__).resolve().parent
DEFAULT_DELAY = (40, 90)


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


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "y", "on")


def load_recipients(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if (row.get("enabled") or "").strip().lower() not in ("yes", "y", "1", "true"):
                continue
            email = (row.get("email") or "").strip()
            if not email or "@" not in email:
                continue
            rows.append(row)
    return rows


def render_template(template: str, row: dict) -> str:
    mapping = {
        "name": (row.get("name") or "").strip(),
        "city": (row.get("city") or "").strip(),
        "email": (row.get("email") or "").strip(),
        "id": (row.get("id") or "").strip(),
        "note": (row.get("note") or "").strip(),
    }
    # Не падаем на неизвестных {плейсхолдерах}
    class SafeDict(dict):
        def __missing__(self, key: str) -> str:
            return "{" + key + "}"

    return Formatter().vformat(template, (), SafeDict(mapping))


def append_log(path: Path, row: dict) -> None:
    new_file = not path.is_file()
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["ts", "id", "name", "email", "status", "detail"],
        )
        if new_file:
            w.writeheader()
        w.writerow(row)


def build_message(
    *,
    subject: str,
    body: str,
    from_addr: str,
    from_name: str,
    reply_to: str,
    to_addr: str,
) -> MIMEText:
    msg = MIMEText(body, _subtype="plain", _charset="utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = formataddr((str(Header(from_name, "utf-8")), from_addr))
    msg["To"] = to_addr
    msg["Reply-To"] = reply_to
    msg["Message-ID"] = make_msgid(domain=from_addr.split("@")[-1])
    msg["X-Mailer"] = "MyWay-outreach/1.0"
    return msg


def smtp_send(msg: MIMEText, to_addr: str) -> None:
    host = os.environ["SMTP_HOST"].strip()
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ["SMTP_USER"].strip()
    password = os.environ["SMTP_PASSWORD"]
    # Порт 465 = implicit SSL; 587 = STARTTLS. Явные флаги в .env имеют приоритет,
    # но если оба false/противоречат порту — выбираем по порту.
    use_tls = env_bool("SMTP_USE_TLS", port == 587)
    use_ssl = env_bool("SMTP_USE_SSL", port == 465)
    if port == 465 and not use_ssl:
        use_ssl, use_tls = True, False
    if port == 587 and use_ssl:
        use_ssl, use_tls = False, True

    if use_ssl:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context, timeout=60) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg, to_addrs=[to_addr])
        return

    with smtplib.SMTP(host, port, timeout=60) as smtp:
        smtp.ehlo()
        if use_tls:
            context = ssl.create_default_context()
            smtp.starttls(context=context)
            smtp.ehlo()
        smtp.login(user, password)
        smtp.send_message(msg, to_addrs=[to_addr])


def main() -> int:
    parser = argparse.ArgumentParser(description="Email outreach блока A через SMTP")
    parser.add_argument("--send", action="store_true", help="Реально отправить")
    parser.add_argument("--csv", type=Path, default=DIR / "recipients_a.csv")
    parser.add_argument("--message", type=Path, default=DIR / "message.txt")
    parser.add_argument("--subject", type=Path, default=DIR / "subject.txt")
    parser.add_argument("--env", type=Path, default=DIR / ".env")
    parser.add_argument("--log", type=Path, default=DIR / "send_log.csv")
    parser.add_argument("--delay-min", type=float, default=DEFAULT_DELAY[0])
    parser.add_argument("--delay-max", type=float, default=DEFAULT_DELAY[1])
    parser.add_argument("--only", type=str, default="", help="id через запятую, напр. 1,3,7")
    parser.add_argument(
        "--to",
        type=str,
        default="",
        help="Тестовый адрес: одно письмо себе (подставляет первый enabled из CSV)",
    )
    args = parser.parse_args()

    load_env(args.env)

    required = ["SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "SMTP_FROM"]
    missing = [k for k in required if not os.environ.get(k, "").strip()]
    if args.send and missing:
        print(
            "Для --send нужны в .env: " + ", ".join(missing) + "\n"
            "Скопируйте .env.example → .env и заполните SMTP ящика @myway-line.ru",
            file=sys.stderr,
        )
        return 1

    if not args.message.is_file() or not args.subject.is_file():
        print("Нужны message.txt и subject.txt", file=sys.stderr)
        return 1

    template = args.message.read_text(encoding="utf-8").strip()
    subject_tpl = args.subject.read_text(encoding="utf-8").strip()
    if not template or not subject_tpl:
        print("message.txt или subject.txt пустые", file=sys.stderr)
        return 1

    recipients = load_recipients(args.csv)
    if args.only:
        allow = {x.strip() for x in args.only.split(",") if x.strip()}
        recipients = [r for r in recipients if r.get("id", "").strip() in allow]

    if args.to:
        if not recipients:
            print("Нет строки в CSV для шаблона персонализации", file=sys.stderr)
            return 1
        probe = dict(recipients[0])
        probe["email"] = args.to.strip()
        probe["name"] = probe.get("name") or "Тест"
        probe["city"] = probe.get("city") or "тест"
        recipients = [probe]

    if not recipients:
        print("Нет получателей (enabled / --only / email)")
        return 1

    from_addr = os.environ.get("SMTP_FROM", os.environ.get("SMTP_USER", "")).strip()
    from_name = os.environ.get("SMTP_FROM_NAME", "MyWay").strip()
    reply_to = os.environ.get("SMTP_REPLY_TO", from_addr).strip()

    mode = "SEND" if args.send else "DRY-RUN"
    print(f"Режим: {mode}")
    print(f"From: {from_name} <{from_addr or '(не задан — только dry-run)'}>")
    print(f"SMTP: {os.environ.get('SMTP_HOST', '(нет)')}:{os.environ.get('SMTP_PORT', '587')}")
    print(f"Получателей: {len(recipients)}")
    print(f"Тема: {subject_tpl}\n")

    for i, row in enumerate(recipients):
        to_addr = row["email"].strip()
        name = (row.get("name") or "").strip()
        rid = (row.get("id") or "").strip()
        body = render_template(template, row)
        subject = render_template(subject_tpl, row)

        print(f"[{i + 1}/{len(recipients)}] {name} <{to_addr}> …", end=" ", flush=True)

        try:
            msg = build_message(
                subject=subject,
                body=body,
                from_addr=from_addr or "noreply@myway-line.ru",
                from_name=from_name,
                reply_to=reply_to or from_addr or "noreply@myway-line.ru",
                to_addr=to_addr,
            )

            if not args.send:
                preview = body.splitlines()[:4]
                print("dry-run OK")
                for line in preview:
                    print(f"    | {line}")
                append_log(
                    args.log,
                    {
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "id": rid,
                        "name": name,
                        "email": to_addr,
                        "status": "dry-run",
                        "detail": f"chars={len(body)}",
                    },
                )
            else:
                smtp_send(msg, to_addr)
                print("sent")
                append_log(
                    args.log,
                    {
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "id": rid,
                        "name": name,
                        "email": to_addr,
                        "status": "sent",
                        "detail": subject,
                    },
                )
                if i < len(recipients) - 1:
                    delay = random.uniform(args.delay_min, args.delay_max)
                    print(f"    пауза {delay:.0f} с …")
                    time.sleep(delay)

        except Exception as e:
            print(f"ERROR: {e}")
            append_log(
                args.log,
                {
                    "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "id": rid,
                    "name": name,
                    "email": to_addr,
                    "status": "error",
                    "detail": str(e),
                },
            )
            if args.send and i < len(recipients) - 1:
                time.sleep(random.uniform(args.delay_min, args.delay_max))

    print(f"\nЛог: {args.log}")
    if not args.send:
        print("Тест себе:  python send_email_outreach.py --send --to you@myway-line.ru")
        print("Всем из CSV: python send_email_outreach.py --send")
    return 0


if __name__ == "__main__":
    sys.exit(main())
