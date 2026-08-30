"""
AUREA Smart Customer Segmentation
==================================

RFM-based customer segmentation with K-Means clustering.

Features:
- RFM (Recency, Frequency, Monetary) feature engineering
- K-Means clustering on normalized RFM
- Segment profiling & natural-language descriptions
- Customer lifetime value (CLV) prediction
- Churn risk scoring
- Actionable recommendations per segment
- 8 standard segments:
    * Champions (high R, F, M)
    * Loyal Customers (high F, M)
    * Potential Loyalists (recent, frequent)
    * Recent Customers (recent, low F)
    * Promising (recent, moderate F)
    * Need Attention (above-avg but slipping)
    * About to Sleep (below-avg, long recency)
    * At Risk (used to buy, now long recency)
    * Hibernating (long recency, low F)
    * Lost (lowest engagement)
"""

from __future__ import annotations

import math
import random
import statistics
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

# ============================================================
# DATA MODELS
# ============================================================

class Segment(str, Enum):
    CHAMPIONS = "Champions"
    LOYAL = "Loyal Customers"
    POTENTIAL_LOYALIST = "Potential Loyalists"
    RECENT = "Recent Customers"
    PROMISING = "Promising"
    NEED_ATTENTION = "Need Attention"
    ABOUT_TO_SLEEP = "About to Sleep"
    AT_RISK = "At Risk"
    HIBERNATING = "Hibernating"
    LOST = "Lost"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Customer:
    """Customer record for segmentation analysis."""
    id: str
    name: str
    email: str
    registration_date: datetime
    last_purchase_date: Optional[datetime]
    total_orders: int
    total_spend: float          # IDR
    avg_order_value: float      # IDR
    support_tickets: int
    product_categories: list[str]
    preferred_channel: str
    age: int
    city: str
    gender: str
    # Derived
    recency_days: int = 0
    frequency_score: float = 0.0
    monetary_score: float = 0.0

    def to_dict(self):
        d = asdict(self)
        d["registration_date"] = self.registration_date.isoformat()
        d["last_purchase_date"] = self.last_purchase_date.isoformat() if self.last_purchase_date else None
        return d


@dataclass
class SegmentProfile:
    """Aggregated profile for a segment."""
    name: Segment
    description: str
    customer_count: int
    percentage: float
    total_revenue: float
    avg_clv: float
    avg_recency: float
    avg_frequency: float
    avg_monetary: float
    churn_risk: RiskLevel
    color: str
    icon: str
    characteristics: list[str]
    recommendations: list[str]
    sample_customers: list[dict] = field(default_factory=list)

    def to_dict(self):
        d = asdict(self)
        d["name"] = self.name.value
        d["churn_risk"] = self.churn_risk.value
        return d


@dataclass
class CustomerSegment:
    """A single customer's segment assignment."""
    customer_id: str
    customer_name: str
    segment: Segment
    recency_days: int
    frequency: int
    monetary: float
    rfm_score: str
    clv_12m: float
    churn_probability: float
    next_best_action: str

    def to_dict(self):
        d = asdict(self)
        d["segment"] = self.segment.value
        return d


# ============================================================
# RFM FEATURE ENGINEERING
# ============================================================

class RFMAnalyzer:
    """Compute RFM features from customer data."""

    @staticmethod
    def compute_rfm(customer: Customer, reference_date: datetime) -> Customer:
        """Compute recency, frequency, monetary for a customer."""
        # Recency: days since last purchase
        if customer.last_purchase_date:
            customer.recency_days = (reference_date - customer.last_purchase_date).days
        else:
            customer.recency_days = (reference_date - customer.registration_date).days

        # Frequency: orders per month since registration
        months_active = max(1.0, (reference_date - customer.registration_date).days / 30.0)
        customer.frequency_score = customer.total_orders / months_active

        # Monetary: avg monthly spend
        customer.monetary_score = customer.total_spend / months_active

        return customer

    @staticmethod
    def rfm_quintile_scores(customer: Customer, all_customers: list[Customer]) -> tuple[int, int, int]:
        """Score R, F, M on 1-5 scale using quintiles."""
        if not all_customers:
            return (3, 3, 3)

        r_values = sorted([c.recency_days for c in all_customers])
        f_values = sorted([c.frequency_score for c in all_customers])
        m_values = sorted([c.monetary_score for c in all_customers])

        def quintile_score(value: float, values: list[float], reverse: bool) -> int:
            n = len(values)
            if n == 0:
                return 3
            # Find position
            pos = sum(1 for v in values if v <= value)
            pct = pos / n
            if pct <= 0.2: score = 1
            elif pct <= 0.4: score = 2
            elif pct <= 0.6: score = 3
            elif pct <= 0.8: score = 4
            else: score = 5
            return 6 - score if reverse else score

        # Recency: lower is better → reverse
        r_score = quintile_score(customer.recency_days, r_values, reverse=True)
        # Frequency: higher is better → normal
        f_score = quintile_score(customer.frequency_score, f_values, reverse=False)
        # Monetary: higher is better → normal
        m_score = quintile_score(customer.monetary_score, m_values, reverse=False)
        return (r_score, f_score, m_score)


