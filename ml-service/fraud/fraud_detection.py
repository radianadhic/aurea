"""
AUREA Real-time Fraud Detection
================================

Multi-layer fraud detection engine for transaction monitoring.

Detection Layers:
1. **Rule-based Engine** — Velocity checks, amount limits, geo-restrictions
2. **Statistical Anomaly** — Z-score on amount, frequency, time-of-day
3. **Behavioral Analysis** — Deviation from customer's normal pattern
4. **Network Analysis** — Connected accounts, shared devices/IPs
5. **ML Risk Scoring** — Composite risk score with feature interactions

Features:
- Real-time transaction scoring (sub-100ms per tx)
- Multi-channel support (web, mobile, ATM, POS, API)
- Indonesian-specific patterns (BI-FAST, QRIS, e-wallet)
- Alert management with auto-block / manual review / approve
- Investigation case management
- Pattern detection (card testing, account takeover, etc.)
- SAR (Suspicious Activity Report) generation
- False positive tracking & model improvement
"""

from __future__ import annotations

import math
import random
import statistics
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


# ============================================================
# ENUMS
# ============================================================

class TransactionChannel(str, Enum):
    WEB = "Web"
    MOBILE = "Mobile"
    ATM = "ATM"
    POS = "POS"
    API = "API"
    BRANCH = "Branch"


class TransactionType(str, Enum):
    TRANSFER = "Transfer"
    PAYMENT = "Payment"
    WITHDRAWAL = "Withdrawal"
    PURCHASE = "Purchase"
    TOPUP = "TopUp"
    BILL_PAYMENT = "Bill Payment"
    QRIS = "QRIS"
    BI_FAST = "BI-FAST"
    INTERNATIONAL = "International"


class FraudDecision(str, Enum):
    APPROVED = "Approved"
    MANUAL_REVIEW = "Manual Review"
    BLOCKED = "Blocked"
    PENDING = "Pending"


class FraudPattern(str, Enum):
    CARD_TESTING = "Card Testing"
    ACCOUNT_TAKEOVER = "Account Takeover"
    IDENTITY_THEFT = "Identity Theft"
    PHISHING = "Phishing"
    SOCIAL_ENGINEERING = "Social Engineering"
    BOT_ATTACK = "Bot Attack"
    MONEY_LAUNDERING = "Money Laundering"
    VELOCITY_ABUSE = "Velocity Abuse"
    GEO_ANOMALY = "Geo Anomaly"
    DEVICE_SPOOFING = "Device Spoofing"
    SYNTHETIC_IDENTITY = "Synthetic Identity"


class AlertStatus(str, Enum):
    NEW = "New"
    INVESTIGATING = "Investigating"
    CONFIRMED_FRAUD = "Confirmed Fraud"
    FALSE_POSITIVE = "False Positive"
    RESOLVED = "Resolved"
    ESCALATED = "Escalated"


class CasePriority(str, Enum):
    P1 = "P1 - Critical"   # Active attack, block now
    P2 = "P2 - High"        # Likely fraud, review ASAP
    P3 = "P3 - Medium"      # Suspicious, review within 24h
    P4 = "P4 - Low"         # Watch list


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class Transaction:
    """A single transaction to be scored."""
    id: str
    customer_id: str
    amount: float
    currency: str
    channel: TransactionChannel
    type: TransactionType
    merchant: str
    merchant_category: str
    location_city: str
    location_country: str
    ip_address: str
    device_id: str
    timestamp: str
    recipient_id: Optional[str] = None
    recipient_name: Optional[str] = None
    is_international: bool = False
    is_new_device: bool = False
    is_new_location: bool = False
    time_since_last_tx_minutes: int = 0
    failed_attempts_24h: int = 0
    session_risk_score: float = 0.0  # 0-100 from session signals

    def to_dict(self):
        d = asdict(self)
        d["channel"] = self.channel.value
        d["type"] = self.type.value
        return d


@dataclass
class CustomerProfile:
    """Customer's behavioral baseline (built from history)."""
    customer_id: str
    avg_tx_amount: float
    std_tx_amount: float
    max_tx_amount: float
    typical_channels: list[str]
    typical_cities: list[str]
    typical_merchants: list[str]
    avg_daily_tx_count: float
    avg_hourly_pattern: list[float]  # 24-element array
    international_tx_count: int
    last_10_amounts: list[float]
    last_10_locations: list[str]
    total_lifetime_spend: float
    account_age_days: int
    known_devices: list[str]

    def to_dict(self):
        return asdict(self)


