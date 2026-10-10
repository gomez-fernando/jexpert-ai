from pathlib import Path

import requests

from .auth import get_access_token
from .config import load_config
from .exceptions import AEPAPIError

BASE_URL = 'https://platform.adobe.io'


def aep_request(
    method: str,
    path: str,
    params: dict | None = None,
    json_body: dict | list | None = None,
    headers: dict[str, str] | None = None,
    credentials_path: str | Path | None = None,
    sandbox: str | None = None,
    timeout: int | None = None,
) -> requests.Response:
    """Authenticated request against an Adobe Experience Platform REST API.

    `path` is relative to https://platform.adobe.io (e.g. '/data/foundation/catalog/dataSets')
    or a full URL, used as is (e.g. a pagination link returned by the API).
    """
    config = load_config(credentials_path=credentials_path, sandbox=sandbox)
    token = get_access_token(config)
    request_headers = {
        'Authorization': f'Bearer {token}',
        'x-api-key': config.api_key,
        'x-gw-ims-org-id': config.org_id,
        'x-sandbox-name': config.sandbox_name,
        'Content-Type': 'application/json',
    }
    if headers:
        request_headers.update(headers)
    url = path if path.startswith('http') else f'{BASE_URL}{path}'

    response = None
    try:
        response = requests.request(
            method,
            url,
            params=params,
            json=json_body,
            headers=request_headers,
            timeout=timeout or config.http_timeout,
        )
        response.raise_for_status()
    except requests.HTTPError as exc:
        body = response.text if response is not None else ''
        raise AEPAPIError(f'AEP API request failed ({method} {url}): {exc}. Response body: {body}') from exc
    except requests.RequestException as exc:
        raise AEPAPIError(f'AEP API request failed ({method} {url}): {exc}') from exc
    return response


def aep_get(
    path: str,
    params: dict | None = None,
    headers: dict[str, str] | None = None,
    credentials_path: str | Path | None = None,
    sandbox: str | None = None,
    timeout: int | None = None,
) -> dict:
    response = aep_request(
        'GET',
        path,
        params=params,
        headers=headers,
        credentials_path=credentials_path,
        sandbox=sandbox,
        timeout=timeout,
    )
    return response.json()
