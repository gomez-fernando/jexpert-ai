from datetime import datetime, timedelta, timezone

import requests

from .config import AEPConfig
from .exceptions import AEPAuthError

_TOKEN_CACHE: dict[tuple[str, str], tuple[str, datetime]] = {}


def clear_token_cache() -> None:
    _TOKEN_CACHE.clear()


def get_access_token(config: AEPConfig) -> str:
    cache_key = (str(config.credentials_path), config.client_id)
    now = datetime.now(timezone.utc)
    cached_entry = _TOKEN_CACHE.get(cache_key)
    if cached_entry and now < cached_entry[1]:
        return cached_entry[0]

    try:
        response = requests.post(
            config.ims_token_url,
            data={
                'grant_type': 'client_credentials',
                'client_id': config.client_id,
                'client_secret': config.client_secret,
                'scope': config.scopes,
            },
            timeout=config.http_timeout,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise AEPAuthError(f'Could not retrieve Adobe IMS token: {exc}') from exc

    token = payload.get('access_token')
    if not token:
        raise AEPAuthError('Adobe IMS token response did not include access_token')

    expires_in = int(payload.get('expires_in', 86400))
    _TOKEN_CACHE[cache_key] = (token, now + timedelta(seconds=max(expires_in - 60, 60)))
    return token
