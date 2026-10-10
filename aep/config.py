import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .exceptions import AEPConfigError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_GLOB = '*.postman_environment.json'
DEFAULT_IMS_HOST = 'ims-na1.adobelogin.com'
DEFAULT_SCOPES = 'openid,AdobeID,read_organizations,additional_info.projectedProductContext'


@dataclass(frozen=True)
class AEPConfig:
    credentials_path: Path
    client_id: str
    client_secret: str
    api_key: str
    org_id: str
    sandbox_name: str
    db_name: str
    scopes: str
    ims_token_url: str
    http_timeout: int = 60
    connect_timeout: int = 30
    query_timeout: int = 300


def _find_credentials_file() -> Path:
    candidates = sorted(PROJECT_ROOT.glob(CREDENTIALS_GLOB))
    if not candidates:
        raise AEPConfigError(
            f'No credentials file found. Put the Postman environment exported from the '
            f'Adobe Developer Console ({CREDENTIALS_GLOB}) in {PROJECT_ROOT}, '
            'or pass credentials_path.'
        )
    if len(candidates) > 1:
        names = ', '.join(path.name for path in candidates)
        raise AEPConfigError(f'More than one credentials file in {PROJECT_ROOT} ({names}). Pass credentials_path.')
    return candidates[0]


def _resolve_credentials_path(credentials_path: str | Path | None) -> Path:
    if not credentials_path:
        return _find_credentials_file()
    path = Path(credentials_path)
    path = path if path.is_absolute() else (PROJECT_ROOT / path)
    if not path.exists():
        raise AEPConfigError(f'Credentials file not found: {path}')
    return path


def _load_postman_values(path: Path) -> dict[str, Any]:
    try:
        doc = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        raise AEPConfigError(f'Invalid JSON in {path}: {exc}') from exc
    values = doc.get('values')
    if not isinstance(values, list):
        raise AEPConfigError(f'{path} is not a Postman environment export (missing "values").')
    return {item['key']: item.get('value') for item in values if item.get('enabled', True) and item.get('key')}


def _normalize_scopes(raw_scopes: Any) -> str:
    # Postman can store SCOPES as a JSON list or as a string. IMS v3 expects them comma separated:
    # sent as a repeated form field it only grants the first one, and Platform then answers 403027.
    if not raw_scopes:
        return DEFAULT_SCOPES
    if isinstance(raw_scopes, list):
        return ','.join(str(scope).strip() for scope in raw_scopes if str(scope).strip())
    return ','.join(str(raw_scopes).replace(',', ' ').split())


def load_config(credentials_path: str | Path | None = None, sandbox: str | None = None) -> AEPConfig:
    path = _resolve_credentials_path(credentials_path)
    values = _load_postman_values(path)

    client_id = values.get('CLIENT_ID') or values.get('API_KEY')
    client_secret = values.get('CLIENT_SECRET')
    org_id = values.get('IMS_ORG')
    sandbox_name = sandbox or values.get('SANDBOX_NAME')
    missing = [
        name
        for name, value in (
            ('CLIENT_ID', client_id),
            ('CLIENT_SECRET', client_secret),
            ('IMS_ORG', org_id),
            ('SANDBOX_NAME', sandbox_name),
        )
        if not value
    ]
    if missing:
        raise AEPConfigError(f'Missing values in {path}: {", ".join(missing)}')

    ims_host = values.get('IMS') or DEFAULT_IMS_HOST
    return AEPConfig(
        credentials_path=path,
        client_id=client_id,
        client_secret=client_secret,
        api_key=values.get('API_KEY') or client_id,
        org_id=org_id,
        sandbox_name=sandbox_name,
        db_name=f'{sandbox_name}:all',
        scopes=_normalize_scopes(values.get('SCOPES')),
        ims_token_url=f'https://{ims_host}/ims/token/v3',
    )
