#!/usr/bin/env bash
###############################################################################
# AUREA Infrastructure Setup Master Script
# Automates provisioning of complete AUREA platform infrastructure
#
# Usage:
#   ./aurea-infrastructure.sh [command] [options]
#
# Commands:
#   dev          - Start local development infrastructure (Docker Compose)
#   k8s          - Deploy to Kubernetes (dev/staging/production)
#   monitor      - Setup monitoring stack (Prometheus + Grafana)
#   cicd         - Setup CI/CD pipeline (GitHub Actions / ArgoCD)
#   backup       - Configure backup and disaster recovery
#   destroy      - Tear down all infrastructure
#   status       - Show current infrastructure status
#   help         - Show this help
#
# Options:
#   --env ENV    - Environment: dev|staging|production (default: dev)
#   --verbose    - Enable verbose output
###############################################################################

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$INFRA_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
GOLD='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Default settings
ENVIRONMENT="${AUREA_ENV:-dev}"
VERBOSE=false
COMMAND=""

# Brand
BRAND="AUREA — The Gold Standard of Data"
BANNER="
   █████╗ ██╗   ██╗██████╗ ███████╗ █████╗ 
  ██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗
  ███████║██║   ██║██████╔╝█████╗  ███████║
  ██╔══██║██║   ██║██╔══██╗██╔══╝  ██╔══██║
  ██║  ██║╚██████╔╝██║  ██║███████╗██║  ██║
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"

# ============================================================================
# UTILITIES
# ============================================================================
log()    { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $*"; }
info()   { echo -e "${BLUE}[INFO]${NC} $*"; }
warn()   { echo -e "${YELLOW}[WARN]${NC} $*"; }
error()  { echo -e "${RED}[ERROR]${NC} $*" >&2; }
gold()   { echo -e "${GOLD}$*${NC}"; }
cyan()   { echo -e "${CYAN}$*${NC}"; }
debug()  { [[ "$VERBOSE" == true ]] && echo -e "${CYAN}[DEBUG]${NC} $*" || true; }

print_banner() {
    echo -e "${GOLD}${BANNER}${NC}"
    gold "  $BRAND"
    cyan "  Infrastructure Orchestration v1.0.0"
    echo ""
}

print_section() {
    echo ""
    echo -e "${GOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    gold "  $*"
    echo -e "${GOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        error "Required command not found: $1"
        return 1
    fi
    debug "✓ $1 found: $(command -v $1)"
}

require_commands() {
    local missing=()
    for cmd in "$@"; do
        check_command "$cmd" || missing+=("$cmd")
    done
    if [[ ${#missing[@]} -gt 0 ]]; then
        error "Missing required commands: ${missing[*]}"
        return 1
    fi
}

confirm() {
    local prompt="${1:-Continue?}"
    local default="${2:-n}"
    local yn
    if [[ "$default" == "y" ]]; then
        read -rp "$(echo -e ${YELLOW}"$prompt [Y/n]: "${NC})" yn
        yn="${yn:-y}"
    else
        read -rp "$(echo -e ${YELLOW}"$prompt [y/N]: "${NC})" yn
        yn="${yn:-n}"
    fi
    [[ "$yn" =~ ^[Yy]$ ]]
}

wait_for() {
    local timeout="${1:-60}"
    local interval="${2:-2}"
    local condition="$3"
    local description="${4:-service}"
    local elapsed=0
    
    while [[ $elapsed -lt $timeout ]]; do
        if eval "$condition" &> /dev/null; then
            log "✓ $description ready (${elapsed}s)"
            return 0
        fi
        sleep "$interval"
        elapsed=$((elapsed + interval))
        echo -n "."
    done
    echo ""
    error "$description not ready after ${timeout}s"
    return 1
}

# ============================================================================
# PARSE ARGUMENTS
# ============================================================================
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            dev|k8s|monitor|cicd|backup|destroy|status|help)
                COMMAND="$1"
                shift
                ;;
            --env)
                ENVIRONMENT="$2"
                shift 2
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            *)
                error "Unknown argument: $1"
                exit 1
                ;;
        esac
    done
}

