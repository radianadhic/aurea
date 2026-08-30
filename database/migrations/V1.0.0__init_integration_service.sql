-- =============================================
-- INTEGRATION SERVICE - Initial Schema
-- =============================================
-- Service: integration-service (Port 8091)

CREATE TABLE integrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(100) UNIQUE NOT NULL,  -- e.g., 'LOS', 'CMS', 'T24'
    name VARCHAR(200) NOT NULL,
    type VARCHAR(30) NOT NULL CHECK (type IN (
        'DATABASE', 'REST_API', 'SOAP', 'FTP', 'SFTP', 'KAFKA', 'WEBHOOK', 'FILE'
    )),
    direction VARCHAR(10) NOT NULL CHECK (direction IN ('INBOUND', 'OUTBOUND', 'BIDIRECTIONAL')),
    endpoint VARCHAR(500) NOT NULL,
    auth_config JSONB DEFAULT '{}'::jsonb,  -- Encrypted credentials
    config JSONB DEFAULT '{}'::jsonb,
    sync_mode VARCHAR(20) NOT NULL DEFAULT 'BATCH' CHECK (sync_mode IN (
        'REAL_TIME', 'BATCH', 'SCHEDULED', 'MANUAL', 'EVENT_DRIVEN'
    )),
    schedule_cron VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE', 'ERROR', 'MAINTENANCE')),
    last_sync_at TIMESTAMPTZ,
    last_sync_status VARCHAR(20),
    last_error TEXT,
    sync_interval_seconds INT,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE integration_sync_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    integration_id UUID NOT NULL,
    sync_type VARCHAR(20) NOT NULL CHECK (sync_type IN ('FULL', 'INCREMENTAL', 'MANUAL')),
    status VARCHAR(20) NOT NULL CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED', 'PARTIAL')),
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    records_processed INT NOT NULL DEFAULT 0,
    records_succeeded INT NOT NULL DEFAULT 0,
    records_failed INT NOT NULL DEFAULT 0,
    error_message TEXT,
    log_details JSONB DEFAULT '{}'::jsonb,
    
    CONSTRAINT fk_sync_logs_integration FOREIGN KEY (integration_id) REFERENCES integrations(id) ON DELETE CASCADE
);

CREATE TABLE field_mappings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    integration_id UUID NOT NULL,
    source_field VARCHAR(200) NOT NULL,
    target_field VARCHAR(200) NOT NULL,
    transformation VARCHAR(50),  -- DIRECT, UPPERCASE, LOWERCASE, DATE_FORMAT, etc
    transformation_config JSONB DEFAULT '{}'::jsonb,
    required BOOLEAN NOT NULL DEFAULT FALSE,
    default_value TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_mappings_integration FOREIGN KEY (integration_id) REFERENCES integrations(id) ON DELETE CASCADE
);
