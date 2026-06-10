# Соответствие Playwright E2E и ручным тест-кейсам

Источник сценариев: [test-cases-by-role.md](test-cases-by-role.md) (синхронизирован с [user-guides/ru/](../user-guides/ru/)).  
Запуск: [e2e-seed.md](e2e-seed.md), [frontend/e2e/README.md](../../frontend/e2e/README.md).  
Подробное описание каждого теста: [e2e-tests-catalog.md](e2e-tests-catalog.md).

**Легенда:** `automated` — полный UI-сценарий; `partial` — упрощённая проверка; `skip-ci` — только локально с `E2E_INTEGRATION=1`.

| ID | Spec / тест | Статус |
|----|-------------|--------|
| TC-GEN-001 | `auth-from-manual.spec.ts` | automated |
| TC-GEN-002 | `auth-from-manual.spec.ts` | automated (меню OWNER по гл.01) |
| TC-GEN-003 | `auth-from-manual.spec.ts` | automated (по умолчанию при `E2E_INTEGRATION`) |
| TC-GEN-004 | `auth-from-manual.spec.ts` | automated |
| TC-GEN-005 | `auth-from-manual.spec.ts` | automated (нужен seed: предмет+тариф) |
| — | `layout-menu-from-guide.spec.ts` | automated (навигация гл.01) |
| TC-SA-001 | `platform-from-manual.spec.ts` | automated |
| TC-SA-002 | `platform-from-manual.spec.ts` | automated |
| TC-SA-003 | `platform-from-manual.spec.ts` | automated |
| TC-SA-004 | `platform-from-manual.spec.ts` | automated |
| TC-SA-005 | `platform-from-manual.spec.ts` | automated |
| TC-SA-006 | `platform-from-manual.spec.ts` | automated (по умолчанию, teardown unblock) |
| TC-SA-007 | `platform-from-manual.spec.ts` | automated |
| TC-SA-008 | `platform-from-manual.spec.ts` | automated |
| TC-SA-009 … TC-SA-021 | `platform-plans-from-manual.spec.ts` | automated (`E2E_INTEGRATION`, план DEVELOPER) |
| TC-SA-020, 023, 024 | `platform-org-subscriptions-from-manual.spec.ts` | automated |
| TC-OWN-001 | `owner-settings.spec.ts` | automated |
| TC-OWN-002 | `owner-settings.spec.ts` | automated |
| TC-OWN-003 | `owner-settings.spec.ts` | automated (UI switch или API PATCH) |
| TC-OWN-004 | `owner-settings.spec.ts` | partial (без почты) |
| TC-OWN-005 | `owner-settings.spec.ts` | automated |
| TC-OWN-006 | `owner-operations.spec.ts` | automated (одобрение + отклонение) |
| TC-OWN-007 | `owner-schedule-from-manual.spec.ts` | automated |
| TC-OWN-008 | `owner-schedule-from-manual.spec.ts` | automated |
| TC-OWN-009 | `owner-schedule-from-manual.spec.ts` | automated |
| TC-OWN-010 | `owner-schedule-from-manual.spec.ts` | automated |
| TC-OWN-011 | `owner-operations.spec.ts` | automated |
| TC-OWN-012 | `owner-operations.spec.ts` | automated |
| TC-OWN-013 | `owner-operations.spec.ts` | automated |
| TC-OWN-014 | `owner-operations.spec.ts` | automated |
| TC-OWN-015 | `owner-operations.spec.ts` | partial (модалки категории и расхода; POST расхода 500 на стенде) |
| TC-OWN-016 | `owner-operations.spec.ts` | automated |
| TC-OWN-017 | `owner-operations.spec.ts` | partial (skip если слоты заняты предыдущими тестами) |
| TC-OWN-018 | `owner-operations.spec.ts` | automated |
| TC-OWN-019 | `owner-operations.spec.ts` | automated |
| TC-OWN-020 | `owner-operations.spec.ts` | automated |
| TC-OWN-021 | `owner-operations.spec.ts` | automated |
| TC-OWN-022 | `owner-operations.spec.ts` | automated |
| TC-ADM-001 | `admin.spec.ts` | automated |
| TC-ADM-002 | `admin.spec.ts` | automated |
| TC-SUB-001 | `sub-tenant.spec.ts` | partial (skip если нет свободного слота после прогона) |
| TC-SUB-002 | `sub-tenant.spec.ts` | automated |
| TC-SUB-003 | `sub-tenant.spec.ts` | automated |
| TC-SUB-004 | `sub-tenant.spec.ts` | automated |
| TC-INS-001 | `instructor.spec.ts` | automated |
| TC-INS-002 | `instructor.spec.ts` | automated |
| TC-INS-003 | `instructor.spec.ts` | automated |
| TC-INS-004 | `instructor.spec.ts` | partial (если нет кнопки тарифа) |
| TC-INS-005 | `instructor.spec.ts` | automated |
| TC-INS-006 | `instructor.spec.ts` | automated |
| TC-STU-001 | `student.spec.ts` | automated |
| TC-STU-002 | `student.spec.ts` | partial (read-only посещаемость) |
| TC-STU-003 | `student.spec.ts` | automated |
| TC-STU-004 | `student.spec.ts` | automated |
| TC-STU-005 | `student.spec.ts` | automated |
| TC-PRV-001 | `privacy.spec.ts` | automated |
| TC-PRV-002 | `privacy.spec.ts` | automated (по умолчанию) |
| TC-PRV-003 | `privacy.spec.ts` | automated |

Смоки без полного backend: `frontend/e2e/*.smoke.spec.ts`, `catalog.spec.ts` (11 тестов).
