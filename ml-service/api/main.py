"""
AUREA ML Service — Auto-Insights + Customer Segmentation
==========================================================

Single FastAPI app hosting:
  - Auto-Insights (anomaly detection on time-series)
  - Smart Customer Segmentation (RFM + K-Means + CLV)
"""

import sys
import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Auto-Insights
from insights.auto_insights import get_engine as get_insights_engine, refresh_engine as refresh_insights_engine

# Customer Segmentation
from segmentation.customer_segmentation import (
    get_engine as get_segmentation_engine,
    refresh_engine as refresh_segmentation_engine,
    Segment,
)

# Churn Watch List
from churn.churn_watch import (
    get_engine as get_churn_engine,
    refresh_engine as refresh_churn_engine,
    WatchLevel, InterventionType, InterventionStatus,
)

# Real-time Fraud Detection
from fraud.fraud_detection import (
    get_engine as get_fraud_engine,
    refresh_engine as refresh_fraud_engine,
    FraudDecision, FraudPattern, AlertStatus, CasePriority,
)

# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="AUREA ML Service",
    description="ML-powered intelligence for AUREA MDM Platform",
    version="4.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow all (dev mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AUREA ML Service",
        "version": "2.0.0",
        "modules": ["auto_insights", "customer_segmentation", "churn_watch_list", "fraud_detection"],
    }


# ============================================================
# AUTO-INSIGHTS ENDPOINTS
# ============================================================

@app.get("/insights/summary")
def insights_summary():
    """Top-level summary of all insights."""
    engine = get_insights_engine()
    return engine.get_summary()


@app.get("/insights")
def insights_list(
    severity: Optional[str] = Query(None, description="CRITICAL, WARNING, INFO"),
    category: Optional[str] = Query(None, description="Customer, Transaction, System, KYC, Matching"),
    insight_type: Optional[str] = Query(None, description="ANOMALY, TREND, THRESHOLD"),
    limit: int = Query(100, ge=1, le=500),
):
    """List all insights with optional filters."""
    engine = get_insights_engine()
    return engine.get_insights(severity=severity, category=category, insight_type=insight_type, limit=limit)


@app.get("/insights/critical")
def insights_critical():
    """Only critical-severity insights."""
    engine = get_insights_engine()
    return engine.get_insights(severity="CRITICAL", limit=100)


@app.get("/insights/category/{category}")
def insights_by_category(category: str):
    """Insights for a specific category."""
    engine = get_insights_engine()
    return engine.get_insights(category=category, limit=100)


@app.get("/insights/{insight_id}")
def insight_detail(insight_id: str):
    """Get a specific insight by ID."""
    engine = get_insights_engine()
    insight = engine.get_insight(insight_id)
    if not insight:
        raise HTTPException(404, f"Insight {insight_id} not found")
    return insight


@app.post("/insights/refresh")
def insights_refresh():
    """Re-run insight generation (regenerates mock time-series)."""
    summary = refresh_insights_engine()
    return {"status": "refreshed", "summary": summary}


# ============================================================
# CUSTOMER SEGMENTATION ENDPOINTS
# ============================================================

@app.get("/segments")
def list_segments():
    """List all customer segments with their profiles."""
    _, result = get_segmentation_engine()
    return {
        "summary": result["summary"],
        "segments": result["segments"],
    }


@app.get("/segments/summary")
def segments_summary():
    """Quick summary of all segments (counts & revenue)."""
    _, result = get_segmentation_engine()
    return {
        "reference_date": result["reference_date"],
        "summary": result["summary"],
        "segments": [
            {
                "name": s["name"],
                "customer_count": s["customer_count"],
                "percentage": s["percentage"],
                "total_revenue": s["total_revenue"],
                "avg_clv": s["avg_clv"],
                "churn_risk": s["churn_risk"],
                "color": s["color"],
                "icon": s["icon"],
            }
            for s in result["segments"]
        ],
    }


