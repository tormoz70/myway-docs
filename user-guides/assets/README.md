# Иллюстрации для руководства пользователя

Снимки в репозитории сняты с **локального** стенда `http://127.0.0.1:5173` под учёткой из `.env.e2e` (май 2026). При обновлении можно использовать тот же стенд или тестовый `http://46.21.244.114`. Имена файлов должны совпадать с ссылками в `docs/user-guides/ru/*.md`.

## Файлы в репозитории

| Файл | Содержимое | Глава |
|------|------------|-------|
| `login-page.png` | `/go/login` | [00-vvedenie.md](../ru/00-vvedenie.md) |
| `register-page.png` | `/go/register` | [00-vvedenie.md](../ru/00-vvedenie.md) |
| `platform-landing.png` | `/go/` — лендинг (trailing slash обязателен для Vite `base`) | (справочно) |
| `layout-sidebar.png` | Дашборд: меню + контент | [01-layout-i-menu.md](../ru/01-layout-i-menu.md) |
| `schedule-week.png` | Расписание, «Неделя» | [02-raspisanie-podrobno.md](../ru/02-raspisanie-podrobno.md) |
| `schedule-day.png` | Расписание, «День» | [02-raspisanie-podrobno.md](../ru/02-raspisanie-podrobno.md) |
| `schedule-month.png` | Расписание, «Месяц» | [02-raspisanie-podrobno.md](../ru/02-raspisanie-podrobno.md) |
| `schedule-modal-new.png` | Модал «Новая запись», «Свойства» | [02-raspisanie-podrobno.md](../ru/02-raspisanie-podrobno.md) |
| `schedule-modal-attendance.png` | Модал записи, «Факт посещаемости» | [02-raspisanie-podrobno.md](../ru/02-raspisanie-podrobno.md) |
| `subjects-table.png` | Предметы | [03-predmety-i-tarify.md](../ru/03-predmety-i-tarify.md) |
| `rooms-table.png` | Залы | [04-zaly.md](../ru/04-zaly.md) |
| `access-tabs.png` | Пропуска: вкладки | [05-propusk.md](../ru/05-propusk.md) |
| `access-gate-qr.png` | Пропуска: «Станция / QR» | [05-propusk.md](../ru/05-propusk.md) |
| `billing-tabs.png` | Биллинг | [06-billing.md](../ru/06-billing.md) |
| `finance-turnover.png` | Финансы → сводный оборот | [07-finansy.md](../ru/07-finansy.md) |
| `sublease-workspace.png` | Субаренда | [08-subarenda-i-eksport.md](../ru/08-subarenda-i-eksport.md) |
| `export-1c.png` | Экспорт 1С | [08-subarenda-i-eksport.md](../ru/08-subarenda-i-eksport.md) |
| `admin-work.png` | График работы администраторов | [09-polzovateli-grafik.md](../ru/09-polzovateli-grafik.md) |
| `news-admin.png` | Новости студии | [10-novosti-zayavki.md](../ru/10-novosti-zayavki.md) |
| `join-requests.png` | Заявки на участие | [10-novosti-zayavki.md](../ru/10-novosti-zayavki.md) |
| `me-home.png` | Личный кабинет (карточки) | [11-lichniy-kabinet.md](../ru/11-lichniy-kabinet.md) |
| `settings-org.png` | Настройки → «Организация» | [12-nastroiki.md](../ru/12-nastroiki.md) |
| `privacy.png` | Профиль и приватность | [12-nastroiki.md](../ru/12-nastroiki.md) |
| `feedback.png` | Обратная связь | [13-obratnaya-svyaz.md](../ru/13-obratnaya-svyaz.md) |
| `platform-admin.png` | Платформа (`/go/platform`, вкладки тенантов/подписок) | [14-platforma-super-admin.md](../ru/14-platforma-super-admin.md) |

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

Для `platform-admin.png` — учётка **SUPER_ADMIN** или **SUPER_USER** (`/go/platform`). Желательно обновить снимок после появления вкладок **«Тарифы»** и **«Рассылки»** (май 2026).

В Markdown:

```markdown
![Подпись к рисунку](../assets/имя-файла.png)
```
