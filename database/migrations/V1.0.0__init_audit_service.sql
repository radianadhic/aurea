-- =============================================
-- AUDIT SERVICE - Initial Schema
-- =============================================
-- Service: audit-service (Port 8084)
-- IMMUTABLE audit log (no UPDATE/DELETE allowed)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    action VARCHAR(50) NOT NULL,  -- CREATE, READ, UPDATE, DELETE, MERGE, BLACKLIST, etc
    user_id UUID,
    user_name VARCHAR(100),
    user_roles TEXT[],
    ip_address INET,
    user_agent TEXT,
    correlation_id UUID,  -- For distributed tracing
    request_id VARCHAR(100),
    service_name VARCHAR(50) NOT NULL,
    before_state JSONB,
    after_state JSONB,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Hash chain for tamper detection
    prev_hash VARCHAR(64),  -- SHA256 of previous entry
    hash VARCHAR(64) NOT NULL,  -- SHA256 of this entry (computed from prev_hash + all fields)
    
    CONSTRAINT chk_audit_action CHECK (action IN (
        'CREATE', 'READ', 'UPDATE', 'DELETE', 'MERGE', 'UNMERGE',
        'BLACKLIST', 'UNBLACKLIST', 'APPROVE', 'REJECT', 'LOGIN', 'LOGOUT',
        'EXPORT', 'IMPORT', 'BULK_OPERATION', 'WORKFLOW_TRANSITION',
        'PERMISSION_GRANT', 'PERMISSION_REVOKE', 'CONFIG_CHANGE'
    ))
);

CREATE INDEX idx_audit_resource ON audit_log(resource_type, resource_id);
CREATE INDEX idx_audit_user ON audit_log(user_id, created_at DESC);
CREATE INDEX idx_audit_action ON audit_log(action);
CREATE INDEX idx_audit_service ON audit_log(service_name, created_at DESC);
CREATE INDEX idx_audit_created ON audit_log(created_at DESC);
CREATE INDEX idx_audit_correlation ON audit_log(correlation_id);
CREATE INDEX idx_audit_ip ON audit_log(ip_address, created_at DESC);

COMMENT ON TABLE audit_log IS 'IMMUTABLE audit log - hash chain ensures tamper detection (compliance: UU PDP, OJK)';

-- Revoke UPDATE/DELETE to enforce immutability
REVOKE UPDATE, DELETE ON audit_log FROM mdm_user;
GRANT INSERT, SELECT ON audit_log TO mdm_user;
GRANT INSERT, SELECT, UPDATE, DELETE ON audit_log TO mdm_admin;

-- Audit log field changes (for UPDATE actions)
CREATE TABLE audit_field_changes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    audit_log_id UUID NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    sensitive BOOLEAN NOT NULL DEFAULT FALSE,  -- If true, value is masked
    
    CONSTRAINT fk_audit_field_changes_log FOREIGN KEY (audit_log_id) REFERENCES audit_log(id) ON DELETE CASCADE
);

CREATE INDEX idx_audit_field_changes_log ON audit_field_changes(audit_log_id);

REVOKE UPDATE, DELETE ON audit_field_changes FROM mdm_user;
