# Покрытие Playwright ↔ кейсы

Источник кейсов: [cases/](cases/). Спеки: `myway/frontend/e2e/`.
Запуск: [run.md](run.md).

**Контуры**

| Контур | Как запускается |
|--------|-----------------|
| integration-manual | `npm run test:e2e:integration` (`e2e/manual/`) |
| chromium + seed | тот же seed, но **не** в оркестраторе — отдельный `npx playwright test … --project=chromium` |
| smoke | `test:e2e` с `E2E_INTEGRATION=0`, mock/статика, backend не нужен |

**Статус:** `automated` — сценарий доходит до проверки; `partial` — UI/API кусок или skip по условию; `manual` — только руками; `removed` — фичи нет.

Имена тестов `TC-OWN-*` / `TC-GEN-*` / `TC-SA-*` в коде — ярлыки. Канон — колонка **Кейс**.

## Integration-manual (`e2e/manual/`)

| Кейс | Spec | Тест (ярлык в коде) | Статус |
|------|------|---------------------|--------|
| TC-ANON-LOGIN-03 | `manual/auth-from-manual.spec.ts` | TC-GEN-001 | automated |
| TC-ANON-LOGIN-01 | `manual/auth-from-manual.spec.ts` | TC-GEN-002 | automated |
| TC-ANON-REG-01 | `manual/auth-from-manual.spec.ts` | TC-GEN-003 | automated (`E2E_ALLOW_REGISTRATION`) |
| TC-ANON-VERIFY-05 | `manual/auth-from-manual.spec.ts` | TC-GEN-003A | partial (skip если guard выключен / email уже verified) |
| TC-ANON-JOIN-INS-01 | `manual/auth-from-manual.spec.ts` | TC-GEN-004 | automated |
| TC-ANON-JOIN-STU-01 | `manual/auth-from-manual.spec.ts` | TC-GEN-005 | automated (нужен seed-предмет) |
| — | `manual/layout-menu-from-guide.spec.ts` | OWNER меню гл.01 | automated |
| TC-SUPERADMIN-TENANTS-01 | `manual/platform-from-manual.spec.ts` | TC-SA-001…008 | automated (006 destructive) |
| TC-SUPERADMIN-PLANS-* | `manual/platform-plans-from-manual.spec.ts` | TC-SA-009…021 | automated; 019 skip без ARCHIVED |
| TC-SUPERADMIN-SUBS-* | `manual/platform-org-subscriptions-from-manual.spec.ts` | TC-SA-020, 023, 024 | automated |
| TC-OWNER-SET-ORG-01 | `manual/owner-settings.spec.ts` | TC-OWN-001 | automated |
| TC-OWNER-SET-PUB-01 | `manual/owner-settings.spec.ts` | TC-OWN-002 | automated |
| TC-OWNER-SET-ORG (finance flag) | `manual/owner-settings.spec.ts` | TC-OWN-003 | automated |
| TC-OWNER-USERS-02 | `manual/owner-settings.spec.ts` | TC-OWN-004 | partial (UI invite, без письма) |
| TC-OWNER-USERS-02 | `manual/owner-settings.spec.ts` | TC-OWN-005 | partial (smoke instructor) |
| TC-OWNER-SUBJ-02 / 04 | `manual/owner-schedule-from-manual.spec.ts` | TC-OWN-007 | automated |
| TC-OWNER-PREM-02 + HALL-01 | `manual/owner-schedule-from-manual.spec.ts` | TC-OWN-008 | automated |
| TC-OWNER-SCHED-02 / 06 | `manual/owner-schedule-from-manual.spec.ts` | TC-OWN-009 | automated |
| TC-OWNER-SCHED-01 | `manual/owner-schedule-from-manual.spec.ts` | TC-OWN-009b | automated (вечерний слот) |
| TC-OWNER-SCHED-08 | `manual/owner-schedule-from-manual.spec.ts` | TC-OWN-010 | automated |
| TC-OWNER-PREM-02 | `manual/premise-hall-manual.spec.ts` | UI создание помещения | automated |
| TC-OWNER-HALL-01 | `manual/premise-hall-manual.spec.ts` | UI создание зала | automated |
| TC-OWNER-SUBJ-03A | `manual/entity-content-manual.spec.ts` | HTML предмета | automated |
| TC-ANON-TEACHERS-01 | `manual/entity-content-manual.spec.ts` | публичное био | automated |
| TC-OWNER-PREM-02A | `manual/entity-content-manual.spec.ts` | HTML помещения smoke | partial |
| TC-OWNER-JOIN-02 / 03 | `manual/owner-operations.spec.ts` | TC-OWN-006 | automated |
| TC-OWNER-ACCESS-01 / 02 | `manual/owner-operations.spec.ts` | TC-OWN-011 | automated |
| TC-OWNER-ACCESS-08 | `manual/owner-operations.spec.ts` | TC-OWN-012 | automated |
| TC-OWNER-BILL-01…03 | `manual/owner-operations.spec.ts` | TC-OWN-013 | automated |
| TC-OWNER-FIN-TURN-05 | `manual/owner-operations.spec.ts` | TC-OWN-014 | automated |
| TC-OWNER-FIN-CAT / EXP | `manual/owner-operations.spec.ts` | TC-OWN-015 | partial (модалки, без сохранения) |
| TC-OWNER-SUB-02 | `manual/owner-operations.spec.ts` | TC-OWN-017 | partial (skip без слота / SUB_TENANT) |
| TC-OWNER-EXPORT-01 | `manual/owner-operations.spec.ts` | TC-OWN-018 | automated |
| TC-OWNER-NEWS-02 | `manual/owner-operations.spec.ts` | TC-OWN-019 | automated |
| TC-OWNER-ADMWORK-02 | `manual/owner-operations.spec.ts` | TC-OWN-020 | automated |
| TC-OWNER-ME-04 | `manual/owner-operations.spec.ts` | TC-OWN-021 | automated |
| TC-OWNER-FEEDBACK-01 | `manual/owner-operations.spec.ts` | TC-OWN-022 | automated |
| TC-ADMIN finance flag | `manual/admin.spec.ts` | TC-ADM-001 / 002 | automated (serial) |
| TC-INSTRUCTOR-SCHED | `manual/instructor.spec.ts` | TC-INS-001…003, 005, 006 | automated; 002/003 зависят от 001 |
| TC-INSTRUCTOR-SUBJ-02 | `manual/instructor.spec.ts` | TC-INS-004 | **removed/stale** (тарифы V63) |
| TC-STUDENT-* | `manual/student.spec.ts` | TC-STU-001…005 | automated; 002 skip без слота |
| TC-SUBTENANT-SUB-02 | `manual/sub-tenant.spec.ts` | TC-SUB-001 | partial (слот) |
| TC-SUBTENANT-RO-02 | `manual/sub-tenant.spec.ts` | TC-SUB-002 | automated |
| TC-SUBTENANT export | `manual/sub-tenant.spec.ts` | TC-SUB-003 | automated |
| TC-SUBTENANT ME | `manual/sub-tenant.spec.ts` | TC-SUB-004 | automated |
| TC-ANON-PRIVACY-01 | `manual/privacy.spec.ts` | TC-PRV-001 | automated |
| TC-ANON-PRIVACY-04 | `manual/privacy.spec.ts` | TC-PRV-002 | automated (destructive) |
| TC-ANON-PRIVACY-03 | `manual/privacy.spec.ts` | TC-PRV-003 | automated |
| TC-OWNER-ACCESS-06 | `manual/passage-navigation.spec.ts` | Проходная / регистрация входа | automated |
| TC-OWNER-FIN / SUB UI | `manual/finance-income-subroutes.spec.ts` | income subroutes | automated |
| TC-SUPERADMIN-ETR-01 / 02 | `manual/etracker.spec.ts` | issue + like/subscribe | automated (SUPER_ADMIN) |

