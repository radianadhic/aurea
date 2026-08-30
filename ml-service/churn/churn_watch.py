"""
AUREA Churn Watch List
======================

Real-time churn risk monitoring & intervention management.

Features:
- Continuous churn risk scoring per customer
- Risk-level classification (Watch / Alert / Critical / Lost)
- Churn driver analysis (what's causing the risk)
- Intervention tracking (campaigns, contacts, offers)
- Win-back campaign management
- Historical churn event log
- Early warning system (catches customers BEFORE they churn)
- Retention rate predictions
- Revenue at risk calculation
"""

from __future__ import annotations

import math
import random
import statistics
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

# Reuse customer data from segmentation
from segmentation.customer_segmentation import (
    Customer, CustomerDataGenerator, SegmentationEngine,
    CLVPredictor, RFMAnalyzer, Segment
)


# ============================================================
# ENUMS
# ============================================================

class WatchLevel(str, Enum):
    """Churn risk severity levels."""
    SAFE = "Safe"               # < 20% risk
    WATCH = "Watch"             # 20-45% risk - monitor
    ALERT = "Alert"             # 45-70% risk - take action
    CRITICAL = "Critical"       # 70-90% risk - URGENT
    LOST = "Lost"               # > 90% risk or confirmed churned


class ChurnDriver(str, Enum):
    """Reasons driving the churn risk."""
    LONG_INACTIVITY = "Long Inactivity"
    DECLINING_FREQUENCY = "Declining Frequency"
    LOWER_SPENDING = "Lower Spending"
    SUPPORT_ISSUES = "Support Issues"
    PRODUCT_DISSATISFACTION = "Product Dissatisfaction"
    PRICE_SENSITIVITY = "Price Sensitivity"
    COMPETITOR_SWITCH = "Competitor Switch Signal"
    CHANNEL_FRICTION = "Channel Friction"
    DEMOGRAPHIC_SHIFT = "Demographic Shift"
    LIFECYCLE_NATURAL = "Lifecycle (natural churn)"


class InterventionType(str, Enum):
    """Types of retention interventions."""
    EMAIL = "Email"
    SMS = "SMS"
    PHONE_CALL = "Phone Call"
    PERSONAL_OUTREACH = "Personal Outreach"
    DISCOUNT_OFFER = "Discount Offer"
    LOYALTY_BONUS = "Loyalty Bonus"
    PRODUCT_RECOMMENDATION = "Product Recommendation"
    SURVEY = "Survey"
    WIN_BACK_CAMPAIGN = "Win-Back Campaign"
    VIP_INVITATION = "VIP Invitation"


class InterventionStatus(str, Enum):
    """Status of an intervention."""
    PLANNED = "Planned"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CUSTOMER_RESPONDED = "Customer Responded"
    NO_RESPONSE = "No Response"


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class ChurnSignal:
    """A signal that contributes to churn risk."""
    driver: ChurnDriver
    severity: int  # 1-10
    description: str
    detected_at: str

    def to_dict(self):
        d = asdict(self)
        d["driver"] = self.driver.value
        return d


@dataclass
class Intervention:
    """A retention action taken for a customer."""
    id: str
    customer_id: str
    type: InterventionType
    channel: str
    subject: str
    message: str
    status: InterventionStatus
    assigned_to: str
    created_at: str
    scheduled_for: str
    completed_at: Optional[str]
    outcome: Optional[str]
    expected_recovery_clv: float
    actual_recovery_clv: float = 0.0

    def to_dict(self):
        d = asdict(self)
        d["type"] = self.type.value
        d["status"] = self.status.value
        return d


@dataclass
class ChurnAlert:
    """An alert for a high-risk customer."""
    id: str
    customer_id: str
    customer_name: str
    email: str
    phone: str
    level: WatchLevel
    churn_probability: float
    risk_score: int  # 0-100
    clv_at_risk: float
    monthly_revenue: float
    last_purchase_date: str
    days_since_purchase: int
    total_orders: int
    total_spend: float
    segment: str
    drivers: list[ChurnSignal]
    recommended_actions: list[str]
    assigned_to: Optional[str]
    intervention_count: int
    status: str  # "new", "acknowledged", "in_intervention", "monitoring", "resolved"
    created_at: str
    acknowledged_at: Optional[str]
    resolved_at: Optional[str]
    notes: list[str] = field(default_factory=list)

    def to_dict(self):
        d = asdict(self)
        d["level"] = self.level.value
        d["drivers"] = [s.to_dict() if hasattr(s, 'to_dict') else s for s in self.drivers]
        return d