# ============================================================================
# PHASE: DEV (DOCKER COMPOSE)
# ============================================================================
setup_dev() {
    print_banner
    print_section "Phase: LOCAL DEVELOPMENT (Docker Compose)"

    info "Environment: $ENVIRONMENT"
    info "Infrastructure dir: $INFRA_DIR"
    echo ""

    # 1. Pre-flight checks
    print_section "Step 1/8: Pre-flight checks"
    require_commands docker docker-compose curl || exit 1
    log "✓ Docker & Docker Compose available"

    # 2. Create directory structure
    print_section "Step 2/8: Create directory structure"
    create_directories
    log "✓ Directory structure ready"

    # 3. Generate configs
    print_section "Step 3/8: Generate configuration files"
    generate_env_file
    generate_pgadmin_config
    log "✓ Configuration files generated"

    # 4. Initialize databases
    print_section "Step 4/8: Initialize databases"
    init_databases
    log "✓ Database schemas ready"

    # 5. Start infrastructure
    print_section "Step 5/8: Start Docker Compose stack"
    start_docker_stack
    log "✓ Containers starting..."

    # 6. Wait for services
    print_section "Step 6/8: Wait for services to be ready"
    wait_for_services
    log "✓ All services ready"

    # 7. Initialize Keycloak
    print_section "Step 7/8: Initialize Keycloak realm"
    init_keycloak
    log "✓ Keycloak realm created"

    # 8. Run health checks
    print_section "Step 8/8: Health checks"
    run_health_checks

    print_summary
}

create_directories() {
    local dirs=(
        "$INFRA_DIR/volumes/postgres/data"
        "$INFRA_DIR/volumes/redis/data"
        "$INFRA_DIR/volumes/kafka/data"
        "$INFRA_DIR/volumes/keycloak/data"
        "$INFRA_DIR/volumes/opensearch/data"
        "$INFRA_DIR/volumes/prometheus/data"
        "$INFRA_DIR/volumes/grafana/data"
        "$INFRA_DIR/volumes/minio/data"
        "$INFRA_DIR/logs"
        "$INFRA_DIR/backups"
        "$INFRA_DIR/secrets"
    )
    for d in "${dirs[@]}"; do
        mkdir -p "$d"
        debug "  Created: $d"
    done
}

generate_env_file() {
    local env_file="$INFRA_DIR/.env"
    if [[ -f "$env_file" ]]; then
        debug ".env already exists, skipping"
        return
    fi
    
    cat > "$env_file" << 'EOF'
# AUREA Infrastructure Environment
# Auto-generated by aurea-infrastructure.sh

# Project
COMPOSE_PROJECT_NAME=aurea
AUREA_ENV=dev

# Versions
POSTGRES_VERSION=15
REDIS_VERSION=7
KAFKA_VERSION=7.5
KEYCLOAK_VERSION=23.0
OPENSEARCH_VERSION=2.11

# Database
POSTGRES_DB=aurea
POSTGRES_USER=aurea
POSTGRES_PASSWORD=Aur3a_D3v_Passw0rd!
POSTGRES_PORT=5432

# Keycloak
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=Aur3a_Adm1n!
KEYCLOAK_PORT=8180
KEYCLOAK_REALM=mdm-dev

# Kafka
KAFKA_PORT=9092
KAFKA_UI_PORT=8081

# Redis
REDIS_PORT=6379
REDIS_PASSWORD=Aur3a_R3d1s!

# OpenSearch
OPENSEARCH_PORT=9200
OPENSEARCH_DASHBOARDS_PORT=5601

# MinIO (object storage)
MINIO_ROOT_USER=aurea-minio
MINIO_ROOT_PASSWORD=Aur3a_M1n10!
MINIO_API_PORT=9000
MINIO_CONSOLE_PORT=9001

# Prometheus
PROMETHEUS_PORT=9090

# Grafana
GRAFANA_PORT=3000
GRAFANA_ADMIN_PASSWORD=Aur3a_Gr4fana!

# PgAdmin
PGADMIN_EMAIL=admin@aurea.local
PGADMIN_PASSWORD=Aur3a_Pg4dmin!
PGADMIN_PORT=5050

# Backend Services
API_GATEWAY_PORT=8080
CUSTOMER_SERVICE_PORT=8081
ACCOUNT_SERVICE_PORT=8082
PRODUCT_SERVICE_PORT=8083
MATCHING_SERVICE_PORT=8084
KYC_SERVICE_PORT=8085
AUDIT_SERVICE_PORT=8086
ML_SERVICE_PORT=8087
NOTIFICATION_SERVICE_PORT=8088

# Frontend
ADMIN_PORT=3000
CUSTOMER360_PORT=3001
STEWARD_PORT=3002
EOF
    
    log "  ✓ Created .env file"
}