# ============================================================
# K-MEANS CLUSTERING (Simple, pure-Python)
# ============================================================

class KMeans:
    """Lightweight K-Means for RFM segmentation.
    Uses random initialization and Lloyd's algorithm.
    """

    def __init__(self, k: int = 8, max_iter: int = 100, seed: int = 42):
        self.k = k
        self.max_iter = max_iter
        self.seed = seed
        self.centroids: list[list[float]] = []
        self.labels_: list[int] = []

    def _distance(self, a: list[float], b: list[float]) -> float:
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

    def fit(self, X: list[list[float]]):
        if not X:
            return
        rng = random.Random(self.seed)
        n = len(X)
        k = min(self.k, n)

        # K-Means++ initialization for better centroids
        self.centroids = [list(X[rng.randint(0, n - 1)])]
        while len(self.centroids) < k:
            distances = [min(self._distance(x, c) for c in self.centroids) for x in X]
            total = sum(d ** 2 for d in distances)
            if total == 0:
                self.centroids.append(list(X[rng.randint(0, n - 1)]))
                continue
            probs = [(d ** 2) / total for d in distances]
            r = rng.random()
            cum = 0.0
            chosen = 0
            for i, p in enumerate(probs):
                cum += p
                if r <= cum:
                    chosen = i
                    break
            self.centroids.append(list(X[chosen]))

        # Lloyd's algorithm
        for _ in range(self.max_iter):
            # Assign
            new_labels = [self._nearest(x) for x in X]
            # Update
            new_centroids = []
            for j in range(k):
                members = [X[i] for i in range(n) if new_labels[i] == j]
                if members:
                    dim = len(members[0])
                    centroid = [sum(m[d] for m in members) / len(members) for d in range(dim)]
                else:
                    centroid = list(self.centroids[j])
                new_centroids.append(centroid)
            # Check convergence
            shift = sum(self._distance(self.centroids[i], new_centroids[i]) for i in range(k))
            self.centroids = new_centroids
            self.labels_ = new_labels
            if shift < 1e-4:
                break

    def predict(self, X: list[list[float]]) -> list[int]:
        return [self._nearest(x) for x in X]

    def _nearest(self, x: list[float]) -> int:
        return min(range(len(self.centroids)), key=lambda i: self._distance(x, self.centroids[i]))


# ============================================================
# SEGMENT CLASSIFIER
# ============================================================

class SegmentClassifier:
    """Map K-Means clusters to business-meaningful segments.

    Uses a rule-based approach on RFM quintile scores (R, F, M each 1-5)
    to assign the most appropriate business segment.
    """

    @staticmethod
    def classify(r: int, f: int, m: int) -> Segment:
        """Rule-based RFM segmentation."""
        avg = (r + f + m) / 3.0
        # Champions: high on all axes
        if r >= 4 and f >= 4 and m >= 4:
            return Segment.CHAMPIONS
        # Loyal: high frequency & monetary
        if f >= 4 and m >= 3:
            return Segment.LOYAL
        # Potential Loyalists: recent + decent frequency
        if r >= 4 and f >= 2 and m >= 2:
            return Segment.POTENTIAL_LOYALIST
        # Recent Customers: very recent but low frequency
        if r >= 4 and f <= 2:
            return Segment.RECENT
        # Promising: recent, moderate frequency
        if r >= 3 and f >= 2 and avg >= 3:
            return Segment.PROMISING
        # Need Attention: above-average overall, but slipping
        if r == 3 and f >= 3 and m >= 3:
            return Segment.NEED_ATTENTION
        # About to Sleep: recency below avg, frequency below avg
        if r == 2 and f <= 3 and m <= 3:
            return Segment.ABOUT_TO_SLEEP
        # At Risk: was valuable, now long recency
        if r <= 2 and f >= 3 and m >= 3:
            return Segment.AT_RISK
        # Hibernating: long recency, low frequency
        if r <= 2 and f <= 2:
            return Segment.HIBERNATING
        # Lost: very low across the board
        if avg < 1.8:
            return Segment.LOST
        # Default: need attention
        return Segment.NEED_ATTENTION


