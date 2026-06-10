# MyWay — документация

Отдельный репозиторий для материалов, которые можно открыть без доступа к коду продукта ([myway](https://github.com/tormoz70/myway)).

## Содержимое

| Каталог | Назначение |
|---------|------------|
| [`user-guides/`](user-guides/) | Руководства пользователя (RU), скриншоты UI |
| [`manual-testing/`](manual-testing/) | Тест-кейсы по ролям, E2E seed, каталог и матрица Playwright |

## Локальная разработка

Клонируйте рядом с основным репозиторием:

```text
C:\data\prjs\myway\          # приложение
C:\data\prjs\myway-docs\     # эта документация
```

Скриншоты для руководств снимаются из **myway** (нужны backend :8080 и Vite :5173):

```bash
cd myway/frontend
npm run capture:user-guide-screenshots
```

Файлы попадают в `myway-docs/user-guides/assets/`.

## Связь с кодом

- E2E и manual-спеки в `myway/frontend/e2e/` ссылаются на `manual-testing/test-cases-by-role.md` здесь.
- Excel-реестр кейсов (если используется) может жить в `myway/docs/qa/` — см. `myway/scripts/generate_manual_testcases_xlsx.py`.