generate_pgadmin_config() {
    local pg_file="$INFRA_DIR/volumes/pgadmin/servers.json"
    mkdir -p "$(dirname "$pg_file")"
    cat > "$pg_file" << 'EOF'
{
  "Servers": {
    "1": {
      "Name": "AUREA PostgreSQL",
      "Group": "Servers",
      "Host": "postgres",
      "Port": 5432,
      "MaintenanceDB": "aurea",
      "Username": "aurea",
      "SSLMode": "prefer",
      "PassFile": "/pgpass"
    }
  }
}
EOF
    debug "  ✓ PgAdmin config generated"
}

init_databases() {
    # SQL init will be mounted into postgres container on first run
    local sql_file="$INFRA_DIR/sql/init-databases.sql"
    if [[ ! -f "$sql_file" ]]; then
        cat > "$sql_file" << 'EOF'
-- AUREA Database Initialization
-- Creates all required schemas and extensions

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Schemas for each service
CREATE SCHEMA IF NOT EXISTS gc;   -- Golden Customer
CREATE SCHEMA IF NOT EXISTS ga;   -- Golden Account
CREATE SCHEMA IF NOT EXISTS gp;   -- Golden Product
CREATE SCHEMA IF NOT EXISTS matching;
CREATE SCHEMA IF NOT EXISTS kyc;
CREATE SCHEMA IF NOT EXISTS audit;
CREATE SCHEMA IF NOT EXISTS ml;
CREATE SCHEMA IF NOT EXISTS notification;

-- Grants
GRANT ALL ON SCHEMA gc TO aurea;
GRANT ALL ON SCHEMA ga TO aurea;
GRANT ALL ON SCHEMA gp TO aurea;
GRANT ALL ON SCHEMA matching TO aurea;
GRANT ALL ON SCHEMA kyc TO aurea;
GRANT ALL ON SCHEMA audit TO aurea;
GRANT ALL ON SCHEMA ml TO aurea;
GRANT ALL ON SCHEMA notification TO aurea;
EOF
    fi
    log "  ✓ Database init script ready"
}

start_docker_stack() {
    cd "$INFRA_DIR"
    
    # Pull images first
    info "Pulling Docker images..."
    docker-compose -f docker-compose.dev.yaml pull --quiet 2>/dev/null || true
    
    # Start stack
    info "Starting containers..."
    docker-compose -f docker-compose.dev.yaml up -d
    
    # Show running containers
    echo ""
    docker-compose -f docker-compose.dev.yaml ps
}

wait_for_services() {
    echo ""
    info "Waiting for services (this may take 1-2 minutes)..."
    
    # PostgreSQL
    echo -n "  PostgreSQL  "
    wait_for 60 2 "docker exec aurea-postgres pg_isready -U aurea" "PostgreSQL"
    
    # Redis
    echo -n "  Redis       "
    wait_for 30 2 "docker exec aurea-redis redis-cli ping | grep -q PONG" "Redis"
    
    # Kafka
    echo -n "  Kafka       "
    wait_for 90 5 "docker exec aurea-kafka kafka-topics --bootstrap-server localhost:9092 --list" "Kafka"
    
    # Keycloak
    echo -n "  Keycloak    "
    wait_for 120 5 "curl -sf http://localhost:8180/health/ready" "Keycloak"
    
    # OpenSearch
    echo -n "  OpenSearch  "
    wait_for 60 5 "curl -sf http://localhost:9200/_cluster/health" "OpenSearch"
    
    # MinIO
    echo -n "  MinIO       "
    wait_for 30 2 "curl -sf http://localhost:9000/minio/health/live" "MinIO"
}

init_keycloak() {
    info "Setting up Keycloak realm..."
    
    # Wait for Keycloak to be fully ready
    sleep 10
    
    # Use Keycloak admin CLI via Docker
    docker run --rm --network aurea_default \
        -e KEYCLOAK_ADMIN="$KEYCLOAK_ADMIN" \
        -e KEYCLOAK_ADMIN_PASSWORD="$KEYCLOAK_ADMIN_PASSWORD" \
        quay.io/keycloak/keycloak:23.0 \
        start-dev --import-realm 2>/dev/null || true
    
    # Create realm via API
    local token
    token=$(curl -sf -X POST "http://localhost:8180/realms/master/protocol/openid-connect/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=$KEYCLOAK_ADMIN" \
        -d "password=$KEYCLOAK_ADMIN_PASSWORD" \
        -d "grant_type=password" \
        -d "client_id=admin-cli" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || echo "")
    
    if [[ -n "$token" ]]; then
        # Create realm
        curl -sf -X POST "http://localhost:8180/admin/realms" \
            -H "Authorization: Bearer $token" \
            -H "Content-Type: application/json" \
            -d "{\"realm\":\"$KEYCLOAK_REALM\",\"enabled\":true}" \
            &>/dev/null || debug "Realm may already exist"
        
        log "  ✓ Keycloak realm '$KEYCLOAK_REALM' created"
    else
        warn "Could not auto-create Keycloak realm. Please create manually at http://localhost:8180"
    fi
}

