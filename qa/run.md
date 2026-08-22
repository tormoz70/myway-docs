# Запуск Playwright E2E

Единственная инструкция по прогону. Команды — из корня **myway**, если не сказано иначе.
Шаблон переменных: `myway/.env.e2e.example` → `frontend/.env.e2e` (в `.gitignore`).

## Режимы

| Режим | Команда | Backend | Project |
|-------|---------|---------|---------|
| **Integration** (основной) | `cd frontend && npm run test:e2e:integration` | `:8080` + Vite `:5173` | `integration` |
| **Simulator** (ручной стенд UC) | `cd frontend && npm run test:e2e:simulator` | `:8080` + Vite `:5173` + `manual-test-stand.json` | `simulator` |
| **Smoke** | `CI=true`, `E2E_INTEGRATION=0`, `npm run build`, `npm run test:e2e -- --project=smoke` | не нужен | `smoke` |

Smoke **не** замена integration. `npm run test:e2e` без `--project=smoke` и без `E2E_INTEGRATION=0` подтянет integration-спеки и потребует seed.

Оркестратор `scripts/qa/run_e2e_integration.py`: cleanup → seed → `npx playwright test --project=integration --workers=1` → cleanup.

Покрытие spec ↔ кейс: [coverage.md](coverage.md).

## Preflight (перед integration)

1. Docker Postgres/Redis/MinIO (`cd backend && docker compose up -d`) и стенд: skill `run-dev-stack` или `.\scripts\dev-local.ps1`.
2. **Локальный SMTP** (иначе seed падает на invite/join):

```powershell
pip install aiosmtpd
python -m aiosmtpd -n -l 127.0.0.1:2525
```

Порт **2525** (на Windows 1025 часто нужен admin). `python -m smtpd` в Python 3.12+ нет.

Backend с перебитой почтой (не Timeweb из `compose.env`). Перед integration отключите rate limit на login:

```powershell
$env:APP_AUTH_RATE_LIMIT_ENABLED = "false"
cd backend
.\gradlew.bat :myway-api:bootRun --no-daemon --args="--spring.mail.host=127.0.0.1 --spring.mail.port=2525 --spring.mail.properties.mail.smtp.auth=false --spring.mail.properties.mail.smtp.ssl.enable=false --spring.mail.properties.mail.smtp.starttls.enable=false"
```

Не поднимать второй `bootRun` на занятом `:8080`. JDBC приложения — роль `myway_app`.

3. Проверки:

| Проверка | Ожидание |
|----------|----------|
| `POST /api/auth/register` (уникальный email/slug) | **200** (409 = email занят, для probe тоже OK) |
| `GET /actuator/health` | 200 желательно; 503 при register 200 часто только Redis indicator |
| `GET http://127.0.0.1:5173/go/` | 200 |

Register **500** → перезапуск стенда (`dev-local.ps1 -Stop` затем снова, с SMTP `--args`).

## Integration

```powershell
cd frontend
npm run test:e2e:integration
```

`scripts/qa/run_e2e_integration.py`: cleanup → пароль SUPER_ADMIN = `TestPass12` → seed (OWNER…CLEANER, SUPER_USER) → Playwright project `integration` → cleanup + восстановление hash SUPER_ADMIN.

Seed пишет `frontend/.env.e2e`. Протухший файл → `Login API failed: 401`.

Кроме учёток и каталога seed заводит данные, без которых экраны пусты и проверки сводились
к заголовку страницы:

| Фикстура | Что создаётся | Где видно |
|----------|---------------|-----------|
| Лид воронки | заявка с сайта от «Мария Лидова», `+79005550101`, источник `INQUIRY` | «Воронка», кадр `funnel.png` |
| Занятие студента | ежедневное занятие с сегодняшнего дня + запись студента на первое будущее вхождение | «Моё расписание», кадр `me-schedule.png` |
| Пропуск | прошедшее занятие (10 дней назад) + `NO_SHOW` | карточка «Нужна отработка» на главной ADMIN |

Каждый шаг проверяет результат (лид дошёл до воронки, запись попала в `needs-makeup`) и падает
с понятным текстом. Пропуск требует `--db-url`: `NO_SHOW` ставит только ночной
`LessonEnrollmentNoShowJob`, поэтому запись пишется в БД, а seed выставляет `E2E_SEED_MAKEUP_READY=1`.

Занятие ежедневное, потому что «Моё расписание» показывает только текущую неделю: одиночная
запись на фиксированный день недели давала бы «Нет записей на эту неделю» в зависимости от дня прогона.

В `.env.e2e` достаточно email SUPER_ADMIN (`E2E_USER_SUPER_ADMIN_EMAIL`); иначе берётся первый SUPER_ADMIN в БД.

Ручной seed:

