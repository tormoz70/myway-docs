# Тест-кейсы: мониторинг пилота (ops)

Профиль Docker Compose `observability`. UI Grafana/Prometheus/Alertmanager/GlitchTip
доступны только через SSH-туннель на loopback VM. Runbook:
`myway/deploy/pilot/OBSERVABILITY.md`. Локальный стенд: skill `run-observability-stack`.

Семейство `TC-OPS-*` — инфраструктура вне ролевой матрицы (см. `00-conventions.md` §3).
Прогонять `TC-OPS-MON-01` и `TC-OPS-MON-03` имеет смысл после фикса postgres-exporter
в `myway` (встроенная `pg_stat_activity_max_tx_duration`, без `--extend.query-path`).

---

### TC-OPS-MON-01 — [Доступ] Включение профиля observability
- **Предусловие:** в `~/.myway/compose.env` заданы `COMPOSE_PROFILES=observability`,
  `GRAFANA_ADMIN_PASSWORD`, `GLITCHTIP_SECRET_KEY`, `OBSERVABILITY_ALERT_EMAIL_TO`,
  `POSTGRES_EXPORTER_PASSWORD` (не заглушки). Роль `myway_exporter` создана
  (`deploy/yc/sync-db-exporter-role.sh`).
- **Шаги:**
  1. `docker compose --env-file ~/.myway/compose.env -f docker-compose.prod.yml --profile observability up -d`
  2. `bash scripts/smoke/observability-targets.sh`
- **Ожидаемый результат:** сервисы `prometheus`, `alertmanager`, `grafana`,
  `node-exporter`, `cadvisor`, `postgres-exporter`, `redis-exporter`, `blackbox-exporter`
  в состоянии running; preflight/glitchtip-db-init — `Exited (0)`.
- **Проверка:** `/api/v1/targets` — для каждого job есть хотя бы один active target
  со статусом `up`: `myway-backend`, `node`, `cadvisor`, `postgres`, `redis`,
  `blackbox-http`, `prometheus`, `alertmanager`, `grafana`. Отсутствующий job —
  провал (не «все из списка up»). В `/api/v1/rules` есть
  `BackendDown`, `DiskSpaceLow`, `HighLatencyP95`, `Watchdog`.

### TC-OPS-MON-02 — [Отображение] Доставка письма алерта
- **Предусловие:** профиль поднят, SMTP из `MAIL_*` рабочий (пилот) **или** локальный
  `aiosmtpd :2525` (dev-оверлей).
- **Шаги:** отправить синтетический алерт в Alertmanager (команда из runbook,
  `severity=critical`, заполнен `runbook_url`).
- **Ожидаемый результат:** письмо приходит в течение `group_wait` (30 с для critical).
  Тема содержит стенд (`env`) и имя алерта; в теле есть `runbook_url`.
- **Проверка:** `docker compose … logs alertmanager | grep -i notify`.

### TC-OPS-MON-03 — [Инцидент] Срабатывание PostgresDown
- **Предусловие:** профиль поднят, таргет `postgres` был `up`.
- **Шаги:** `docker compose … stop postgres` (или остановить только БД на локальном оверлее).
- **Ожидаемый результат:** через ~2 минуты firing `PostgresDown` (`severity=critical`).
  Производные `PostgresConnectionsHigh` / `DatabaseSizeNearCapacity` подавлены inhibit-правилом.
- **Проверка:** Prometheus `/alerts`, затем письмо. После `start postgres` алерт гаснет
  в течение минуты-двух (Prometheus перестаёт слать firing; `EndsAt` уже в payload).
  Приходит письмо `[RESOLVED]`. `resolve_timeout: 5m` относится только к синтетическим
  алертам без `EndsAt` (как в `TC-OPS-MON-02`), не к этому сценарию.

### TC-OPS-MON-04 — [Отображение] Поиск логов по traceId
- **Предусловие:** либо подпрофиль `observability-logs` (Loki/Promtail), либо `docker logs`
  backend (ECS JSON).
- **Шаги:**
  1. `curl -sS -D - -o /dev/null http://127.0.0.1:8080/api/public/organizations/by-slug/no-such-slug`
     (GET, не `curl -I` / HEAD: `permitAll` для `/api/public/**` привязан к GET,
     HEAD даст 401 до `GlobalExceptionHandler`). Запомнить `X-Trace-Id`.
     Ответ 404; handler пишет WARN с `traceId` в MDC. Per-request access-лога
     в проекте нет, поэтому в лог попадает только то, что прошло через
     `GlobalExceptionHandler` — `/livez` заголовок ставит, строки не пишет.
  2. Grafana → Explore → Loki, LogQL:
     `{container=~".+"} | json | traceId="<значение>"`
     (не дашборд `myway-logs` как единственный способ). Либо
     `docker logs backend | grep <traceId>`.
  3. Для тега в GlitchTip нужен 5xx (ERROR): например вызвать заведомый 500
     или найти событие с тем же `traceId`, если оно уже есть. 404 в GlitchTip не уходит.
- **Ожидаемый результат:** находятся строки того же запроса. Если проверяли 5xx —
  событие в GlitchTip несёт тот же тег `traceId`.
- **Проверка:** значение `traceId` совпадает с заголовком ответа.

### TC-OPS-MON-05 — [Валидация] Конфиги не едут сломанными
- **Шаги:** `bash scripts/observability/validate-configs.sh` из корня `myway`.
- **Ожидаемый результат:** `promtool check/test rules`, `amtool check-config`
  и схема дашбордов — код 0. `docker compose config` выполняется только при
  наличии Docker (иначе в логе `SKIP docker compose config`).
- **Негатив:** изменить порог в `alerts-*.yml`, не трогая `*_test.yml` →
  падает `promtool test rules` (гейт ловит расхождение правил и тестов), код 1.