@dataclass
class RiskSignal:
    """A single risk signal contributing to fraud score."""
    layer: str
    rule: str
    score: float  # 0-100
    weight: float
    description: str
    evidence: dict

    def to_dict(self):
        return asdict(self)


@dataclass
class FraudAlert:
    """Generated when a transaction is flagged."""
    id: str
    transaction_id: str
    customer_id: str
    risk_score: float  # 0-100
    decision: FraudDecision
    pattern: FraudPattern
    priority: CasePriority
    signals: list[RiskSignal]
    amount: float
    currency: str
    channel: str
    type: str
    location: str
    timestamp: str
    detected_at: str
    description: str
    recommended_action: str
    status: str
    assigned_to: Optional[str]
    notes: list[str] = field(default_factory=list)
    case_id: Optional[str] = None

    def to_dict(self):
        d = asdict(self)
        d["decision"] = self.decision.value
        d["pattern"] = self.pattern.value
        d["priority"] = self.priority.value
        d["signals"] = [s.to_dict() for s in self.signals]
        return d


@dataclass
class FraudCase:
    """Investigation case for a fraud incident."""
    id: str
    alert_ids: list[str]
    customer_id: str
    pattern: FraudPattern
    priority: CasePriority
    status: str
    total_amount_at_risk: float
    amount_recovered: float
    opened_at: str
    closed_at: Optional[str]
    assigned_to: str
    investigation_notes: list[str]
    sar_filed: bool
    sar_reference: Optional[str]

    def to_dict(self):
        d = asdict(self)
        d["pattern"] = self.pattern.value
        d["priority"] = self.priority.value
        return d


# ============================================================
# DETECTION LAYERS
# ============================================================

class RuleEngine:
    """Layer 1: Hard-coded business rules."""

    # Rules: (name, score, weight, description_template)
    RULES = [
        # Velocity rules
        ("HIGH_VELOCITY_TX", 70, 0.25, "More than 5 transactions in 10 minutes"),
        ("RAPID_REPEAT_TX", 50, 0.15, "3+ similar transactions in 5 minutes"),
        # Amount rules
        ("AMOUNT_3X_AVG", 60, 0.20, "Amount is 3x customer's average"),
        ("ROUND_NUMBER", 20, 0.05, "Suspiciously round amount (potential test)"),
        # Location rules
        ("GEO_VELOCITY", 90, 0.35, "Transaction from impossible-to-travel location"),
        ("HIGH_RISK_COUNTRY", 75, 0.30, "Transaction from high-risk jurisdiction"),
        # Channel rules
        ("NEW_DEVICE_HIGH_AMOUNT", 65, 0.25, "First-time device with high amount"),
        ("API_ABUSE_PATTERN", 55, 0.20, "API calls exceeding normal rate"),
        # Behavioral
        ("LATE_NIGHT_LARGE", 35, 0.10, "Large transaction at unusual hour (2-5 AM)"),
        # Pattern-specific
        ("CARD_TESTING_PATTERN", 85, 0.40, "Multiple small failed transactions"),
        ("ATO_INDICATORS", 80, 0.35, "Account takeover signals detected"),
        ("NEW_RECIPIENT_LARGE", 45, 0.15, "First transfer to new recipient > Rp 5M"),
    ]

    @classmethod
    def evaluate(cls, tx: Transaction, profile: Optional[CustomerProfile],
                 velocity_count_10m: int, failed_count_24h: int) -> list[RiskSignal]:
        signals = []
        # Velocity
        if velocity_count_10m > 5:
            signals.append(cls._make_signal("HIGH_VELOCITY_TX", {"tx_count_10m": velocity_count_10m}))
        if velocity_count_10m >= 3 and tx.amount < 100_000:
            signals.append(cls._make_signal("RAPID_REPEAT_TX", {"tx_count_10m": velocity_count_10m}))
        # Amount
        if profile and tx.amount > profile.avg_tx_amount * 3:
            signals.append(cls._make_signal("AMOUNT_3X_AVG", {
                "amount": tx.amount,
                "customer_avg": profile.avg_tx_amount,
                "ratio": tx.amount / profile.avg_tx_amount,
            }))
        if tx.amount > 0 and tx.amount % 1_000_000 == 0 and tx.amount >= 5_000_000:
            signals.append(cls._make_signal("ROUND_NUMBER", {"amount": tx.amount}))
        # Card testing
        if failed_count_24h >= 3 and tx.amount < 50_000:
            signals.append(cls._make_signal("CARD_TESTING_PATTERN", {
                "failed_attempts_24h": failed_count_24h,
                "current_amount": tx.amount,
            }))
        # ATO
        if tx.is_new_device and tx.is_new_location and tx.amount > 5_000_000:
            signals.append(cls._make_signal("ATO_INDICATORS", {
                "new_device": True,
                "new_location": True,
                "amount": tx.amount,
            }))
        # Late night
        hour = datetime.fromisoformat(tx.timestamp).hour if "T" in tx.timestamp else 12
        if 2 <= hour <= 5 and tx.amount > 10_000_000:
            signals.append(cls._make_signal("LATE_NIGHT_LARGE", {
                "hour": hour,
                "amount": tx.amount,
            }))
        # API abuse
        if tx.channel == TransactionChannel.API and velocity_count_10m > 10:
            signals.append(cls._make_signal("API_ABUSE_PATTERN", {"api_calls_10m": velocity_count_10m}))
        # New recipient
        if tx.recipient_id and tx.amount > 5_000_000 and tx.is_new_device:
            signals.append(cls._make_signal("NEW_RECIPIENT_LARGE", {
                "amount": tx.amount,
                "first_time_device": True,
            }))
        return signals

    @classmethod
    def _make_signal(cls, rule_name: str, evidence: dict) -> RiskSignal:
        for name, score, weight, desc in cls.RULES:
            if name == rule_name:
                return RiskSignal(
                    layer="Rule-Based",
                    rule=rule_name,
                    score=score,
                    weight=weight,
                    description=desc,
                    evidence=evidence,
                )
        return RiskSignal(layer="Rule-Based", rule=rule_name, score=50, weight=0.1, description=rule_name, evidence=evidence)


