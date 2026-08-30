"""Risk scoring API."""
from fastapi import APIRouter, HTTPException, Path
import structlog

from app.services.risk_predictor import RiskPredictor

router = APIRouter()
logger = structlog.get_logger()
predictor = RiskPredictor()


@router.get("/{customer_id}")
async def predict_risk(customer_id: str = Path(...)) -> dict:
    """Predict risk score for a customer."""
    try:
        return await predictor.predict_with_cache(customer_id, {})
    except Exception as e:
        logger.error("risk.prediction_failed", customer_id=customer_id, error=str(e))
        raise HTTPException(status_code=500, detail="Prediction failed")
