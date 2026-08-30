-- =============================================
-- AUTH SERVICE - Initial Schema (V1.0.0)
-- =============================================
-- Service: auth-service (Port 8081)
-- Database: PostgreSQL 16
-- Description: User sessions, MFA settings, audit login

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =============================================
-- Table: user_sessions
-- =============================================
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    ip_address INET,
    user_agent TEXT,
    access_token_jti VARCHAR(100) UNIQUE,
    refresh_token_hash VARCHAR(255),
    expires_at TIMESTAMPTZ NOT NULL,
    refresh_expires_at TIMESTAMPTZ,
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    revoked_at TIMESTAMPTZ,
    revoked_reason VARCHAR(100),
    last_active_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_user_sessions_user FOREIGN KEY (user_id) REFERENCES admin_service.users(id) ON DELETE CASCADE
);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id) WHERE revoked = FALSE;
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at) WHERE revoked = FALSE;
CREATE INDEX idx_user_sessions_access_token ON user_sessions(access_token_jti);

COMMENT ON TABLE user_sessions IS 'Active user login sessions (for revocation & monitoring)';

-- =============================================
-- Table: mfa_settings
-- =============================================
CREATE TABLE mfa_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE,
    method VARCHAR(20) NOT NULL CHECK (method IN ('TOTP', 'SMS', 'EMAIL', 'WEB_AUTHN')),
    secret_encrypted BYTEA NOT NULL,  -- Encrypted TOTP secret
    backup_codes_hash TEXT[],  -- BCrypt hashes of backup codes
    enabled BOOLEAN NOT NULL DEFAULT FALSE,
    enabled_at TIMESTAMPTZ,
    last_used_at TIMESTAMPTZ,
    failed_attempts INT NOT NULL DEFAULT 0,
    locked_until TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_mfa_settings_user FOREIGN KEY (user_id) REFERENCES admin_service.users(id) ON DELETE CASCADE
);

CREATE INDEX idx_mfa_settings_user_id ON mfa_settings(user_id);

-- =============================================
-- Table: password_reset_tokens
-- =============================================
CREATE TABLE password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    token_hash VARCHAR(255) NOT NULL UNIQUE,  -- SHA256 of reset token
    expires_at TIMESTAMPTZ NOT NULL,
    used BOOLEAN NOT NULL DEFAULT FALSE,
    used_at TIMESTAMPTZ,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_password_reset_user FOREIGN KEY (user_id) REFERENCES admin_service.users(id) ON DELETE CASCADE
);

CREATE INDEX idx_password_reset_token ON password_reset_tokens(token_hash);
CREATE INDEX idx_password_reset_expires ON password_reset_tokens(expires_at) WHERE used = FALSE;

-- =============================================
-- Table: login_attempts
-- =============================================
CREATE TABLE login_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    username_attempted VARCHAR(100) NOT NULL,
    ip_address INET NOT NULL,
    user_agent TEXT,
    success BOOLEAN NOT NULL,
    failure_reason VARCHAR(100),
    mfa_required BOOLEAN NOT NULL DEFAULT FALSE,
    mfa_success BOOLEAN,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_login_attempts_username ON login_attempts(username_attempted, created_at DESC);
CREATE INDEX idx_login_attempts_ip ON login_attempts(ip_address, created_at DESC);
CREATE INDEX idx_login_attempts_created ON login_attempts(created_at DESC);

COMMENT ON TABLE login_attempts IS 'Audit trail of all login attempts (for brute force detection)';

-- =============================================
-- Table: api_client_credentials
-- =============================================
CREATE TABLE api_client_credentials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id VARCHAR(100) NOT NULL UNIQUE,
    client_secret_hash VARCHAR(255) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    scopes TEXT[] NOT NULL DEFAULT '{}',
    service_account_user_id UUID,  -- Linked to users table
    rate_limit_per_minute INT NOT NULL DEFAULT 60,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    expires_at TIMESTAMPTZ,
    last_used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID NOT NULL,
    
    CONSTRAINT fk_client_created_by FOREIGN KEY (created_by) REFERENCES admin_service.users(id)
);

CREATE INDEX idx_client_credentials_enabled ON api_client_credentials(client_id) WHERE enabled = TRUE;

-- =============================================
-- Triggers
-- =============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_mfa_settings_updated_at
BEFORE UPDATE ON mfa_settings
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- Seed data
-- =============================================
-- No seed data for auth-service (uses Keycloak as source of truth)

-- =============================================
-- DOWN (Rollback)
-- =============================================
-- DROP TABLE IF EXISTS api_client_credentials CASCADE;
-- DROP TABLE IF EXISTS login_attempts CASCADE;
-- DROP TABLE IF EXISTS password_reset_tokens CASCADE;
-- DROP TABLE IF EXISTS mfa_settings CASCADE;
-- DROP TABLE IF EXISTS user_sessions CASCADE;
-- DROP FUNCTION IF EXISTS update_updated_at_column CASCADE;