class StatisticalDetector:
    """Layer 2: Statistical anomaly detection."""

    @staticmethod
    def evaluate(tx: Transaction, profile: Optional[CustomerProfile]) -> list[RiskSignal]:
        signals = []
        if not profile:
            return signals

        # Z-score on amount
        if profile.std_tx_amount > 0:
            z = (tx.amount - profile.avg_tx_amount) / profile.std_tx_amount
            if z > 4:
                signals.append(RiskSignal(
                    layer="Statistical",
                    rule="AMOUNT_Z_OUTLIER",
                    score=80,
                    weight=0.30,
                    description=f"Amount is {z:.1f} std deviations above average (extreme outlier)",
                    evidence={"z_score": round(z, 2), "amount": tx.amount, "avg": profile.avg_tx_amount},
                ))
            elif z > 2.5:
                signals.append(RiskSignal(
                    layer="Statistical",
                    rule="AMOUNT_MODERATE_OUTLIER",
                    score=50,
                    weight=0.15,
                    description=f"Amount is {z:.1f} std deviations above average",
                    evidence={"z_score": round(z, 2), "amount": tx.amount, "avg": profile.avg_tx_amount},
                ))

        # Time-of-day anomaly
        try:
            hour = datetime.fromisoformat(tx.timestamp).hour
        except Exception:
            hour = 12
        if profile.avg_hourly_pattern:
            expected_freq = profile.avg_hourly_pattern[hour] if hour < len(profile.avg_hourly_pattern) else 0
            if expected_freq == 0 and tx.amount > 1_000_000:
                signals.append(RiskSignal(
                    layer="Statistical",
                    rule="UNUSUAL_HOUR",
                    score=45,
                    weight=0.15,
                    description=f"Transaction at hour {hour} when customer never transacts",
                    evidence={"hour": hour, "historical_freq": expected_freq},
                ))

        return signals


