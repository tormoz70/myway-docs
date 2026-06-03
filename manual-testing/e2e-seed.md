# Подготовка данных для Playwright E2E (локально)

Полный набор manual-тестов (`frontend/e2e/manual/`) требует **живой backend** и переменных из `frontend/.env.e2e`.

## Рекомендуемый прогон (всё автоматически)

```powershell
cd backend
docker compose up -d

# backend + frontend в отдельных терминалах (или .\scripts\dev-local.ps1)

cd frontend
npm run test:e2e:integration
```

Скрипт [`scripts/qa/run_e2e_integration.py`](../../scripts/qa/run_e2e_integration.py):

1. **cleanup** — удаляет тестовые org (`e2e-*`, `pwe2e*`) и пользователей с префиксами `e2e-`, `studio-owner-`, `instr-pw-`, `student-pw-`, `admin-invite-`, `instr-invite-` на `@example.com` (в т.ч. без привязки к студии после CASCADE)
2. **SUPER_ADMIN** — бэкап `password_hash` → временный `TestPass12` → после прогона **восстановление**
3. **seed** — новая студия и роли, запись `frontend/.env.e2e`
4. **Playwright** — все `integration-manual` без ручных `E2E_ALLOW_*`
5. **cleanup** снова

### SUPER_ADMIN

В `frontend/.env.e2e` (или корневом `.env.e2e`) укажите только email:

```env
E2E_USER_SUPER_ADMIN_EMAIL=your-super-admin@example.com
```

Пароль в файле не нужен: скрипт подставит `TestPass12` на время прогона и вернёт исходный hash из БД.  
Если email не задан — берётся первый пользователь с ролью `SUPER_ADMIN` в PostgreSQL.

## Ручной seed (без оркестратора)

```bash
pip install -r scripts/qa/requirements.txt
python scripts/qa/seed_e2e_fixtures.py ^
  --api-base http://127.0.0.1:8080/api ^
  --db-url postgresql://myway:myway@127.0.0.1:5432/myway ^
  --write-env frontend/.env.e2e ^
  --super-admin-email YOUR_SA@example.com ^
  --super-admin-password TestPass12
```

После прогона:

```bash
python scripts/qa/cleanup_e2e_fixtures.py --db-url postgresql://myway:myway@127.0.0.1:5432/myway
```

## Только Playwright (если seed уже есть)

```powershell
cd frontend
# загрузите .env.e2e в окружение
$env:E2E_INTEGRATION="1"
$env:PLAYWRIGHT_SKIP_WEBSERVER="1"
npx playwright test --project=integration-manual --workers=1
```

`global-teardown` вызовет cleanup, если не задан `E2E_SKIP_CLEANUP=1`.

## Отключение сценариев

| Переменная | Значение |
|------------|----------|
| `E2E_ALLOW_REGISTRATION=0` | пропустить TC-GEN-003 |
| `E2E_ALLOW_DESTRUCTIVE=0` | пропустить TC-SA-006, TC-PRV-002 |
| `E2E_SKIP_CLEANUP=1` | не удалять данные после прогона |

## Матрица покрытия

См. [playwright-coverage-matrix.md](playwright-coverage-matrix.md).
