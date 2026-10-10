import time
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

from .client import open_pg_connection
from .exceptions import AEPQueryError

try:
    import pandas as pd
except ImportError:  # pragma: no cover - optional dependency
    pd = None

SQLParams = Sequence[Any] | dict[str, Any] | None

_RETRYABLE_MARKERS = (
    'system error',
    'connection to server',
    'server closed the connection',
    'terminating connection',
    'could not connect',
    'connection reset',
    'timeout',
    'timed out',
    'temporarily unavailable',
    'too many requests',
    'bad gateway',
    'service unavailable',
    'gateway timeout',
)


def _is_retryable_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return any(marker in message for marker in _RETRYABLE_MARKERS)


def _run_with_retries(runner, retries: int, retry_delay: int):
    last_error: Exception | None = None
    for attempt in range(1, int(retries) + 1):
        try:
            return runner()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt >= int(retries) or not _is_retryable_error(exc):
                break
            time.sleep(int(retry_delay) * (2 ** (attempt - 1)))
    if isinstance(last_error, AEPQueryError):
        raise last_error
    raise AEPQueryError(str(last_error)) from last_error


def query_all(
    sql: str,
    sql_params: SQLParams = None,
    credentials_path: str | Path | None = None,
    sandbox: str | None = None,
    connect_timeout: int | None = None,
    query_timeout: int | None = None,
    retries: int = 3,
    retry_delay: int = 5,
) -> list[dict[str, Any]]:
    def runner() -> list[dict[str, Any]]:
        conn = None
        try:
            conn = open_pg_connection(
                credentials_path=credentials_path,
                sandbox=sandbox,
                connect_timeout=connect_timeout,
                query_timeout=query_timeout,
            )
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, sql_params)
                if cur.description is None:
                    conn.commit()
                    return []
                return [dict(row) for row in cur.fetchall()]
        except psycopg2.Error as exc:
            raise AEPQueryError(f'Database error: {exc}') from exc
        finally:
            if conn:
                conn.close()

    return _run_with_retries(runner, retries=retries, retry_delay=retry_delay)


def query_iter(
    sql: str,
    sql_params: SQLParams = None,
    credentials_path: str | Path | None = None,
    sandbox: str | None = None,
    fetch_size: int = 50000,
    connect_timeout: int | None = None,
    query_timeout: int | None = None,
) -> Iterator[dict[str, Any]]:
    conn = None
    try:
        conn = open_pg_connection(
            credentials_path=credentials_path,
            sandbox=sandbox,
            connect_timeout=connect_timeout,
            query_timeout=query_timeout,
        )
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.arraysize = int(fetch_size)
            cur.execute(sql, sql_params)
            while True:
                rows = cur.fetchmany(int(fetch_size))
                if not rows:
                    break
                for row in rows:
                    yield dict(row)
    except psycopg2.Error as exc:
        raise AEPQueryError(f'Database error: {exc}') from exc
    finally:
        if conn:
            conn.close()


def query_df(sql: str, sql_params: SQLParams = None, **kwargs):
    if pd is None:
        raise AEPQueryError('pandas is not installed. Run: python -m pip install -r requirements.txt')
    return pd.DataFrame(query_all(sql, sql_params=sql_params, **kwargs))


def execute(sql: str, sql_params: SQLParams = None, **kwargs) -> None:
    query_all(sql, sql_params=sql_params, **kwargs)


def scalar(sql: str, sql_params: SQLParams = None, **kwargs) -> Any:
    rows = query_all(sql, sql_params=sql_params, **kwargs)
    if not rows or not rows[0]:
        return None
    return next(iter(rows[0].values()))
