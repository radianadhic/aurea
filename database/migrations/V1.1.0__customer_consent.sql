-- Customer consent tracking (UU PDP / GDPR)
CREATE TABLE customer_consent (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL,
    consent_type VARCHAR(50) NOT NULL CHECK (consent_type IN (
        'MARKETING_EMAIL', 'MARKETING_SMS', 'MARKETING_WHATSAPP',
        'DATA_PROCESSING', 'DATA_SHARING', 'THIRD_PARTY_DISCLOSURE',
        'PROFILING', 'AUTOMATED_DECISION', 'CROSS_BORDER_TRANSFER'
    )),
    granted BOOLEAN NOT NULL,
    granted_at TIMESTAMPTZ,
    withdrawn_at TIMESTAMPTZ,
    consent_version VARCHAR(20) NOT NULL,
    purpose TEXT NOT NULL,
    legal_basis VARCHAR(50),  -- CONSENT, CONTRACT, LEGAL_OBLIGATION, VITAL_INTEREST, PUBLIC_TASK, LEGITIMATE_INTEREST
    expiry_date TIMESTAMPTZ,
    ip_address INET,
    user_agent TEXT,
    evidence_url TEXT,  -- Link to signed consent form (S3/MinIO)
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_customer_consent_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

CREATE INDEX idx_customer_consent_customer ON customer_consent(customer_id);
CREATE INDEX idx_customer_consent_type ON customer_consent(customer_id, consent_type);
CREATE INDEX idx_customer_consent_granted ON customer_consent(customer_id, consent_type) WHERE granted = TRUE;

COMMENT ON TABLE customer_consent IS 'Customer consent tracking (UU PDP / GDPR compliance)';
