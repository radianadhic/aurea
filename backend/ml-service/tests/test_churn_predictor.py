"""Unit tests for churn predictor."""
import pytest
from app.services.churn_predictor import ChurnPredictor


@pytest.fixture
def predictor() -> ChurnPredictor:
    return ChurnPredictor()


@pytest.mark.asyncio
async def test_churn_prediction_returns_valid_structure(predictor):
    """Test that churn prediction returns expected fields."""
    result = await predictor.predict_with_cache("test-cust-001", {})
    assert "model" in result
    assert result["model"] == "churn"
    assert "churn_probability_30d" in result
    assert "churn_probability_60d" in result
    assert "churn_probability_90d" in result
    assert "risk_level" in result
    assert result["risk_level"] in ["LOW", "MEDIUM", "HIGH"]


@pytest.mark.asyncio
async def test_churn_probabilities_in_valid_range(predictor):
    """Probabilities should be between 0 and 1."""
    result = await predictor.predict_with_cache("test-cust-002", {})
    for key in ["churn_probability_30d", "churn_probability_60d", "churn_probability_90d"]:
        assert 0 <= result[key] <= 1


@pytest.mark.asyncio
async def test_churn_increasing_over_time(predictor):
    """30-day prob should be <= 60-day prob <= 90-day prob."""
    result = await predictor.predict_with_cache("test-cust-003", {})
    assert result["churn_probability_30d"] <= result["churn_probability_60d"]
    assert result["churn_probability_60d"] <= result["churn_probability_90d"]


@pytest.mark.asyncio
async def test_cache_returns_same_result(predictor):
    """Cached prediction should return same result."""
    r1 = await predictor.predict_with_cache("test-cust-004", {})
    r2 = await predictor.predict_with_cache("test-cust-004", {})
    assert r1["churn_probability_30d"] == r2["churn_probability_30d"]
