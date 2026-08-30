-- =============================================
-- CUSTOMER SERVICE - Initial Schema (V1.0.0)
-- =============================================
-- Service: customer-service (Port 8082)
-- Database: PostgreSQL 16

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For trigram text search


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tables will be added in subsequent migration files:
-- V1.0.1: customers (main CIF table)
-- V1.0.2: customer_identifiers
-- V1.0.3: customer_addresses
-- V1.0.4: customer_contacts
-- V1.0.5: customer_products (link to product-service)
-- V1.0.6: family_relationships
-- V1.0.7: customer_tags
-- V1.0.8: customer_consent
-- V1.0.9: merge_history
-- V1.0.10: indexes & performance
