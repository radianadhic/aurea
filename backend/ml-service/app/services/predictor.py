"""ML model service base class."""
import time
from abc import ABC, abstractmethod
from typing import Any

import joblib
import numpy as np
import structlog
from app.core.cache import cache_manager
from app.core.config import settings

logger = structlog.get_logger()


class BasePredictor(ABC):
    """Base class for all ML predictors."""

    def __init__(self, model_name: str, model_path: str) -> None:
        self.model_name = model_name
        self.model_path = model_path
        self.model: Any = None

    async def load_model(self) -> None:
        """Lazy load the model from disk."""
        if self.model is None:
            try:
                import os
                if os.path.exists(self.model_path):
                    self.model = joblib.load(self.model_path)
                    logger.info("ml.model_loaded", model=self.model_name)
                else:
                    logger.warning("ml.model_not_found", path=self.model_path)
                    self.model = None
            except Exception as e:
                logger.error("ml.model_load_failed", model=self.model_name, error=str(e))

    async def predict_with_cache(
        self,
        customer_id: str,
        features: dict,
        cache_ttl: int | None = None
    ) -> dict:
        """Make prediction with Redis caching."""
        cache_key = f"ml:{self.model_name}:{customer_id}"
        cached = await cache_manager.get(cache_key)
        if cached:
            logger.debug("ml.cache_hit", model=self.model_name, customer_id=customer_id)
            return cached

        start = time.time()
        result = await self._predict(customer_id, features)
        duration = time.time() - start

        await cache_manager.set(cache_key, result, cache_ttl or settings.CACHE_TTL)
        logger.info(
            "ml.prediction",
            model=self.model_name,
            customer_id=customer_id,
            duration_ms=int(duration * 1000)
        )
        return result

    @abstractmethod
    async def _predict(self, customer_id: str, features: dict) -> dict:
        """Make the actual prediction. Must be implemented by subclass."""
        ...

    def _get_mock_prediction(self) -> dict:
        """Fallback mock prediction when no model is loaded."""
        return {
            "model": self.model_name,
            "score": 0.5,
            "confidence": 0.0,
            "explanation": "Model not loaded - returning mock prediction",
            "model_version": "mock-1.0",
        }
