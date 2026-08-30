-- Customer merge history (for undo within 24h)
CREATE TABLE customer_merge_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    primary_customer_id UUID NOT NULL,  -- The surviving customer
    merged_customer_ids UUID[] NOT NULL,  -- Customers that were merged in
    merge_strategy VARCHAR(20) NOT NULL CHECK (merge_strategy IN ('PRIMARY_WINS', 'LATEST_WINS', 'MANUAL')),
    field_overrides JSONB DEFAULT '{}'::jsonb,
    primary_before_state JSONB NOT NULL,
    primary_after_state JSONB NOT NULL,
    merged_customers_state JSONB NOT NULL,  -- Array of pre-merge states
    reason TEXT,
    initiated_by UUID NOT NULL,
    approved_by UUID,  -- 4-eyes principle
    approved_at TIMESTAMPTZ,
    merged_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    undone BOOLEAN NOT NULL DEFAULT FALSE,
    undone_at TIMESTAMPTZ,
    undone_by UUID,
    undo_reason TEXT,
    can_undo_until TIMESTAMPTZ NOT NULL,  -- merged_at + 24h
    
    CONSTRAINT fk_merge_history_primary FOREIGN KEY (primary_customer_id) REFERENCES customers(id)
);

CREATE INDEX idx_merge_history_primary ON customer_merge_history(primary_customer_id);
CREATE INDEX idx_merge_history_can_undo ON customer_merge_history(can_undo_until) WHERE undone = FALSE;
