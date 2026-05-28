"""Tests for the `l3_savepoints_and_advisory` homework scaffold.

Юнит-тесты не требуют БД и проходят из коробки. Интеграционный тест
помечен skipif и включается через PG_INTEGRATION=1 (нужен docker compose up -d).
"""

import os

import pytest

import main


def test_database_url_default(monkeypatch):
    """database_url() возвращает postgresql:// DSN по умолчанию."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert main.database_url().startswith("postgresql://")


def test_database_url_env_override(monkeypatch):
    """env DATABASE_URL перекрывает дефолт."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@h:5432/db")
    assert main.database_url() == "postgresql://u:p@h:5432/db"


@pytest.mark.skipif(
    os.environ.get("PG_INTEGRATION") != "1",
    reason="set PG_INTEGRATION=1 and run `docker compose up -d` to enable",
)
def test_integration():
    """Интеграция: подключиться к реальному PostgreSQL и проверить логику урока «Savepoints, advisory locks, deadlocks»."""
    with main.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            assert cur.fetchone()[0] == 1
    # TODO: вызови свои реализованные функции и проверь поведение урока.
