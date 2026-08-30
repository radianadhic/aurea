# AUREA Infrastructure Setup

Automation scripts and configurations for AUREA Master Data Management platform.

## 📁 Structure

```
infrastructure/
├── scripts/                      # Automation scripts
│   ├── aurea-infrastructure.sh  # Master orchestrator (entry point)
│   ├── start-all-services.sh    # Start all backend services
│   ├── stop-all-services.sh     # Stop all backend services
│   ├── backup-postgres.sh       # PostgreSQL backup
│   ├── restore-postgres.sh      # PostgreSQL restore
│   ├── health-check.sh          # Health verification
│   ├── smoke-test.sh            # End-to-end functional tests
│   └── init-databases.sql       # Database initialization
├── docker-compose.dev.yaml       # Local dev infrastructure
├── k8s/                          # Kubernetes manifests
│   ├── 00-namespace.yaml
│   ├── api-gateway.yaml
│   ├── customer-service.yaml
│   ├── production/               # Production-grade configs
│   └── base/                     # Base configs (ConfigMap, Secrets)
├── monitoring/                   # Prometheus, Grafana, alerts
├── ci-cd/                        # CI/CD pipelines
├── observability/                # Loki, Tempo configs
├── istio/                        # Service mesh configs
├── terraform/                    # Infrastructure as Code
├── volumes/                      # Persistent data (mounted into containers)
├── logs/                         # Application logs
├── backups/                      # Database backups
└── .env                          # Environment variables (auto-generated)
```

## 🚀 Quick Start

### One-line setup
```bash
cd /home/user/infrastructure
./scripts/aurea-infrastructure.sh dev
```

### Available commands
```bash
./scripts/aurea-infrastructure.sh dev          # Start local dev infrastructure
./scripts/aurea-infrastructure.sh k8s          # Deploy to Kubernetes
./scripts/aurea-infrastructure.sh monitor      # Setup monitoring
./scripts/aurea-infrastructure.sh cicd         # Setup CI/CD
./scripts/aurea-infrastructure.sh backup       # Configure backups
./scripts/aurea-infrastructure.sh status       # Check current state
./scripts/aurea-infrastructure.sh destroy      # Tear down all
./scripts/aurea-infrastructure.sh help         # Show help
```

## 🛠️ Individual Scripts

| Script | Purpose |
|--------|---------|
| `aurea-infrastructure.sh` | **Master orchestrator** — one entry point for all infra operations |
| `start-all-services.sh` | Start all Spring Boot backend services in background |
| `stop-all-services.sh` | Gracefully stop all backend services |
| `health-check.sh` | Verify all services are healthy |
| `smoke-test.sh` | End-to-end functional test |
| `backup-postgres.sh` | Create compressed backup of all databases |
| `restore-postgres.sh` | Restore from a backup archive |

## 📋 Common Tasks

### First-time setup
```bash
cd /home/user/infrastructure
./scripts/aurea-infrastructure.sh dev --verbose
# Wait for "DEVELOPMENT INFRASTRUCTURE READY"
./scripts/health-check.sh
./scripts/smoke-test.sh
```

### Daily development
```bash
# Start infrastructure
cd /home/user/infrastructure
docker-compose -f docker-compose.dev.yaml up -d

# Start backend services
./scripts/start-all-services.sh

# Open apps
open http://localhost:3000  # AUREA Console
open http://localhost:8180  # Keycloak
open http://localhost:3000  # Grafana
```

### Backup before risky changes
```bash
./scripts/backup-postgres.sh
# Creates: backups/postgres/aurea-backup-YYYYMMDD_HHMMSS.tar.gz
```

### Restore from backup
```bash
./scripts/restore-postgres.sh backups/postgres/aurea-backup-20260120_140000.tar.gz
# Or specific database:
./scripts/restore-postgres.sh backup.tar.gz mdm_customer
```

### Check system health
```bash
./scripts/health-check.sh
# Shows: docker, services, databases, frontend
```

### Run end-to-end tests
```bash
./scripts/smoke-test.sh
# Tests: infrastructure, frontend, auth, monitoring, storage
```

### Stop everything
```bash
./scripts/stop-all-services.sh         # Stop backend
docker-compose -f docker-compose.dev.yaml down  # Stop infra
```

### Reset everything (DESTRUCTIVE)
```bash
./scripts/aurea-infrastructure.sh destroy
# Confirm: removes containers, volumes, data
```

## 🔐 Default Credentials