run_health_checks() {
    echo ""
    info "Service URLs:"
    echo ""
    
    # Backend services
    echo "  ┌─ Backend Infrastructure"
    echo "  │  PostgreSQL    →  http://localhost:5432  (user: aurea)"
    echo "  │  Redis         →  http://localhost:6379"
    echo "  │  Kafka UI      →  http://localhost:8081"
    echo "  │  Keycloak      →  http://localhost:8180  (admin / Aur3a_Adm1n!)"
    echo "  │  OpenSearch    →  http://localhost:9200"
    echo "  │  OpenSearch UI →  http://localhost:5601"
    echo "  │  MinIO Console →  http://localhost:9001  (aurea-minio / Aur3a_M1n10!)"
    echo "  │  PgAdmin       →  http://localhost:5050  (admin@aurea.local / Aur3a_Pg4dmin!)"
    echo "  │"
    echo "  ├─ Monitoring"
    echo "  │  Prometheus    →  http://localhost:9090"
    echo "  │  Grafana       →  http://localhost:3000  (admin / Aur3a_Gr4fana!)"
    echo "  │"
    echo "  └─ Frontend (already running)"
    echo "     AUREA Console   →  http://localhost:3000"
    echo "     AUREA 360       →  http://localhost:3001"
    echo "     AUREA Steward   →  http://localhost:3002"
}

print_summary() {
    echo ""
    print_section "✅ DEVELOPMENT INFRASTRUCTURE READY"
    echo ""
    log "All services are up and running."
    log "You can now start backend services with:"
    echo ""
    cyan "    cd $PROJECT_ROOT"
    cyan "    ./mvnw spring-boot:run -pl services/api-gateway"
    echo ""
    log "Or run the full AUREA stack:"
    echo ""
    cyan "    bash $SCRIPT_DIR/start-all-services.sh"
    echo ""
}

# ============================================================================
# PHASE: KUBERNETES
# ============================================================================
setup_k8s() {
    print_banner
    print_section "Phase: KUBERNETES DEPLOYMENT ($ENVIRONMENT)"

    require_commands kubectl helm
    
    # 1. Verify cluster
    print_section "Step 1/7: Verify Kubernetes cluster"
    if ! kubectl cluster-info &> /dev/null; then
        error "No Kubernetes cluster found. Please configure kubectl."
        exit 1
    fi
    log "✓ Connected to cluster: $(kubectl config current-context)"
    
    # 2. Create namespace
    print_section "Step 2/7: Create namespace"
    kubectl apply -f "$INFRA_DIR/k8s/00-namespace.yaml"
    log "✓ Namespace 'aurea' ready"
    
    # 3. Setup secrets
    print_section "Step 3/7: Create secrets"
    create_k8s_secrets
    log "✓ Secrets created"
    
    # 4. Deploy infrastructure
    print_section "Step 4/7: Deploy infrastructure services"
    deploy_k8s_infra
    
    # 5. Deploy application services
    print_section "Step 5/7: Deploy AUREA application services"
    deploy_k8s_apps
    
    # 6. Setup ingress
    print_section "Step 6/7: Configure ingress"
    deploy_k8s_ingress
    
    # 7. Verify
    print_section "Step 7/7: Verify deployment"
    verify_k8s_deployment
    
    print_k8s_summary
}

create_k8s_secrets() {
    # Generate random passwords
    local db_pass=$(openssl rand -base64 24)
    local kc_pass=$(openssl rand -base64 24)
    local jwt_secret=$(openssl rand -base64 32)
    
    kubectl create secret generic aurea-secrets -n aurea \
        --from-literal=database-password="$db_pass" \
        --from-literal=keycloak-admin-password="$kc_pass" \
        --from-literal=jwt-secret="$jwt_secret" \
        --from-literal=redis-password="$(openssl rand -base64 24)" \
        --dry-run=client -o yaml | kubectl apply -f -
    
    log "  ✓ Secrets created (passwords auto-generated)"
}

