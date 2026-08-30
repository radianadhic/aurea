"""
Customer Segmentation Predictor
K-means clustering for segmenting customers into 5 groups.
"""
from __future__ import annotations

import logging
from typing import Any

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from app.services.predictor import BasePredictor
from app.services.feature_store import FeatureStore

logger = logging.getLogger(__name__)


class SegmentPredictor(BasePredictor):
    """Customer segmentation using K-means clustering.

    Segments:
    - VIP: High balance, high transaction, premium products
    - MASS_AFFLUENT: Above average balance, active
    - MASS: Average balance, regular activity
    - STUDENT: Low balance, learning accounts, young
    - SENIOR: Mature customers, conservative products
    """

    SEGMENTS = ["VIP", "MASS_AFFLUENT", "MASS", "STUDENT", "SENIOR"]
    N_CLUSTERS = 5
    MODEL_VERSION = "1.0.0"

    def __init__(self) -> None:
        super().__init__(model_name="segment", model_version=self.MODEL_VERSION)
        self.scaler = StandardScaler()
        self.kmeans: KMeans | None = None
        self.feature_store = FeatureStore()

    async def load_model(self) -> None:
        """Load or initialize the K-means model."""
        try:
            import pickle
            from pathlib import Path
            model_path = Path("/app/models/segment_kmeans.pkl")
            if model_path.exists():
                with open(model_path, "rb") as f:
                    data = pickle.load(f)
                    self.kmeans = data["kmeans"]
                    self.scaler = data["scaler"]
                logger.info("Loaded segment model from disk")
            else:
                # Train on synthetic data as fallback
                self._train_synthetic()
                logger.info("Trained segment model on synthetic data")
            self.is_loaded = True
        except Exception as e:
            logger.warning("Model load failed, using mock: %s", e)
            self._train_synthetic()
            self.is_loaded = True

    def _train_synthetic(self) -> None:
        """Train K-means on synthetic customer data for bootstrap."""
        np.random.seed(42)
        # Generate synthetic features: [avg_balance, txn_count, age, product_count]
        n_samples = 1000
        # VIP: high balance, high txn
        vip = np.random.normal([500_000_000, 80, 45, 5], [100_000_000, 20, 10, 1], 200)
        # Mass affluent: medium-high
        ma = np.random.normal([100_000_000, 50, 40, 4], [30_000_000, 15, 8, 1], 250)
        # Mass: average
        mass = np.random.normal([20_000_000, 20, 35, 2], [10_000_000, 10, 12, 1], 300)
        # Student: low balance, young
        student = np.random.normal([2_000_000, 10, 20, 1], [1_000_000, 5, 3, 0.5], 150)
        # Senior: mature, conservative
        senior = np.random.normal([50_000_000, 15, 60, 3], [20_000_000, 8, 8, 1], 100)

        X = np.vstack([vip, ma, mass, student, senior])
        X = np.clip(X, 0, None)  # ensure non-negative

        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        self.kmeans = KMeans(n_clusters=self.N_CLUSTERS, random_state=42, n_init=10)
        self.kmeans.fit(X_scaled)

        # Map cluster IDs to segment labels based on cluster centroids
        # Cluster with highest avg_balance → VIP
        centroids = self.kmeans.cluster_centers_[:, 0]  # balance is first feature
        sorted_clusters = np.argsort(-centroids)  # descending
        self._cluster_map = {
            sorted_clusters[0]: "VIP",
            sorted_clusters[1]: "MASS_AFFLUENT",
            sorted_clusters[2]: "MASS",
            sorted_clusters[3]: "SENIOR",
            sorted_clusters[4]: "STUDENT",
        }

    async def _extract_features(self, customer_id: str) -> np.ndarray:
        """Extract customer features for segmentation."""
        features = await self.feature_store.get_segmentation_features(customer_id)
        return np.array([[
            features.get("avg_balance_90d", 10_000_000),
            features.get("txn_count_90d", 15),
            features.get("age", 35),
            features.get("product_count", 2),
        ]])

    async def _run_inference(self, customer_id: str) -> dict[str, Any]:
        """Run segment prediction."""
        if not self.is_loaded:
            await self.load_model()
        if self.kmeans is None:
            self._train_synthetic()

        features = await self._extract_features(customer_id)
        features_scaled = self.scaler.transform(features)
        cluster_id = int(self.kmeans.predict(features_scaled)[0])
        segment = self._cluster_map.get(cluster_id, "MASS")
        # Distance to cluster centroid (lower = more confident)
        distances = self.kmeans.transform(features_scaled)[0]
        confidence = float(1.0 - (distances[cluster_id] / distances.sum()))
        confidence = round(max(0.5, min(0.99, confidence)), 3)

        return {
            "customer_id": customer_id,
            "segment": segment,
            "cluster_id": cluster_id,
            "confidence": confidence,
            "features": {
                "avg_balance_90d": float(features[0, 0]),
                "txn_count_90d": float(features[0, 1]),
                "age": int(features[0, 2]),
                "product_count": int(features[0, 3]),
            },
            "model_version": self.MODEL_VERSION,
        }
