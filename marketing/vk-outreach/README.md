# Рассылка в ВК (сообщения сообществ)

Скрипт шлёт текст из `message.txt` в ЛС сообществ из `recipients_a.csv` (блок A без LapLap и ПОТОК — у них нет ВК).

## Подготовка

1. Создайте приложение: https://vk.com/apps?act=manage (тип Standalone / «Прочее»).
2. Получите **user access token** с правами `messages` и желательно `offline`  
   (OAuth Implicit / токен вашего личного аккаунта — не токен сообщества).
3. Скопируйте окружение и вставьте токен:

```bash
cd marketing/vk-outreach
copy .env.example .env
# отредактируйте .env: VK_TOKEN=...
pip install -r requirements.txt
```

## Запуск

Сначала проверка без отправки (резолв групп + план):

```bash
python send_vk_outreach.py
```

Реальная отправка (пауза ~35–75 с между сообщениями):

```bash
python send_vk_outreach.py --send
```

Только выбранные id из CSV:

```bash
python send_vk_outreach.py --send --only 1,3,7
```

Лог: `send_log.csv` (не коммитить).

## Важно

- Нужен токен **личного** аккаунта: писать чужим сообществам может пользователь, не community-token.
- Сообщество должно принимать сообщения; иначе в логе будет ошибка API.
- Одинаковый текст + частые запросы → риск captcha / ограничений ВК. Не гоняйте сотни адресов.
- Токен только в `.env`, не в git и не в чат.
