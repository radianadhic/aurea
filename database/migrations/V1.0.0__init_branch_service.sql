-- =============================================
-- BRANCH SERVICE - Initial Schema
-- =============================================
-- Service: branch-service (Port 8088)

CREATE TABLE regions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    regional_director VARCHAR(200),
    address TEXT,
    phone VARCHAR(20),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE branches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('HEAD_OFFICE', 'KCU', 'KCP', 'UNIT', 'CASH_OFFICE')),
    parent_branch_id UUID,
    region_id UUID NOT NULL,
    address TEXT NOT NULL,
    village VARCHAR(100),
    district VARCHAR(100),
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    fax VARCHAR(20),
    email VARCHAR(200),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    branch_manager_id UUID,
    opening_date DATE,
    closing_date DATE,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version INT NOT NULL DEFAULT 0,
    
    CONSTRAINT fk_branches_region FOREIGN KEY (region_id) REFERENCES regions(id),
    CONSTRAINT fk_branches_parent FOREIGN KEY (parent_branch_id) REFERENCES branches(id)
);

CREATE INDEX idx_branches_region ON branches(region_id);
CREATE INDEX idx_branches_active ON branches(active) WHERE active = TRUE;
CREATE INDEX idx_branches_parent ON branches(parent_branch_id);
CREATE INDEX idx_branches_geo ON branches(latitude, longitude);