@dataclass
class WatchListSummary:
    """Aggregate stats for the watch list."""
    total_alerts: int
    by_level: dict[str, int]
    by_status: dict[str, int]
    total_clv_at_risk: float
    total_monthly_revenue_at_risk: float
    avg_churn_probability: float
    intervention_success_rate: float
    recovery_this_month: float
    new_alerts_24h: int
    resolved_alerts_24h: int
    trends: dict[str, float]  # week-over-week changes


# ============================================================
# CHURN PREDICTION ENGINE
# ============================================================

class ChurnPredictor:
    """Multi-signal churn risk predictor."""

    # Weight configuration
    WEIGHTS = {
        ChurnDriver.LONG_INACTIVITY: 0.30,
        ChurnDriver.DECLINING_FREQUENCY: 0.20,
        ChurnDriver.LOWER_SPENDING: 0.15,
        ChurnDriver.SUPPORT_ISSUES: 0.10,
        ChurnDriver.PRODUCT_DISSATISFACTION: 0.08,
        ChurnDriver.PRICE_SENSITIVITY: 0.07,
        ChurnDriver.COMPETITOR_SWITCH: 0.05,
        ChurnDriver.CHANNEL_FRICTION: 0.03,
        ChurnDriver.DEMOGRAPHIC_SHIFT: 0.01,
        ChurnDriver.LIFECYCLE_NATURAL: 0.01,
    }

    @staticmethod
    def analyze(customer: Customer, all_customers: list[Customer],
                reference_date: datetime) -> tuple[float, list[ChurnSignal]]:
        """Analyze churn risk and identify drivers.
        Returns (churn_probability, list_of_signals).
        """
        signals: list[ChurnSignal] = []
        risk_components: list[tuple[ChurnDriver, float, str]] = []

        # 1. Recency signal
        if customer.recency_days > 365:
            risk_components.append((
                ChurnDriver.LONG_INACTIVITY,
                0.95,
                f"No purchase in {customer.recency_days} days (>1 year)"
            ))
        elif customer.recency_days > 180:
            risk_components.append((
                ChurnDriver.LONG_INACTIVITY,
                0.75,
                f"Inactive for {customer.recency_days} days (6+ months)"
            ))
        elif customer.recency_days > 90:
            risk_components.append((
                ChurnDriver.LONG_INACTIVITY,
                0.50,
                f"Last purchase {customer.recency_days} days ago"
            ))
        elif customer.recency_days > 60:
            risk_components.append((
                ChurnDriver.LONG_INACTIVITY,
                0.25,
                f"Inactivity growing ({customer.recency_days} days)"
            ))

        # 2. Declining frequency
        if customer.total_orders == 0:
            risk_components.append((
                ChurnDriver.DECLINING_FREQUENCY,
                0.90,
                "Zero orders placed"
            ))
        elif customer.frequency_score < 0.1:
            risk_components.append((
                ChurnDriver.DECLINING_FREQUENCY,
                0.60,
                f"Very low frequency: {customer.frequency_score:.2f} orders/month"
            ))

        # 3. Support issues
        if customer.support_tickets >= 5:
            risk_components.append((
                ChurnDriver.SUPPORT_ISSUES,
                0.65,
                f"{customer.support_tickets} support tickets (high)"
            ))
        elif customer.support_tickets >= 3:
            risk_components.append((
                ChurnDriver.SUPPORT_ISSUES,
                0.35,
                f"{customer.support_tickets} support tickets (moderate)"
            ))

        # 4. Spending decline (compare to peer avg)
        if all_customers:
            peer_avg_spend = statistics.mean(c.avg_order_value for c in all_customers)
            if customer.avg_order_value < peer_avg_spend * 0.3:
                risk_components.append((
                    ChurnDriver.LOWER_SPENDING,
                    0.45,
                    f"AOV {customer.avg_order_value:,.0f} is {customer.avg_order_value/peer_avg_spend*100:.0f}% of peer avg"
                ))

        # 5. Product dissatisfaction proxy (no categories = no engagement)
        if len(customer.product_categories) == 0:
            risk_components.append((
                ChurnDriver.PRODUCT_DISSATISFACTION,
                0.50,
                "No product category engagement"
            ))
        elif len(customer.product_categories) == 1 and customer.total_orders < 2:
            risk_components.append((
                ChurnDriver.PRODUCT_DISSATISFACTION,
                0.30,
                "Single-category, low engagement"
            ))

        # 6. Channel friction (call center = more friction than app)
        if customer.preferred_channel == "Call Center" and customer.total_orders < 3:
            risk_components.append((
                ChurnDriver.CHANNEL_FRICTION,
                0.25,
                f"High-friction channel ({customer.preferred_channel})"
            ))

        # 7. Lifecycle natural churn (very old customers)
        tenure_days = (reference_date - customer.registration_date).days
        if tenure_days > 730 and customer.frequency_score < 0.5:
            risk_components.append((
                ChurnDriver.LIFECYCLE_NATURAL,
                0.40,
                f"Long tenure ({tenure_days//365} years) with declining activity"
            ))

        # 8. Random competitor-switch signal (for demo realism)
        if customer.recency_days > 120 and customer.recency_days < 240:
            if random.Random(customer.id).random() < 0.3:
                risk_components.append((
                    ChurnDriver.COMPETITOR_SWITCH,
                    0.55,
                    "Browsing patterns suggest competitor evaluation"
                ))

        # Compute weighted churn probability
        if not risk_components:
            churn_prob = 0.05  # baseline healthy
        else:
            # Combine: 1 - product(1 - p_i)
            survival = 1.0
            for _, p, _ in risk_components:
                survival *= (1.0 - p)
            churn_prob = 1.0 - survival

        # Clamp and add small noise
        churn_prob = max(0.0, min(0.99, churn_prob + random.Random(customer.id + "n").uniform(-0.02, 0.02)))

        # Build signals list
        for driver, severity, desc in risk_components:
            signals.append(ChurnSignal(
                driver=driver,
                severity=int(severity * 10),
                description=desc,
                detected_at=datetime.utcnow().isoformat(),
            ))
        signals.sort(key=lambda s: s.severity, reverse=True)

        return churn_prob, signals


