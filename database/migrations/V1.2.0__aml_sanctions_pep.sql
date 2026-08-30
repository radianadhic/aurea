-- AML / Sanctions / PEP screening
CREATE TABLE aml_screenings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL,
    screening_type VARCHAR(50) NOT NULL CHECK (screening_type IN ('SANCTIONS', 'PEP', 'ADVERSE_MEDIA', 'WATCHLIST')),
    list_name VARCHAR(100),  -- e.g., 'OFAC', 'UN', 'EU', 'ID_DTTOT'
    match_status VARCHAR(20) NOT NULL CHECK (match_status IN ('CLEAR', 'POTENTIAL_MATCH', 'CONFIRMED_MATCH', 'FALSE_POSITIVE')),
    match_score DECIMAL(5,2),  -- 0.00-100.00
    matches JSONB DEFAULT '[]'::jsonb,  -- Array of match details
    screened_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    reviewed_by UUID,
    reviewed_at TIMESTAMPTZ,
    review_notes TEXT,
    next_screening_due TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_aml_screenings_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

CREATE INDEX idx_aml_screenings_customer ON aml_screenings(customer_id);
CREATE INDEX idx_aml_screenings_status ON aml_screenings(match_status) WHERE match_status != 'CLEAR';
CREATE INDEX idx_aml_screenings_due ON aml_screenings(next_screening_due) WHERE next_screening_due IS NOT NULL;

COMMENT ON TABLE aml_screenings IS 'AML sanctions / PEP / adverse media screening results (OJK, PPATK compliance)';
