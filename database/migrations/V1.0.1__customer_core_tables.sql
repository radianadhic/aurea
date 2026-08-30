-- =============================================
-- CUSTOMER SERVICE - Customer Core Tables (V1.0.1)
-- =============================================
-- Service: customer-service (Port 8082)
-- Database: PostgreSQL 16
-- Description: Core customer (CIF) tables

-- =============================================
-- Table: customers (Main CIF table)
-- =============================================
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cif_number VARCHAR(20) UNIQUE NOT NULL,
    customer_type VARCHAR(20) NOT NULL CHECK (customer_type IN ('INDIVIDUAL', 'CORPORATE', 'SYARIAH')),
    full_name VARCHAR(255) NOT NULL,
    legal_name VARCHAR(255),
    date_of_birth DATE,
    place_of_birth VARCHAR(100),
    gender VARCHAR(10) CHECK (gender IN ('MALE', 'FEMALE')),
    nationality CHAR(2) DEFAULT 'ID',
    marital_status VARCHAR(20) CHECK (marital_status IN ('SINGLE', 'MARRIED', 'DIVORCED', 'WIDOWED')),
    religion VARCHAR(50),
    occupation VARCHAR(100),
    monthly_income DECIMAL(18,2),
    risk_profile VARCHAR(10) CHECK (risk_profile IN ('LOW', 'MEDIUM', 'HIGH')),
    pep_status BOOLEAN DEFAULT FALSE,
    sanctions_list TEXT[] DEFAULT '{}',
    kyc_status VARCHAR(20) NOT NULL DEFAULT 'PENDING' 
        CHECK (kyc_status IN ('PENDING', 'IN_REVIEW', 'APPROVED', 'REJECTED', 'EXPIRED')),
    kyc_expiry_date DATE,
    cif_status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' 
        CHECK (cif_status IN ('ACTIVE', 'DORMANT', 'CLOSED', 'BLACKLIST')),
    branch_id VARCHAR(50) NOT NULL,
    region_id VARCHAR(50),
    tags TEXT[] DEFAULT '{}',
    custom_fields JSONB DEFAULT '{}'::jsonb,
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by UUID,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version BIGINT NOT NULL DEFAULT 0,
    deleted_at TIMESTAMPTZ,
    merged_into_id UUID,
    merged_at TIMESTAMPTZ,
    
    CONSTRAINT fk_customers_branch FOREIGN KEY (branch_id) REFERENCES branch_service.branches(code),
    CONSTRAINT fk_customers_merged_into FOREIGN KEY (merged_into_id) REFERENCES customers(id)
);

-- Indexes
CREATE INDEX idx_customers_cif_number ON customers(cif_number) WHERE deleted_at IS NULL;
CREATE INDEX idx_customers_full_name ON customers USING gin(full_name gin_trgm_ops) WHERE deleted_at IS NULL;
CREATE INDEX idx_customers_branch_id ON customers(branch_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_customers_cif_status ON customers(cif_status) WHERE deleted_at IS NULL;
CREATE INDEX idx_customers_kyc_status ON customers(kyc_status) WHERE deleted_at IS NULL;
CREATE INDEX idx_customers_date_of_birth ON customers(date_of_birth) WHERE deleted_at IS NULL;
CREATE INDEX idx_customers_created_at ON customers(created_at DESC);
CREATE INDEX idx_customers_tags ON customers USING gin(tags) WHERE deleted_at IS NULL;
CREATE INDEX idx_customers_custom_fields ON customers USING gin(custom_fields) WHERE deleted_at IS NULL;
CREATE INDEX idx_customers_merged_into ON customers(merged_into_id) WHERE merged_into_id IS NOT NULL;
CREATE UNIQUE INDEX idx_customers_active_cif ON customers(cif_number) WHERE deleted_at IS NULL;

-- Comments
COMMENT ON TABLE customers IS 'Master table for Customer Information File (CIF)';
COMMENT ON COLUMN customers.cif_number IS 'CIF number (format: CIF-YYYY-NNNNNNNN)';
COMMENT ON COLUMN customers.custom_fields IS 'Dynamic custom fields (validated against schema)';
COMMENT ON COLUMN customers.merged_into_id IS 'If this customer was merged, points to the surviving customer';

-- Trigger
CREATE TRIGGER update_customers_updated_at
BEFORE UPDATE ON customers
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- Table: customer_identifiers
-- =============================================
CREATE TABLE customer_identifiers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('NIK', 'NPWP', 'NIB', 'PASSPORT', 'KITAS', 'SIM', 'AKTA_LAHIR')),
    number VARCHAR(50) NOT NULL,
    country CHAR(2) NOT NULL DEFAULT 'ID',
    issue_date DATE,
    expiry_date DATE,
    issuing_authority VARCHAR(100),
    verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_at TIMESTAMPTZ,
    verified_by UUID,
    verification_method VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version BIGINT NOT NULL DEFAULT 0,
    deleted_at TIMESTAMPTZ,
    
    CONSTRAINT fk_customer_identifiers_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Unique constraint: same identifier type + number cannot be duplicated