# ============================================================
# INTERVENTION ENGINE
# ============================================================

class InterventionEngine:
    """Manage retention interventions and recommend actions."""

    INTERVENTION_PLAYBOOKS = {
        WatchLevel.SAFE: [],
        WatchLevel.WATCH: [
            ("Send 'We miss you' email with curated picks", InterventionType.EMAIL, "low"),
            ("Add to monthly newsletter with engagement focus", InterventionType.EMAIL, "low"),
        ],
        WatchLevel.ALERT: [
            ("Send 15% discount with 7-day expiry", InterventionType.DISCOUNT_OFFER, "medium"),
            ("Trigger product recommendation email", InterventionType.PRODUCT_RECOMMENDATION, "medium"),
            ("Send NPS survey to gauge satisfaction", InterventionType.SURVEY, "low"),
        ],
        WatchLevel.CRITICAL: [
            ("URGENT: Personal phone call from account manager", InterventionType.PHONE_CALL, "high"),
            ("Send 25-30% retention offer with personal note", InterventionType.DISCOUNT_OFFER, "high"),
            ("Offer free product or service upgrade", InterventionType.LOYALTY_BONUS, "high"),
        ],
        WatchLevel.LOST: [
            ("Final win-back attempt: 40% off + personal letter", InterventionType.WIN_BACK_CAMPAIGN, "high"),
            ("Move to dormant list if no response in 30 days", InterventionType.EMAIL, "low"),
        ],
    }

    @classmethod
    def recommend_actions(cls, level: WatchLevel, signals: list[ChurnSignal]) -> list[str]:
        """Get recommended actions for a watch level."""
        actions = []
        for desc, _, _ in cls.INTERVENTION_PLAYBOOKS.get(level, []):
            actions.append(desc)
        # Add driver-specific actions
        for signal in signals[:3]:
            if signal.driver == ChurnDriver.SUPPORT_ISSUES:
                actions.insert(0, "🔧 Address support ticket backlog first")
            elif signal.driver == ChurnDriver.COMPETITOR_SWITCH:
                actions.insert(0, "🎯 Highlight unique value vs. competitors")
            elif signal.driver == ChurnDriver.PRICE_SENSITIVITY:
                actions.insert(0, "💰 Offer loyalty pricing or payment plan")
        return actions[:5]  # top 5


