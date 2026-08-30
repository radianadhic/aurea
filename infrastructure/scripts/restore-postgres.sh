#!/usr/bin/env bash
###############################################################################
# AUREA PostgreSQL Restore Script
# Restores from a backup archive created by backup-postgres.sh
###############################################################################

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()   { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

BACKUP_FILE="${1:-}"
TARGET_DB="${2:-all}"

if [[ -z "$BACKUP_FILE" ]]; then
    error "Usage: $0 <backup-file.tar.gz> [database-name]"
    echo ""
    echo "Available backups:"
    ls -1 /home/user/infrastructure/backups/postgres/*.tar.gz 2>/dev/null | tail -5 || echo "  No backups found"
    exit 1
fi

if [[ ! -f "$BACKUP_FILE" ]]; then
    error "Backup file not found: $BACKUP_FILE"
    exit 1
fi

CONTAINER="${PG_CONTAINER:-mdm-postgres}"
DB_USER="${POSTGRES_USER:-mdm_admin}"

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    error "Container '$CONTAINER' is not running."
    exit 1
fi

log "Verifying backup integrity..."
if ! tar tzf "$BACKUP_FILE" &>/dev/null; then
    error "Backup archive is corrupted!"
    exit 1
fi
log "Archive integrity verified"

log "Backup contents:"
tar tzf "$BACKUP_FILE" | head -20

echo ""
warn "WARNING: This will OVERWRITE existing data!"
warn "  Database: $TARGET_DB"
warn "  Backup:   $BACKUP_FILE"
echo ""

read -rp "$(echo -e ${YELLOW}"Continue with restore? [y/N]: "${NC})" yn
if [[ ! "$yn" =~ ^[Yy]$ ]]; then
    log "Cancelled."
    exit 0
fi

TMPDIR=$(mktemp -d)
log "Extracting backup..."
tar xzf "$BACKUP_FILE" -C "$TMPDIR"
log "Extracted to: $TMPDIR"

if [[ -f "$TMPDIR"/global_*.sql ]]; then
    log "Restoring globals (users/roles)..."
    cat "$TMPDIR"/global_*.sql | docker exec -i "$CONTAINER" psql -U "$DB_USER"
    log "Globals restored"
fi

for dump_file in "$TMPDIR"/*.dump; do
    [[ ! -f "$dump_file" ]] && continue
    db_name=$(basename "$dump_file" | cut -d'_' -f1)
    if [[ "$TARGET_DB" != "all" && "$TARGET_DB" != "$db_name" ]]; then
        continue
    fi
    log "Restoring database: $db_name"
    db_exists=$(docker exec "$CONTAINER" psql -U "$DB_USER" -tAc "SELECT 1 FROM pg_database WHERE datname='$db_name'" 2>/dev/null || echo "0")
    if [[ "$db_exists" != "1" ]]; then
        warn "  Database $db_name doesn't exist, creating..."
        docker exec "$CONTAINER" createdb -U "$DB_USER" "$db_name"
    fi
    docker cp "$dump_file" "${CONTAINER}:/tmp/restore.dump"
    if docker exec "$CONTAINER" pg_restore \
        -U "$DB_USER" \
        -d "$db_name" \
        --clean --if-exists \
        --no-owner \
        /tmp/restore.dump 2>&1 | grep -v "WARNING" || true; then
        log "  $db_name restored"
    fi
    docker exec "$CONTAINER" rm /tmp/restore.dump
done

rm -rf "$TMPDIR"
log "Cleanup complete"

log "========================================"
log "RESTORE COMPLETE"
log "========================================"
