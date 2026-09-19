from fastapi import APIRouter
from backend.app.api.v1 import telemetry, incidents, copilot, containment

api_router = APIRouter()
api_router.include_router(telemetry.router, prefix="/telemetry", tags=["telemetry"])
api_router.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["copilot"])
api_router.include_router(containment.router, prefix="/containment", tags=["containment"])