@app.get("/segments/{segment_name}")
def segment_detail(segment_name: str):
    """Detail of a specific segment including sample customers."""
    _, result = get_segmentation_engine()
    for s in result["segments"]:
        if s["name"].lower() == segment_name.lower():
            return s
    raise HTTPException(404, f"Segment '{segment_name}' not found")


@app.get("/segments/{segment_name}/customers")
def segment_customers(
    segment_name: str,
    limit: int = Query(50, ge=1, le=500),
):
    """List customers in a specific segment."""
    _, result = get_segmentation_engine()
    matches = [
        a for a in result["assignments"]
        if a["segment"].lower() == segment_name.lower()
    ]
    return {
        "segment": segment_name,
        "total": len(matches),
        "customers": matches[:limit],
    }


@app.get("/customers")
def customers_list(
    segment: Optional[str] = Query(None),
    min_clv: Optional[float] = Query(None),
    min_churn: Optional[float] = Query(None),
    limit: int = Query(50, ge=1, le=500),
):
    """List all customers with optional filters."""
    _, result = get_segmentation_engine()
    customers = result["assignments"]
    if segment:
        customers = [c for c in customers if c["segment"].lower() == segment.lower()]
    if min_clv is not None:
        customers = [c for c in customers if c["clv_12m"] >= min_clv]
    if min_churn is not None:
        customers = [c for c in customers if c["churn_probability"] >= min_churn]
    return {
        "total": len(customers),
        "customers": customers[:limit],
    }


@app.get("/customers/{customer_id}")
def customer_detail(customer_id: str):
    """Get a specific customer with full RFM details."""
    _, result = get_segmentation_engine()
    for a in result["assignments"]:
        if a["customer_id"] == customer_id:
            return a
    raise HTTPException(404, f"Customer {customer_id} not found")


@app.get("/dashboard")
def unified_dashboard():
    """Combined dashboard: insights + segmentation overview."""
    insights_engine = get_insights_engine()
    _, seg_result = get_segmentation_engine()
    return {
        "generated_at": datetime.now().isoformat(),
        "insights": insights_engine.get_summary(),
        "segmentation": seg_result["summary"],
        "top_segments": [
            {
                "name": s["name"],
                "count": s["customer_count"],
                "revenue": s["total_revenue"],
                "clv": s["avg_clv"],
                "churn_risk": s["churn_risk"],
            }
            for s in seg_result["segments"][:5]
        ],
    }


@app.post("/segments/refresh")
def segments_refresh(n: int = Query(200, ge=10, le=10000), seed: int = Query(42)):
    """Regenerate customer data and re-run segmentation."""
    result = refresh_segmentation_engine(n=n, seed=seed)
    return {
        "status": "refreshed",
        "total_customers": result["total_customers"],
        "segments": len(result["segments"]),
    }


# ============================================================
# CHURN WATCH LIST ENDPOINTS
# ============================================================

@app.get("/churn")
def churn_dashboard():
    """Full churn watch list dashboard data."""
    _, result = get_churn_engine()
    return result


@app.get("/churn/summary")
def churn_summary():
    """Quick summary stats for churn."""
    _, result = get_churn_engine()
    return {
        "generated_at": result["generated_at"],
        "summary": result["summary"],
        "top_at_risk": result["top_at_risk"],
        "driver_breakdown": result["driver_breakdown"],
    }


@app.get("/churn/alerts")
def churn_alerts(
    level: Optional[str] = Query(None, description="Watch, Alert, Critical, Lost"),
    status: Optional[str] = Query(None, description="new, acknowledged, in_intervention, monitoring"),
    min_risk: Optional[int] = Query(None, ge=0, le=100),
    min_clv: Optional[float] = Query(None),
    limit: int = Query(100, ge=1, le=500),
):
    """List churn alerts with optional filters."""
    _, result = get_churn_engine()
    alerts = result["alerts"]
    if level:
        alerts = [a for a in alerts if a["level"] == level]
    if status:
        alerts = [a for a in alerts if a["status"] == status]
    if min_risk is not None:
        alerts = [a for a in alerts if a["risk_score"] >= min_risk]
    if min_clv is not None:
        alerts = [a for a in alerts if a["clv_at_risk"] >= min_clv]
    return {
        "total": len(alerts),
        "alerts": alerts[:limit],
    }