CREATE UNIQUE INDEX idx_customer_identifiers_unique 
    ON customer_identifiers(customer_id, type, number) WHERE deleted_at IS NULL;

-- Global uniqueness for NIK (across all customers) - critical for Indonesia
CREATE UNIQUE INDEX idx_customer_identifiers_nik_unique 
    ON customer_identifiers(number) 
    WHERE type = 'NIK' AND deleted_at IS NULL;

CREATE INDEX idx_customer_identifiers_verified ON customer_identifiers(customer_id) WHERE verified = TRUE AND deleted_at IS NULL;

COMMENT ON TABLE customer_identifiers IS 'Customer identification documents (NIK, NPWP, Passport, etc)';

CREATE TRIGGER update_customer_identifiers_updated_at
BEFORE UPDATE ON customer_identifiers
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- Table: customer_addresses
-- =============================================
CREATE TABLE customer_addresses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('HOME', 'OFFICE', 'MAILING', 'KTP', 'BILLING')),
    line1 VARCHAR(255) NOT NULL,
    line2 VARCHAR(255),
    rt VARCHAR(5),
    rw VARCHAR(5),
    village VARCHAR(100),
    district VARCHAR(100),
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    country CHAR(2) NOT NULL DEFAULT 'ID',
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    geo_latitude DECIMAL(10,8),
    geo_longitude DECIMAL(11,8),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version BIGINT NOT NULL DEFAULT 0,
    deleted_at TIMESTAMPTZ,
    
    CONSTRAINT fk_customer_addresses_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

CREATE INDEX idx_customer_addresses_customer ON customer_addresses(customer_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_customer_addresses_city ON customer_addresses(city) WHERE deleted_at IS NULL;
CREATE INDEX idx_customer_addresses_postal ON customer_addresses(postal_code) WHERE deleted_at IS NULL;
CREATE INDEX idx_customer_addresses_geo ON customer_addresses(geo_latitude, geo_longitude) WHERE geo_latitude IS NOT NULL;
-- One primary address per customer per type
CREATE UNIQUE INDEX idx_customer_addresses_primary 
    ON customer_addresses(customer_id, type) 
    WHERE is_primary = TRUE AND deleted_at IS NULL;

CREATE TRIGGER update_customer_addresses_updated_at
BEFORE UPDATE ON customer_addresses
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE customer_addresses IS 'Customer addresses (KTP, home, office, etc)';

-- =============================================
-- Table: customer_contacts
-- =============================================
CREATE TABLE customer_contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('EMAIL', 'PHONE', 'MOBILE', 'FAX', 'WHATSAPP')),
    value VARCHAR(100) NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_at TIMESTAMPTZ,
    verified_by UUID,
    verification_method VARCHAR(50),
    opt_in_marketing BOOLEAN NOT NULL DEFAULT FALSE,
    opt_in_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version BIGINT NOT NULL DEFAULT 0,
    deleted_at TIMESTAMPTZ,
    
    CONSTRAINT fk_customer_contacts_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

CREATE INDEX idx_customer_contacts_customer ON customer_contacts(customer_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_customer_contacts_value ON customer_contacts(value) WHERE deleted_at IS NULL;
CREATE UNIQUE INDEX idx_customer_contacts_unique 
    ON customer_contacts(customer_id, type, value) WHERE deleted_at IS NULL;
-- One primary per type per customer
CREATE UNIQUE INDEX idx_customer_contacts_primary 
    ON customer_contacts(customer_id, type) 
    WHERE is_primary = TRUE AND deleted_at IS NULL;

CREATE TRIGGER update_customer_contacts_updated_at
BEFORE UPDATE ON customer_contacts
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE customer_contacts IS 'Customer contact information (email, phone, mobile, WhatsApp)';
