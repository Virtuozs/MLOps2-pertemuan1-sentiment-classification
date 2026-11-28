"""Static API key check on the `x-api-key` header."""

import secrets

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from api.core.config import Settings, get_settings

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def verify_api_key(
    key: str | None = Security(api_key_header),
    settings: Settings = Depends(get_settings),
) -> None:
    """Reject the request unless the header matches the configured key."""
    if not settings.api_key or key is None or not secrets.compare_digest(
        key.encode(), settings.api_key.encode()
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
