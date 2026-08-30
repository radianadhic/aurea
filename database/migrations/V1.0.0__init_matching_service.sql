-- =============================================
-- MATCHING SERVICE - Initial Schema
-- =============================================
-- Service: matching-service (Port 8083)
-- Tables for matching rules and duplicate tracking

CREATE TABLE matching_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    field_name VARCHAR(100) NOT NULL,  -- e.g., 'fullName', 'nik', 'dateOfBirth'
    algorithm VARCHAR(30) NOT NULL CHECK (algorithm IN ('EXACT', 'LEVENSHTEIN', 'JAROWINKLER', 'PHONETIC', 'FUZZY', 'HYBRID')),
    weight DECIMAL(3,2) NOT NULL CHECK (weight BETWEEN 0 AND 1),
    threshold DECIMAL(3,2) NOT NULL CHECK (threshold BETWEEN 0 AND 1),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    priority INT NOT NULL DEFAULT 100,
    version INT NOT NULL DEFAULT 1,
    created_by UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    published_at TIMESTAMPTZ
);

CREATE INDEX idx_matching_rules_active ON matching_rules(active, priority) WHERE active = TRUE;

CREATE TABLE duplicate_candidates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id_1 UUID NOT NULL,
    customer_id_2 UUID NOT NULL,
    overall_score DECIMAL(4,3) NOT NULL,  -- 0.000-1.000
    match_details JSONB NOT NULL,  -- {field: score, ...}
    match_method VARCHAR(30) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'CONFIRMED', 'REJECTED')),
    reviewed_by UUID,
    reviewed_at TIMESTAMPTZ,
    review_notes TEXT,
    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT chk_not_self_match CHECK (customer_id_1 != customer_id_2),
    CONSTRAINT uq_duplicate_pair UNIQUE (customer_id_1, customer_id_2)
);

CREATE INDEX idx_duplicate_candidates_status ON duplicate_candidates(status);
CREATE INDEX idx_duplicate_candidates_customer1 ON duplicate_candidates(customer_id_1);
CREATE INDEX idx_duplicate_candidates_customer2 ON duplicate_candidates(customer_id_2);
CREATE INDEX idx_duplicate_candidates_score ON duplicate_candidates(overall_score DESC);

CREATE TABLE matching_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_type VARCHAR(30) NOT NULL CHECK (job_type IN ('FULL', 'INCREMENTAL', 'SPECIFIC')),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED')),
    total_customers INT NOT NULL DEFAULT 0,
    processed_count INT NOT NULL DEFAULT 0,
    found_duplicates INT NOT NULL DEFAULT 0,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    duration_seconds INT,
    error_message TEXT,
    triggered_by VARCHAR(50) NOT NULL,  -- SCHEDULED, MANUAL, AUTO_DEPLOY
    run_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