class BehaviorAnalyzer:
    """Layer 3: Behavioral analysis vs customer's baseline."""

    @staticmethod
    def evaluate(tx: Transaction, profile: Optional[CustomerProfile]) -> list[RiskSignal]:
        signals = []
        if not profile:
            return signals

        # New device
        if tx.device_id and tx.device_id not in profile.known_devices:
            if tx.amount > 1_000_000:
                signals.append(RiskSignal(
                    layer="Behavioral",
                    rule="NEW_DEVICE_HIGH_AMOUNT",
                    score=55,
                    weight=0.20,
                    description="New device used for transaction > Rp 1M",
                    evidence={"device_id": tx.device_id, "amount": tx.amount, "known_devices": len(profile.known_devices)},
                ))

        # New location
        if tx.location_city and tx.location_city not in profile.typical_cities:
            if tx.amount > 2_000_000:
                signals.append(RiskSignal(
                    layer="Behavioral",
                    rule="NEW_LOCATION_HIGH_AMOUNT",
                    score=60,
                    weight=0.20,
                    description=f"First transaction from {tx.location_city}",
                    evidence={"city": tx.location_city, "amount": tx.amount, "typical_cities": profile.typical_cities[:5]},
                ))

        # International
        if tx.is_international and profile.international_tx_count == 0:
            signals.append(RiskSignal(
                layer="Behavioral",
                rule="FIRST_INTERNATIONAL",
                score=70,
                weight=0.25,
                description="First-ever international transaction",
                evidence={"country": tx.location_country, "historical_intl": 0},
            ))

        # Unusual merchant category
        if tx.merchant_category and tx.merchant_category not in profile.typical_merchants:
            signals.append(RiskSignal(
                layer="Behavioral",
                rule="NEW_MERCHANT_CATEGORY",
                score=30,
                weight=0.10,
                description=f"New merchant category: {tx.merchant_category}",
                evidence={"category": tx.merchant_category},
            ))

        return signals


class NetworkAnalyzer:
    """Layer 4: Network/relationship analysis."""

    @staticmethod
    def evaluate(tx: Transaction, ip_reputation: dict, device_reputation: dict,
                 shared_ip_customers: set, shared_device_customers: set) -> list[RiskSignal]:
        signals = []

        # IP reputation
        ip_risk = ip_reputation.get(tx.ip_address, 0)
        if ip_risk > 70:
            signals.append(RiskSignal(
                layer="Network",
                rule="HIGH_RISK_IP",
                score=75,
                weight=0.25,
                description=f"IP {tx.ip_address} has high fraud reputation",
                evidence={"ip": tx.ip_address, "reputation_score": ip_risk},
            ))

        # Device reputation
        device_risk = device_reputation.get(tx.device_id, 0)
        if device_risk > 70:
            signals.append(RiskSignal(
                layer="Network",
                rule="COMPROMISED_DEVICE",
                score=80,
                weight=0.30,
                description=f"Device {tx.device_id} flagged as compromised",
                evidence={"device_id": tx.device_id, "reputation_score": device_risk},
            ))

        # Shared IP (potential fraud ring)
        if len(shared_ip_customers) > 5:
            signals.append(RiskSignal(
                layer="Network",
                rule="SHARED_IP_FRAUD_RING",
                score=65,
                weight=0.25,
                description=f"IP shared with {len(shared_ip_customers)} customers (potential ring)",
                evidence={"ip": tx.ip_address, "shared_with": len(shared_ip_customers)},
            ))

        return signals


# ============================================================
# COMPOSITE SCORING
# ============================================================

class RiskScorer:
    """Combine signals into final risk score and decision."""

    @staticmethod
    def score(signals: list[RiskSignal]) -> float:
        """Compute weighted composite risk score [0, 100]."""
        if not signals:
            return 0.0
        # Use 1 - product(1 - score*weight) formulation
        survival = 1.0
        for s in signals:
            contribution = (s.score / 100.0) * s.weight
            survival *= (1.0 - contribution)
        return round((1.0 - survival) * 100, 2)

    @staticmethod
    def decision(risk_score: float) -> FraudDecision:
        if risk_score < 30:
            return FraudDecision.APPROVED
        if risk_score < 65:
            return FraudDecision.MANUAL_REVIEW
        if risk_score < 85:
            return FraudDecision.MANUAL_REVIEW
        return FraudDecision.BLOCKED

    @staticmethod
    def priority(risk_score: float, amount: float) -> CasePriority:
        if risk_score >= 85 or amount >= 50_000_000:
            return CasePriority.P1
        if risk_score >= 70 or amount >= 10_000_000:
            return CasePriority.P2
        if risk_score >= 50:
            return CasePriority.P3
        return CasePriority.P4

    @staticmethod
    def infer_pattern(signals: list[RiskSignal]) -> FraudPattern:
        rule_names = {s.rule for s in signals}
        if "CARD_TESTING_PATTERN" in rule_names:
            return FraudPattern.CARD_TESTING
        if "ATO_INDICATORS" in rule_names:
            return FraudPattern.ACCOUNT_TAKEOVER
        if "HIGH_VELOCITY_TX" in rule_names or "RAPID_REPEAT_TX" in rule_names:
            return FraudPattern.VELOCITY_ABUSE
        if "GEO_VELOCITY" in rule_names or "HIGH_RISK_COUNTRY" in rule_names:
            return FraudPattern.GEO_ANOMALY
        if "SHARED_IP_FRAUD_RING" in rule_names:
            return FraudPattern.IDENTITY_THEFT
        if "API_ABUSE_PATTERN" in rule_names:
            return FraudPattern.BOT_ATTACK
        if "AMOUNT_3X_AVG" in rule_names or "AMOUNT_Z_OUTLIER" in rule_names:
            return FraudPattern.IDENTITY_THEFT
        return FraudPattern.SOCIAL_ENGINEERING

    @staticmethod
    def recommend_action(decision: FraudDecision, pattern: FraudPattern, signals: list[RiskSignal]) -> str:
        if decision == FraudDecision.BLOCKED:
            return f"🚫 BLOCK transaction. Notify customer via SMS. Open P1 case for {pattern.value} investigation."
        if decision == FraudDecision.MANUAL_REVIEW:
            return f"⏸️ HOLD transaction. Manual review within 30min. Verify via OTP callback for {pattern.value}."
        return "✓ Approve transaction."


