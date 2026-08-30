#!/usr/bin/env bash
###############################################################################
# AUREA Health Check Script
# Verifies all infrastructure and application services are healthy
###############################################################################

set -uo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0
SKIP=0

check() {
    local name="$1"
    local cmd="$2"
    local expected="$3"
    
    if result=$(eval "$cmd" 2>/dev/null); then
        if [[ -z "$expected" ]] || [[ "$result" == *"$expected"* ]]; then
            echo -e "  ${GREEN}✓${NC} $name"
            ((PASS++))
        else
            echo -e "  ${RED}✗${NC} $name (got: $result)"
            ((FAIL++))
        fi
    else
        echo -e "  ${RED}✗${NC} $name"
        ((FAIL++))
    fi
}

skip() {
    local name="$1"
    local reason="$2"
    echo -e "  ${YELLOW}○${NC} $name (skipped: $reason)"
    ((SKIP++))
}

echo ""
echo "========================================"
echo "  AUREA HEALTH CHECK"
echo "  $(date)"
echo "========================================"
echo ""

# Docker availability
DOCKER_AVAILABLE=false
if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
    DOCKER_AVAILABLE=true
elif command -v docker &>/dev/null; then
    skip "Docker daemon" "Docker CLI found but daemon not responding (sandbox mode)"
else
    skip "Docker" "Not installed in this environment"
fi

# Docker infrastructure
if [[ "$DOCKER_AVAILABLE" == true ]]; then
    echo -e "${CYAN}Infrastructure (Docker):${NC}"
    check "PostgreSQL container" "docker ps --format '{{.Names}}' | grep -iE 'postgres'" "postgres"
    check "Keycloak container" "docker ps --format '{{.Names}}' | grep -iE 'keycloak'" "keycloak"
    check "Kafka container" "docker ps --format '{{.Names}}' | grep -iE 'kafka'" "kafka"
    check "Redis/Valkey container" "docker ps --format '{{.Names}}' | grep -iE 'valkey|redis'" "valkey"
    check "Eureka container" "docker ps --format '{{.Names}}' | grep -iE 'eureka'" "eureka"
    check "MinIO container" "docker ps --format '{{.Names}}' | grep -iE 'minio'" "minio"
    check "Prometheus container" "docker ps --format '{{.Names}}' | grep -iE 'prometheus'" "prometheus"
    check "Grafana container" "docker ps --format '{{.Names}}' | grep -iE 'grafana'" "grafana"
    echo ""
fi

# Service health (HTTP)
echo -e "${CYAN}Service Endpoints (HTTP):${NC}"
check "Keycloak    (8180)" "curl -sf http://localhost:8180/health/ready" ""
check "Eureka      (8761)" "curl -sf http://localhost:8761/actuator/health" ""
check "MinIO       (9000)" "curl -sf http://localhost:9000/minio/health/live" ""
check "MinIO UI    (9001)" "curl -sf http://localhost:9001" ""
check "Prometheus  (9090)" "curl -sf http://localhost:9090/-/healthy" ""
check "Grafana     (3000)" "curl -sf http://localhost:3000/api/health || curl -sf http://localhost:3001/api/health" ""
check "Tempo       (3200)" "curl -sf http://localhost:3200/ready" ""
check "Loki        (3100)" "curl -sf http://localhost:3100/ready" ""
echo ""

# Database connectivity
echo -e "${CYAN}Database Connectivity:${NC}"
if [[ "$DOCKER_AVAILABLE" == true ]]; then
    check "PostgreSQL login" "docker exec mdm-postgres pg_isready -U mdm_admin 2>&1" "accepting"
else
    skip "PostgreSQL (direct)" "Docker not available; use HTTP-based checks"
fi
check "Keycloak realm" "curl -sf http://localhost:8180/realms/master/.well-known/openid-configuration | head -c 50" "issuer"
echo ""

# Frontend applications
echo -e "${CYAN}Frontend Applications:${NC}"
check "AUREA Console   (3000)" "curl -sf http://localhost:3000/ | grep -o '<title>[^<]*</title>'" "AUREA"
check "AUREA 360       (3001)" "curl -sf http://localhost:3001/ | grep -o '<title>[^<]*</title>'" "AUREA"
check "AUREA Steward   (3002)" "curl -sf -L http://localhost:3002/ | grep -o '<title>[^<]*</title>'" "AUREA"
echo ""

# Resource usage
echo -e "${CYAN}Resource Usage:${NC}"
if [[ "$DOCKER_AVAILABLE" == true ]]; then
    total_cpu=$(docker stats --no-stream --format "{{.CPUPerc}}" 2>/dev/null | grep -oE "[0-9.]+" | awk '{s+=$1} END {printf "%.1f%%", s}')
    echo "  CPU (sum of all containers): ${total_cpu:-N/A}"
    echo "  Memory (top 5):"
    docker stats --no-stream --format "    {{.Name}}: {{.MemUsage}}" 2>/dev/null | head -5 || echo "    N/A"
fi
echo ""

# Disk usage
echo -e "${CYAN}Disk Usage:${NC}"
df -h / | tail -1 | awk '{print "  Root:  " $3 " used of " $2 " (" $5 " full)"}'
df -h /home 2>/dev/null | tail -1 | awk '{print "  Home:  " $3 " used of " $2 " (" $5 " full)"}' || true
echo ""

# Summary
echo "========================================"
echo "  SUMMARY"
echo "========================================"
echo -e "  ${GREEN}PASS${NC}: $PASS"
echo -e "  ${RED}FAIL${NC}: $FAIL"
echo -e "  ${YELLOW}WARN${NC}: $WARN"
echo -e "  ${YELLOW}SKIP${NC}: $SKIP"
echo "========================================"

if [[ $FAIL -gt 0 ]]; then
    exit 1
fi
exit 0
