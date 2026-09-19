from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.v1 import api_router
from backend.app.models.domain import Base
from backend.app.db.session import engine

try:
    from google.genai._api_client import BaseApiClient
    async def _safe_aclose(self):
        if hasattr(self, '_async_httpx_client') and self._async_httpx_client is not None:
            await self._async_httpx_client.aclose()
    BaseApiClient.aclose = _safe_aclose
except Exception:
    pass

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Atheus",
    description="AI-Powered Autonomous Cybersecurity & Incident Investigation Platform",
    version="1.0.0",
)

@app.middleware("http")
async def options_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)
    return await call_next(request)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
