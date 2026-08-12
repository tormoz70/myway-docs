# QA и E2E (MyWay)

Канон ручных кейсов, запуска Playwright и покрытия. Руководства пользователя — в [`user-guides/`](../user-guides/).

| Файл | Назначение |
|------|------------|
| [run.md](run.md) | Как поднять стенд, SMTP, seed, smoke vs integration |
| [coverage.md](coverage.md) | Живые `*.spec.ts` ↔ ID кейса |
| [cases/](cases/) | Ручные тест-кейсы по ролям (`TC-OWNER-*`, `TC-ANON-*`, …) |

## Кейсы по ролям

| Файл | Роль |
|------|------|
| [00-conventions.md](cases/00-conventions.md) | Формат, CONV-*, стенд |
| [01-access-matrix.md](cases/01-access-matrix.md) | Роль × форма |
| [role-anonymous.md](cases/role-anonymous.md) | Гость |
| [role-super-admin.md](cases/role-super-admin.md) | SUPER_ADMIN (+ SMTP, eTracker) |
| [role-super-user.md](cases/role-super-user.md) | SUPER_USER |
| [role-owner.md](cases/role-owner.md) | OWNER |
| [role-admin.md](cases/role-admin.md) | ADMIN |
| [role-cleaner.md](cases/role-cleaner.md) | CLEANER |
| [role-sub-tenant.md](cases/role-sub-tenant.md) | SUB_TENANT |
| [role-instructor.md](cases/role-instructor.md) | INSTRUCTOR |
| [role-student.md](cases/role-student.md) | STUDENT |

Идентификаторы вида `TC-<РОЛЬ>-<ФОРМА>-NN`. Префикс URL — `/go`. Ярлыки `TC-OWN-*` / `TC-GEN-*` в именах Playwright-тестов — исторические; канон — колонка «Кейс» в [coverage.md](coverage.md).

Код спеков: `myway/frontend/e2e/`. Skill агента: `myway/.cursor/skills/run-e2e`.
