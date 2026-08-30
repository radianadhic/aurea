-- KYC verification tracking
CREATE TABLE kyc_checks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL,
    kyc_level VARCHAR(20) NOT NULL CHECK (kyc_level IN ('SIMPLIFIED', 'STANDARD', 'ENHANCED', 'ULTIMATE')),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'IN_REVIEW', 'APPROVED', 'REJECTED', 'EXPIRED')),
    risk_level VARCHAR(10) CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH')),
    risk_score DECIMAL(5,2),  -- 0.00-100.00
    risk_factors JSONB DEFAULT '[]'::jsonb,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    reviewed_by UUID,
    approved_by UUID,
    rejection_reason TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_kyc_checks_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

CREATE INDEX idx_kyc_checks_customer ON kyc_checks(customer_id);
CREATE INDEX idx_kyc_checks_status ON kyc_checks(status);
CREATE INDEX idx_kyc_checks_expires ON kyc_checks(expires_at) WHERE status = 'APPROVED';

CREATE TABLE kyc_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    kyc_check_id UUID NOT NULL,
    document_id UUID NOT NULL,  -- Reference to document-service
    document_type VARCHAR(50) NOT NULL,  -- KTP, NPWP, PASSPORT, SELFIE, etc
    required BOOLEAN NOT NULL DEFAULT TRUE,
    verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_at TIMESTAMPTZ,
    verified_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_kyc_documents_check FOREIGN KEY (kyc_check_id) REFERENCES kyc_checks(id) ON DELETE CASCADE
);

CREATE INDEX idx_kyc_documents_check ON kyc_documents(kyc_check_id);
