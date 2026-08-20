# Симулятор студии (UC Playwright)

Детерминированный «день студии» на **ручном стенде** (`ritm-hall` + контроль изоляции `flow-street`).  
Не смешивать с integration E2E (`e2e-seed`, cleanup).

## Предусловия

1. Dev stack: Postgres/Redis/MinIO, backend `:8080`, Vite `:5173` (skill `run-dev-stack` или `scripts/dev-local.ps1`).
2. Ручной стенд: `python scripts/qa/seed_manual_test_stand.py` (три студии, `generated/manual-test-stand.json`).
3. Фикстуры симулятора (только **ritm-hall**):

```powershell
python scripts/qa/manual_stand_simulator.py
# или
python scripts/qa/seed_manual_test_stand.py --simulator-fixtures-only
```

Досев идемпотентный: семья, воронка, waitlist, отработка, класс для замены.

## Запуск

```powershell
cd frontend
npm run test:e2e:simulator
```

Оркестратор: `scripts/qa/run_e2e_simulator.py` — preflight API, `E2E_SIMULATOR=1`, project `simulator`, **без** cleanup integration.

Опции:

```powershell
python scripts/qa/run_e2e_simulator.py --seed-simulator-fixtures
python scripts/qa/run_e2e_simulator.py --skip-playwright
```

Учётки и пароль — из `generated/manual-test-stand.json` (`ManualQa12!`), **не** `frontend/.env.e2e`.

## Спеки ↔ UC

| Spec | UC |
|------|-----|
| `e2e/simulator/uc-owner-admin.spec.ts` | UC-OWNER-01, UC-FRONTDESK-09, UC-SALES-02, UC-OWNER-04 |
| `e2e/simulator/uc-frontdesk.spec.ts` | UC-FRONTDESK-03…06, 11, 12 |
| `e2e/simulator/uc-teacher-student.spec.ts` | UC-TEACHER-01…03, UC-CLIENT-01/02/04, UC-PARENT-02 |
| `e2e/simulator/uc-renter.spec.ts` | UC-RENTER-01/02/05 |
| `e2e/simulator/uc-isolation.spec.ts` | изоляция tenant (flow-street ≠ ritm-hall) |

Не автоматизируются (gap «нет» / вне скоупа): FRONTDESK-01, FRONTDESK-07, TEACHER-06, RENTER-04.

## Soak (этап 3)

После зелёных UC-сценариев — отдельный API soak, не CI:

```powershell
python scripts/qa/soak_studio_simulator.py --duration 5
```

## Связанные документы

- Каталог UC: [catalog.md](./catalog.md)
- Gap: [myway-gap.md](./myway-gap.md)
- Запуск E2E: [../run.md](../run.md)
- Покрытие: [../coverage.md](../coverage.md)
