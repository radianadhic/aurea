"""Batch predictions API."""
import asyncio
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import structlog

from app.services.churn_predictor import ChurnPredictor
from app.services.risk_predictor import RiskPredictor

router = APIRouter()
logger = structlog.get_logger()
churn_predictor = ChurnPredictor()
risk_predictor = RiskPredictor()


class BatchPredictRequest(BaseModel):
    customer_ids: List[str] = Field(..., min_length=1, max_length=1000)
    model: str = Field(..., description="churn, risk, segment, anomaly, clv")


class BatchPredictResponse(BaseModel):
    model: str
    total: int
    succeeded: int
    failed: int
    results: List[dict]
    errors: List[dict] = []


@router.post("/predict", response_model=BatchPredictResponse)
async def batch_predict(request: BatchPredictRequest) -> BatchPredictResponse:
    """Run predictions for multiple customers in parallel."""
    logger.info("batch.predict_start", model=request.model, count=len(request.customer_ids))

    predictor = _get_predictor(request.model)
    if not predictor:
        raise HTTPException(status_code=400, detail=f"Unknown model: {request.model}")

    semaphore = asyncio.Semaphore(10)  # max 10 concurrent

    async def predict_one(customer_id: str) -> dict | None:
        async with semaphore:
            try:
                return await predictor.predict_with_cache(customer_id, {})
            except Exception as e:
                logger.error("batch.predict_failed", customer_id=customer_id, error=str(e))
                return None

    results = await asyncio.gather(*[predict_one(cid) for cid in request.customer_ids])
    succeeded = [r for r in results if r is not None]
    failed_count = sum(1 for r in results if r is None)

    logger.info("batch.predict_done", model=request.model, succeeded=len(succeeded), failed=failed_count)
    return BatchPredictResponse(
        model=request.model,
        total=len(request.customer_ids),
        succeeded=len(succeeded),
        failed=failed_count,
        results=succeeded,
    )


def _get_predictor(model: str):
    return {
        "churn": churn_predictor,
        "risk": risk_predictor,
    }.get(model)
