"""
MDM ML Service - Customer predictions.

Endpoints:
  - /predict/churn/{customer_id}      - Churn probability
  - /predict/risk/{customer_id}       - Risk score
  - /predict/segment/{customer_id}    - Customer segment
  - /predict/anomaly/{customer_id}    - Anomaly detection
  - /predict/lifetime-value/{customer_id} - CLV
  - /batch/predict                    - Batch predictions
"""
import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

from app.api import (
    churn,
    risk,
    segment,
    anomaly,
    clv,
    batch,
    health,
)
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.telemetry import configure_telemetry
from app.core.kafka_consumer import kafka_lifecycle
from app.core.cache import cache_manager

configure_logging()
logger = structlog.get_logger()

# Prometheus metrics
PREDICTION_COUNTER = Counter(
    "mdm_ml_predictions_total",
    "Total ML predictions made",
    ["model", "result"]
)
PREDICTION_LATENCY = Histogram(
    "mdm_ml_prediction_duration_seconds",
    "ML prediction latency",
    ["model"]
)
ERROR_COUNTER = Counter(
    "mdm_ml_errors_total",
    "Total ML service errors",
    ["endpoint", "error_type"]
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Startup & shutdown lifecycle."""
    logger.info("ml_service.starting", version=settings.VERSION, env=settings.ENV)
    configure_telemetry()
    await cache_manager.connect()
    await kafka_lifecycle.start()
    yield
    logger.info("ml_service.shutting_down")
    await kafka_lifecycle.stop()
    await cache_manager.disconnect()


app = FastAPI(
    title="MDM ML Service",
    version=settings.VERSION,
    description="Customer ML predictions (churn, risk, segment, anomaly, CLV)",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FastAPIInstrumentor.instrument_app(app)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(churn.router, prefix="/predict/churn", tags=["Churn Prediction"])
app.include_router(risk.router, prefix="/predict/risk", tags=["Risk Scoring"])
app.include_router(segment.router, prefix="/predict/segment", tags=["Customer Segmentation"])
app.include_router(anomaly.router, prefix="/predict/anomaly", tags=["Anomaly Detection"])
app.include_router(clv.router, prefix="/predict/lifetime-value", tags=["Customer Lifetime Value"])
app.include_router(batch.router, prefix="/batch", tags=["Batch Predictions"])


@app.get("/metrics", include_in_schema=False)
async def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    ERROR_COUNTER.labels(
        endpoint=str(request.url.path),
        error_type=type(exc).__name__
    ).inc()
    logger.error("ml_service.error", path=str(request.url.path), error=str(exc), exc_info=True)
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal ML service error"
    )


@app.middleware("http")
async def add_correlation_id(request, call_next):
    correlation_id = request.headers.get("X-Correlation-Id", str(uuid.uuid4()))
    structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
    response = await call_next(request)
    response.headers["X-Correlation-Id"] = correlation_id
    return response
