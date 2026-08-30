-- ===========================================================================
-- V1: matching-service initial schema
-- ===========================================================================

CREATE TABLE IF NOT EXISTS match_groups (
    id                  UUID PRIMARY KEY,
    match_type          VARCHAR(20) NOT NULL,
    match_score         INTEGER NOT NULL CHECK (match_score >= 0 AND match_score <= 100),
    algorithm           VARCHAR(50) NOT NULL,
    status              VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    member_count        INTEGER NOT NULL DEFAULT 0,
    reviewer_id         VARCHAR(50),
    reviewer_name       VARCHAR(200),
    reviewed_at         TIMESTAMP WITH TIME ZONE,
    resolution_notes    VARCHAR(2000),
    rejection_reason    VARCHAR(500),
    auto_detected       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    version             BIGINT NOT NULL DEFAULT 0,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    created_by          VARCHAR(50),
    updated_by          VARCHAR(50),

    CONSTRAINT chk_match_type CHECK (match_type IN ('EXACT', 'FUZZY', 'PHONETIC', 'TRANSACTION')),
    CONSTRAINT chk_status CHECK (status IN ('PENDING', 'IN_REVIEW', 'AUTO_MERGED', 'MANUALLY_MERGED', 'REJECTED', 'ESCALATED'))
);

CREATE INDEX idx_match_groups_status ON match_groups(status);
CREATE INDEX idx_match_groups_score ON match_groups(match_score);
CREATE INDEX idx_match_groups_created ON match_groups(created_at);
CREATE INDEX idx_match_groups_type_status ON match_groups(match_type, status);
CREATE INDEX idx_match_groups_reviewer ON match_groups(reviewer_id) WHERE reviewer_id IS NOT NULL;
CREATE INDEX idx_match_groups_deleted ON match_groups(deleted_at) WHERE deleted_at IS NULL;

CREATE TABLE IF NOT EXISTS match_candidates (
    id                  UUID PRIMARY KEY,
    match_group_id      UUID NOT NULL REFERENCES match_groups(id) ON DELETE CASCADE,
    customer_id         VARCHAR(50) NOT NULL,
    cif_number          VARCHAR(30) NOT NULL,
    full_name           VARCHAR(200) NOT NULL,
    date_of_birth       DATE,
    nik                 VARCHAR(16),
    email               VARCHAR(200),
    mobile_phone        VARCHAR(20),
    address             VARCHAR(500),
    match_score         INTEGER NOT NULL,
    matched_fields      VARCHAR(500),
    is_primary          BOOLEAN NOT NULL DEFAULT FALSE,
    merge_selected      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    version             BIGINT NOT NULL DEFAULT 0,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    created_by          VARCHAR(50),
    updated_by          VARCHAR(50)
);

CREATE INDEX idx_match_cand_group ON match_candidates(match_group_id);
CREATE INDEX idx_match_cand_customer ON match_candidates(customer_id);
CREATE INDEX idx_match_cand_cif ON match_candidates(cif_number);
CREATE INDEX idx_match_cand_score ON match_candidates(match_score DESC);
CREATE INDEX idx_match_cand_deleted ON match_candidates(deleted_at) WHERE deleted_at IS NULL;

-- Auto-merge history
CREATE TABLE IF NOT EXISTS match_merge_log (
    id                  UUID PRIMARY KEY,
    match_group_id      UUID NOT NULL REFERENCES match_groups(id),
    primary_customer_id VARCHAR(50) NOT NULL,
    secondary_ids       TEXT NOT NULL,
    performed_by        VARCHAR(50) NOT NULL,
    manual              BOOLEAN NOT NULL,
    notes               VARCHAR(2000),
    merged_at           TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_merge_log_group ON match_merge_log(match_group_id);
CREATE INDEX idx_merge_log_primary ON match_merge_log(primary_customer_id);
CREATE INDEX idx_merge_log_date ON match_merge_log(merged_at);

-- Matching run history (batch jobs)
CREATE TABLE IF NOT EXISTS matching_runs (
    id                  UUID PRIMARY KEY,
    started_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at        TIMESTAMP WITH TIME ZONE,
    batch_size          INTEGER NOT NULL,
    customers_processed INTEGER NOT NULL DEFAULT 0,
    groups_created      INTEGER NOT NULL DEFAULT 0,
    auto_merged         INTEGER NOT NULL DEFAULT 0,
    status              VARCHAR(20) NOT NULL DEFAULT 'RUNNING',
    error_message       TEXT,
    triggered_by        VARCHAR(50)
);

CREATE INDEX idx_matching_runs_started ON matching_runs(started_at);
CREATE INDEX idx_matching_runs_status ON matching_runs(status);

-- View: pending matches by age
CREATE OR REPLACE VIEW v_match_age AS
SELECT
    id,
    status,
    match_score,
    created_at,
    EXTRACT(EPOCH FROM (NOW() - created_at))/3600 AS age_hours
FROM match_groups
WHERE status IN ('PENDING', 'IN_REVIEW')
  AND deleted_at IS NULL;

COMMENT ON TABLE match_groups IS 'Customer duplicate detection groups';
COMMENT ON TABLE match_candidates IS 'Customer records within a match group';
COMMENT ON TABLE match_merge_log IS 'Audit log of merge operations';
COMMENT ON TABLE matching_runs IS 'History of batch matching jobs';
