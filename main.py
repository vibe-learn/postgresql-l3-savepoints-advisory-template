"""Homework scaffold — postgresql lesson `l3_savepoints_and_advisory` (Vibe Learn).

Задача: worker pool с FOR UPDATE SKIP LOCKED, advisory locks per-tenant, savepoint per-row импорт.

Реализуй функции ниже — сигнатуры и тестовая поверхность фиксированы;
CI (.github/workflows/ci.yml) ставит зависимости и гоняет `pytest`.
Подробности и критерии приёмки — в README.md.

Драйвер: psycopg (v3). DSN берётся из env DATABASE_URL.
"""

import os

import psycopg


def database_url() -> str:
    """DSN PostgreSQL из env. Дефолт совпадает с docker-compose.yml."""
    return os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/postgres",
    )


def connect() -> "psycopg.Connection":
    """Открыть соединение psycopg из DATABASE_URL."""
    return psycopg.connect(database_url())


# ----- TODO #1: claim_job -----
def claim_job(conn) -> dict | None:
    """SELECT ... FOR UPDATE SKIP LOCKED LIMIT 1 — взять задание, не блокируясь на чужих"""
    raise NotImplementedError("claim_job: реализуй меня")


# ----- TODO #2: with_tenant_lock -----
def with_tenant_lock(conn, tenant_id: int) -> bool:
    """pg_try_advisory_xact_lock(tenant_id) — координация в рамках транзакции, вернуть успех"""
    raise NotImplementedError("with_tenant_lock: реализуй меня")


# ----- TODO #3: import_csv_rows -----
def import_csv_rows(conn, rows: list[dict]) -> tuple[int, int]:
    """импорт с SAVEPOINT на строку: валидные коммитятся, невалидные → import_errors; вернуть (ok, failed)"""
    raise NotImplementedError("import_csv_rows: реализуй меня")



def main() -> None:
    """Точка входа: подключиться и напомнить, что реализовать.

    Замени тело на демонстрацию реализованных функций.
    """
    print("Vibe Learn — postgresql lesson scaffold up")
    print(f"DATABASE_URL: {database_url()}")
    print("Реализуй TODO-функции, затем `pytest`. README.md содержит задачу.")


if __name__ == "__main__":
    main()
