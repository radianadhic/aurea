"""
AUREA Auto-Insights Engine
Generates automatic insights from platform data:
- Anomaly detection on KPIs
- Smart segmentation
- Auto-generated narratives
- Predictive alerts
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os
import random
from dataclasses import dataclass, asdict
from enum import Enum


class InsightType(str, Enum):
    ANOMALY = "ANOMALY"
    TREND = "TREND"
    CORRELATION = "CORRELATION"
    PREDICTION = "PREDICTION"
    RECOMMENDATION = "RECOMMENDATION"
    ALERT = "ALERT"


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass
class Insight:
    """A single auto-generated insight."""
    id: str
    type: str  # InsightType
    severity: str  # Severity
    title: str
    description: str
    metric: str
    current_value: float
    expected_value: float
    deviation_pct: float
    detected_at: str
    category: str
    recommendations: List[str]
    confidence: float
    related_entities: List[Dict]
    chart_data: Optional[Dict] = None


class AnomalyDetector:
    """Statistical anomaly detection using multiple methods."""
    
    def __init__(self, sensitivity: float = 2.0):
        self.sensitivity = sensitivity  # Standard deviations
    
    def detect(self, values: List[float], dates: List[str]) -> Dict:
        """Detect anomalies using Z-score and IQR methods."""
        if len(values) < 7:
            return {"anomalies": [], "trend": "INSUFFICIENT_DATA"}
        
        arr = np.array(values, dtype=float)
        dates_arr = np.array(dates)
        
        # Z-score method
        mean = np.mean(arr)
        std = np.std(arr)
        z_scores = np.abs((arr - mean) / std) if std > 0 else np.zeros_like(arr)
        z_anomalies = z_scores > self.sensitivity
        
        # IQR method
        q1, q3 = np.percentile(arr, [25, 75])
        iqr = q3 - q1
        iqr_lower = q1 - 1.5 * iqr
        iqr_upper = q3 + 1.5 * iqr
        iqr_anomalies = (arr < iqr_lower) | (arr > iqr_upper)
        
        # Combined
        combined = z_anomalies | iqr_anomalies
        
        # Trend
        if len(arr) >= 14:
            recent = arr[-7:].mean()
            previous = arr[-14:-7].mean()
            change_pct = ((recent - previous) / previous * 100) if previous != 0 else 0
            if abs(change_pct) > 10:
                trend = "INCREASING" if change_pct > 0 else "DECREASING"
            else:
                trend = "STABLE"
        else:
            trend = "STABLE"
            change_pct = 0
        
        anomalies = []
        for i, (is_anom, val, date) in enumerate(zip(combined, arr, dates_arr)):
            if is_anom:
                deviation = ((val - mean) / mean * 100) if mean != 0 else 0
                anomalies.append({
                    "date": str(date),
                    "value": float(val),
                    "expected": float(mean),
                    "z_score": float(z_scores[i]),
                    "deviation_pct": float(deviation),
                    "direction": "spike" if val > mean else "drop"
                })
        
        return {
            "anomalies": anomalies,
            "trend": trend,
            "trend_change_pct": float(change_pct),
            "mean": float(mean),
            "std": float(std),
            "latest": float(arr[-1]),
            "previous": float(arr[-2]) if len(arr) > 1 else float(arr[-1])
        }


class InsightGenerator:
    """Generates natural-language insights from data."""
    
    def __init__(self):
        self.anomaly_detector = AnomalyDetector(sensitivity=2.0)
    
    def generate_narrative(self, anomaly_data: Dict, metric_name: str) -> str:
        """Create human-readable narrative from anomaly data."""
        anomalies = anomaly_data.get('anomalies', [])
        trend = anomaly_data.get('trend', 'STABLE')
        change = anomaly_data.get('trend_change_pct', 0)
        
        if not anomalies:
            if trend != "STABLE":
                return (f"📊 {metric_name} is {trend.lower()} with a "
                       f"{change:.1f}% change over the past week. "
                       f"Current value: {anomaly_data.get('latest', 0):,.0f}.")
            return f"✅ {metric_name} is stable at {anomaly_data.get('latest', 0):,.0f}. No anomalies detected."
        
        latest = anomalies[-1]
        direction = "spike" if latest['value'] > latest['expected'] else "drop"
        emoji = "🚨" if abs(latest['deviation_pct']) > 50 else "⚠️"
        
        return (f"{emoji} {metric_name} shows a significant {direction} on {latest['date']}. "
               f"Value reached {latest['value']:,.0f}, which is {abs(latest['deviation_pct']):.1f}% "
               f"{'above' if direction == 'spike' else 'below'} the expected value of {latest['expected']:,.0f}.")
    
    def generate_recommendations(self, anomaly_data: Dict, metric_name: str) -> List[str]:
        """Generate actionable recommendations."""
        recs = []
        anomalies = anomaly_data.get('anomalies', [])
        trend = anomaly_data.get('trend', 'STABLE')
        
        if anomalies:
            latest = anomalies[-1]
            if latest['deviation_pct'] > 50:
                recs.append("🔍 Investigate root cause immediately")
                recs.append("📞 Notify operations team")
                recs.append("📊 Check related metrics for correlation")
            elif latest['deviation_pct'] > 20:
                recs.append("👀 Monitor for next 24 hours")
                recs.append("📋 Document in incident log")
        
        if trend == "DECREASING" and anomaly_data.get('trend_change_pct', 0) < -15:
            recs.append("📉 Review recent changes that may have impacted this metric")
            recs.append("🎯 Consider intervention to reverse trend")
        elif trend == "INCREASING" and anomaly_data.get('trend_change_pct', 0) > 30:
            recs.append("⚡ Capitalize on positive trend")
            recs.append("📈 Document success factors for replication")
        
        if not recs:
            recs.append("✅ Continue normal monitoring")
        
        return recs


class AutoInsightsEngine:
    """
    Main engine for generating automatic insights across AUREA platform.
    """
    
    def __init__(self):
        self.generator = InsightGenerator()
        self.anomaly_detector = AnomalyDetector(sensitivity=2.0)
        self.insights_cache: List[Insight] = []
        self.last_refresh = None
    
    def generate_platform_insights(self) -> List[Insight]:
        """Generate insights for the entire AUREA platform."""
        insights = []
        
        # Customer Insights
        customer_metrics = self._get_customer_metrics()
        for metric_name, data in customer_metrics.items():
            insight = self._create_insight_from_metric(
                "Customer", metric_name, data
            )
            if insight:
                insights.append(insight)
        
        # Transaction Insights
        txn_metrics = self._get_transaction_metrics()
        for metric_name, data in txn_metrics.items():
            insight = self._create_insight_from_metric(
                "Transaction", metric_name, data
            )
            if insight:
                insights.append(insight)
        
        # System Performance Insights
        sys_metrics = self._get_system_metrics()
        for metric_name, data in sys_metrics.items():
            insight = self._create_insight_from_metric(
                "System", metric_name, data
            )
            if insight:
                insights.append(insight)
        
        # KYC Insights
        kyc_metrics = self._get_kyc_metrics()
        for metric_name, data in kyc_metrics.items():
            insight = self._create_insight_from_metric(
                "KYC", metric_name, data
            )
            if insight:
                insights.append(insight)
        
        # Matching Engine Insights
        match_metrics = self._get_matching_metrics()
        for metric_name, data in match_metrics.items():
            insight = self._create_insight_from_metric(
                "Matching", metric_name, data
            )
            if insight:
                insights.append(insight)
        
        # Sort by severity and time
        severity_order = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}
        insights.sort(key=lambda x: (severity_order.get(x.severity, 3), x.detected_at), reverse=False)
        
        self.insights_cache = insights
        self.last_refresh = datetime.utcnow().isoformat()
        
        return insights
    
    def _create_insight_from_metric(self, category: str, metric_name: str, data: Dict) -> Optional[Insight]:
        """Create an Insight object from metric data."""
        anomaly_result = self.anomaly_detector.detect(data['values'], data['dates'])
        anomalies = anomaly_result.get('anomalies', [])
        
        if not anomalies and anomaly_result.get('trend') == 'STABLE':
            return None  # Skip non-actionable
        
        # Determine severity
        if anomalies:
            max_dev = max(abs(a['deviation_pct']) for a in anomalies)
            if max_dev > 50:
                severity = Severity.CRITICAL
            elif max_dev > 20:
                severity = Severity.WARNING
            else:
                severity = Severity.INFO
        else:
            severity = Severity.INFO
        
        # Determine type
        if anomalies:
            insight_type = InsightType.ANOMALY
        elif anomaly_result.get('trend') != 'STABLE':
            insight_type = InsightType.TREND
        else:
            return None
        
        narrative = self.generator.generate_narrative(anomaly_result, metric_name)
        recs = self.generator.generate_recommendations(anomaly_result, metric_name)
        
        latest = anomaly_result.get('latest', 0)
        expected = anomaly_result.get('mean', 0)
        deviation = ((latest - expected) / expected * 100) if expected != 0 else 0
        
        return Insight(
            id=f"INS-{category[:3].upper()}-{metric_name[:10]}-{int(datetime.utcnow().timestamp())}",
            type=insight_type,
            severity=severity,
            title=f"{metric_name}: {anomaly_result.get('trend', 'STABLE').title()}",
            description=narrative,
            metric=metric_name,
            current_value=latest,
            expected_value=expected,
            deviation_pct=deviation,
            detected_at=datetime.utcnow().isoformat(),
            category=category,
            recommendations=recs,
            confidence=min(0.99, 0.6 + len(anomalies) * 0.1),
            related_entities=data.get('related_entities', []),
            chart_data={
                "labels": data['dates'][-14:],
                "values": data['values'][-14:],
                "expected": [anomaly_result.get('mean', 0)] * 14,
                "anomaly_indices": [
                    len(data['dates']) - 14 + i 
                    for i, d in enumerate(data['dates'][-14:]) 
                    if any(a['date'] == d for a in anomalies)
                ]
            }
        )
    
    def _get_customer_metrics(self) -> Dict:
        """Generate customer-related metrics (mock data with realistic patterns)."""
        today = datetime.utcnow()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        
        return {
            "New Customers": {
                "dates": dates,
                "values": self._generate_metric_series(150, 50, 0.15, anomaly_day=18),
                "related_entities": [{"type": "branch", "id": "JKT-001", "name": "Jakarta Pusat"}]
            },
            "Active Customers": {
                "dates": dates,
                "values": self._generate_metric_series(45000, 5000, 0.05, anomaly_day=None),
                "related_entities": []
            },
            "Customer Churn Rate": {
                "dates": dates,
                "values": self._generate_metric_series(2.5, 0.8, 0.20, anomaly_day=7),
                "related_entities": [{"type": "segment", "id": "VIP", "name": "VIP Segment"}]
            },
            "CLV Average": {
                "dates": dates,
                "values": self._generate_metric_series(12500000, 2000000, 0.08, anomaly_day=None),
                "related_entities": []
            }
        }
    
    def _get_transaction_metrics(self) -> Dict:
        today = datetime.utcnow()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        
        return {
            "Transaction Volume": {
                "dates": dates,
                "values": self._generate_metric_series(850000, 100000, 0.12, anomaly_day=22),
                "related_entities": []
            },
            "Avg Transaction Value": {
                "dates": dates,
                "values": self._generate_metric_series(1500000, 300000, 0.18, anomaly_day=12),
                "related_entities": [{"type": "channel", "id": "MOBILE", "name": "Mobile Banking"}]
            },
            "Failed Transactions": {
                "dates": dates,
                "values": self._generate_metric_series(120, 30, 0.30, anomaly_day=25),
                "related_entities": []
            },
            "Cross-sell Conversion": {
                "dates": dates,
                "values": self._generate_metric_series(8.5, 2.0, 0.15, anomaly_day=None),
                "related_entities": []
            }
        }
    
    def _get_system_metrics(self) -> Dict:
        today = datetime.utcnow()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        
        return {
            "API Latency (p95)": {
                "dates": dates,
                "values": self._generate_metric_series(180, 40, 0.25, anomaly_day=15),
                "related_entities": [{"type": "service", "id": "gc-service", "name": "Customer Service"}]
            },
            "Error Rate": {
                "dates": dates,
                "values": self._generate_metric_series(0.05, 0.02, 0.40, anomaly_day=20),
                "related_entities": []
            },
            "Database Connections": {
                "dates": dates,
                "values": self._generate_metric_series(150, 30, 0.10, anomaly_day=None),
                "related_entities": []
            }
        }
    
    def _get_kyc_metrics(self) -> Dict:
        today = datetime.utcnow()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        
        return {
            "KYC Verifications": {
                "dates": dates,
                "values": self._generate_metric_series(320, 80, 0.18, anomaly_day=8),
                "related_entities": []
            },
            "KYC Auto-Approval Rate": {
                "dates": dates,
                "values": self._generate_metric_series(78, 5, 0.05, anomaly_day=3),
                "related_entities": []
            },
            "KYC Manual Review Queue": {
                "dates": dates,
                "values": self._generate_metric_series(45, 15, 0.35, anomaly_day=27),
                "related_entities": [{"type": "team", "id": "steward-team", "name": "Steward Team"}]
            }
        }
    
    def _get_matching_metrics(self) -> Dict:
        today = datetime.utcnow()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        
        return {
            "Match Queue Size": {
                "dates": dates,
                "values": self._generate_metric_series(230, 60, 0.20, anomaly_day=14),
                "related_entities": []
            },
            "Auto-Match Rate": {
                "dates": dates,
                "values": self._generate_metric_series(87, 4, 0.03, anomaly_day=None),
                "related_entities": []
            },
            "Match Precision": {
                "dates": dates,
                "values": self._generate_metric_series(0.94, 0.03, 0.02, anomaly_day=None),
                "related_entities": []
            }
        }
    
    def _generate_metric_series(self, base: float, variance: float, noise: float, anomaly_day: Optional[int] = None) -> List[float]:
        """Generate realistic time series with optional anomaly."""
        n = 30
        values = []
        
        for i in range(n):
            # Base trend (slight growth)
            trend = base * (1 + 0.001 * i)
            
            # Daily variance (sinusoidal pattern)
            day_pattern = variance * 0.3 * np.sin(2 * np.pi * i / 7)
            
            # Random noise
            random_noise = variance * noise * (random.random() - 0.5) * 2
            
            value = trend + day_pattern + random_noise
            
            # Inject anomaly
            if anomaly_day is not None and i == anomaly_day:
                direction = random.choice([1, -1])
                spike_magnitude = variance * (2.5 + random.random())
                value += direction * spike_magnitude
            
            values.append(max(0, value))
        
        return values


# Singleton instance
_engine = None


class _EngineFacade:
    """Convenience facade for the AutoInsightsEngine that adds query helpers
    and pre-computes the insight cache for fast access."""

    def __init__(self, engine: AutoInsightsEngine):
        self.engine = engine
        self.insights: List[Insight] = engine.generate_platform_insights()
        self.last_refresh = datetime.utcnow().isoformat()

    def refresh(self) -> List[Insight]:
        self.insights = self.engine.generate_platform_insights()
        self.last_refresh = datetime.utcnow().isoformat()
        return self.insights

    def get_insights(
        self,
        severity: Optional[str] = None,
        category: Optional[str] = None,
        insight_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict]:
        results = []
        for i in self.insights:
            if severity and i.severity != severity.upper():
                continue
            if category and i.category.lower() != category.lower():
                continue
            if insight_type and i.type != insight_type.upper():
                continue
            results.append(self._to_dict(i))
            if len(results) >= limit:
                break
        return results

    def get_insight(self, insight_id: str) -> Optional[Dict]:
        for i in self.insights:
            if i.id == insight_id:
                return self._to_dict(i)
        return None

    def get_summary(self) -> Dict:
        by_severity = {"CRITICAL": 0, "WARNING": 0, "INFO": 0}
        by_category: Dict[str, int] = {}
        by_type: Dict[str, int] = {}
        for i in self.insights:
            sev = i.severity if i.severity in by_severity else "INFO"
            by_severity[sev] += 1
            by_category[i.category] = by_category.get(i.category, 0) + 1
            by_type[i.type] = by_type.get(i.type, 0) + 1

        # Top 3 critical insights
        critical = [i for i in self.insights if i.severity == "CRITICAL"]
        critical.sort(key=lambda x: x.deviation_pct, reverse=True)
        top = [
            {
                "id": i.id,
                "title": i.title,
                "metric": i.metric,
                "deviation_pct": i.deviation_pct,
                "description": i.description,
            }
            for i in critical[:3]
        ]

        return {
            "total_insights": len(self.insights),
            "by_severity": by_severity,
            "by_category": by_category,
            "by_type": by_type,
            "top_critical": top,
            "last_refresh": self.last_refresh,
        }

    def _to_dict(self, insight: Insight) -> Dict:
        return {
            "id": insight.id,
            "type": insight.type,
            "severity": insight.severity,
            "title": insight.title,
            "description": insight.description,
            "metric": insight.metric,
            "current_value": insight.current_value,
            "expected_value": insight.expected_value,
            "deviation_pct": insight.deviation_pct,
            "detected_at": insight.detected_at,
            "category": insight.category,
            "recommendations": insight.recommendations,
            "confidence": insight.confidence,
            "related_entities": insight.related_entities,
            "chart_data": insight.chart_data,
        }


def get_engine() -> _EngineFacade:
    global _engine
    if _engine is None:
        _engine = _EngineFacade(AutoInsightsEngine())
    return _engine


def refresh_engine() -> Dict:
    global _engine
    _engine = _EngineFacade(AutoInsightsEngine())
    return _engine.get_summary()
