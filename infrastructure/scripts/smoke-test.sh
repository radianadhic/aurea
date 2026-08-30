#!/usr/bin/env bash
###############################################################################
# AUREA Smoke Test
# End-to-end functional test for AUREA platform
###############################################################################

set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

PASS=0
FAIL=0

assert() {
    local desc="$1"
    local actual="$2"
    local expected="$3"
    if [[ "$actual" == *"$expected"* ]]; then
        echo -e "  ${GREEN}✓${NC} $desc"
        ((PASS++))
    else
        echo -e "  ${RED}✗${NC} $desc"
        echo "      Expected: $expected"
        echo "      Got:      $actual"
        ((FAIL++))
    fi
}

echo ""
echo "=========================================="
echo "  AUREA SMOKE TEST"
echo "  $(date)"
echo "=========================================="
echo ""

# ====================
# INFRASTRUCTURE
# ====================
echo -e "${CYAN}[1/5] Infrastructure Tests${NC}"

# PostgreSQL
result=$(docker exec mdm-postgres pg_isready -U mdm_admin 2>&1 || true)
assert "PostgreSQL ready" "$result" "accepting"

# Count databases
db_count=$(docker exec mdm-postgres psql -U mdm_admin -tAc "SELECT count(*) FROM pg_database WHERE datname LIKE 'mdm_%'" 2>/dev/null || echo "0")
if [[ "$db_count" -ge 5 ]]; then
    echo -e "  ${GREEN}✓${NC} Found $db_count AUREA databases"
    ((PASS++))
else
    echo -e "  ${RED}✗${NC} Expected at least 5 databases, found $db_count"
    ((FAIL++))
fi

# Keycloak
kc_realm=$(curl -sf "http://localhost:8180/realms/master/.well-known/openid-configuration" | head -c 50 || echo "")
assert "Keycloak OIDC discovery" "$kc_realm" "issuer"

# Kafka
if docker exec mdm-kafka kafka-topics --bootstrap-server localhost:9092 --list &>/dev/null; then
    topic_count=$(docker exec mdm-kafka kafka-topics --bootstrap-server localhost:9092 --list 2>/dev/null | wc -l)
    echo -e "  ${GREEN}✓${NC} Kafka has $topic_count topics"
    ((PASS++))
else
    echo -e "  ${RED}✗${NC} Kafka not accessible"
    ((FAIL++))
fi

# ====================
# FRONTEND
# ====================
echo ""
echo -e "${CYAN}[2/5] Frontend Applications${NC}"

for entry in "3000:AUREA Console" "3001:AUREA 360" "3002:AUREA Steward"; do
    port="${entry%:*}"
    name="${entry#*:}"
    title=$(curl -sf "http://localhost:$port/" 2>/dev/null | grep -oP '(?<=<title>)[^<]+' | head -1 || echo "")
    if [[ "$title" == *"AUREA"* ]]; then
        echo -e "  ${GREEN}✓${NC} $name (port $port): $title"
        ((PASS++))
    else
        echo -e "  ${RED}✗${NC} $name (port $port): not responding or wrong title"
        ((FAIL++))
    fi
done

# ====================
# AUTH
# ====================
echo ""
echo -e "${CYAN}[3/5] Authentication${NC}"

# Keycloak admin accessible
admin_health=$(curl -sf "http://localhost:8180/admin/master/console/" -o /dev/null -w "%{http_code}" || echo "000")
if [[ "$admin_health" == "200" || "$admin_health" == "302" ]]; then
    echo -e "  ${GREEN}✓${NC} Keycloak admin console accessible (HTTP $admin_health)"
    ((PASS++))
else
    echo -e "  ${RED}✗${NC} Keycloak admin not accessible"
    ((FAIL++))
fi

# ====================
# MONITORING
# ====================
echo ""
echo -e "${CYAN}[4/5] Monitoring Stack${NC}"

# Prometheus
prom_targets=$(curl -sf "http://localhost:9090/api/v1/targets" 2>/dev/null | python3 -c "import sys, json; d=json.load(sys.stdin); print(len(d.get('data',{}).get('activeTargets',[])))" 2>/dev/null || echo "0")
if [[ "$prom_targets" -gt 0 ]]; then
    echo -e "  ${GREEN}✓${NC} Prometheus has $prom_targets active targets"
    ((PASS++))
else
    echo -e "  ${YELLOW}!${NC} Prometheus has no targets (expected if backend not running)"
fi

# Grafana
grafana_ds=$(curl -sf -u admin:admin "http://localhost:3000/api/datasources" 2>/dev/null | python3 -c "import sys, json; d=json.load(sys.stdin); print(len(d))" 2>/dev/null || echo "0")
if [[ "$grafana_ds" -ge 1 ]]; then
    echo -e "  ${GREEN}✓${NC} Grafana has $grafana_ds datasource(s)"
    ((PASS++))
else
    echo -e "  ${YELLOW}!${NC} Grafana has no datasources (default password may be 'admin')"
fi

# ====================
# STORAGE
# ====================
echo ""
echo -e "${CYAN}[5/5] Object Storage${NC}"

# MinIO
mc_health=$(curl -sf "http://localhost:9000/minio/health/live" -o /dev/null -w "%{http_code}" || echo "000")
if [[ "$mc_health" == "200" ]]; then
    echo -e "  ${GREEN}✓${NC} MinIO is healthy"
    ((PASS++))
else
    echo -e "  ${RED}✗${NC} MinIO not responding"
    ((FAIL++))
fi

# ====================
# SUMMARY
# ====================
echo ""
echo "=========================================="
TOTAL=$((PASS + FAIL))
PERCENT=$((PASS * 100 / TOTAL))
echo "  RESULT: $PASS / $TOTAL passed ($PERCENT%)"
echo "=========================================="

if [[ $FAIL -gt 0 ]]; then
    echo -e "  ${RED}SOME TESTS FAILED${NC}"
    exit 1
fi
echo -e "  ${GREEN}ALL TESTS PASSED${NC}"
exit 0