# ============================================================
# CLV & CHURN PREDICTION
# ============================================================

class CLVPredictor:
    """Simple CLV & churn probability prediction.

    CLV = avg_monthly_spend × 12 × retention_rate
    Churn probability based on recency + support tickets + RFM
    """

    @staticmethod
    def predict_clv(customer: Customer) -> float:
        """12-month CLV projection in IDR."""
        if customer.frequency_score == 0:
            return 0.0
        # Expected monthly spend
        monthly = customer.monetary_score
        # Retention probability (1 - churn probability)
        churn = CLVPredictor.predict_churn_probability(customer)
        retention = max(0.05, 1.0 - churn)
        # 12-month CLV with discount factor (simple 10% annual)
        clv = 0.0
        for m in range(1, 13):
            clv += monthly * (retention ** m) * (0.99 ** m)
        return clv

    @staticmethod
    def predict_churn_probability(customer: Customer) -> float:
        """Predict churn probability [0, 1]."""
        # Base churn on recency
        if customer.recency_days <= 30:
            recency_churn = 0.05
        elif customer.recency_days <= 60:
            recency_churn = 0.15
        elif customer.recency_days <= 90:
            recency_churn = 0.30
        elif customer.recency_days <= 180:
            recency_churn = 0.55
        else:
            recency_churn = 0.80

        # Adjust by frequency
        if customer.frequency_score >= 2:
            recency_churn *= 0.6
        elif customer.frequency_score >= 1:
            recency_churn *= 0.8

        # Adjust by support tickets
        ticket_penalty = min(0.20, customer.support_tickets * 0.03)
        churn = min(0.95, recency_churn + ticket_penalty)
        return churn

    @staticmethod
    def risk_level(churn_prob: float) -> RiskLevel:
        if churn_prob < 0.20:
            return RiskLevel.LOW
        elif churn_prob < 0.45:
            return RiskLevel.MEDIUM
        elif churn_prob < 0.70:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

    @staticmethod
    def next_best_action(customer: Customer, segment: Segment) -> str:
        """Recommend the next best action for a customer."""
        if segment in (Segment.CHAMPIONS, Segment.LOYAL):
            return "Offer VIP program, early access to new products, and personal thank-you."
        if segment == Segment.POTENTIAL_LOYALIST:
            return "Recommend products based on browsing history, offer loyalty enrollment."
        if segment == Segment.RECENT:
            return "Send welcome series + first-purchase incentive (10% off second order)."
        if segment == Segment.PROMISING:
            return "Cross-sell related products; offer free shipping on next order."
        if segment == Segment.NEED_ATTENTION:
            return "Send personalized re-engagement email with curated picks."
        if segment == Segment.ABOUT_TO_SLEEP:
            return "Win-back campaign: 20% discount + product recommendations."
        if segment == Segment.AT_RISK:
            return "URGENT: Personal outreach from account manager + exclusive retention offer."
        if segment == Segment.HIBERNATING:
            return "Reactivation campaign: 'We miss you' with strong discount (25-30%)."
        return "Survey to understand disengagement; consider sunset communication."


# ============================================================
# MOCK DATA GENERATION
# ============================================================

