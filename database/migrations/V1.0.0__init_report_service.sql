-- =============================================
-- REPORT SERVICE - Initial Schema (PostgreSQL metadata)
-- =============================================
-- Service: report-service (Port 8089)
-- Actual analytics data lives in ClickHouse

CREATE TABLE report_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    code VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(50),
    query_template TEXT NOT NULL,  -- SQL template with {{parameters}}
    parameters JSONB DEFAULT '[]'::jsonb,  -- List of parameter definitions
    output_format VARCHAR(20) NOT NULL DEFAULT 'TABLE' CHECK (output_format IN (
        'TABLE', 'CHART_LINE', 'CHART_BAR', 'CHART_PIE', 'EXCEL', 'PDF', 'JSON'
    )),
    cache_ttl_seconds INT DEFAULT 300,
    allowed_roles TEXT[] NOT NULL DEFAULT '{}',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE report_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_definition_id UUID NOT NULL,
    parameters JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (status IN (
        'PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED'
    )),
    row_count INT,
    duration_ms INT,
    error_message TEXT,
    result_url VARCHAR(500),  -- S3/MinIO URL
    run_by UUID NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    
    CONSTRAINT fk_report_runs_def FOREIGN KEY (report_definition_id) REFERENCES report_definitions(id)
);

CREATE TABLE dashboard_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    code VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    layout JSONB NOT NULL,  -- Grid layout with widgets
    widgets JSONB NOT NULL DEFAULT '[]'::jsonb,  -- Array of widget configs
    refresh_interval_seconds INT DEFAULT 60,
    allowed_roles TEXT[] NOT NULL DEFAULT '{}',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
