        # postgresql — Savepoints, advisory locks, deadlocks

        Homework-шаблон для урока **l3_savepoints_and_advisory** (Savepoints, advisory locks, deadlocks) на платформе Vibe Learn.

        ## Что делать

        Дано: testcontainers PG + спека CSV-импортёра. Реализуй:
1) Worker pool с SELECT ... FOR UPDATE SKIP LOCKED для разбора заданий.
2) Per-tenant координация через pg_try_advisory_xact_lock.
3) Импорт CSV с savepoint per row — невалидные строки попадают в import_errors,
   валидные коммитятся.
4) Heartbeat для long-running tasks: если worker не обновлял heartbeat > 60s,
   другой worker может перехватить.
Тесты в template запустят 4 worker-а параллельно с CSV содержащим валидные и
невалидные строки + проверят, что нет race conditions.

## Контекст (из transfer-задачи урока)

Тебе на ревью кладут архитектуру системы импорта данных из CSV в PG. Спека:

- **Один импорт = один CSV** с 10k-1M строк, каждая строка должна провалидироваться и
  записаться в `import_rows`. Невалидные строки сохраняются в `import_errors`.
- **Несколько worker-ов** обрабатывают пул заданий из `import_jobs`. Каждое задание
  должен взять только один worker.
- **При ошибке в строке** не должна откатываться вся пачка из 1М — только проблемная.
- **Иногда два разных импорта** могут пытаться писать в один и тот же tenant — нужна
  коррдинация (только один импорт на tenant в один момент времени).
- **Если worker зависнет** (OOM, kill -9), его задание должно стать доступным другим.

## Recap из урока

- **SAVEPOINT — частичный rollback внутри транзакции.** Без него одна ошибка убивает всю транзакцию. С ним — откатываешь только проблемный шаг.
- **Advisory locks — app-level именованные блокировки**, не связаны со строками. Идеальны для distributed cron, singleton-jobs, координации между подами.
- **pg_advisory_xact_lock безопаснее**, чем pg_advisory_lock — отпускается автоматически на COMMIT/ROLLBACK, не утечёт при crash.
- **Deadlock = взаимное ожидание; PG детектит и роняет одну из транзакций (40P01).** Профилактика: детерминированный порядок локов + retry-loop.
- **Lock monitoring**: `pg_stat_activity.wait_event_type` + `pg_blocking_pids(pid)` = диагностика 'кто кого блокирует' в инциденте.

        ## Как работать

        1. Платформа Vibe Learn создаёт копию этого репо в твоём GitHub-аккаунте по клику «Начать домашку» на странице урока (через GitHub `/generate`, codecrafters-pattern).
        2. Склонируй копию локально, реализуй TODO в `main.py`, прогони тесты, запушь.
        3. CI (`.github/workflows/ci.yml`) ставит зависимости и запускает `pytest` на каждый push. Платформа слушает результат через webhook от GitHub Actions и обновляет статус домашки на странице урока.

        ## Локальное окружение

        - Python 3.12+
        - Docker + docker-compose — `docker compose up -d` поднимает single-node PostgreSQL 16 на `localhost:5432` с healthcheck. DSN: `postgresql://postgres:postgres@localhost:5432/postgres`. Переопределяется через env `DATABASE_URL`.

        ## Запуск

        ```bash
        # Поднять локальный PostgreSQL
        docker compose up -d

        # Установить зависимости
        pip install -r requirements.txt

        # Прогнать тесты (интеграционный включается через PG_INTEGRATION=1)
        pytest
        PG_INTEGRATION=1 pytest

        # Запустить main (печатает marker; замени stub на реализацию)
        python main.py
        ```

        ## Заметка автора

        Это baseline-шаблон, сгенерированный платформой. Бизнес-сущность задачи (что конкретно реализовать в `main.py`, какие тесты сделать строгими) расширяется по ходу итераций — параллельно с углублением теории урока.
