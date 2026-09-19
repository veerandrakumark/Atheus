from fastapi import Security, HTTPException, status, Request
from fastapi.security.api_key import APIKeyHeader
from backend.app.core.config import settings

api_key_header = APIKeyHeader(name="X-Atheus-Key", auto_error=False)

async def get_api_key(request: Request, api_key_header: str = Security(api_key_header)) -> str:
    """Validate the API key from the header. Allows bypass in development if key is unset."""
    if request.method == "OPTIONS":
        return "options_bypass"
    if settings.ENVIRONMENT == "development" and not settings.ATHEUS_API_KEY:
        import logging
        logging.warning("Dev mode: ATHEUS_API_KEY not set. Permitting request without authentication.")
        return "development_bypass"
    
    if api_key_header and api_key_header == settings.ATHEUS_API_KEY:
        return api_key_header
        
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
    )
