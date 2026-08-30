"""Anomaly detection API."""
from fastapi import APIRouter, Path
from app.core.cache import cache_manager

router = APIRouter()


@router.get("/{customer_id}")
async def detect_anomaly(customer_id: str) -> dict:
    """Detect anomalies in customer behavior."""
    cache_key = f"ml:anomaly:{customer_id}"
    cached = await cache_manager.get(cache_key)
    if cached:
        return cached

    # Mock anomaly detection
    return {
        "customer_id": customer_id,
        "anomaly_score": 0.15,
        "is_anomaly": False,
        "anomalies": [],
        "model_version": "1.0",
        "analyzed_at": "2026-01-26T10:00:00Z",
    }
