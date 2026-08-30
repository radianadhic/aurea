"""Risk scoring service."""
from app.core.config import settings
from app.services.predictor import BasePredictor
from app.services.feature_store import feature_store


class RiskPredictor(BasePredictor):
    """Predicts customer risk score (0-100)."""

    def __init__(self) -> None:
        super().__init__("risk", settings.RISK_MODEL_PATH)

    async def _predict(self, customer_id: str, features: dict) -> dict:
        await self.load_model()
        customer_features = await feature_store.get_customer_features(customer_id)
        if not customer_features:
            customer_features = features

        if self.model is None:
            return {
                **self._get_mock_prediction(),
                "risk_score": 35,
                "risk_category": "MEDIUM",
                "components": {
                    "credit_risk": 0.25,
                    "behavioral_risk": 0.30,
                    "transaction_risk": 0.45,
                    "compliance_risk": 0.15,
                },
                "recommendations": [
                    "Monitor transaction patterns closely",
                    "Schedule annual KYC review"
                ],
            }

        # ... real implementation
        return self._get_mock_prediction()
