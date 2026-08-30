"""
Customer Lifetime Value (CLV) Predictor
Predicts 1-year, 3-year, and 5-year CLV based on historical behavior.
"""
from __future__ import annotations

import logging
from typing import Any

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

from app.services.predictor import BasePredictor
from app.services.feature_store import FeatureStore

logger = logging.getLogger(__name__)


class ClvPredictor(BasePredictor):
    """Customer Lifetime Value prediction using Gradient Boosting.

    Predicts:
    - CLV 1 year
    - CLV 3 years
    - CLV 5 years

    Considers:
    - Average monthly revenue (margin × balance + fees)
    - Retention probability
    - Growth trajectory
    - Product holding depth
    """

    MODEL_VERSION = "1.0.0"

    def __init__(self) -> None:
        super().__init__(model_name="clv", model_version=self.MODEL_VERSION)
        self.model_1y: GradientBoostingRegressor | None = None
        self.model_3y: GradientBoostingRegressor | None = None
        self.model_5y: GradientBoostingRegressor | None = None
        self.feature_store = FeatureStore()

    async def load_model(self) -> None:
        """Load or train CLV models."""
        try:
            import pickle
            from pathlib import Path
            model_path = Path("/app/models/clv_gbdt.pkl")
            if model_path.exists():
                with open(model_path, "rb") as f:
                    data = pickle.load(f)
                    self.model_1y = data["model_1y"]
                    self.model_3y = data["model_3y"]
                    self.model_5y = data["model_5y"]
                logger.info("Loaded CLV models from disk")
            else:
                self._train_synthetic()
                logger.info("Trained CLV models on synthetic data")
            self.is_loaded = True
        except Exception as e:
            logger.warning("Model load failed, using mock: %s", e)
            self._train_synthetic()
            self.is_loaded = True

    def _train_synthetic(self) -> None:
        """Train GBDT models on synthetic CLV data."""
        np.random.seed(42)
        n_samples = 3000
        # Features: [avg_balance, monthly_fee, monthly_revenue, retention_prob, age, products]
        X = np.random.normal(
            [50_000_000, 25_000, 350_000, 0.85, 40, 2.5],
            [40_000_000, 15_000, 250_000, 0.10, 12, 1.0],
            n_samples,
        )
        X = np.clip(X, [0, 0, 0, 0, 18, 1], None)
        # Targets: CLV = monthly_revenue * 12 * retention_years * (1 + growth)^t
        # Simulated with some noise
        monthly_rev = X[:, 2]
        retention = X[:, 3]
        growth = 0.05
        y_1y = monthly_rev * 12 * retention * (1 + growth)
        y_3y = monthly_rev * 12 * (1 - (1 - retention) ** 3) / (1 - (1 - retention)) * (1 + growth) ** 1.5
        y_5y = monthly_rev * 12 * (1 - (1 - retention) ** 5) / (1 - (1 - retention)) * (1 + growth) ** 2.5
        y_1y += np.random.normal(0, 500_000, n_samples)
        y_3y += np.random.normal(0, 1_500_000, n_samples)
        y_5y += np.random.normal(0, 3_000_000, n_samples)
        y_1y = np.clip(y_1y, 0, None)
        y_3y = np.clip(y_3y, 0, None)
        y_5y = np.clip(y_5y, 0, None)

        for y, name in [(y_1y, "1y"), (y_3y, "3y"), (y_5y, "5y")]:
            model = GradientBoostingRegressor(
                n_estimators=150,
                max_depth=5,
                learning_rate=0.05,
                random_state=42,
            )
            model.fit(X, y)
            if name == "1y":
                self.model_1y = model
            elif name == "3y":
                self.model_3y = model
            else:
                self.model_5y = model

    async def _extract_features(self, customer_id: str) -> np.ndarray:
        """Extract customer financial features for CLV prediction."""
        features = await self.feature_store.get_clv_features(customer_id)
        return np.array([[
            features.get("avg_balance_12m", 50_000_000),
            features.get("monthly_fee", 25_000),
            features.get("monthly_revenue", 350_000),
            features.get("retention_probability", 0.85),
            features.get("age", 40),
            features.get("product_count", 2.5),
        ]])

    async def _run_inference(self, customer_id: str) -> dict[str, Any]:
        """Run CLV prediction."""
        if not self.is_loaded:
            await self.load_model()
        if self.model_1y is None:
            self._train_synthetic()

        features = await self._extract_features(customer_id)
        clv_1y = float(self.model_1y.predict(features)[0])
        clv_3y = float(self.model_3y.predict(features)[0])
        clv_5y = float(self.model_5y.predict(features)[0])
        # Clamp to non-negative
        clv_1y = max(0, clv_1y)
        clv_3y = max(0, clv_3y)
        clv_5y = max(0, clv_5y)

        # CLV tier
        if clv_5y >= 100_000_000:
            tier = "PLATINUM"
        elif clv_5y >= 50_000_000:
            tier = "GOLD"
        elif clv_5y >= 10_000_000:
            tier = "SILVER"
        else:
            tier = "BRONZE"

        return {
            "customer_id": customer_id,
            "clv_1y": round(clv_1y, 2),
            "clv_3y": round(clv_3y, 2),
            "clv_5y": round(clv_5y, 2),
            "tier": tier,
            "currency": "IDR",
            "features": {
                "avg_balance_12m": float(features[0, 0]),
                "monthly_revenue": float(features[0, 2]),
                "retention_probability": float(features[0, 3]),
                "product_count": float(features[0, 5]),
            },
            "model_version": self.MODEL_VERSION,
        }
