#!/usr/bin/env bash
###############################################################################
# AUREA PostgreSQL Backup Script
# Creates compressed backups of all schemas with 30-day retention
###############################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="${BACKUP_DIR:-$INFRA_DIR/backups/postgres}"
LOG_FILE="${LOG_FILE:-$INFRA_DIR/logs/backup.log}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()    { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $*" | tee -a "$LOG_FILE"; }
warn()   { echo -e "${YELLOW}[WARN]${NC} $*" | tee -a "$LOG_FILE"; }
error()  { echo -e "${RED}[ERROR]${NC} $*" | tee -a "$LOG_FILE" >&2; }

# Setup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

log "═══════════════════════════════════════════════════════════════"
log "  AUREA PostgreSQL Backup — $TIMESTAMP"
log "═══════════════════════════════════════════════════════════════"

# Detect container name
CONTAINER="${PG_CONTAINER:-mdm-postgres}"
DB_USER="${POSTGRES_USER:-mdm_admin}"
DB_NAME="${POSTGRES_DB:-mdm_auth}"

# Verify container is running
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    error "Container '$CONTAINER' is not running. Aborting."
    exit 1
fi
log "✓ Container verified: $CONTAINER"

# List of databases to backup
DATABASES=(
    "mdm_auth"
    "mdm_customer"
    "mdm_matching"
    "mdm_audit"
    "mdm_notification"
    "mdm_workflow"
    "mdm_product"
    "mdm_branch"
    "mdm_report"
    "mdm_ml"
    "mdm_integration"
    "mdm_document"
    "mdm_admin"
)

# Backup each database
for db in "${DATABASES[@]}"; do
    log "Backing up database: $db"
    
    # Check if database exists
    db_exists=$(docker exec "$CONTAINER" psql -U "$DB_USER" -tAc "SELECT 1 FROM pg_database WHERE datname='$db'" 2>/dev/null || echo "0")
    if [[ "$db_exists" != "1" ]]; then
        warn "  Skipping $db (does not exist)"
        continue
    fi
    
    BACKUP_FILE="$BACKUP_DIR/${db}_${TIMESTAMP}.dump"
    
    if docker exec "$CONTAINER" pg_dump \
        -U "$DB_USER" \
        -d "$db" \
        -F c \
        -Z 9 \
        -f "/tmp/${db}_${TIMESTAMP}.dump" 2>>"$LOG_FILE"; then
        
        docker cp "${CONTAINER}:/tmp/${db}_${TIMESTAMP}.dump" "$BACKUP_FILE"
        docker exec "$CONTAINER" rm "/tmp/${db}_${TIMESTAMP}.dump"
        
        size=$(du -h "$BACKUP_FILE" | cut -f1)
        log "  ✓ $db ($size) → $BACKUP_FILE"
    else
        error "  ✗ Failed to backup $db"
    fi
done

# Also do a global backup (users, roles, etc.)
GLOBAL_BACKUP="$BACKUP_DIR/global_${TIMESTAMP}.sql"
log "Backing up globals (users, roles)..."
if docker exec "$CONTAINER" pg_dumpall \
    -U "$DB_USER" \
    --globals-only \
    > "$GLOBAL_BACKUP" 2>>"$LOG_FILE"; then
    log "  ✓ Globals → $GLOBAL_BACKUP"
fi

# Create a single tar.gz archive
ARCHIVE="$BACKUP_DIR/aurea-backup-${TIMESTAMP}.tar.gz"
log "Creating archive..."
cd "$BACKUP_DIR"
tar czf "$ARCHIVE" \
    *_${TIMESTAMP}.dump \
    global_${TIMESTAMP}.sql 2>/dev/null

# Cleanup individual files
rm -f *_${TIMESTAMP}.dump global_${TIMESTAMP}.sql

archive_size=$(du -h "$ARCHIVE" | cut -f1)
log "✓ Archive created: $ARCHIVE ($archive_size)"

# Apply retention policy (keep 30 days)
log "Applying retention policy (30 days)..."
DELETED=$(find "$BACKUP_DIR" -name "aurea-backup-*.tar.gz" -mtime +30 -delete -print | wc -l)
log "✓ Cleaned up $DELETED old backup(s)"

# Verify backup integrity
log "Verifying backup integrity..."
if tar tzf "$ARCHIVE" &>/dev/null; then
    log "✓ Archive integrity verified"
else
    error "Archive integrity check failed!"
    exit 1
fi

# Summary
log "═══════════════════════════════════════════════════════════════"
log "  BACKUP COMPLETE"
log "  File:     $ARCHIVE"
log "  Size:     $archive_size"
log "  Database: ${#DATABASES[@]} databases + globals"
log "═══════════════════════════════════════════════════════════════"

# Optional: Upload to S3/MinIO
if [[ -n "${S3_BUCKET:-}" ]]; then
    log "Uploading to S3..."
    if command -v aws &> /dev/null; then
        aws s3 cp "$ARCHIVE" "s3://${S3_BUCKET}/postgres/" 2>>"$LOG_FILE" && \
            log "✓ Uploaded to s3://${S3_BUCKET}/postgres/"
    elif command -v mc &> /dev/null && [[ -n "${MC_ALIAS:-}" ]]; then
        mc cp "$ARCHIVE" "${MC_ALIAS}/postgres/" 2>>"$LOG_FILE" && \
            log "✓ Uploaded to ${MC_ALIAS}/postgres/"
    fi
fi

exit 0
