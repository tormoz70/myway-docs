# Иллюстрации для руководства пользователя

Снимки в репозитории сняты с **локального** стенда `http://127.0.0.1:5173` под учёткой из `.env.e2e` (май 2026). При обновлении можно использовать тот же стенд или тестовый `http://46.21.244.114`. Имена файлов должны совпадать с ссылками в `user-guides/ru/role-*.md`.

Пересъёмка: из репозитория **myway** — `cd frontend && npm run capture:user-guide-screenshots` (пишет сюда; см. `MYWAY_DOCS_ROOT`).

## Файлы в репозитории

| Файл | Содержимое | Глава |
|------|------------|-------|
| `login-page.png` | Вход в студию (`/go/<slug>/login`), заголовок — название студии | [role-vladelec.md](../ru/role-vladelec.md#vhod) |
| `register-page.png` | Регистрация студии | [role-vladelec.md](../ru/role-vladelec.md#vhod) |
| `platform-landing.png` | `/go/` — лендинг | [role-super-admin.md](../ru/role-super-admin.md) |
| `layout-sidebar.png` | Дашборд: меню + контент | [role-vladelec.md](../ru/role-vladelec.md#kabinet-i-menyu) |
| `schedule-week.png` | Расписание, «Неделя» | [role-vladelec.md](../ru/role-vladelec.md#raspisanie) |
| `schedule-day.png` | Расписание, «День» | [role-vladelec.md](../ru/role-vladelec.md#raspisanie) |
| `schedule-month.png` | Расписание, «Месяц» | [role-vladelec.md](../ru/role-vladelec.md#raspisanie) |
| `schedule-modal-new.png` | Модал «Новая запись» | [role-vladelec.md](../ru/role-vladelec.md#raspisanie) |
| `schedule-modal-attendance.png` | «Факт посещаемости» | [role-vladelec.md](../ru/role-vladelec.md#raspisanie) |
| `subjects-table.png` | Предметы | [role-vladelec.md](../ru/role-vladelec.md#predmety) |
| `rooms-table.png` | Залы | [role-vladelec.md](../ru/role-vladelec.md#zaly) |
| `access-tabs.png` | Пропуска | [role-vladelec.md](../ru/role-vladelec.md#propuska) |
| `access-gate-qr.png` | Регистрация входа | [role-vladelec.md](../ru/role-vladelec.md#propuska) |
| `billing-tabs.png` | Коммуналка и счётчики | [role-vladelec.md](../ru/role-vladelec.md#kommunalka) |
| `finance-turnover.png` | Сводная ведомость | [role-vladelec.md](../ru/role-vladelec.md#finansy) |
| `sublease-workspace.png` | Субаренда | [role-vladelec.md](../ru/role-vladelec.md#subarenda) |
| `export-1c.png` | Экспорт 1С | [role-vladelec.md](../ru/role-vladelec.md#finansy) |
| `admin-work.png` | График работы | [role-vladelec.md](../ru/role-vladelec.md#kadry) |
| `news-admin.png` | Новости студии | [role-vladelec.md](../ru/role-vladelec.md#novosti-i-zayavki) |
| `join-requests.png` | Заявки | [role-vladelec.md](../ru/role-vladelec.md#novosti-i-zayavki) |
| `me-home.png` | Личная главная | [role-uchenik.md](../ru/role-uchenik.md#kabinet-i-menyu) |
| `settings-org.png` | Настройки | [role-vladelec.md](../ru/role-vladelec.md#nastroiki) |
| `privacy.png` | Профиль и приватность | [role-vladelec.md](../ru/role-vladelec.md#nastroiki) |
| `feedback.png` | Обратная связь | [role-vladelec.md](../ru/role-vladelec.md#obratnaya-svyaz) |
| `platform-admin.png` | Платформа | [role-super-admin.md](../ru/role-super-admin.md#platforma) |

## Как обновить снимки

**Автоматически (все файлы из таблицы):**

```bash
# 1. Backend :8080, Vite :5173, PostgreSQL
cd frontend
python ../scripts/qa/seed_e2e_fixtures.py --api-base http://127.0.0.1:8080/api --write-env .env.e2e

# 2. Снять PNG в эту папку
set PLAYWRIGHT_SKIP_WEBSERVER=1
set E2E_INTEGRATION=1
npm run capture:user-guide-screenshots
```

Скрипт: `frontend/e2e/capture-user-guide-screenshots.spec.ts`.

**Вручную:** API + фронт, учётки из `.env.e2e`, открыть экран и сохранить PNG с именем из таблицы.

Для `schedule-modal-attendance.png` нужна **сохранённая** запись типа **«Занятие»**: откройте её в расписании → вкладка **«Факт посещаемости»**.

Для `platform-admin.png` — учётка **SUPER_ADMIN** или **SUPER_USER** (`/go/platform`).

В Markdown:

```markdown
![Подпись к рисунку](../assets/имя-файла.png)
```