@app.get("/churn/alerts/{alert_id}")
def churn_alert_detail(alert_id: str):
    """Get a specific churn alert."""
    _, result = get_churn_engine()
    for a in result["alerts"]:
        if a["id"] == alert_id:
            return a
    raise HTTPException(404, f"Alert {alert_id} not found")


@app.post("/churn/alerts/{alert_id}/acknowledge")
def churn_acknowledge(alert_id: str, user: str = Query("system")):
    """Acknowledge a churn alert."""
    engine, _ = get_churn_engine()
    alert = engine.acknowledge_alert(alert_id, user)
    if not alert:
        raise HTTPException(404, f"Alert {alert_id} not found")
    return alert.to_dict()


@app.post("/churn/alerts/{alert_id}/resolve")
def churn_resolve(alert_id: str, outcome: str = Query("Customer retained"), user: str = Query("system")):
    """Resolve a churn alert."""
    engine, _ = get_churn_engine()
    alert = engine.resolve_alert(alert_id, outcome, user)
    if not alert:
        raise HTTPException(404, f"Alert {alert_id} not found")
    return {"status": "resolved", "alert_id": alert_id, "outcome": outcome}


@app.post("/churn/alerts/{alert_id}/intervene")
def churn_intervene(
    alert_id: str,
    intervention_type: str = Query(..., description="Email, SMS, PhoneCall, etc."),
    message: str = Query(..., min_length=1),
    assigned_to: str = Query("Retention Team"),
):
    """Create an intervention for a churn alert."""
    engine, _ = get_churn_engine()
    # Normalize: PhoneCall, phone_call, "Phone Call" -> "Phone Call"
    normalized = intervention_type.replace("_", " ").strip()
    # Try case-insensitive match against enum values
    itype = None
    for it in InterventionType:
        if it.value.lower() == normalized.lower():
            itype = it
            break
        if it.name.lower().replace("_", " ") == normalized.lower():
            itype = it
            break
    if itype is None:
        valid = ", ".join([i.value for i in InterventionType])
        raise HTTPException(400, f"Unknown intervention type: {intervention_type}. Valid: {valid}")
    intv = engine.create_intervention(alert_id, itype, message, assigned_to)
    if not intv:
        raise HTTPException(404, f"Alert {alert_id} not found")
    return intv.to_dict()


@app.get("/churn/interventions")
def churn_interventions(
    status: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
):
    """List interventions."""
    _, result = get_churn_engine()
    intvs = result["interventions"]
    if status:
        intvs = [i for i in intvs if i["status"] == status]
    if customer_id:
        intvs = [i for i in intvs if i["customer_id"] == customer_id]
    return {
        "total": len(intvs),
        "interventions": intvs[:limit],
    }


@app.post("/churn/refresh")
def churn_refresh(n: int = Query(200, ge=10, le=10000), seed: int = Query(42)):
    """Regenerate churn watch data."""
    result = refresh_churn_engine(n=n, seed=seed)
    return {
        "status": "refreshed",
        "total_alerts": result["summary"]["total_alerts"],
    }


# ============================================================
# FRAUD DETECTION ENDPOINTS
# ============================================================

@app.get("/fraud")
def fraud_dashboard():
    """Full fraud detection dashboard data."""
    _, result = get_fraud_engine()
    return result


