#!/usr/bin/env bash
###############################################################################
# AUREA Quick Stop
# Stops all running services (frontend + backend + Docker if available)
###############################################################################

set -uo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo ""
echo "=========================================="
echo "  AUREA QUICK STOP"
echo "=========================================="
echo ""

# Stop backend services (if started via start-all-services.sh)
if [[ -d "$PROJECT_ROOT/infrastructure/pids" ]]; then
    log "[1/4] Stopping backend services..."
    bash "$SCRIPT_DIR/stop-all-services.sh" 2>/dev/null || warn "  No backend services to stop"
else
    log "[1/4] No backend services to stop"
fi

# Stop frontend dev servers
log "[2/4] Stopping frontend dev servers..."

for port in 3000 3001 3002; do
    pids=$(lsof -ti :$port 2>/dev/null || true)
    if [[ -n "$pids" ]]; then
        log "  Stopping process on port $port (PIDs: $pids)..."
        for pid in $pids; do
            kill -TERM "$pid" 2>/dev/null || true
        done
        sleep 1
        for pid in $pids; do
            kill -KILL "$pid" 2>/dev/null || true
        done
        log "  ✓ Port $port freed"
    else
        log "  Port $port: no process"
    fi
done

# Also kill any node processes related to aurea
log "[3/4] Killing orphaned AUREA node/vite processes..."
pkill -f "vite.*aurea" 2>/dev/null || true
pkill -f "nuxt.*aurea" 2>/dev/null || true
pkill -f "aurea-mobile" 2>/dev/null || true
log "  ✓ Done"

# Stop Docker infrastructure
log "[4/4] Stopping Docker infrastructure..."
if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
    cd "$PROJECT_ROOT/infrastructure"
    docker-compose -f docker-compose.dev.yaml stop 2>/dev/null || warn "  No containers to stop"
    log "  ✓ Docker containers stopped (use 'down -v' to remove volumes)"
else
    log "  Skipped (Docker not available)"
fi

echo ""
log "All services stopped."
echo ""
log "To restart: $SCRIPT_DIR/start-all.sh"
echo ""
