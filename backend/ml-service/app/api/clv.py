"""Customer Lifetime Value prediction API."""
from fastapi import APIRouter, Path
from app.core.cache import cache_manager

router = APIRouter()


@router.get("/{customer_id}")
async def predict_clv(customer_id: str) -> dict:
    """Predict Customer Lifetime Value."""
    return {
        "customer_id": customer_id,
        "clv_1y": 1_500_000,
        "clv_3y": 4_200_000,
        "clv_5y": 7_800_000,
        "currency": "IDR",
        "confidence": 0.78,
        "model_version": "1.0",
    }
