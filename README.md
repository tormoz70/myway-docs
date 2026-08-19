# MyWay — документация

Отдельный репозиторий для материалов без доступа к коду продукта ([myway](https://github.com/tormoz70/myway)).

## Содержимое

| Каталог | Назначение |
|---------|------------|
| [`user-guides/`](user-guides/) | Руководства пользователя (RU), скриншоты UI |
| [`qa/`](qa/) | Ручные кейсы по ролям, запуск E2E, покрытие Playwright, каталог use case |
| [`manual-testing/`](manual-testing/) | Прогон стенда по ролям (`manual-stand-role-scenarios.md`); остальное в `qa/` |

## Локальная разработка

```text
C:\data\prjs\myway\          # приложение
C:\data\prjs\myway-docs\     # эта документация
```

Скриншоты: из **myway** (`cd frontend && npm run capture:user-guide-screenshots`) → `user-guides/assets/`.

E2E: [qa/run.md](qa/run.md). Кейсы: [qa/cases/](qa/cases/). Покрытие: [qa/coverage.md](qa/coverage.md).
Прогон стенда: [manual-testing/manual-stand-role-scenarios.md](manual-testing/manual-stand-role-scenarios.md).
Use case'ы отрасли: [qa/use-cases/](qa/use-cases/).
