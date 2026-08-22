# Покрытие Playwright ↔ кейсы

Источник кейсов: [cases/](cases/). Спеки: `myway/frontend/e2e/`.
Запуск: [run.md](run.md).

**Контуры**

| Контур | Project | Как запускается |
|--------|---------|-----------------|
| **integration** | `integration` | `npm run test:e2e:integration` — seed → все `e2e/integration/**` → cleanup |
| **simulator** | `simulator` | `npm run test:e2e:simulator` — ручной стенд UC, без cleanup |
| **smoke** | `smoke` | `CI=true E2E_INTEGRATION=0 npm run test:e2e -- --project=smoke` — mock/статика, backend не нужен |

**Статус:** `automated` — сценарий доходит до проверки; `partial` — UI/API кусок или skip по условию; `manual` — только руками; `removed` — фичи нет.

Имена тестов в коде используют **канон** `TC-OWNER-*`, `TC-INSTRUCTOR-*` и т.д. из `cases/role-*.md`.

## Integration (`e2e/integration/`)

| Spec | Кейсы (канон) | Статус |
|------|---------------|--------|
| `role-anonymous.spec.ts` | TC-ANON-LOGIN-03, LOGIN-01, REG-01, VERIFY-05, JOIN-INS-01, JOIN-STU-01 | automated |
| `role-anonymous-privacy.spec.ts` | TC-ANON-PRIVACY-01, 04, 03 | automated (04 destructive) |
| `role-owner-nav.spec.ts` | меню OWNER (layout) | automated |
| `role-owner-settings.spec.ts` | TC-OWNER-SET-ORG-01, SET-PUB-01, SET-ORG, USERS-02 | automated / partial |
| `role-owner-schedule.spec.ts` | TC-OWNER-SUBJ-02, PREM-02+HALL-01, SCHED-02, SCHED-01, SCHED-08 | automated |
| `role-owner-premises.spec.ts` | TC-OWNER-PREM-02, HALL-01 | automated |
| `role-owner-entity-content.spec.ts` | TC-OWNER-SUBJ-03A, TC-ANON-TEACHERS-01, PREM-02A | automated / partial |
| `role-owner-operations.spec.ts` | TC-OWNER-JOIN-02, ACCESS-01/02/08, BILL-01, FIN-TURN-05, FIN-CAT, SUB-02, EXPORT-01, NEWS-02, ADMWORK-02, ME-04, FEEDBACK-01 | automated / partial |
| `role-owner-passage.spec.ts` | TC-OWNER-ACCESS-06 | automated |
| `role-owner-finance.spec.ts` | income subroutes UI | automated |
| `role-admin.spec.ts` | TC-ADMIN-FIN-FLAG-01, 03 | automated (serial) |
| `role-instructor.spec.ts` | TC-INSTRUCTOR-SCHED-01…03, ACCESS-01, ME-02, SUBJ-01 | automated (serial) |
| `role-student.spec.ts` | TC-STUDENT-RO-02, ACCESS-01, ME-02 (своё занятие недели), RO-06 | automated |
| `role-sub-tenant.spec.ts` | TC-SUBTENANT-SUB-02, RO-02, RO-05, ME-01 | automated / partial |
| `role-cleaner.spec.ts` | TC-CLEANER-NAV-01/02, DASH-01, ACCESS-01 | automated |
| `role-super-admin-platform.spec.ts` | TC-SUPERADMIN-DASH-01…05, TENANTS-01, FB-01, ACCESS-01, FEEDBACK-01 | automated (006 destructive) |
| `role-super-admin-plans.spec.ts` | TC-SUPERADMIN-PLANS-01…07 | automated |
| `role-super-admin-subscriptions.spec.ts` | TC-SUPERADMIN-SUBS-02, 03 | automated |
| `role-super-admin-etracker.spec.ts` | TC-SUPERADMIN-ETR-01, 02 | automated |
| `role-super-user.spec.ts` | TC-SUPERUSER-OPS-01…03 | automated |
| `entity-content.api.spec.ts` | TC-OWNER-SUBJ-03A/03B, TC-ANON-TEACHERS-01 | automated |
| `staff-invite.api.spec.ts` | TC-OWNER-USERS-02A/02B/02C | partial (SMTP) |
| `premise-hall.api.spec.ts` | TC-OWNER-HALL-05…08, PREM-04/05, ACCESS-01 | automated |
| `schedule-entry-overnight.api.spec.ts` | overnight RENT | automated |
| `chats/support-chat.spec.ts` | TC-OWNER-FEEDBACK / platform feedback | automated |
| `chats/tenant-chat.spec.ts` | tenant ↔ platform chat | automated |
| `chats/platform-chat.spec.ts` | platform operator chat | automated |
| `stage2-gap.spec.ts` | TC-ADMIN-MAKEUP-01, TC-OWNER-FUNNEL-01 (+ FUNNEL-03), TC-ADMIN-SUB-01, TC-INSTRUCTOR-SUB-01, TC-STUDENT-FAMILY-01, TC-OWNER-FAMILY-02 | automated / partial |
| `capture-user-guide-screenshots.spec.ts` | не кейс: съёмка PNG для `user-guides/assets` | tool |

