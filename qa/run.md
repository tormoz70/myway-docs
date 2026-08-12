# Запуск Playwright E2E

Единственная инструкция по прогону. Команды — из корня **myway**, если не сказано иначе.
Шаблон переменных: `myway/.env.e2e.example` → `frontend/.env.e2e` (в `.gitignore`).

## Два режима

| Режим | Команда | Backend | Что бежит |
|-------|---------|---------|-----------|
| **Integration** (основной) | `cd frontend && npm run test:e2e:integration` | `:8080` + Vite `:5173` | seed → `entity-content.spec.ts` → `e2e/manual/` → cleanup |
| **Smoke** | `CI=true`, `E2E_INTEGRATION=0`, `npm run build`, `npm run test:e2e` | не нужен | project `chromium`, `manual/` skip |

Smoke **не** замена integration. `npm run test:e2e` без `E2E_INTEGRATION=0` подтягивает старый `.env.e2e` и валит manual.

Оркестратор **не** запускает: `staff-invite.spec.ts`, `premise-hall.spec.ts`, overnight, чаты. Их список — в [coverage.md](coverage.md) (контур «chromium + seed»).

## Preflight (перед integration)

1. Docker Postgres/Redis/MinIO (`cd backend && docker compose up -d`) и стенд: skill `run-dev-stack` или `.\scripts\dev-local.ps1`.
2. **Локальный SMTP** (иначе seed падает на invite/join):

```powershell
pip install aiosmtpd
python -m aiosmtpd -n -l 127.0.0.1:2525
```

Порт **2525** (на Windows 1025 часто нужен admin). `python -m smtpd` в Python 3.12+ нет.

Backend с перебитой почтой (не Timeweb из `compose.env`):

```powershell
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

`scripts/qa/run_e2e_integration.py`: cleanup → пароль SUPER_ADMIN = `TestPass12` → seed → Playwright → cleanup + восстановление hash SUPER_ADMIN.

Seed пишет `frontend/.env.e2e`. Протухший файл → `Login API failed: 401`.

В `.env.e2e` достаточно email SUPER_ADMIN (`E2E_USER_SUPER_ADMIN_EMAIL`); иначе берётся первый SUPER_ADMIN в БД.

Ручной seed:

```powershell
python scripts/qa/seed_e2e_fixtures.py `
  --api-base http://127.0.0.1:8080/api `
  --db-url postgresql://myway:myway@127.0.0.1:5432/myway `
  --write-env frontend/.env.e2e
```

Только Playwright после seed:

```powershell
cd frontend
$env:E2E_INTEGRATION="1"
$env:PLAYWRIGHT_SKIP_WEBSERVER="1"
npx playwright test --project=integration-manual --workers=1
```

Дополнительно (тот же `.env.e2e`):

```powershell
npx playwright test staff-invite.spec.ts premise-hall.spec.ts schedule-entry-overnight.spec.ts --project=chromium --workers=1
npx playwright test support-chat.spec.ts tenant-chat.spec.ts platform-chat.spec.ts --project=chromium --workers=1
```

## Smoke (без backend)

```powershell
cd frontend
$env:CI = "true"
$env:E2E_INTEGRATION = "0"
npm run build
npm run test:e2e
```

Известный дефект: `finance-turnover.spec.ts` (strict mode, несколько «Абонементы»).

## Переменные

| Переменная | Назначение |
|------------|------------|
| `E2E_INTEGRATION` | `1` — включить `e2e/manual/` и integration-спеки |
| `E2E_BASE_URL` | SPA, обычно `http://127.0.0.1:5173` |
| `E2E_API_BASE` | API, по умолчанию `http://127.0.0.1:8080/api` |
| `E2E_TENANT_SLUG` | slug seed-студии |
| `E2E_USER_*_EMAIL` / `PASSWORD` | OWNER, ADMIN, INSTRUCTOR, STUDENT, SUB_TENANT, SUPER_ADMIN |
| `E2E_ALLOW_REGISTRATION` | по умолчанию `1` при integration (регистрация студии) |
| `E2E_ALLOW_DESTRUCTIVE` | по умолчанию `1` (блокировка тенанта, удаление аккаунта) |
| `E2E_SKIP_CLEANUP` | `1` — не чистить данные после прогона |
| `E2E_SEED_ROOM_NAME` / `E2E_SEED_SUBLEASE_ROOM_NAME` | залы seed |
| `E2E_SEED_SUBJECT_NAME` | предмет seed |
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
| integration **skipped** | нет `E2E_INTEGRATION=1` |
| 68 failed + manual | `test:e2e` без `E2E_INTEGRATION=0` |

Отчёт: `frontend/playwright-report/index.html`.
