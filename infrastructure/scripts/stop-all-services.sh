#!/usr/bin/env bash
###############################################################################
# AUREA Backend Services Stopper
# Stops all running Spring Boot microservices gracefully
###############################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PID_DIR="$PROJECT_ROOT/infrastructure/pids"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

# Reverse order to stop
SERVICES=(
    "notification-service"
    "ml-service"
    "audit-service"
    "kyc-service"
    "matching-service"
    "product-service"
    "account-service"
    "customer-service"
    "auth-service"
    "api-gateway"
    "config-server"
    "eureka-server"
)

echo ""
echo "=========================================="
echo "  AUREA BACKEND SERVICES STOPPER"
echo "=========================================="
echo ""

stopped=0
skipped=0
for service in "${SERVICES[@]}"; do
    pid_file="$PID_DIR/${service}.pid"
    if [[ ! -f "$pid_file" ]]; then
        warn "$service: no PID file, skipping"
        ((skipped++))
        continue
    fi
    pid=$(cat "$pid_file")
    if ! kill -0 "$pid" 2>/dev/null; then
        warn "$service: not running (stale PID file)"
        rm -f "$pid_file"
        ((skipped++))
        continue
    fi
    log "Stopping $service (PID: $pid)..."
    kill "$pid" 2>/dev/null || true
    # Wait for graceful shutdown
    for i in 1 2 3 4 5; do
        if ! kill -0 "$pid" 2>/dev/null; then
            break
        fi
        sleep 1
    done
    # Force kill if still running
    if kill -0 "$pid" 2>/dev/null; then
        warn "  Force killing $service..."
        kill -9 "$pid" 2>/dev/null || true
    fi
    rm -f "$pid_file"
    log "  ✓ $service stopped"
    ((stopped++))
done

echo ""
log "Stopped $stopped services, skipped $skipped"
