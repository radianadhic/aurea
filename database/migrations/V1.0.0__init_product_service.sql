-- =============================================
-- PRODUCT SERVICE - Initial Schema
-- =============================================
-- Service: product-service (Port 8087)

CREATE TABLE product_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    parent_category_id UUID,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    display_order INT NOT NULL DEFAULT 0,
    icon_url VARCHAR(500),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_product_categories_parent FOREIGN KEY (parent_category_id) REFERENCES product_categories(id)
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id UUID NOT NULL,
    product_type VARCHAR(30) NOT NULL CHECK (product_type IN (
        'SAVINGS', 'CURRENT_ACCOUNT', 'TIME_DEPOSIT', 'CREDIT_CARD', 'LOAN',
        'MORTGAGE', 'INVESTMENT', 'INSURANCE', 'FUND', 'BOND', 'CURRENCY'
    )),
    currency CHAR(3) NOT NULL DEFAULT 'IDR',
    min_balance DECIMAL(18,2),
    max_balance DECIMAL(18,2),
    min_age INT,
    max_age INT,
    risk_level VARCHAR(10) CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH')),
    features JSONB DEFAULT '[]'::jsonb,
    benefits JSONB DEFAULT '[]'::jsonb,
    terms_and_conditions_url VARCHAR(500),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    launch_date DATE,
    discontinue_date DATE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version INT NOT NULL DEFAULT 0,
    
    CONSTRAINT fk_products_category FOREIGN KEY (category_id) REFERENCES product_categories(id)
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(active) WHERE active = TRUE;

CREATE TABLE product_pricing_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL,
    name VARCHAR(200) NOT NULL,
    pricing_type VARCHAR(30) NOT NULL CHECK (pricing_type IN (
        'INTEREST_RATE', 'FEE', 'COMMISSION', 'DISCOUNT', 'PENALTY'
    )),
    calculation_method VARCHAR(50),  -- FLAT, PERCENTAGE, TIERED
    amount DECIMAL(18,4),
    percentage DECIMAL(5,2),
    tiers JSONB DEFAULT '[]'::jsonb,  -- For tiered pricing
    conditions JSONB DEFAULT '{}'::jsonb,  -- e.g., min balance, customer segment
    effective_from DATE NOT NULL,
    effective_to DATE,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_pricing_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE INDEX idx_pricing_product ON product_pricing_rules(product_id, active, effective_from);
