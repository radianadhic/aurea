"""Health check endpoints."""
from fastapi import APIRouter
from app.core.cache import cache_manager
import structlog

router = APIRouter()
logger = structlog.get_logger()


@router.get("/health")
async def health() -> dict:
    """Liveness probe."""
    return {"status": "UP", "service": "ml-service", "version": "1.0.0"}


@router.get("/ready")
async def readiness() -> dict:
    """Readiness probe - check all dependencies."""
    checks = {
        "cache": "UP" if cache_manager._client else "DOWN",
    }
    all_up = all(v == "UP" for v in checks.values())
    return {
        "status": "UP" if all_up else "DEGRADED",
        "checks": checks,
    }