class CustomerDataGenerator:
    """Generate realistic Indonesian customer dataset for demo."""

    FIRST_NAMES = [
        "Budi", "Siti", "Agus", "Dewi", "Eko", "Fitri", "Hadi", "Indah", "Joko", "Kartika",
        "Lutfi", "Maya", "Nanda", "Oki", "Putri", "Rizky", "Sari", "Toni", "Umi", "Vina",
        "Wahyu", "Yanti", "Zaki", "Ahmad", "Bayu", "Citra", "Dedi", "Erna", "Fajar", "Gita",
        "Hendra", "Irma", "Jaka", "Kiki", "Lina", "Made", "Nia", "Omar", "Putra", "Ratna"
    ]
    LAST_NAMES = [
        "Santoso", "Wijaya", "Pratama", "Lestari", "Sukma", "Rahmawati", "Setiawan", "Anggraini",
        "Wibowo", "Sari", "Putri", "Hidayat", "Nugroho", "Maharani", "Saputra", "Permata",
        "Kusuma", "Handayani", "Maulana", "Safitri"
    ]
    CITIES = [
        "Jakarta", "Surabaya", "Bandung", "Medan", "Semarang", "Makassar", "Palembang",
        "Tangerang", "Depok", "Bekasi", "Bogor", "Yogyakarta", "Malang", "Denpasar", "Cilegon"
    ]
    CATEGORIES = [
        "Electronics", "Fashion", "Groceries", "Beauty", "Home & Living",
        "Sports", "Books", "Toys", "Health", "Automotive"
    ]
    CHANNELS = ["Mobile App", "Website", "Marketplace", "Branch Office", "Call Center"]

    @classmethod
    def generate_customers(cls, n: int = 200, seed: int = 42) -> list[Customer]:
        rng = random.Random(seed)
        reference = datetime(2026, 8, 27)
        customers = []

        for i in range(n):
            first = rng.choice(cls.FIRST_NAMES)
            last = rng.choice(cls.LAST_NAMES)
            name = f"{first} {last}"
            # Registration: 0-3 years ago
            reg_days_ago = rng.randint(30, 1095)
            reg_date = reference - timedelta(days=reg_days_ago)

            # Customer archetype probabilities
            archetype = rng.random()
            if archetype < 0.15:  # Champions
                last_days_ago = rng.randint(1, 30)
                orders = rng.randint(20, 60)
                avg_value = rng.uniform(500_000, 2_500_000)
            elif archetype < 0.30:  # Loyal
                last_days_ago = rng.randint(15, 60)
                orders = rng.randint(10, 30)
                avg_value = rng.uniform(300_000, 1_500_000)
            elif archetype < 0.45:  # Potential Loyalist
                last_days_ago = rng.randint(5, 45)
                orders = rng.randint(5, 15)
                avg_value = rng.uniform(200_000, 800_000)
            elif archetype < 0.55:  # Recent
                last_days_ago = rng.randint(1, 30)
                orders = rng.randint(1, 3)
                avg_value = rng.uniform(100_000, 500_000)
            elif archetype < 0.70:  # Promising
                last_days_ago = rng.randint(20, 60)
                orders = rng.randint(3, 10)
                avg_value = rng.uniform(150_000, 600_000)
            elif archetype < 0.80:  # Need Attention / About to Sleep
                last_days_ago = rng.randint(60, 150)
                orders = rng.randint(3, 12)
                avg_value = rng.uniform(100_000, 500_000)
            elif archetype < 0.90:  # At Risk
                last_days_ago = rng.randint(90, 240)
                orders = rng.randint(5, 20)
                avg_value = rng.uniform(200_000, 1_200_000)
            else:  # Hibernating / Lost
                last_days_ago = rng.randint(180, 720)
                orders = rng.randint(0, 5)
                avg_value = rng.uniform(50_000, 300_000)

            total_spend = orders * avg_value
            n_categories = rng.randint(1, 3)
            cats = rng.sample(cls.CATEGORIES, n_categories)

            cust = Customer(
                id=f"CUST-{str(i+1).zfill(5)}",
                name=name,
                email=f"{first.lower()}.{last.lower()}@{'gmail.com' if rng.random() < 0.7 else 'yahoo.co.id'}",
                registration_date=reg_date,
                last_purchase_date=reference - timedelta(days=last_days_ago),
                total_orders=orders,
                total_spend=round(total_spend, 0),
                avg_order_value=round(avg_value, 0),
                support_tickets=rng.choices([0, 1, 2, 3, 5], weights=[60, 25, 8, 5, 2])[0],
                product_categories=cats,
                preferred_channel=rng.choice(cls.CHANNELS),
                age=rng.randint(20, 65),
                city=rng.choice(cls.CITIES),
                gender=rng.choice(["M", "F"]),
            )
            customers.append(cust)

        return customers


