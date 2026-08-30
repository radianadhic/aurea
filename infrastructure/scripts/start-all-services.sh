#!/usr/bin/env bash
###############################################################################
# AUREA Backend Services Starter
# Starts all Spring Boot microservices in background
###############################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/infrastructure/logs"
PID_DIR="$PROJECT_ROOT/infrastructure/pids"

mkdir -p "$LOG_DIR" "$PID_DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

log()   { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# List of services to start (in order)
SERVICES=(
    "eureka-server:8761"
    "config-server:8888"
    "api-gateway:8080"
    "auth-service:8081"
    "customer-service:8082"
    "account-service:8083"
    "product-service:8084"
    "matching-service:8085"
    "kyc-service:8086"
    "audit-service:8087"
    "ml-service:8088"
    "notification-service:8089"
)

# Java options
JAVA_OPTS="${JAVA_OPTS:--Xms256m -Xmx1g -XX:+UseG1GC}"
SPRING_OPTS="${SPRING_OPTS:--Dspring.profiles.active=dev}"

start_service() {
    local service_name="$1"
    local port="$2"
    local log_file="$LOG_DIR/${service_name}.log"
    local pid_file="$PID_DIR/${service_name}.pid"
    
    # Check if already running
    if [[ -f "$pid_file" ]] && kill -0 "$(cat "$pid_file")" 2>/dev/null; then
        warn "$service_name already running (PID: $(cat $pid_file))"
        return 0
    fi
    
    # Check port availability
    if lsof -i :$port &>/dev/null; then
        warn "Port $port already in use, skipping $service_name"
        return 1
    fi
    
    # Check if service directory exists
    local service_dir="$PROJECT_ROOT/backend/$service_name"
    if [[ ! -d "$service_dir" ]]; then
        warn "$service_name directory not found, skipping"
        return 1
    fi
    
    log "Starting $service_name (port $port)..."
    
    cd "$service_dir"
    
    # Start in background
    nohup java $JAVA_OPTS $SPRING_OPTS \
        -jar target/*.jar \
        > "$log_file" 2>&1 &
    
    local pid=$!
    echo "$pid" > "$pid_file"
    
    sleep 2
    if kill -0 "$pid" 2>/dev/null; then
        log "  ✓ $service_name started (PID: $pid, log: $log_file)"
        return 0
    else
        error "  ✗ $service_name failed to start"
        return 1
    fi
}

print_header() {
    echo ""
    echo "=========================================="
    echo "  AUREA BACKEND SERVICES STARTER"
    echo "  $(date)"
    echo "=========================================="
    echo ""
}

print_footer() {
    echo ""
    echo "=========================================="
    echo "  SERVICES STARTED"
    echo "=========================================="
    echo ""
    log "Logs:     $LOG_DIR/*.log"
    log "PIDs:     $PID_DIR/*.pid"
    log "Stop all: $SCRIPT_DIR/stop-all-services.sh"
    echo ""
    log "Eureka dashboard:    http://localhost:8761"
    log "API Gateway:         http://localhost:8080"
    log "Keycloak admin:      http://localhost:8180"
    log "Grafana:             http://localhost:3000"
    echo ""
    log "Waiting 30s for services to be ready..."
    sleep 30
    log "Run health check:    $SCRIPT_DIR/health-check.sh"
}

# Main
print_header

# Verify Java & Maven
command -v java &>/dev/null || { error "Java not installed"; exit 1; }
command -v mvn  &>/dev/null || warn "Maven not found (will need pre-built JARs)"

# Start services in sequence
started=0
for entry in "${SERVICES[@]}"; do
    service="${entry%:*}"
    port="${entry#*:}"
    if start_service "$service" "$port"; then
        ((started++))
    fi
    # Wait between services to avoid resource spikes
    sleep 3
done

echo ""
log "Started $started / ${#SERVICES[@]} services"
print_footer