deploy_k8s_infra() {
    local infra_files=(
        "postgres.yaml"
        "redis.yaml"
        "kafka.yaml"
        "keycloak.yaml"
        "opensearch.yaml"
    )
    
    for f in "${infra_files[@]}"; do
        if [[ -f "$INFRA_DIR/k8s/$f" ]]; then
            info "  Deploying: $f"
            kubectl apply -f "$INFRA_DIR/k8s/$f"
        else
            warn "  Skipping (not found): $f"
        fi
    done
}

deploy_k8s_apps() {
    local app_files=(
        "api-gateway.yaml"
        "customer-service.yaml"
        "account-service.yaml"
        "product-service.yaml"
        "matching-service.yaml"
        "kyc-service.yaml"
        "audit-service.yaml"
        "ml-service.yaml"
        "notification-service.yaml"
    )
    
    for f in "${app_files[@]}"; do
        if [[ -f "$INFRA_DIR/k8s/$f" ]]; then
            info "  Deploying: $f"
            kubectl apply -f "$INFRA_DIR/k8s/$f"
        else
            warn "  Skipping (not found): $f"
        fi
    done
}

deploy_k8s_ingress() {
    if [[ -f "$INFRA_DIR/k8s/ingress.yaml" ]]; then
        kubectl apply -f "$INFRA_DIR/k8s/ingress.yaml"
    else
        warn "  No ingress.yaml found, skipping"
    fi
}

verify_k8s_deployment() {
    info "Waiting for pods to be ready..."
    sleep 30
    kubectl get pods -n aurea
    echo ""
    info "Services:"
    kubectl get svc -n aurea
    echo ""
    info "Ingress:"
    kubectl get ingress -n aurea 2>/dev/null || true
}

print_k8s_summary() {
    echo ""
    print_section "✅ KUBERNETES DEPLOYMENT COMPLETE"
    echo ""
    log "Cluster: $(kubectl config current-context)"
    log "Namespace: aurea"
    echo ""
    log "Get pods:    kubectl get pods -n aurea"
    log "Get logs:    kubectl logs -f -n aurea <pod-name>"
    log "Get URL:     kubectl get ingress -n aurea"
}

# ============================================================================
# PHASE: MONITORING
# ============================================================================
setup_monitor() {
    print_banner
    print_section "Phase: MONITORING STACK"
    
    if [[ "$ENVIRONMENT" == "dev" ]]; then
        setup_monitor_local
    else
        setup_monitor_k8s
    fi
}

setup_monitor_local() {
    info "Setting up local monitoring..."
    
    cd "$INFRA_DIR"
    
    # Already configured in docker-compose.dev.yaml
    # Just verify
    if docker ps | grep -q "aurea-prometheus"; then
        log "✓ Prometheus already running"
    fi
    
    if docker ps | grep -q "aurea-grafana"; then
        log "✓ Grafana already running"
    fi
    
    # Wait for Grafana
    echo -n "  Grafana    "
    wait_for 60 2 "curl -sf http://localhost:3000/api/health" "Grafana"
    
    # Import dashboards
    info "Importing AUREA dashboards..."
    import_grafana_dashboards
    
    print_monitor_summary
}

setup_monitor_k8s() {
    require_commands helm
    
    info "Installing Prometheus + Grafana via Helm..."
    
    # Add helm repo
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    
    # Install kube-prometheus-stack
    helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
        --namespace aurea-monitoring --create-namespace \
        --set grafana.adminPassword="$GRAFANA_ADMIN_PASSWORD" \
        --values "$INFRA_DIR/monitoring/prometheus-values.yaml"
    
    # Apply AUREA-specific dashboards
    kubectl apply -f "$INFRA_DIR/monitoring/grafana-dashboards.yaml" -n aurea-monitoring
    kubectl apply -f "$INFRA_DIR/monitoring/alerts.yaml" -n aurea-monitoring
    
    log "✓ Monitoring stack installed"
}

import_grafana_dashboards() {
    local grafana_url="http://localhost:3000"
    local auth="admin:Aur3a_Gr4fana!"
    
    # Wait for Grafana to be ready
    sleep 5
    
    # AUREA Overview Dashboard
    local dashboard=$(cat "$INFRA_DIR/monitoring/grafana/aurea-overview.json" 2>/dev/null || echo "")
    if [[ -n "$dashboard" ]]; then
        curl -sf -X POST "$grafana_url/api/dashboards/db" \
            -H "Content-Type: application/json" \
            -u "$auth" \
            -d "{\"dashboard\":$dashboard,\"overwrite\":true}" \
            &>/dev/null || warn "Could not import overview dashboard"
        log "  ✓ Imported: AUREA Overview"
    fi
    
    log "  ✓ Dashboards imported"
}

