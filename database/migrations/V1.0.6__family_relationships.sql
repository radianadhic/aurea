-- Family relationships (also synced to Neo4j)
CREATE TABLE family_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL,
    related_customer_id UUID NOT NULL,
    relationship_type VARCHAR(30) NOT NULL CHECK (relationship_type IN (
        'SPOUSE', 'CHILD', 'PARENT', 'SIBLING', 'GRANDPARENT', 'GRANDCHILD',
        'AUNT_UNCLE', 'NIECE_NEPHEW', 'COUSIN', 'IN_LAW', 'GUARDIAN', 'WARD',
        'BUSINESS_PARTNER', 'BENEFICIARY', 'GUARANTOR', 'AUTHORIZED_SIGNATORY'
    )),
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    notes TEXT,
    verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_at TIMESTAMPTZ,
    verified_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    
    CONSTRAINT fk_family_rel_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    CONSTRAINT fk_family_rel_related FOREIGN KEY (related_customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    CONSTRAINT chk_not_self CHECK (customer_id != related_customer_id)
);

CREATE INDEX idx_family_rel_customer ON family_relationships(customer_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_family_rel_related ON family_relationships(related_customer_id) WHERE deleted_at IS NULL;
CREATE UNIQUE INDEX idx_family_rel_unique 
    ON family_relationships(customer_id, related_customer_id, relationship_type) WHERE deleted_at IS NULL;

COMMENT ON TABLE family_relationships IS 'Family & business relationships between customers (also synced to Neo4j)';