# ============================================================
# SEGMENTATION ENGINE
# ============================================================

class SegmentationEngine:
    """Orchestrate the full segmentation pipeline."""

    def __init__(self, reference_date: Optional[datetime] = None):
        self.reference_date = reference_date or datetime(2026, 8, 27)
        self.customers: list[Customer] = []
        self.assignments: list[CustomerSegment] = []
        self.profiles: list[SegmentProfile] = []

    def run(self, customers: list[Customer]) -> dict:
        """Run the full pipeline and return results."""
        # Step 1: Compute RFM
        for c in customers:
            RFMAnalyzer.compute_rfm(c, self.reference_date)

        # Step 2: Quintile scoring
        rfm_scores = {c.id: RFMAnalyzer.rfm_quintile_scores(c, customers) for c in customers}

        # Step 3: K-Means clustering (confirmation layer)
        # Normalize RFM for K-Means
        r_norm = self._normalize([c.recency_days for c in customers], reverse=True)
        f_norm = self._normalize([c.frequency_score for c in customers])
        m_norm = self._normalize([c.monetary_score for c in customers])
        X = list(zip(r_norm, f_norm, m_norm))
        kmeans = KMeans(k=8, max_iter=50)
        kmeans.fit([list(x) for x in X])

        # Step 4: Classify into business segments
        assignments = []
        for i, c in enumerate(customers):
            r, f, m = rfm_scores[c.id]
            segment = SegmentClassifier.classify(r, f, m)
            churn = CLVPredictor.predict_churn_probability(c)
            clv = CLVPredictor.predict_clv(c)
            nba = CLVPredictor.next_best_action(c, segment)
            assignments.append(CustomerSegment(
                customer_id=c.id,
                customer_name=c.name,
                segment=segment,
                recency_days=c.recency_days,
                frequency=c.total_orders,
                monetary=round(c.total_spend, 0),
                rfm_score=f"{r}{f}{m}",
                clv_12m=round(clv, 0),
                churn_probability=round(churn, 3),
                next_best_action=nba,
            ))
        self.assignments = assignments

        # Step 5: Build segment profiles
        self.profiles = self._build_profiles(customers, assignments)
        self.customers = customers

        return {
            "reference_date": self.reference_date.isoformat(),
            "total_customers": len(customers),
            "segments": [p.to_dict() for p in self.profiles],
            "assignments": [a.to_dict() for a in assignments],
            "summary": self._summary(),
        }

    def _normalize(self, values: list[float], reverse: bool = False) -> list[float]:
        """Min-max normalize to [0, 1]."""
        if not values:
            return []
        vmin, vmax = min(values), max(values)
        if vmax == vmin:
            return [0.5] * len(values)
        normalized = [(v - vmin) / (vmax - vmin) for v in values]
        if reverse:
            normalized = [1.0 - n for n in normalized]
        return normalized

    def _build_profiles(self, customers: list[Customer], assignments: list[CustomerSegment]) -> list[SegmentProfile]:
        """Build aggregate profiles for each segment."""
        # Group customers by segment
        by_segment: dict[Segment, list[tuple[Customer, CustomerSegment]]] = {}
        for c, a in zip(customers, assignments):
            by_segment.setdefault(a.segment, []).append((c, a))

        profiles = []
        for segment in Segment:
            entries = by_segment.get(segment, [])
            if not entries:
                continue
            custs = [e[0] for e in entries]
            assigns = [e[1] for e in entries]

            total_revenue = sum(c.total_spend for c in custs)
            avg_clv = statistics.mean(a.clv_12m for a in assigns) if assigns else 0
            avg_recency = statistics.mean(c.recency_days for c in custs)
            avg_freq = statistics.mean(c.frequency_score for c in custs)
            avg_mon = statistics.mean(c.monetary_score for c in custs)
            avg_churn = statistics.mean(a.churn_probability for a in assigns)
            risk = CLVPredictor.risk_level(avg_churn)
            pct = (len(entries) / len(customers)) * 100

            # Sample customers (top 5 by CLV)
            top5 = sorted(entries, key=lambda e: e[1].clv_12m, reverse=True)[:5]
            samples = [
                {"id": c.id, "name": c.name, "clv": a.clv_12m, "rfm": a.rfm_score}
                for c, a in top5
            ]

            profile = SegmentProfile(
                name=segment,
                description=SEGMENT_DESCRIPTIONS[segment]["description"],
                customer_count=len(entries),
                percentage=round(pct, 1),
                total_revenue=round(total_revenue, 0),
                avg_clv=round(avg_clv, 0),
                avg_recency=round(avg_recency, 0),
                avg_frequency=round(avg_freq, 2),
                avg_monetary=round(avg_mon, 0),
                churn_risk=risk,
                color=SEGMENT_DESCRIPTIONS[segment]["color"],
                icon=SEGMENT_DESCRIPTIONS[segment]["icon"],
                characteristics=SEGMENT_DESCRIPTIONS[segment]["characteristics"],
                recommendations=SEGMENT_DESCRIPTIONS[segment]["recommendations"],
                sample_customers=samples,
            )
            profiles.append(profile)

        # Sort by total revenue descending
        profiles.sort(key=lambda p: p.total_revenue, reverse=True)
        return profiles

    def _summary(self) -> dict:
        """Build overall summary statistics."""
        if not self.assignments:
            return {}
        total_clv = sum(a.clv_12m for a in self.assignments)
        avg_clv = total_clv / len(self.assignments)
        total_revenue = sum(c.total_spend for c in self.customers)
        at_risk_count = sum(1 for a in self.assignments if a.churn_probability > 0.5)
        champion_count = sum(1 for a in self.assignments if a.segment == Segment.CHAMPIONS)
        return {
            "total_customers": len(self.customers),
            "total_revenue": round(total_revenue, 0),
            "total_predicted_clv_12m": round(total_clv, 0),
            "avg_clv_12m": round(avg_clv, 0),
            "champions": champion_count,
            "at_risk": at_risk_count,
            "segment_count": len(self.profiles),
        }


