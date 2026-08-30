-- ===========================================================================
-- V1: audit-service initial schema (immutable audit trail)
-- ===========================================================================

CREATE TABLE IF NOT EXISTS audit_entries (
    id                  UUID PRIMARY KEY,
    timestamp           TIMESTAMP WITH TIME ZONE NOT NULL,
    user_id             VARCHAR(50),
    username            VARCHAR(100),
    user_full_name      VARCHAR(200),
    user_role           VARCHAR(100),
    action              VARCHAR(50) NOT NULL,
    entity_type         VARCHAR(50) NOT NULL,
    entity_id           VARCHAR(100),
    ip_address          VARCHAR(45),
    user_agent          VARCHAR(500),
    request_method      VARCHAR(10),
    request_path        VARCHAR(500),
    response_status     INTEGER,
    result              VARCHAR(20) NOT NULL DEFAULT 'SUCCESS',
    error_message       VARCHAR(2000),
    correlation_id      VARCHAR(50),
    session_id          VARCHAR(100),
    source_service      VARCHAR(50),
    changes             JSONB DEFAULT '{}'::jsonb,
    metadata            JSONB DEFAULT '{}'::jsonb,
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMP WITH TIME ZONE,
    deleted_by          VARCHAR(50),
    deletion_reason     VARCHAR(500),

    CONSTRAINT chk_result CHECK (result IN ('SUCCESS', 'FAILURE', 'PARTIAL_SUCCESS'))
);

CREATE INDEX idx_audit_user ON audit_entries(user_id);
CREATE INDEX idx_audit_action ON audit_entries(action);
CREATE INDEX idx_audit_entity ON audit_entries(entity_type, entity_id);
CREATE INDEX idx_audit_timestamp ON audit_entries(timestamp DESC);
CREATE INDEX idx_audit_result ON audit_entries(result);
CREATE INDEX idx_audit_correlation ON audit_entries(correlation_id) WHERE correlation_id IS NOT NULL;
CREATE INDEX idx_audit_session ON audit_entries(session_id) WHERE session_id IS NOT NULL;
CREATE INDEX idx_audit_deleted ON audit_entries(deleted_at) WHERE deleted_at IS NULL;
CREATE INDEX idx_audit_user_time ON audit_entries(user_id, timestamp DESC);
CREATE INDEX idx_audit_action_time ON audit_entries(action, timestamp DESC);

-- GIN index for JSONB metadata search
CREATE INDEX idx_audit_metadata_gin ON audit_entries USING GIN (metadata);
CREATE INDEX idx_audit_changes_gin ON audit_entries USING GIN (changes);

-- Trigram index for username search
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_audit_username_trgm ON audit_entries USING GIN (username gin_trgm_ops);

-- View: recent failed operations
CREATE OR REPLACE VIEW v_recent_failures AS
SELECT id, timestamp, username, action, entity_type, entity_id, error_message
FROM audit_entries
WHERE result = 'FAILURE'
  AND timestamp >= NOW() - INTERVAL '7 days'
  AND deleted_at IS NULL
ORDER BY timestamp DESC;

-- View: high-risk actions audit
CREATE OR REPLACE VIEW v_high_risk_actions AS
SELECT id, timestamp, user_id, username, action, entity_type, entity_id, ip_address
FROM audit_entries
WHERE action IN ('CUSTOMER_DELETE', 'BLACKLIST_ADD', 'MATCH_MERGE', 'CONFIG_CHANGE', 'KYC_REJECT')
  AND deleted_at IS NULL
ORDER BY timestamp DESC;

COMMENT ON TABLE audit_entries IS 'Immutable audit trail - never hard-deleted (compliance with UU PDP, OJK, BI, PPATK)';