@app.get("/fraud/summary")
def fraud_summary():
    """Quick summary stats for fraud detection."""
    _, result = get_fraud_engine()
    return {
        "generated_at": result["generated_at"],
        "summary": result["summary"],
        "top_risky_customers": result["top_risky_customers"],
    }


@app.get("/fraud/alerts")
def fraud_alerts(
    decision: Optional[str] = Query(None, description="Approved, Manual Review, Blocked"),
    pattern: Optional[str] = Query(None),
    priority: Optional[str] = Query(None, description="P1, P2, P3, P4"),
    min_risk: Optional[float] = Query(None, ge=0, le=100),
    min_amount: Optional[float] = Query(None),
    limit: int = Query(100, ge=1, le=500),
):
    """List fraud alerts with filters."""
    _, result = get_fraud_engine()
    alerts = result["alerts"]
    if decision:
        alerts = [a for a in alerts if a["decision"] == decision]
    if pattern:
        alerts = [a for a in alerts if a["pattern"] == pattern]
    if priority:
        alerts = [a for a in alerts if a["priority"].startswith(priority)]
    if min_risk is not None:
        alerts = [a for a in alerts if a["risk_score"] >= min_risk]
    if min_amount is not None:
        alerts = [a for a in alerts if a["amount"] >= min_amount]
    return {
        "total": len(alerts),
        "alerts": alerts[:limit],
    }


@app.get("/fraud/alerts/{alert_id}")
def fraud_alert_detail(alert_id: str):
    """Get a specific fraud alert."""
    _, result = get_fraud_engine()
    for a in result["alerts"]:
        if a["id"] == alert_id:
            return a
    raise HTTPException(404, f"Alert {alert_id} not found")


@app.get("/fraud/cases")
def fraud_cases(status: Optional[str] = Query(None), limit: int = Query(50, ge=1, le=500)):
    """List investigation cases."""
    _, result = get_fraud_engine()
    cases = result["cases"]
    if status:
        cases = [c for c in cases if c["status"] == status]
    return {"total": len(cases), "cases": cases[:limit]}


@app.post("/fraud/alerts/{alert_id}/approve")
def fraud_approve(alert_id: str, user: str = Query("system")):
    """Approve a flagged transaction."""
    return {"status": "approved", "alert_id": alert_id, "user": user, "action": "Transaction released"}


@app.post("/fraud/alerts/{alert_id}/block")
def fraud_block(alert_id: str, user: str = Query("system")):
    """Block a flagged transaction."""
    return {"status": "blocked", "alert_id": alert_id, "user": user, "action": "Transaction blocked, customer notified"}


@app.post("/fraud/refresh")
def fraud_refresh(n_tx: int = Query(500, ge=10, le=10000), seed: int = Query(42)):
    """Regenerate fraud detection data."""
    result = refresh_fraud_engine(n_tx=n_tx, seed=seed)
    return {
        "status": "refreshed",
        "scanned": result["summary"]["total_scanned"],
        "flagged": result["summary"]["total_flagged"],
    }


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup():
    """Pre-warm engines."""
    import sys
    print("[AUREA ML] Pre-warming engines...", flush=True)
    print(f"  Module path: {sys.path[0]}", flush=True)
    try:
        get_insights_engine()
        print("  ✓ insights engine ready", flush=True)
    except Exception as e:
        print(f"  ✗ insights engine failed: {e}", flush=True)
    try:
        get_segmentation_engine()
        print("  ✓ segmentation engine ready", flush=True)
    except Exception as e:
        print(f"  ✗ segmentation engine failed: {e}", flush=True)
    try:
        get_churn_engine()
        print("  ✓ churn engine ready", flush=True)
    except Exception as e:
        print(f"  ✗ churn engine failed: {e}", flush=True)
    try:
        get_fraud_engine()
        print("  ✓ fraud engine ready", flush=True)
    except Exception as e:
        print(f"  ✗ fraud engine failed: {e}", flush=True)
    print("[AUREA ML] Service ready.", flush=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