## Chromium + seed (не в оркестраторе)

Нужны `E2E_INTEGRATION=1` и `.env.e2e`. Команды — в [run.md](run.md).

| Кейс | Spec | Статус |
|------|------|--------|
| TC-OWNER-SUBJ-03A / 03B, TC-ANON-TEACHERS-01 | `entity-content.spec.ts` | automated (**оркестратор запускает**) |
| TC-OWNER-HALL-05…08, PREM-04/05, ACCESS-01 | `premise-hall.spec.ts` | automated (API) |
| TC-OWNER-SCHED overnight RENT | `schedule-entry-overnight.spec.ts` | automated |
| TC-OWNER-USERS-02 / 02A / 02B | `staff-invite.spec.ts` | partial API; skip при SMTP 502 |
| TC-OWNER-FEEDBACK / platform chats | `support-chat.spec.ts`, `tenant-chat.spec.ts`, `platform-chat.spec.ts` | automated |
| — | `capture-user-guide-screenshots.spec.ts` | отдельный конфиг, не E2E-регресс |

## Smoke (без backend)

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
| `finance-turnover.spec.ts` | mock таблицы оборота | known fail (strict «Абонементы») |
| `access-pass-payment.spec.ts` | mock оплата/refund | automated |
| `etracker.smoke.spec.ts` | mock списка/карточки | automated |

## Нет E2E / только руки

| Кейс | Комментарий |
|------|-------------|
| TC-CLEANER-* | нет спека |
| TC-SUPERUSER-* | нет спека (только SUPER_ADMIN) |
| TC-SUPERADMIN-BC-SMTP-01 | реальный SMTP, пилот |
| TC-OWNER-USERS-02 первый вход + смена пароля | UI manual |
| TC-OWNER-FIN-CAT-02 / EXP-02 сохранение | 015 только модалки |
| PassAllocation, utility rebill, tickets как оборот | нет |
| RLS / чужой tenant | CONV-TENANT-ISOLATION, нет спека |

## Удалено (не описывать и не чинить)

| Было | Почему |
|------|--------|
| `finance-tariff-charges.spec.ts`, TC-OWN-016, `recalcTariffCharges` | V63, поурочные тарифы сняты |
| `catalog.spec.ts` + `generated/qa-catalog.json` + xlsx | мёртвый контур |
| Selenium `backend/e2e-selenium` | уже удалён |

## Бывший ярлык → канон (фрагмент)

| Ярлык в spec | Канон |
|--------------|--------|
| TC-GEN-001…005 | TC-ANON-LOGIN / REG / JOIN |
| TC-OWN-001 / 002 | TC-OWNER-SET-ORG-01 / SET-PUB-01 |
| TC-OWN-004 / 004B / 004C | TC-OWNER-USERS-02 / 02A / 02B |
| TC-OWN-007 | TC-OWNER-SUBJ-02 |
| TC-OWN-011 | TC-OWNER-ACCESS-01 / 02 |
| TC-OWN-014 | TC-OWNER-FIN-TURN-05 |
| TC-OWN-016 | **removed** |
| TC-SA-001…008 | TC-SUPERADMIN-* |
| TC-SA-025 | TC-SUPERADMIN-BC-SMTP-01 |
| TC-ETR-001…003 | TC-SUPERADMIN-ETR-01…03 |
| TC-INS-004 | **removed** (V63) |
