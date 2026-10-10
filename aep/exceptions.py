class AEPError(Exception):
    """Base error for the AEP helpers."""


class AEPConfigError(AEPError):
    """Raised when the credentials file is missing or incomplete."""


class AEPAuthError(AEPError):
    """Raised when OAuth token retrieval fails."""


class AEPConnectionError(AEPError):
    """Raised when the Query Service connection cannot be established."""


class AEPQueryError(AEPError):
    """Raised when SQL execution fails."""


class AEPAPIError(AEPError):
    """Raised when an AEP REST API request fails or returns a non-2xx response."""