| Service | URL | Credentials |
|---------|-----|-------------|
| **AUREA Console** | http://localhost:3000 | (UI login via Keycloak) |
| **AUREA 360** | http://localhost:3001 | (UI login via Keycloak) |
| **AUREA Steward** | http://localhost:3002 | (UI login via Keycloak) |
| **Keycloak** | http://localhost:8180 | `admin` / `admin` |
| **Grafana** | http://localhost:3000 | `admin` / `admin` |
| **MinIO** | http://localhost:9001 | `minioadmin` / `minioadmin` |
| **pgAdmin** | http://localhost:5050 | `admin@admin.com` / `admin` |
| **Eureka** | http://localhost:8761 | (no auth) |
| **Prometheus** | http://localhost:9090 | (no auth) |
| **PostgreSQL** | localhost:5432 | `mdm_admin` / `mdm_dev_password` |

⚠️ **These are DEV credentials only. Change for production!**

## 🔄 CI/CD Pipeline

The CI/CD pipeline is auto-generated by `./scripts/aurea-infrastructure.sh cicd`:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   Git    │───▶│   CI     │───▶│  Tests   │───▶│  Build   │───▶│  Push    │
│  Push    │    │  Trigger │    │  + Lint  │    │ Docker   │    │ Registry │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                                     │
                                                                     ▼
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Prod    │◀───│  Smoke   │◀───│ Staging  │◀───│   Dev    │◀───│  ArgoCD  │
│  Deploy  │    │  Tests   │    │  Deploy  │    │  Deploy  │    │  Sync    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

Stages:
1. **Trigger** — push to `main`, `develop`, or `feature/*`
2. **Tests** — unit + integration + SonarQube
3. **Build** — multi-service Docker images
4. **Push** — to GitHub Container Registry
5. **Dev** — auto-deploy to dev cluster
6. **Staging** — auto-deploy with smoke tests
7. **Production** — manual approval, canary rollout (5% → 25% → 100%)

## 💾 Backup Strategy

| Component | Frequency | Retention | Location |
|-----------|-----------|-----------|----------|
| PostgreSQL | Daily 02:00 | 30 days | Local + S3/MinIO |
| OpenSearch snapshots | Weekly | 12 weeks | S3 |
| Kafka topics | Replicated 3x | 7 days | Brokers |
| Vault secrets | On change | Forever | Encrypted backup |
| Configuration | Git | Forever | Git history |

Cron job is auto-registered by `./scripts/aurea-infrastructure.sh backup`:
```
0 2 * * * /home/user/infrastructure/scripts/backup-postgres.sh
```

## 📊 Monitoring

- **Prometheus** — metrics collection (http://localhost:9090)
- **Grafana** — dashboards (http://localhost:3000)
- **Loki** — log aggregation
- **Tempo** — distributed tracing
- **AlertManager** — alerts to Slack/email

Pre-configured alerts:
- API latency > 500ms (p95)
- Error rate > 1%
- Database connections > 80% of max
- Disk usage > 85%
- Service down > 2 minutes
- Backup failure

## 🔧 Troubleshooting

### "Port already in use"
```bash
# Check what's using the port
lsof -i :3000
# Kill the process or change port in .env
```

### "Container won't start"
```bash
# Check logs
docker logs mdm-postgres
# Or for a specific service
docker logs mdm-postgres 2>&1 | tail -50
```

### "Database connection refused"
```bash
# Verify container is running
docker ps | grep postgres
# Check if accepting connections
docker exec mdm-postgres pg_isready -U mdm_admin
# Restart if needed
docker restart mdm-postgres
```

### "Keycloak not initializing"
```bash
# Reset Keycloak (DEV ONLY - data loss)
docker-compose -f docker-compose.dev.yaml down -v
docker-compose -f docker-compose.dev.yaml up -d keycloak
# Wait 60s for startup
```

### Reset everything
```bash
./scripts/aurea-infrastructure.sh destroy
# Then re-setup
./scripts/aurea-infrastructure.sh dev
```

## 📚 Related Documentation

- 📄 [AUREA-MDM-Technical-Documentation-v1.0.docx](../AUREA-MDM-Technical-Documentation-v1.0.docx) — full technical reference
- 📄 [AUREA-MASTER-DOCUMENTATION.docx](../AUREA-MASTER-DOCUMENTATION.docx) — branding & apps
- 📊 [AUREA_Gold_Standard_of_Data_V1.0.pptx](../AUREA_Gold_Standard_of_Data_V1.0.pptx) — exec presentation
- 🌐 http://localhost:3000 (Console) / 3001 (360) / 3002 (Steward) — live apps

## 🎯 Support

For issues, check:
1. `./scripts/health-check.sh` — quick diagnostic
2. `./scripts/smoke-test.sh` — full E2E test
3. Container logs: `docker logs <container>`
4. Service logs: `tail -f infrastructure/logs/*.log`
