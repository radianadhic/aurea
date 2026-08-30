-- Customer product subscriptions
CREATE TABLE customer_products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL,
    product_id UUID NOT NULL,  -- Reference to product-service
    account_number VARCHAR(30),
    subscribed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'DORMANT', 'CLOSED')),
    balance DECIMAL(18,2),
    currency CHAR(3) NOT NULL DEFAULT 'IDR',
    closed_at TIMESTAMPTZ,
    closed_reason TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version BIGINT NOT NULL DEFAULT 0,
    
    CONSTRAINT fk_customer_products_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

CREATE INDEX idx_customer_products_customer ON customer_products(customer_id);
CREATE INDEX idx_customer_products_product ON customer_products(product_id);
CREATE UNIQUE INDEX idx_customer_products_account ON customer_products(account_number) WHERE account_number IS NOT NULL;
CREATE INDEX idx_customer_products_status ON customer_products(status);

COMMENT ON TABLE customer_products IS 'Customer product subscriptions (accounts, cards, loans, etc)';
