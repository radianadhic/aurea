"""
Anomaly Detection Predictor
Isolation Forest for detecting anomalous customer behavior.
"""
from __future__ import annotations

import logging
from typing import Any

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from app.services.predictor import BasePredictor
from app.services.feature_store import FeatureStore

logger = logging.getLogger(__name__)


class AnomalyPredictor(BasePredictor):
    """Anomaly detection using Isolation Forest.

    Detects:
    - Unusual transaction patterns (potential fraud)
    - Sudden balance changes (potential account takeover)
    - Login location anomalies
    - Velocity anomalies (rapid-fire transactions)
    """

    MODEL_VERSION = "1.0.0"
    CONTAMINATION = 0.05  # expect 5% anomalies

    def __init__(self) -> None:
        super().__init__(model_name="anomaly", model_version=self.MODEL_VERSION)
        self.scaler = StandardScaler()
        self.model: IsolationForest | None = None
        self.feature_store = FeatureStore()

    async def load_model(self) -> None:
        """Load or train the Isolation Forest model."""
        try:
            import pickle
            from pathlib import Path
            model_path = Path("/app/models/anomaly_iforest.pkl")
            if model_path.exists():
                with open(model_path, "rb") as f:
                    data = pickle.load(f)
                    self.model = data["model"]
                    self.scaler = data["scaler"]
                logger.info("Loaded anomaly model from disk")
            else:
                self._train_synthetic()
                logger.info("Trained anomaly model on synthetic data")
            self.is_loaded = True
        except Exception as e:
            logger.warning("Model load failed, using mock: %s", e)
            self._train_synthetic()
            self.is_loaded = True

    def _train_synthetic(self) -> None:
        """Train Isolation Forest on synthetic normal behavior data."""
        np.random.seed(42)
        n_samples = 2000
        # Normal behavior: [txn_amount, txn_velocity, geo_distance, hour_of_day, device_change]
        normal = np.random.normal(
            [500_000, 5, 10, 14, 0],
            [300_000, 3, 15, 4, 0.3],
            n_samples,
        )
        normal = np.clip(normal, 0, None)
        self.scaler.fit(normal)
        normal_scaled = self.scaler.transform(normal)
        self.model = IsolationForest(
            n_estimators=200,
            contamination=self.CONTAMINATION,
            random_state=42,
            n_jobs=-1,
        )
        self.model.fit(normal_scaled)

    async def _extract_features(self, customer_id: str) -> np.ndarray:
        """Extract recent transaction features for anomaly detection."""
        features = await self.feature_store.get_anomaly_features(customer_id)
        return np.array([[
            features.get("last_txn_amount", 500_000),
            features.get("txn_velocity_1h", 5),
            features.get("geo_distance_km", 10),
            features.get("txn_hour", 14),
            features.get("device_change_count_7d", 0),
        ]])

    async def _run_inference(self, customer_id: str) -> dict[str, Any]:
        """Run anomaly detection."""
        if not self.is_loaded:
            await self.load_model()
        if self.model is None:
            self._train_synthetic()

        features = await self._extract_features(customer_id)
        features_scaled = self.scaler.transform(features)
        # Isolation Forest: -1 = anomaly, 1 = normal
        prediction = int(self.model.predict(features_scaled)[0])
        # Anomaly score (decision_function): lower = more anomalous
        raw_score = float(self.model.decision_function(features_scaled)[0])
        # Normalize to 0-1 (1 = definitely anomaly)
        anomaly_score = round(1.0 / (1.0 + np.exp(raw_score * 5)), 3)
        is_anomaly = prediction == -1

        # Determine anomaly type based on which feature deviates most
        anomaly_type = "NONE"
        if is_anomaly:
            deviations = np.abs(features_scaled[0])
            max_idx = int(np.argmax(deviations))
            anomaly_types = [
                "UNUSUAL_TRANSACTION_AMOUNT",
                "HIGH_VELOCITY",
                "GEO_ANOMALY",
                "UNUSUAL_TIME",
                "DEVICE_CHANGE",
            ]
            anomaly_type = anomaly_types[max_idx]

        return {
            "customer_id": customer_id,
            "is_anomaly": is_anomaly,
            "anomaly_score": anomaly_score,
            "anomaly_type": anomaly_type,
            "raw_score": round(raw_score, 4),
            "features": {
                "last_txn_amount": float(features[0, 0]),
                "txn_velocity_1h": int(features[0, 1]),
                "geo_distance_km": float(features[0, 2]),
                "txn_hour": int(features[0, 3]),
                "device_change_count_7d": int(features[0, 4]),
            },
            "recommendation": (
                "BLOCK_AND_REVIEW" if anomaly_score > 0.85
                else "MONITOR" if anomaly_score > 0.6
                else "ALLOW"
            ),
            "model_version": self.MODEL_VERSION,
        }
