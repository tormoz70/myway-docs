# Тест-кейсы: мониторинг пилота (ops)

Профиль Docker Compose `observability`. UI Grafana/Prometheus/Alertmanager/GlitchTip
доступны только через SSH-туннель на loopback VM. Runbook:
`myway/deploy/pilot/OBSERVABILITY.md`. Локальный стенд: skill `run-observability-stack`.

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
- **Проверка:** `/api/v1/targets` — все active targets `up`; в `/api/v1/rules` есть
  `BackendDown`, `DiskSpaceLow`, `HighLatencyP95`, `Watchdog`.

### TC-OPS-MON-02 — [Отображение] Доставка письма алерта
- **Предусловие:** профиль поднят, SMTP из `MAIL_*` рабочий (пилот) **или** локальный
  `aiosmtpd :2525` (dev-оверлей).
- **Шаги:** отправить синтетический алерт в Alertmanager (команда из runbook,
  `severity=critical`, заполнен `runbook_url`).
- **Ожидаемый результат:** письмо приходит в течение `group_wait` (30 с для critical).
  Тема содержит стенд (`env`) и имя алерта; в теле есть `runbook_url`.
- **Проверка:** `docker compose … logs alertmanager | grep -i notify`.

### TC-OPS-MON-03 — [Кнопка] Срабатывание PostgresDown
- **Предусловие:** профиль поднят, таргет `postgres` был `up`.
- **Шаги:** `docker compose … stop postgres` (или остановить только БД на локальном оверлее).
- **Ожидаемый результат:** через ~2 минуты firing `PostgresDown` (`severity=critical`).
  Производные `PostgresConnectionsHigh` / `DatabaseSizeNearCapacity` подавлены inhibit-правилом.
- **Проверка:** Prometheus `/alerts`, затем письмо. После `start postgres` алерт снимается
  (`resolve_timeout` 5 минут).

### TC-OPS-MON-04 — [Отображение] Поиск логов по traceId
- **Предусловие:** либо подпрофиль `observability-logs` (Loki/Promtail), либо `docker logs`
  backend (ECS JSON). Есть любой ответ API с заголовком `X-Trace-Id`.
- **Шаги:**
  1. `curl -sI http://127.0.0.1:8080/livez` (или публичный URL) — запомнить `X-Trace-Id`.
  2. В Grafana дашборд `myway-logs` (если Loki включён) отфильтровать по `traceId`,
     иначе `docker logs backend | grep <traceId>`.
- **Ожидаемый результат:** находятся строки того же запроса. В GlitchTip событие 5xx
  несёт тот же тег `traceId`.
- **Проверка:** значение `traceId` совпадает с заголовком ответа.

### TC-OPS-MON-05 — [Валидация] Конфиги не едут сломанными
- **Шаги:** `bash scripts/observability/validate-configs.sh` из корня `myway`.
- **Ожидаемый результат:** `promtool check/test rules`, `amtool check-config`,
  `docker compose config` и схема дашбордов — код 0.
- **Негатив:** намеренная опечатка в PromQL → скрипт завершается с кодом 1.