# ============================================================
# CHURN ENGINE (Main orchestrator)
# ============================================================

class ChurnEngine:
    """Orchestrate churn watch list, alerts, and interventions."""

    def __init__(self, reference_date: Optional[datetime] = None):
        self.reference_date = reference_date or datetime(2026, 8, 27)
        self.customers: list[Customer] = []
        self.alerts: list[ChurnAlert] = []
        self.interventions: list[Intervention] = []
        self.resolved_history: list[ChurnAlert] = []
        self.acknowledged_ids: set[str] = set()

    def run(self, n_customers: int = 200, seed: int = 42) -> dict:
        """Run the full churn analysis pipeline."""
        # Generate or reuse customers
        customers = CustomerDataGenerator.generate_customers(n=n_customers, seed=seed)
        for c in customers:
            RFMAnalyzer.compute_rfm(c, self.reference_date)
        self.customers = customers

        # Analyze each customer
        self.alerts = []
        for c in customers:
            churn_prob, signals = ChurnPredictor.analyze(c, customers, self.reference_date)
            if churn_prob >= 0.20:  # Only include at-risk customers
                alert = self._create_alert(c, churn_prob, signals)
                self.alerts.append(alert)

        # Sort by risk (highest first)
        self.alerts.sort(key=lambda a: a.risk_score, reverse=True)

        # Generate historical interventions
        self._generate_intervention_history()

        return self.get_dashboard_data()

    def _create_alert(self, customer: Customer, churn_prob: float, signals: list[ChurnSignal]) -> ChurnAlert:
        """Create an alert for a customer at risk."""
        level = self._classify_level(churn_prob)
        clv = CLVPredictor.predict_clv(customer)
        monthly_revenue = customer.monetary_score

        # Risk score = churn_prob * 100, weighted by CLV
        clv_weight = min(2.0, clv / 10_000_000)  # high-value customers get more attention
        risk_score = int(min(100, churn_prob * 100 * (0.7 + 0.3 * clv_weight)))

        # Generate intervention history count
        int_count = 0
        if churn_prob > 0.5:
            int_count = random.Random(customer.id + "i").choices([0, 1, 2, 3], weights=[20, 40, 30, 10])[0]

        return ChurnAlert(
            id=f"CHURN-{customer.id}",
            customer_id=customer.id,
            customer_name=customer.name,
            email=customer.email,
            phone=f"+62{random.Random(customer.id + 'p').randint(8000000000, 8999999999)}",
            level=level,
            churn_probability=round(churn_prob, 3),
            risk_score=risk_score,
            clv_at_risk=round(clv, 0),
            monthly_revenue=round(monthly_revenue, 0),
            last_purchase_date=customer.last_purchase_date.isoformat() if customer.last_purchase_date else "never",
            days_since_purchase=customer.recency_days,
            total_orders=customer.total_orders,
            total_spend=round(customer.total_spend, 0),
            segment=self._quick_segment(customer),
            drivers=signals,
            recommended_actions=InterventionEngine.recommend_actions(level, signals),
            assigned_to=random.Random(customer.id + "a").choice(
                [None, "Budi Santoso", "Sari Wijaya", "Hadi Pratama", "Dewi Lestari"]
            ) if churn_prob > 0.5 else None,
            intervention_count=int_count,
            status=random.Random(customer.id + "s").choice(
                ["new", "acknowledged", "in_intervention", "monitoring", "new", "new"]
            ) if churn_prob > 0.5 else "new",
            created_at=(self.reference_date - timedelta(days=random.Random(customer.id + "c").randint(0, 14))).isoformat(),
            acknowledged_at=None,
            resolved_at=None,
            notes=[],
        )

    def _classify_level(self, churn_prob: float) -> WatchLevel:
        if churn_prob < 0.20:
            return WatchLevel.SAFE
        if churn_prob < 0.45:
            return WatchLevel.WATCH
        if churn_prob < 0.70:
            return WatchLevel.ALERT
        if churn_prob < 0.90:
            return WatchLevel.CRITICAL
        return WatchLevel.LOST

    def _quick_segment(self, customer: Customer) -> str:
        """Approximate segment name based on RFM for context."""
        if customer.recency_days < 30 and customer.frequency_score > 1 and customer.monetary_score > 1_000_000:
            return "Champions"
        if customer.recency_days < 60 and customer.frequency_score > 0.5:
            return "Loyal"
        if customer.recency_days < 90 and customer.frequency_score > 0.3:
            return "Need Attention"
        if customer.recency_days < 180 and customer.total_orders > 0:
            return "About to Sleep"
        return "At Risk"

    def _generate_intervention_history(self):
        """Generate historical interventions for context."""
        self.interventions = []
        counter = 1
        for alert in self.alerts[:50]:  # only for top 50 risk
            if alert.intervention_count > 0:
                for i in range(alert.intervention_count):
                    int_type = random.Random(alert.customer_id + str(i)).choice(list(InterventionType))
                    intv = Intervention(
                        id=f"INT-{counter:05d}",
                        customer_id=alert.customer_id,
                        type=int_type,
                        channel=random.Random(alert.customer_id + str(i) + "c").choice(
                            ["Email", "WhatsApp", "Phone", "In-App"]
                        ),
                        subject=random.Random(alert.customer_id + str(i) + "s").choice([
                            "We miss you! Come back with 20% off",
                            "Exclusive offer for valued customer",
                            "Your account summary & special perks",
                            "Help us serve you better",
                        ]),
                        message="Personalized message based on customer history.",
                        status=random.Random(alert.customer_id + str(i) + "st").choice(list(InterventionStatus)),
                        assigned_to=alert.assigned_to or "Auto",
                        created_at=(datetime.fromisoformat(alert.created_at) - timedelta(days=random.Random(alert.customer_id + str(i) + "d").randint(1, 30))).isoformat(),
                        scheduled_for=alert.created_at,
                        completed_at=alert.created_at if random.random() < 0.6 else None,
                        outcome=random.Random(alert.customer_id + str(i) + "o").choice([
                            "Customer opened email",
                            "Customer clicked offer",
                            "No response",
                            "Customer responded positively",
                            "Marked as spam",
                        ]) if random.random() < 0.7 else None,
                        expected_recovery_clv=alert.clv_at_risk * 0.5,
                        actual_recovery_clv=alert.clv_at_risk * random.Random(alert.customer_id + str(i) + "r").uniform(0, 0.6),
                    )
                    self.interventions.append(intv)
                    counter += 1

    def get_dashboard_data(self) -> dict:
        """Build full dashboard response."""
        if not self.alerts:
            return self._empty_dashboard()

        # By level
        by_level = {level.value: 0 for level in WatchLevel}
        for a in self.alerts:
            by_level[a.level.value] = by_level.get(a.level.value, 0) + 1

        # By status
        by_status: dict[str, int] = {}
        for a in self.alerts:
            by_status[a.status] = by_status.get(a.status, 0) + 1

        # Revenue at risk
        total_clv_at_risk = sum(a.clv_at_risk for a in self.alerts)
        total_monthly_at_risk = sum(a.monthly_revenue for a in self.alerts)
        avg_churn = statistics.mean(a.churn_probability for a in self.alerts)

        # Intervention success rate
        completed = [i for i in self.interventions if i.status in (InterventionStatus.COMPLETED, InterventionStatus.CUSTOMER_RESPONDED)]
        success_rate = len(completed) / max(1, len(self.interventions))

        # Recovery this month
        recovery = sum(i.actual_recovery_clv for i in self.interventions if i.actual_recovery_clv > 0)

        # 24h changes (synthetic)
        new_24h = sum(1 for a in self.alerts if a.status == "new")
        resolved_24h = random.Random("24h").randint(2, 8)

        # Top customers at risk
        top_at_risk = sorted(self.alerts, key=lambda a: a.clv_at_risk, reverse=True)[:5]
        top_at_risk_data = [
            {
                "id": a.customer_id,
                "name": a.customer_name,
                "level": a.level.value,
                "clv_at_risk": a.clv_at_risk,
                "churn_probability": a.churn_probability,
                "days_since_purchase": a.days_since_purchase,
            }
            for a in top_at_risk
        ]

        # Recent interventions
        recent_interventions = sorted(self.interventions, key=lambda i: i.created_at, reverse=True)[:10]
        recent_int_data = [i.to_dict() for i in recent_interventions]

        # Driver breakdown
        driver_counts: dict[str, int] = {}
        for a in self.alerts:
            for s in a.drivers:
                driver_counts[s.driver] = driver_counts.get(s.driver, 0) + 1

        # Weekly trend (synthetic)
        trend = {
            "alerts_change_pct": -8.5,  # decreasing = good
            "clv_at_risk_change_pct": -12.3,
            "recovery_change_pct": 23.4,
            "success_rate_change_pct": 4.2,
        }

        return {
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "total_alerts": len(self.alerts),
                "by_level": by_level,
                "by_status": by_status,
                "total_clv_at_risk": round(total_clv_at_risk, 0),
                "total_monthly_revenue_at_risk": round(total_monthly_at_risk, 0),
                "avg_churn_probability": round(avg_churn, 3),
                "intervention_success_rate": round(success_rate, 3),
                "recovery_this_month": round(recovery, 0),
                "new_alerts_24h": new_24h,
                "resolved_alerts_24h": resolved_24h,
                "trends": trend,
            },
            "alerts": [a.to_dict() for a in self.alerts],
            "interventions": recent_int_data,
            "top_at_risk": top_at_risk_data,
            "driver_breakdown": driver_counts,
            "total_customers": len(self.customers),
        }

    def _empty_dashboard(self) -> dict:
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {},
            "alerts": [],
            "interventions": [],
            "top_at_risk": [],
            "driver_breakdown": {},
            "total_customers": 0,
        }

    # ============================================================
    # ACTIONS
    # ============================================================

    def acknowledge_alert(self, alert_id: str, user: str = "system") -> Optional[ChurnAlert]:
        for a in self.alerts:
            if a.id == alert_id:
                a.status = "acknowledged"
                a.acknowledged_at = datetime.utcnow().isoformat()
                a.notes.append(f"Acknowledged by {user} at {datetime.utcnow().isoformat()}")
                return a
        return None

    def resolve_alert(self, alert_id: str, outcome: str, user: str = "system") -> Optional[ChurnAlert]:
        for a in self.alerts:
            if a.id == alert_id:
                a.status = "resolved"
                a.resolved_at = datetime.utcnow().isoformat()
                a.notes.append(f"Resolved by {user}: {outcome}")
                self.resolved_history.append(a)
                self.alerts = [x for x in self.alerts if x.id != alert_id]
                return a
        return None

    def create_intervention(self, alert_id: str, intervention_type: InterventionType,
                            message: str, assigned_to: str, scheduled_for: Optional[str] = None) -> Optional[Intervention]:
        for a in self.alerts:
            if a.id == alert_id:
                intv = Intervention(
                    id=f"INT-{len(self.interventions) + 1:05d}",
                    customer_id=a.customer_id,
                    type=intervention_type,
                    channel="Auto",
                    subject=message[:80],
                    message=message,
                    status=InterventionStatus.PLANNED,
                    assigned_to=assigned_to,
                    created_at=datetime.utcnow().isoformat(),
                    scheduled_for=scheduled_for or datetime.utcnow().isoformat(),
                    completed_at=None,
                    outcome=None,
                    expected_recovery_clv=a.clv_at_risk * 0.4,
                )
                self.interventions.append(intv)
                a.intervention_count += 1
                a.status = "in_intervention"
                a.notes.append(f"Intervention planned: {intervention_type.value} by {assigned_to}")
                return intv
        return None


# ============================================================
# SINGLETON
# ============================================================

_engine_instance: Optional[ChurnEngine] = None
_cached_result: Optional[dict] = None


def get_engine() -> tuple[ChurnEngine, dict]:
    """Get or initialize the global churn engine."""
    global _engine_instance, _cached_result
    if _cached_result is None:
        _engine_instance = ChurnEngine()
        _cached_result = _engine_instance.run(n_customers=200)
    return _engine_instance, _cached_result


def refresh_engine(n: int = 200, seed: int = 42) -> dict:
    """Regenerate churn data."""
    global _engine_instance, _cached_result
    _engine_instance = ChurnEngine()
    _cached_result = _engine_instance.run(n_customers=n, seed=seed)
    return _cached_result