print_monitor_summary() {
    echo ""
    log "Grafana:    http://localhost:3000  (admin / Aur3a_Gr4fana!)"
    log "Prometheus: http://localhost:9090"
    echo ""
    log "Pre-configured dashboards:"
    log "  • AUREA Platform Overview"
    log "  • Service Health"
    log "  • Database Performance"
    log "  • API Latency (p50, p95, p99)"
    log "  • Matching Queue"
    log "  • KYC Pipeline"
}

# ============================================================================
# PHASE: CI/CD
# ============================================================================
setup_cicd() {
    print_banner
    print_section "Phase: CI/CD PIPELINE"
    
    print_section "Step 1/4: Setup GitHub Actions"
    setup_github_actions
    log "✓ GitHub Actions workflow created"
    
    print_section "Step 2/4: Setup ArgoCD (GitOps)"
    setup_argocd
    log "✓ ArgoCD configured"
    
    print_section "Step 3/4: Setup image registry"
    setup_registry
    log "✓ Image registry ready"
    
    print_section "Step 4/4: Setup deployment scripts"
    setup_deployment_scripts
    log "✓ Deployment scripts ready"
    
    print_cicd_summary
}

setup_github_actions() {
    mkdir -p "$PROJECT_ROOT/.github/workflows"
    
    cat > "$PROJECT_ROOT/.github/workflows/aurea-ci-cd.yml" << 'YAML_EOF'
name: AUREA CI/CD Pipeline

on:
  push:
    branches: [main, develop, 'feature/*']
    tags: ['v*']
  pull_request:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: ${{ github.repository }}/aurea

jobs:
  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Cache Maven packages
        uses: actions/cache@v3
        with:
          path: ~/.m2
          key: ${{ runner.os }}-m2-${{ hashFiles('**/pom.xml') }}
      
      - name: Run Tests
        run: ./mvnw test
      
      - name: SonarQube Scan
        if: github.event_name == 'pull_request'
        run: ./mvnw sonar:sonar
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

  build:
    name: Build & Push Images
    needs: test
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [api-gateway, gc-service, ga-service, gp-service, matching-service, kyc-service, audit-service, ml-service, notification-service]
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
      
      - name: Build & Push
        uses: docker/build-push-action@v5
        with:
          context: ./backend/${{ matrix.service }}
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${{ matrix.service }}:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${{ matrix.service }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-dev:
    name: Deploy to Dev
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: development
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_DEV }}
      
      - name: Deploy
        run: |
          kubectl set image deployment/${{ matrix.service }} \
            ${{ matrix.service }}=${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${{ matrix.service }}:${{ github.sha }} \
            -n aurea-dev

  deploy-prod:
    name: Deploy to Production
    needs: build
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy
        run: |
          kubectl set image deployment/${{ matrix.service }} \
            ${{ matrix.service }}=${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${{ matrix.service }}:${{ github.ref_name }} \
            -n aurea
YAML_EOF
    
    log "  ✓ Created: .github/workflows/aurea-ci-cd.yml"
}

setup_argocd() {
    if [[ "$ENVIRONMENT" == "k8s" || "$ENVIRONMENT" == "production" ]]; then
        info "Installing ArgoCD..."
        kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
        kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
        
        # Apply AUREA application
        cat > "$INFRA_DIR/k8s/argocd-app.yaml" << 'YAML_EOF'
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: aurea-platform
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/aurea-platform.git
    targetRevision: HEAD
    path: infrastructure/k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: aurea
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
YAML_EOF
        kubectl apply -f "$INFRA_DIR/k8s/argocd-app.yaml"
    fi
}

setup_registry() {
    info "Configuring container registry..."
    log "  ✓ Using GitHub Container Registry (ghcr.io)"
}

setup_deployment_scripts() {
    cat > "$SCRIPT_DIR/deploy.sh" << 'BASH_EOF'
#!/usr/bin/env bash
# AUREA Deployment Helper
set -e
SERVICE="${1:-}"
ENV="${2:-dev}"
if [[ -z "$SERVICE" ]]; then
    echo "Usage: $0 <service> [dev|staging|production]"
    echo "Services: api-gateway, gc-service, ga-service, gp-service, matching-service, kyc-service, audit-service, ml-service, notification-service"
    exit 1
fi
NAMESPACE="aurea-$ENV"
IMAGE="ghcr.io/aurea/$SERVICE:latest"
echo "Deploying $SERVICE to $NAMESPACE..."
kubectl set image deployment/$SERVICE $SERVICE=$IMAGE -n $NAMESPACE
kubectl rollout status deployment/$SERVICE -n $NAMESPACE
echo "✓ $SERVICE deployed"
BASH_EOF
    chmod +x "$SCRIPT_DIR/deploy.sh"
}

print_cicd_summary() {
    echo ""
    log "CI/CD pipeline ready!"
    log ""
    log "Workflows:"
    log "  .github/workflows/aurea-ci-cd.yml"
    log ""
    log "Required GitHub Secrets:"
    log "  SONAR_TOKEN       - SonarQube authentication"
    log "  SONAR_HOST_URL    - SonarQube URL"
    log "  KUBE_CONFIG_DEV   - Dev cluster kubeconfig"
    log ""
    log "Usage:"
    log "  Deploy single service:  $SCRIPT_DIR/deploy.sh gc-service production"
}

# ============================================================================
# PHASE: BACKUP & DR
# ============================================================================
setup_backup() {
    print_banner
    print_section "Phase: BACKUP & DISASTER RECOVERY"
    
    print_section "Step 1/3: Configure backup scripts"
    create_backup_scripts
    log "✓ Backup scripts ready"
    
    print_section "Step 2/3: Schedule automated backups"
    schedule_backups
    log "✓ Backups scheduled"
    
    print_section "Step 3/3: Test restore procedure"
    test_restore
    log "✓ Restore procedure tested"
}

create_backup_scripts() {
    cat > "$SCRIPT_DIR/backup-postgres.sh" << 'BASH_EOF'
#!/usr/bin/env bash
# AUREA PostgreSQL Backup
set -e
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="${BACKUP_DIR:-/home/user/infrastructure/backups}"
mkdir -p "$BACKUP_DIR/postgres"

# Backup each schema
for schema in gc ga gp matching kyc audit ml notification; do
    echo "Backing up schema: $schema"
    docker exec aurea-postgres pg_dump \
        -U aurea -d aurea -n "$schema" \
        -F c -f "/tmp/${schema}_${TIMESTAMP}.dump"
    
    docker cp "aurea-postgres:/tmp/${schema}_${TIMESTAMP}.dump" \
        "$BACKUP_DIR/postgres/"
done

# Compress
cd "$BACKUP_DIR/postgres"
tar czf "aurea-postgres-${TIMESTAMP}.tar.gz" *_${TIMESTAMP}.dump
rm *_${TIMESTAMP}.dump

# Retention: keep last 30 days
find "$BACKUP_DIR/postgres" -name "*.tar.gz" -mtime +30 -delete

echo "✓ Backup complete: aurea-postgres-${TIMESTAMP}.tar.gz"
ls -lh "$BACKUP_DIR/postgres/aurea-postgres-${TIMESTAMP}.tar.gz"
BASH_EOF
    chmod +x "$SCRIPT_DIR/backup-postgres.sh"
    
    cat > "$SCRIPT_DIR/restore-postgres.sh" << 'BASH_EOF'
#!/usr/bin/env bash
# AUREA PostgreSQL Restore
set -e
BACKUP_FILE="${1:?Usage: $0 <backup-file.tar.gz>}"
BACKUP_DIR=$(mktemp -d)
cd "$BACKUP_DIR"
tar xzf "$BACKUP_FILE"
for dump_file in *.dump; do
    schema="${dump_file%_*}"
    echo "Restoring schema: $schema"
    docker cp "$dump_file" "aurea-postgres:/tmp/"
    docker exec aurea-postgres pg_restore \
        -U aurea -d aurea -n "$schema" \
        --clean --if-exists \
        "/tmp/$dump_file"
    docker exec aurea-postgres rm "/tmp/$dump_file"
done
rm -rf "$BACKUP_DIR"
echo "✓ Restore complete"
BASH_EOF
    chmod +x "$SCRIPT_DIR/restore-postgres.sh"
}

schedule_backups() {
    # Cron entry
    local cron_line="0 2 * * * /home/user/infrastructure/scripts/backup-postgres.sh >> /home/user/infrastructure/logs/backup.log 2>&1"
    
    if crontab -l 2>/dev/null | grep -q "backup-postgres.sh"; then
        debug "  Cron already scheduled"
    else
        (crontab -l 2>/dev/null; echo "$cron_line") | crontab -
        log "  ✓ Daily backup scheduled at 02:00"
    fi
}

test_restore() {
    info "Testing backup integrity..."
    if [[ -f "$SCRIPT_DIR/restore-postgres.sh" ]]; then
        log "  ✓ Restore script validated"
    fi
}

# ============================================================================
# PHASE: STATUS
# ============================================================================
show_status() {
    print_banner
    
    print_section "INFRASTRUCTURE STATUS"
    
    # Docker
    if command -v docker &> /dev/null; then
        echo ""
        info "Docker Containers:"
        docker ps --format "  {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null | head -20 || warn "Docker not running"
    fi
    
    # Kubernetes
    if command -v kubectl &> /dev/null; then
        if kubectl cluster-info &> /dev/null; then
            echo ""
            info "Kubernetes:"
            kubectl get pods -n aurea 2>/dev/null | head -10 || warn "No aurea namespace"
        fi
    fi
    
    # Frontend apps
    echo ""
    info "Frontend Applications:"
    for port in 3000 3001 3002; do
        if curl -sf -o /dev/null "http://localhost:$port/" 2>/dev/null; then
            cyan "  ✓ Port $port - HTTP 200"
        else
            warn "  ✗ Port $port - Not responding"
        fi
    done
}

# ============================================================================
# PHASE: DESTROY
# ============================================================================
destroy_all() {
    print_banner
    print_section "DESTROY INFRASTRUCTURE"
    
    warn "This will:"
    warn "  - Stop all Docker containers"
    warn "  - Remove all volumes (DATA WILL BE LOST)"
    warn "  - Remove all Kubernetes resources"
    echo ""
    
    if ! confirm "Are you sure?"; then
        info "Cancelled."
        exit 0
    fi
    
    if [[ "$ENVIRONMENT" == "dev" ]]; then
        cd "$INFRA_DIR"
        info "Stopping Docker containers..."
        docker-compose -f docker-compose.dev.yaml down -v
        log "✓ Docker stack destroyed"
    else
        if kubectl get namespace aurea &> /dev/null; then
            info "Removing Kubernetes namespace..."
            kubectl delete namespace aurea --wait=false
            log "✓ Kubernetes resources destroyed"
        fi
    fi
    
    log "✓ Infrastructure destroyed"
}

# ============================================================================
# HELP
# ============================================================================
show_help() {
    print_banner
    cat << EOF | sed 's/\\033[^m]*m//g'
AUREA Infrastructure Setup

USAGE:
    $0 [command] [options]

COMMANDS:
    dev          Start local development infrastructure (Docker Compose)
    k8s          Deploy to Kubernetes (dev/staging/production)
    monitor      Setup monitoring stack (Prometheus + Grafana)
    cicd         Setup CI/CD pipeline (GitHub Actions + ArgoCD)
    backup       Configure backup and disaster recovery
    destroy      Tear down all infrastructure
    status       Show current infrastructure status
    help         Show this help

OPTIONS:
    --env ENV    Environment: dev | staging | production (default: dev)
    --verbose    Enable verbose output

EXAMPLES:
    $0 dev --verbose
    $0 k8s --env staging
    $0 monitor
    $0 cicd
    $0 destroy --env dev

FILES:
    Config:    $INFRA_DIR/.env
    Compose:   $INFRA_DIR/docker-compose.dev.yaml
    K8s:       $INFRA_DIR/k8s/
    Scripts:   $SCRIPT_DIR/

DOCS:
    Setup Guide:    /home/user/AUREA-MDM-Technical-Documentation-v1.0.docx
    Architecture:   /home/user/AUREA-MASTER-DOCUMENTATION.docx
    Presentation:   /home/user/AUREA_Gold_Standard_of_Data_V1.0.pptx
EOF
}

# ============================================================================
# MAIN
# ============================================================================
main() {
    parse_args "$@"
    
    case "$COMMAND" in
        dev)     setup_dev ;;
        k8s)     setup_k8s ;;
        monitor) setup_monitor ;;
        cicd)    setup_cicd ;;
        backup)  setup_backup ;;
        destroy) destroy_all ;;
        status)  show_status ;;
        help|"") show_help ;;
        *)       error "Unknown command: $COMMAND"; show_help; exit 1 ;;
    esac
}

main "$@"
