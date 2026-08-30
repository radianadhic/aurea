#!/usr/bin/env bash
###############################################################################
# AUREA Quick Start
# One-liner starter that brings up all running services
###############################################################################

set -uo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

log() { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

echo ""
echo "=========================================="
echo "  AUREA QUICK START"
echo "=========================================="
echo ""

# Detect environment
if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
    DOCKER=true
    log "Docker detected: enabling backend infrastructure"
else
    DOCKER=false
    warn "Docker not available: backend services will be skipped"
    warn "Only frontend applications will start"
fi

# 1. Start infrastructure (if Docker available)
if [[ "$DOCKER" == true ]]; then
    log "[1/3] Starting Docker infrastructure..."
    cd "$PROJECT_ROOT/infrastructure"
    docker-compose -f docker-compose.dev.yaml up -d 2>/dev/null || \
        warn "Failed to start some containers"
    
    log "[2/3] Waiting for infrastructure..."
    sleep 20
else
    log "[1/3] Skipping infrastructure (no Docker)"
    log "[2/3] Skipping wait"
fi

# 3. Frontend apps
log "[3/3] Starting frontend applications..."

# Admin Console
if ! curl -sf http://localhost:3000/ -o /dev/null --max-time 2 2>/dev/null; then
    log "  Starting AUREA Console (port 3000)..."
    cd "$PROJECT_ROOT/frontend/admin-dashboard"
    if [[ -d node_modules ]]; then
        nohup npm run dev -- --host 0.0.0.0 --port 3000 > /tmp/aurea-3000.log 2>&1 &
        disown
    else
        warn "  node_modules missing for admin-dashboard, skipping"
    fi
else
    log "  AUREA Console already running (3000)"
fi

# Customer 360
if ! curl -sf http://localhost:3001/ -o /dev/null --max-time 2 2>/dev/null; then
    log "  Starting AUREA 360 (port 3001)..."
    cd "$PROJECT_ROOT/frontend/customer360"
    if [[ -d node_modules ]]; then
        nohup npm run dev -- --host 0.0.0.0 --port 3001 > /tmp/aurea-3001.log 2>&1 &
        disown
    else
        warn "  node_modules missing for customer360, skipping"
    fi
else
    log "  AUREA 360 already running (3001)"
fi

# Steward
if ! curl -sf -L http://localhost:3002/ -o /dev/null --max-time 2 2>/dev/null; then
    log "  Starting AUREA Steward (port 3002)..."
    cd "$PROJECT_ROOT/frontend/steward-ui"
    if [[ -d node_modules ]]; then
        nohup npm run dev -- --host 0.0.0.0 --port 3002 > /tmp/aurea-3002.log 2>&1 &
        disown
    else
        warn "  node_modules missing for steward-ui, skipping"
    fi
else
    log "  AUREA Steward already running (3002)"
fi

# Wait for services to be ready
log "Waiting 20s for frontend apps to start..."
sleep 20

# Summary
echo ""
echo "=========================================="
echo "  AUREA STATUS"
echo "=========================================="
echo ""

for entry in "3000:AUREA Console" "3001:AUREA 360" "3002:AUREA Steward"; do
    port="${entry%:*}"
    name="${entry#*:}"
    if curl -sf "http://localhost:$port/" -o /dev/null --max-time 3 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $name — http://localhost:$port"
    else
        echo -e "  ${RED}✗${NC} $name — http://localhost:$port (NOT RESPONDING)"
    fi
done

echo ""
echo "  Useful commands:"
echo "    Health check:  $SCRIPT_DIR/health-check.sh"
echo "    Smoke test:   $SCRIPT_DIR/smoke-test.sh"
echo "    Stop all:     $SCRIPT_DIR/stop-all.sh"
echo "    Status:       $SCRIPT_DIR/../aurea-infrastructure.sh status"
echo ""

if [[ "$DOCKER" == true ]]; then
    echo "  Backend infrastructure (Docker):"
    echo "    PostgreSQL  →  localhost:5432  (mdm_admin / mdm_dev_password)"
    echo "    Keycloak    →  http://localhost:8180  (admin / admin)"
    echo "    Kafka UI    →  http://localhost:8081"
    echo "    MinIO       →  http://localhost:9001  (minioadmin / minioadmin)"
    echo "    Grafana     →  http://localhost:3000  (admin / admin)"
    echo ""
fi