## Simulator (`e2e/simulator/`)

Ручной стенд, UC-каталог. Запуск и фикстуры: [use-cases/simulator.md](use-cases/simulator.md).

Условных skip внутри тестов нет: незасеянная фикстура — падение с командой досева, а не пропуск.
Единственный skip — «запущено без `E2E_SIMULATOR=1`».

| Spec | UC | Статус |
|------|-----|--------|
| `uc-owner-admin.spec.ts` | UC-OWNER-01, UC-FRONTDESK-09, UC-SALES-02, UC-OWNER-04 | automated |
| `uc-frontdesk.spec.ts` | UC-FRONTDESK-03…06, 11, 12 | automated |
| `uc-teacher-student.spec.ts` | UC-TEACHER-01…03, UC-CLIENT-01/02/04, UC-PARENT-02 | automated |
| `uc-renter.spec.ts` | UC-RENTER-01/02/05 | automated (serial) |
| `uc-isolation.spec.ts` | tenant isolation flow-street ↔ ritm-hall | automated |

Пересечение с integration (`UC-SALES-02` / `TC-OWNER-FUNNEL-01`, `UC-FRONTDESK-06` /
`TC-ADMIN-MAKEUP-01`, `UC-PARENT-02` / `TC-STUDENT-FAMILY-01`) **оставлено**: контуры гоняются на
разных данных (стенд против `e2e-seed` с cleanup) и в разных прогонах — симулятор не входит в
обычный прогон, поэтому удаление integration-проверок сократило бы то, что гоняется всегда.
Совпадение сведено к теме, а не к тексту проверки: обе стороны опираются на свои данные, а не на
наличие раздела. Подробнее: [use-cases/simulator.md](use-cases/simulator.md).

## Smoke (`e2e/smoke/`)

| Spec | Что проверяет | Статус |
|------|---------------|--------|
| `login.smoke.spec.ts` | форма входа, 401/500 тексты | automated |
| `landing.smoke.spec.ts` | лендинг | automated |
| `legal-links.smoke.spec.ts` | ссылки legal под `/go` | automated |
| `build-info.smoke.spec.ts` | `/api/public/build-info`, футер | automated |
| `public-routes.smoke.spec.ts` | публичные страницы | skip без slug |
| `seo.smoke.spec.ts` | OG/canonical | skip без seed |
| `finance-manage.smoke.spec.ts` | редирект на login (categories/expenses) | automated |
| `finance-pages.smoke.spec.ts` | shell finance | automated |
| `finance-turnover.spec.ts` | mock таблицы оборота | automated |
| `access-pass-payment.spec.ts` | mock оплата/refund | automated |
| `etracker.smoke.spec.ts` | mock списка/карточки | automated |

## Вне оркестратора

| Spec | Комментарий |
|------|-------------|
| `e2e/capture-user-guide-screenshots.spec.ts` | отдельный `playwright.user-guide.config.ts`, не регресс |

## Нет E2E / только руки

| Кейс | Комментарий |
|------|-------------|
| TC-CLEANER-SCAN-*, REQ-* | QR-станция / заявки — partial или manual |
| TC-SUPERADMIN-BC-SMTP-01 | реальный SMTP, пилот |
| TC-OWNER-USERS-02 первый вход + смена пароля | UI manual |
| TC-OWNER-FIN-CAT-02 / EXP-02 сохранение | FIN-CAT только модалки |
| PassAllocation, utility rebill, tickets как оборот | нет |
| RLS / чужой tenant | CONV-TENANT-ISOLATION, нет спека |

## Удалено (не описывать и не чинить)

| Было | Почему |
|------|--------|
| `finance-tariff-charges.spec.ts`, TC-OWNER-FIN-TURN-016, `recalcTariffCharges` | V63, поурочные тарифы сняты |
| `catalog.spec.ts` + `generated/qa-catalog.json` + xlsx | мёртвый контур |
| `e2e/manual/` + project `integration-manual` | заменено на `e2e/integration/` + project `integration` |
| TC-INSTRUCTOR-SUBJ-02 (тарифы) | V63 |

## Исторические ярлыки в коде (до рефакторинга 2026-08)

Раньше в `test('…')` использовались `TC-OWN-*`, `TC-INS-*`, `TC-GEN-*`, `TC-SA-*` и т.д. Канон — колонка «Кейс» в таблицах выше и файлы `cases/role-*.md`.
