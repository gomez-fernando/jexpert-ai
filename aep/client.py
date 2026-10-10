from pathlib import Path

import psycopg2
import requests
from psycopg2.extensions import connection as _PgConnection

from .auth import get_access_token
from .config import load_config
from .exceptions import AEPConnectionError

QUERY_SERVICE_URL = 'https://platform.adobe.io/data/foundation/query'


def open_pg_connection(
    credentials_path: str | Path | None = None,
    sandbox: str | None = None,
    connect_timeout: int | None = None,
    query_timeout: int | None = None,
) -> _PgConnection:
    config = load_config(credentials_path=credentials_path, sandbox=sandbox)
    token = get_access_token(config)
    headers = {
        'Authorization': f'Bearer {token}',
        'x-api-key': config.api_key,
        'x-gw-ims-org-id': config.org_id,
        'x-sandbox-name': config.sandbox_name,
    }
    try:
        response = requests.get(f'{QUERY_SERVICE_URL}/connection_parameters', headers=headers, timeout=config.http_timeout)
        response.raise_for_status()
        params = response.json()
    except requests.RequestException as exc:
        raise AEPConnectionError(f'Could not fetch Query Service connection parameters: {exc}') from exc

    resolved_query_timeout = int(query_timeout or config.query_timeout)
    try:
        return psycopg2.connect(
            host=params['host'],
            port=params['port'],
            dbname=config.db_name,
            user=params['username'],
            password=token,
            sslmode='require',
            connect_timeout=int(connect_timeout or config.connect_timeout),
            options=f'-c statement_timeout={resolved_query_timeout * 1000}',
        )
    except psycopg2.Error as exc:
        raise AEPConnectionError(f'Could not open Query Service PostgreSQL connection: {exc}') from exc