# ============================================================
# SEGMENT METADATA
# ============================================================

SEGMENT_DESCRIPTIONS = {
    Segment.CHAMPIONS: {
        "description": "Bought recently, buy often, and spend the most. Your most loyal, highest-value customers.",
        "color": "#D4AF37",
        "icon": "🏆",
        "characteristics": [
            "Recency < 30 days",
            "High order frequency (>2/month)",
            "Top 20% spenders",
            "Low churn risk (<10%)",
        ],
        "recommendations": [
            "Invite to VIP program with exclusive perks",
            "Offer early access to new products",
            "Personal thank-you notes from CEO/management",
            "Referral program with premium rewards",
        ],
    },
    Segment.LOYAL: {
        "description": "Consistent buyers with above-average spend. The reliable backbone of revenue.",
        "color": "#FFD764",
        "icon": "⭐",
        "characteristics": [
            "Regular purchase pattern",
            "Frequency > 1/month",
            "Above-average spend",
            "Low-to-medium churn risk",
        ],
        "recommendations": [
            "Cross-sell premium product lines",
            "Offer loyalty points booster (2x on next order)",
            "Invite to beta-test new features",
        ],
    },
    Segment.POTENTIAL_LOYALIST: {
        "description": "Recent customers with growing frequency. Could become loyalists with right nurturing.",
        "color": "#16A34A",
        "icon": "🌱",
        "characteristics": [
            "First purchase within 30-45 days",
            "2-5 orders placed",
            "Moderate spend",
            "Medium churn risk",
        ],
        "recommendations": [
            "Onboarding email series with educational content",
            "Second-purchase incentive (15% off)",
            "Product recommendations based on browsing",
        ],
    },
    Segment.RECENT: {
        "description": "Just made their first purchase. Critical window to establish habit.",
        "color": "#0284C7",
        "icon": "👋",
        "characteristics": [
            "Single purchase within last 30 days",
            "Low frequency",
            "Lower initial spend",
            "Unknown long-term value",
        ],
        "recommendations": [
            "Welcome series (3-5 emails over 14 days)",
            "Onboarding tutorial for mobile app",
            "First-30-day satisfaction check-in call",
        ],
    },
    Segment.PROMISING: {
        "description": "Engaged recently with decent purchase frequency. Show potential for growth.",
        "color": "#0EA5E9",
        "icon": "📈",
        "characteristics": [
            "Recent activity (within 60 days)",
            "Moderate frequency (3-10 orders)",
            "Average spend",
            "Low-to-medium churn",
        ],
        "recommendations": [
            "Free shipping on next order",
            "Bundle recommendations (frequently bought together)",
            "Birthday/anniversary perks",
        ],
    },
    Segment.NEED_ATTENTION: {
        "description": "Above-average customers whose activity is starting to slip. Intervention needed.",
        "color": "#EA580C",
        "icon": "⚠️",
        "characteristics": [
            "Used to buy frequently, now slowing",
            "Recency 60-90 days",
            "Historical value was high",
            "Medium-to-high churn risk",
        ],
        "recommendations": [
            "Personal re-engagement email from account manager",
            "Survey to identify pain points",
            "Targeted discount on previously-bought categories",
        ],
    },
    Segment.ABOUT_TO_SLEEP: {
        "description": "Below-average activity with slipping recency. Wake them up before they're gone.",
        "color": "#F59E0B",
        "icon": "😴",
        "characteristics": [
            "Recency 90-150 days",
            "Low-to-moderate frequency",
            "Drop in engagement",
            "High churn risk",
        ],
        "recommendations": [
            "Win-back campaign with 20% discount",
            "Show new arrivals in their favorite categories",
            "Limited-time free gift with next order",
        ],
    },
    Segment.AT_RISK: {
        "description": "Were high-value, now long recency. URGENT: aggressive retention needed.",
        "color": "#DC2626",
        "icon": "🚨",
        "characteristics": [
            "Recency > 90 days",
            "High historical spend",
            "Was frequent buyer",
            "Critical churn risk",
        ],
        "recommendations": [
            "URGENT: Personal call from account manager",
            "Exclusive 30% retention offer",
            "Survey + win-back incentive package",
            "Consider if competitor switch occurred",
        ],
    },
    Segment.HIBERNATING: {
        "description": "Long-time inactive, low frequency. Reactivation is the only path forward.",
        "color": "#6B7280",
        "icon": "💤",
        "characteristics": [
            "Recency > 180 days",
            "Very low frequency",
            "Low historical spend",
            "Critical churn risk",
        ],
        "recommendations": [
            "Reactivation: 'We miss you' with 25-30% off",
            "Show what's new since their last visit",
            "Consider sunset from active marketing",
        ],
    },
    Segment.LOST: {
        "description": "Disengaged completely. Lowest priority for retention, but worth one final attempt.",
        "color": "#374151",
        "icon": "👻",
        "characteristics": [
            "Recency > 365 days",
            "Minimal historical engagement",
            "No recent activity",
            "Effectively churned",
        ],
        "recommendations": [
            "Final win-back email with strong incentive",
            "If no response, move to dormant list",
            "Reduce marketing spend on this segment",
        ],
    },
}


# ============================================================
# SINGLETON ACCESSOR
# ============================================================

_engine_instance: Optional[SegmentationEngine] = None
_cached_customers: Optional[list[Customer]] = None
_cached_result: Optional[dict] = None


def get_engine() -> tuple[SegmentationEngine, dict]:
    """Get or initialize the global engine with default data."""
    global _engine_instance, _cached_customers, _cached_result
    if _cached_result is None:
        _engine_instance = SegmentationEngine()
        _cached_customers = CustomerDataGenerator.generate_customers(n=200)
        _cached_result = _engine_instance.run(_cached_customers)
    return _engine_instance, _cached_result


def refresh_engine(n: int = 200, seed: int = 42) -> dict:
    """Refresh the global engine with new random data."""
    global _engine_instance, _cached_customers, _cached_result
    _engine_instance = SegmentationEngine()
    _cached_customers = CustomerDataGenerator.generate_customers(n=n, seed=seed)
    _cached_result = _engine_instance.run(_cached_customers)
    return _cached_result