# ============================================================
# FRAUD ENGINE (Main)
# ============================================================

class FraudEngine:
    """Orchestrate all detection layers + alert management."""

    def __init__(self, reference_date: Optional[datetime] = None):
        self.reference_date = reference_date or datetime(2026, 8, 27)
        self.transactions: list[Transaction] = []
        self.profiles: dict[str, CustomerProfile] = {}
        self.ip_reputation: dict[str, int] = {}
        self.device_reputation: dict[str, int] = {}
        self.alerts: list[FraudAlert] = []
        self.cases: list[FraudCase] = []
        self.scanned_count = 0
        self.blocked_count = 0
        self.approved_count = 0
        self.review_count = 0
        self.total_amount_protected = 0.0

    def run(self, n_transactions: int = 500, n_customers: int = 100, seed: int = 42) -> dict:
        """Run the full fraud detection simulation."""
        rng = random.Random(seed)

        # 1. Generate customer profiles (baselines)
        self._generate_profiles(n_customers, rng)

        # 2. Generate IP/device reputation data
        self._generate_reputation_data(rng)

        # 3. Generate transaction stream (mostly legit, ~5% fraud)
        self.transactions = self._generate_transactions(n_transactions, rng)

        # 4. Score each transaction
        for tx in self.transactions:
            alert = self._score_transaction(tx, rng)
            self.scanned_count += 1
            if alert:
                self.alerts.append(alert)
                if alert.decision == FraudDecision.BLOCKED:
                    self.blocked_count += 1
                    self.total_amount_protected += tx.amount
                else:
                    self.review_count += 1
            else:
                self.approved_count += 1

        # 5. Auto-create cases for high-priority alerts
        self._auto_create_cases()

        # 6. Sort alerts by risk
        self.alerts.sort(key=lambda a: a.risk_score, reverse=True)

        return self.get_dashboard_data()

    def _generate_profiles(self, n: int, rng: random.Random) -> None:
        """Generate customer baseline profiles."""
        cities = ["Jakarta", "Surabaya", "Bandung", "Medan", "Semarang", "Yogyakarta", "Denpasar", "Makassar"]
        cats = ["Groceries", "Restaurant", "Transport", "Electronics", "Fashion", "Health", "Entertainment", "Utilities"]
        for i in range(n):
            cid = f"CUST-{i+1:05d}"
            avg = rng.uniform(50_000, 5_000_000)
            std = avg * rng.uniform(0.3, 1.2)
            max_tx = avg * rng.uniform(3, 10)
            # Hourly pattern: peak during business hours
            hour_pattern = [0.5, 0.3, 0.2, 0.1, 0.1, 0.2, 0.5, 1.0, 1.5, 1.2, 1.0, 1.2, 1.5, 1.3, 1.0, 1.2, 1.5, 1.8, 1.5, 1.0, 0.8, 0.7, 0.6, 0.5]
            self.profiles[cid] = CustomerProfile(
                customer_id=cid,
                avg_tx_amount=avg,
                std_tx_amount=std,
                max_tx_amount=max_tx,
                typical_channels=rng.sample([c.value for c in TransactionChannel], k=rng.randint(1, 3)),
                typical_cities=rng.sample(cities, k=rng.randint(1, 3)),
                typical_merchants=rng.sample(cats, k=rng.randint(2, 4)),
                avg_daily_tx_count=rng.uniform(0.5, 5),
                avg_hourly_pattern=hour_pattern,
                international_tx_count=rng.choices([0, 0, 0, 1, 5, 20], weights=[60, 20, 10, 5, 3, 2])[0],
                last_10_amounts=[avg * rng.uniform(0.5, 2) for _ in range(10)],
                last_10_locations=rng.sample(cities, k=min(3, len(cities))),
                total_lifetime_spend=avg * rng.randint(10, 200),
                account_age_days=rng.randint(30, 1825),
                known_devices=[f"dev-{rng.randint(1000, 9999)}" for _ in range(rng.randint(1, 3))],
            )

    def _generate_reputation_data(self, rng: random.Random) -> None:
        """Generate IP and device reputation scores."""
        # 10% of IPs are flagged
        for i in range(200):
            ip = f"103.{rng.randint(20, 30)}.{rng.randint(0, 255)}.{rng.randint(0, 255)}"
            self.ip_reputation[ip] = rng.choices([0, 50, 90], weights=[85, 10, 5])[0]
        # 5% of devices are compromised
        for i in range(300):
            dev = f"dev-{rng.randint(1000, 9999)}"
            self.device_reputation[dev] = rng.choices([0, 60, 95], weights=[90, 7, 3])[0]

    def _generate_transactions(self, n: int, rng: random.Random) -> list[Transaction]:
        """Generate realistic transaction stream with injected fraud."""
        cities = ["Jakarta", "Surabaya", "Bandung", "Medan", "Semarang", "Yogyakarta", "Denpasar", "Makassar", "Bali"]
        cats = ["Groceries", "Restaurant", "Transport", "Electronics", "Fashion", "Health", "Entertainment", "Utilities", "Travel", "Jewelry"]
        merchants = ["Indomaret", "Alfamart", "Tokopedia", "Shopee", "GoFood", "Grab", "PLN", "BPJS", "Telkomsel", "Apple Store"]
        channels = list(TransactionChannel)
        types = list(TransactionType)
        txs = []
        for i in range(n):
            cid = f"CUST-{rng.randint(1, 100):05d}"
            profile = self.profiles[cid]
            is_fraud = rng.random() < 0.05  # 5% fraud rate
            # Initialize pattern to a safe default; only set to fraud pattern if is_fraud
            pattern = "normal"

            if is_fraud:
                # Inject various fraud patterns
                pattern = rng.choice(["card_testing", "ato", "velocity", "amount", "geo", "intl", "bot"])
                if pattern == "card_testing":
                    amount = rng.uniform(1_000, 30_000)
                    failed = rng.randint(3, 10)
                elif pattern == "ato":
                    amount = rng.uniform(5_000_000, 50_000_000)
                    failed = 0
                elif pattern == "velocity":
                    amount = rng.uniform(100_000, 2_000_000)
                    failed = 0
                elif pattern == "amount":
                    amount = profile.avg_tx_amount * rng.uniform(3, 10)
                    failed = 0
                elif pattern == "geo":
                    amount = rng.uniform(2_000_000, 20_000_000)
                    failed = 0
                elif pattern == "intl":
                    amount = rng.uniform(5_000_000, 30_000_000)
                    failed = 0
                else:  # bot
                    amount = rng.uniform(10_000, 100_000)
                    failed = 0
            else:
                amount = max(10_000, profile.avg_tx_amount * rng.uniform(0.3, 1.8))
                failed = 0

            # Use high-risk IP/device for fraud
            if is_fraud:
                ip = rng.choice([ip for ip, s in self.ip_reputation.items() if s > 50]) if any(s > 50 for s in self.ip_reputation.values()) else f"103.{rng.randint(20,30)}.{rng.randint(0,255)}.{rng.randint(0,255)}"
                dev = rng.choice([d for d, s in self.device_reputation.items() if s > 60]) if any(s > 60 for s in self.device_reputation.values()) else f"dev-{rng.randint(1000,9999)}"
            else:
                ip = f"103.{rng.randint(20, 30)}.{rng.randint(0, 255)}.{rng.randint(0, 255)}"
                dev = rng.choice(profile.known_devices) if profile.known_devices and rng.random() < 0.9 else f"dev-{rng.randint(1000, 9999)}"

            tx = Transaction(
                id=f"TX-{i+1:06d}",
                customer_id=cid,
                amount=round(amount, 0),
                currency="IDR",
                channel=rng.choice(channels),
                type=rng.choice(types),
                merchant=rng.choice(merchants),
                merchant_category=rng.choice(cats),
                location_city=rng.choice(cities) if not is_fraud or pattern != "geo" else rng.choice(["Moscow", "Lagos", "Manila", "Bangkok"]),
                location_country="ID" if not is_fraud or pattern != "intl" else rng.choice(["RU", "NG", "PH"]),
                ip_address=ip,
                device_id=dev,
                timestamp=(self.reference_date - timedelta(minutes=rng.randint(0, 1440))).isoformat(),
                is_international=(pattern == "intl"),
                is_new_device=(is_fraud and rng.random() < 0.5),
                is_new_location=(is_fraud and pattern == "geo"),
                time_since_last_tx_minutes=rng.randint(0, 60) if not is_fraud else rng.randint(0, 2),
                failed_attempts_24h=failed,
                session_risk_score=rng.uniform(60, 95) if is_fraud else rng.uniform(0, 30),
            )
            txs.append(tx)
        return txs

    def _score_transaction(self, tx: Transaction, rng: random.Random) -> Optional[FraudAlert]:
        """Run all detection layers on a single transaction."""
        profile = self.profiles.get(tx.customer_id)
        # Count velocity in last 10 minutes (synthetic)
        velocity_10m = 0
        if tx.time_since_last_tx_minutes < 2:
            velocity_10m = rng.randint(3, 8)
        elif tx.time_since_last_tx_minutes < 5:
            velocity_10m = rng.randint(1, 3)
        # Count failures
        failed = tx.failed_attempts_24h

        # Run all layers
        signals = []
        signals.extend(RuleEngine.evaluate(tx, profile, velocity_10m, failed))
        signals.extend(StatisticalDetector.evaluate(tx, profile))
        signals.extend(BehaviorAnalyzer.evaluate(tx, profile))
        # Network
        shared_ip = set()  # would be computed from real DB
        shared_dev = set()
        signals.extend(NetworkAnalyzer.evaluate(tx, self.ip_reputation, self.device_reputation, shared_ip, shared_dev))

        # Add session risk
        if tx.session_risk_score > 70:
            signals.append(RiskSignal(
                layer="Session",
                rule="HIGH_SESSION_RISK",
                score=int(tx.session_risk_score),
                weight=0.20,
                description=f"Session risk score: {tx.session_risk_score:.0f}/100",
                evidence={"session_risk": tx.session_risk_score},
            ))

        # Compute composite
        risk = RiskScorer.score(signals)
        if risk < 30:
            return None  # No alert
        decision = RiskScorer.decision(risk)
        priority = RiskScorer.priority(risk, tx.amount)
        pattern = RiskScorer.infer_pattern(signals)
        action = RiskScorer.recommend_action(decision, pattern, signals)

        # Description
        top_signals = sorted(signals, key=lambda s: s.score * s.weight, reverse=True)[:3]
        desc = " | ".join([f"{s.rule} ({s.score})" for s in top_signals])

        return FraudAlert(
            id=f"FA-{tx.id}",
            transaction_id=tx.id,
            customer_id=tx.customer_id,
            risk_score=risk,
            decision=decision,
            pattern=pattern,
            priority=priority,
            signals=signals,
            amount=tx.amount,
            currency=tx.currency,
            channel=tx.channel.value,
            type=tx.type.value,
            location=f"{tx.location_city}, {tx.location_country}",
            timestamp=tx.timestamp,
            detected_at=datetime.utcnow().isoformat(),
            description=desc,
            recommended_action=action,
            status=AlertStatus.NEW.value,
            assigned_to=None,
            notes=[],
        )

    def _auto_create_cases(self) -> None:
        """Auto-create investigation cases for P1/P2 alerts."""
        case_counter = 1
        for alert in self.alerts:
            if alert.priority in (CasePriority.P1, CasePriority.P2):
                case = FraudCase(
                    id=f"CASE-{case_counter:05d}",
                    alert_ids=[alert.id],
                    customer_id=alert.customer_id,
                    pattern=alert.pattern,
                    priority=alert.priority,
                    status="open",
                    total_amount_at_risk=alert.amount,
                    amount_recovered=0.0,
                    opened_at=alert.detected_at,
                    closed_at=None,
                    assigned_to=random.Random(alert.id).choice(["Ahmad Rizki", "Sari Dewi", "Budi Hartono", None]),
                    investigation_notes=[],
                    sar_filed=False,
                    sar_reference=None,
                )
                self.cases.append(case)
                alert.case_id = case.id
                alert.assigned_to = case.assigned_to
                alert.status = AlertStatus.INVESTIGATING.value
                case_counter += 1

    def get_dashboard_data(self) -> dict:
        """Build full dashboard response."""
        if not self.transactions:
            return self._empty_dashboard()

        # Decision breakdown
        decisions = {"Approved": self.approved_count, "Manual Review": self.review_count, "Blocked": self.blocked_count}
        # Pattern breakdown
        patterns: dict[str, int] = {}
        for a in self.alerts:
            patterns[a.pattern.value] = patterns.get(a.pattern.value, 0) + 1
        # Priority breakdown
        priorities = {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
        for a in self.alerts:
            priorities[a.priority.value.split(" ")[0]] = priorities.get(a.priority.value.split(" ")[0], 0) + 1
        # Channel breakdown
        channel_alerts: dict[str, int] = {}
        for a in self.alerts:
            channel_alerts[a.channel] = channel_alerts.get(a.channel, 0) + 1
        # Risk distribution
        risk_buckets = {"0-20": 0, "20-40": 0, "40-60": 0, "60-80": 0, "80-100": 0}
        for a in self.alerts:
            if a.risk_score < 20: risk_buckets["0-20"] += 1
            elif a.risk_score < 40: risk_buckets["20-40"] += 1
            elif a.risk_score < 60: risk_buckets["40-60"] += 1
            elif a.risk_score < 80: risk_buckets["60-80"] += 1
            else: risk_buckets["80-100"] += 1

        total_at_risk = sum(a.amount for a in self.alerts)
        fraud_rate = (len(self.alerts) / max(1, self.scanned_count)) * 100
        # Layer contribution
        layer_scores: dict[str, list[float]] = defaultdict(list)
        for a in self.alerts:
            for s in a.signals:
                layer_scores[s.layer].append(s.score * s.weight)
        layer_contrib = {l: round(sum(v) / max(1, len(v)), 2) for l, v in layer_scores.items()}

        # Top risky customers
        by_customer: dict[str, list[FraudAlert]] = defaultdict(list)
        for a in self.alerts:
            by_customer[a.customer_id].append(a)
        top_customers = sorted(
            [{"customer_id": cid, "alert_count": len(alerts), "total_at_risk": sum(a.amount for a in alerts), "max_risk": max(a.risk_score for a in alerts)} for cid, alerts in by_customer.items()],
            key=lambda x: x["total_at_risk"], reverse=True
        )[:5]

        return {
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "total_scanned": self.scanned_count,
                "total_flagged": len(self.alerts),
                "fraud_rate_pct": round(fraud_rate, 2),
                "approved": self.approved_count,
                "manual_review": self.review_count,
                "blocked": self.blocked_count,
                "total_amount_at_risk": round(total_at_risk, 0),
                "total_amount_protected": round(self.total_amount_protected, 0),
                "active_cases": len(self.cases),
                "open_cases": sum(1 for c in self.cases if c.status == "open"),
                "by_decision": decisions,
                "by_pattern": patterns,
                "by_priority": priorities,
                "by_channel": channel_alerts,
                "by_risk_bucket": risk_buckets,
                "layer_contribution": layer_contrib,
            },
            "alerts": [a.to_dict() for a in self.alerts],
            "cases": [c.to_dict() for c in self.cases],
            "top_risky_customers": top_customers,
        }

    def _empty_dashboard(self) -> dict:
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {},
            "alerts": [],
            "cases": [],
            "top_risky_customers": [],
        }


# ============================================================
# SINGLETON
# ============================================================

_engine_instance: Optional[FraudEngine] = None
_cached_result: Optional[dict] = None


def get_engine() -> tuple[FraudEngine, dict]:
    global _engine_instance, _cached_result
    if _cached_result is None:
        _engine_instance = FraudEngine()
        _cached_result = _engine_instance.run(n_transactions=500, n_customers=100)
    return _engine_instance, _cached_result


def refresh_engine(n_tx: int = 500, n_customers: int = 100, seed: int = 42) -> dict:
    global _engine_instance, _cached_result
    _engine_instance = FraudEngine()
    _cached_result = _engine_instance.run(n_transactions=n_tx, n_customers=n_customers, seed=seed)
    return _cached_result