```powershell
python scripts/qa/seed_e2e_fixtures.py `
  --api-base http://127.0.0.1:8080/api `
  --db-url postgresql://myway:myway@127.0.0.1:5432/myway `
  --write-env frontend/.env.e2e `
  --super-admin-email you@example.com `
  --super-admin-password TestPass12
```

Только Playwright после seed:

```powershell
cd frontend
$env:E2E_INTEGRATION="1"
$env:PLAYWRIGHT_SKIP_WEBSERVER="1"
npx playwright test --project=integration --workers=1
```

## Simulator (ручной стенд UC)

Отдельный контур: `generated/manual-test-stand.json`, **без** cleanup integration.

```powershell
# стенд + фикстуры UC на ritm-hall
python scripts/qa/seed_manual_test_stand.py --simulator-fixtures
cd frontend
npm run test:e2e:simulator
```

Фикстуры на уже готовом стенде: `python scripts/qa/manual_stand_simulator.py` (идемпотентно) или
`seed_manual_test_stand.py --simulator-fixtures-only`.

Preflight оркестратора жёсткий: нет API, Vite, учёток или любой фикстуры — `PREFLIGHT FAILED` и код
возврата 2. Незасеянный стенд не должен давать зелёный прогон.

Подробнее — фикстуры, спеки ↔ UC, soak: [use-cases/simulator.md](use-cases/simulator.md).

## Smoke (без backend)

```powershell
cd frontend
$env:CI = "true"
$env:E2E_INTEGRATION = "0"
npm run build
npm run test:e2e -- --project=smoke
```

## Переменные

| Переменная | Назначение |
|------------|------------|
| `E2E_INTEGRATION` | `1` — включить integration-спеки |
| `E2E_SIMULATOR` | `1` — project simulator (ставит оркестратор `run_e2e_simulator.py`) |
| `E2E_MANUAL_STAND_JSON` | путь к `generated/manual-test-stand.json` |
| `E2E_SCHEDULE_TZ` | зона расписания у браузера в project `simulator`, `integration` и при съёмке скриншотов, по умолчанию `Europe/Moscow` |
| `E2E_BASE_URL` | SPA, обычно `http://127.0.0.1:5173` |
| `E2E_API_BASE` | API, по умолчанию `http://127.0.0.1:8080/api` |
| `E2E_TENANT_SLUG` | slug seed-студии |
| `E2E_USER_*_EMAIL` / `PASSWORD` | OWNER, ADMIN, INSTRUCTOR, STUDENT, SUB_TENANT, CLEANER, SUPER_USER, SUPER_ADMIN |
| `E2E_ALLOW_REGISTRATION` | по умолчанию `1` при integration (регистрация студии) |
| `E2E_ALLOW_DESTRUCTIVE` | по умолчанию `1` (блокировка тенанта, удаление аккаунта) |
| `E2E_SKIP_CLEANUP` | `1` — не чистить данные после прогона |
| `E2E_SEED_ROOM_NAME` / `E2E_SEED_SUBLEASE_ROOM_NAME` | залы seed |
| `E2E_SEED_SUBJECT_NAME` | предмет seed (он же подпись занятия) |
| `E2E_SEED_FUNNEL_CONTACT_NAME` / `_PHONE` | лид воронки из seed |
| `E2E_SEED_MAKEUP_READY` | `1` — seed завёл пропуск для очереди отработок (нужен `--db-url`) |
| `PLAYWRIGHT_SKIP_WEBSERVER` | `1` при уже запущенном Vite |

Алиасы `E2E_OWNER_*`, `E2E_ORG_SLUG` ещё читает `helpers/env.ts`.

Cleanup: org `e2e-*` / `pwe2e*`, пользователи `@example.com` с префиксами `e2e-`, `studio-owner-`, `instr-pw-`, `student-pw-`, `admin-invite-`, `instr-invite-`. Чаты с темой `E2E …`. SUPER_ADMIN не удаляется. Студия `divan` (dev) cleanup не трогает.

## Типичные ошибки

| Симптом | Первая причина |
|---------|----------------|
| `Login API failed: 401` | Протухший `.env.e2e` |
| `POST /auth/register -> 500` | Битый backend |
| `POST …/invite -> 502` | SMTP (aiosmtpd + `--args`) |
| `join` timeout 60 s | SMTP не слушает порт |
| `Login API failed: 429` | rate limit — `APP_AUTH_RATE_LIMIT_ENABLED=false` на backend |
| integration **skipped** | нет `E2E_INTEGRATION=1` |
| много failed + integration без seed | `test:e2e` без `--project=smoke` и без integration preflight |
| simulator: `PREFLIGHT FAILED: нет фикстур` | не запускался `manual_stand_simulator.py` |
| simulator: `Нет свободного слота для «…»` | залы стенда заняты расписанием — освободить час или пересоздать стенд |
| simulator **skipped** | нет `E2E_SIMULATOR=1` (его ставит `run_e2e_simulator.py`) |

Отчёт: `frontend/playwright-report/index.html`.
