from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

API_KEY_NAME = "X-API-Key"

API_KEY = "mathapikey47"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def require_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
            headers={"WWW-Authenticate": "API Key"},
        )

    return api_key
