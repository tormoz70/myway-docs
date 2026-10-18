# Рассылка email с домена myway-line.ru (блок A)

Скрипт шлёт plain-text письмо из `message.txt` на адреса из `recipients_a.csv` через SMTP вашего ящика `@myway-line.ru`.

Перед волной: SPF + DKIM + DMARC на домене (см. [outreach.md](../outreach.md)).

## Подготовка

1. Убедитесь, что почта на домене работает (Яндекс 360 / Beget / Timeweb и т.п.).
2. Скопируйте окружение:

```powershell
cd marketing/email-outreach
copy .env.example .env
# заполните SMTP_HOST, SMTP_USER, SMTP_PASSWORD
```

Типичные SMTP:

| Провайдер | Host | Port | Флаги |
|-----------|------|------|--------|
| Яндекс 360 | `smtp.yandex.ru` | 587 | `SMTP_USE_TLS=true` |
| Яндекс 360 | `smtp.yandex.ru` | 465 | `SMTP_USE_SSL=true`, `SMTP_USE_TLS=false` |
| Mail.ru для бизнеса | `smtp.mail.ru` | 587 | TLS |
| Beget | `smtp.beget.com` | 465 | SSL |

`SMTP_FROM` должен совпадать с доменом, для которого настроены SPF/DKIM (лучше тот же `SMTP_USER`).

## Запуск

План без отправки:

```powershell
python send_email_outreach.py
```

Одно тестовое письмо себе:

```powershell
python send_email_outreach.py --send --to support@myway-line.ru
```

Вся первая группа (enabled=yes в CSV):

```powershell
python send_email_outreach.py --send
```

Только выбранные id:

```powershell
python send_email_outreach.py --send --only 1,2,3
```

Пауза между письмами по умолчанию 40–90 с. Лог: `send_log.csv`.

## Файлы

| Файл | Назначение |
|------|------------|
| `message.txt` | Тело; плейсхолдеры `{name}`, `{city}` |
| `subject.txt` | Тема |
| `recipients_a.csv` | Блок A с email (без LapLap — только телефон) |

LapLap (#6) в CSV нет — пишите в WhatsApp вручную.
