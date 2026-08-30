"""Feature store for ML predictions."""
from datetime import datetime, timedelta
from typing import Any, Optional

import structlog
from app.core.cache import cache_manager

logger = structlog.get_logger()


class FeatureStore:
    """In-memory + Redis feature store for ML features."""

    def __init__(self) -> None:
        self._memory: dict[str, dict] = {}

    async def get_customer_features(self, customer_id: str) -> Optional[dict]:
        """Get all features for a customer."""
        cache_key = f"features:customer:{customer_id}"
        cached = await cache_manager.get(cache_key)
        if cached:
            return cached

        # In real impl, query from PostgreSQL/ClickHouse
        # For now, return mock features
        return {
            "customer_id": customer_id,
            "tenure_months": 24,
            "age": 35,
            "txn_count_30d": 12,
            "txn_amount_30d": 5_500_000,
            "txn_avg_amount_30d": 458_333,
            "complaints_90d": 0,
            "product_count": 3,
            "app_logins_30d": 18,
            "balance_trend": 0.05,
            "engagement_score": 0.72,
            "kyc_status_score": 1.0,
            "last_updated": datetime.utcnow().isoformat(),
        }

    async def invalidate_customer(self, customer_id: str) -> None:
        """Invalidate cached features when customer data changes."""
        cache_key = f"features:customer:{customer_id}"
        await cache_manager.delete(cache_key)
        if customer_id in self._memory:
            del self._memory[customer_id]
        logger.info("features.invalidated", customer_id=customer_id)

    async def update_transaction_features(self, transaction_data: dict) -> None:
        """Update features based on new transaction event."""
        customer_id = transaction_data.get("customerId")
        if not customer_id:
            return
        # Increment counters, recompute aggregates, etc.
        # For simplicity, just invalidate
        await self.invalidate_customer(customer_id)


feature_store = FeatureStore()
