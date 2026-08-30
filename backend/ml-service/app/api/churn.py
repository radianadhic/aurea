"""Churn prediction API."""
from fastapi import APIRouter, HTTPException, Path
import structlog

from app.services.churn_predictor import ChurnPredictor

router = APIRouter()
logger = structlog.get_logger()
predictor = ChurnPredictor()


@router.get("/{customer_id}")
async def predict_churn(
    customer_id: str = Path(..., description="Customer CIF or UUID")
) -> dict:
    """Predict churn probability for a customer."""
    try:
        result = await predictor.predict_with_cache(customer_id, {})
        return result
    except Exception as e:
        logger.error("churn.prediction_failed", customer_id=customer_id, error=str(e))
        raise HTTPException(status_code=500, detail="Prediction failed")
