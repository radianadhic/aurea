-- ===========================================================================
-- V1: workflow-service initial schema
-- ===========================================================================

CREATE TABLE IF NOT EXISTS workflow_tasks (
    id                      UUID PRIMARY KEY,
    process_instance_id     VARCHAR(100),
    process_definition_key  VARCHAR(100),
    task_definition_key     VARCHAR(100),
    name                    VARCHAR(200) NOT NULL,
    description             VARCHAR(1000),
    status                  VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    assignee_id             VARCHAR(50),
    assignee_name           VARCHAR(200),
    requester_id            VARCHAR(50),
    requester_name          VARCHAR(200),
    entity_type             VARCHAR(50),
    entity_id               VARCHAR(100),
    candidate_group         VARCHAR(100),
    priority                VARCHAR(20) DEFAULT 'NORMAL',
    due_date                TIMESTAMP WITH TIME ZONE,
    claimed_at              TIMESTAMP WITH TIME ZONE,
    completed_at            TIMESTAMP WITH TIME ZONE,
    completion_notes        VARCHAR(2000),
    approver_id             VARCHAR(50),
    approver_name           VARCHAR(200),
    variables               TEXT DEFAULT '{}',
    created_at              TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    version                 BIGINT NOT NULL DEFAULT 0,
    deleted_at              TIMESTAMP WITH TIME ZONE,
    created_by              VARCHAR(50),
    updated_by              VARCHAR(50),

    CONSTRAINT chk_task_status CHECK (status IN ('OPEN', 'CLAIMED', 'IN_PROGRESS', 'COMPLETED', 'REJECTED', 'CANCELLED', 'EXPIRED')),
    CONSTRAINT chk_task_priority CHECK (priority IN ('URGENT', 'HIGH', 'NORMAL', 'LOW'))
);

CREATE INDEX idx_task_assignee ON workflow_tasks(assignee_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_task_status ON workflow_tasks(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_task_process ON workflow_tasks(process_instance_id) WHERE process_instance_id IS NOT NULL;
CREATE INDEX idx_task_entity ON workflow_tasks(entity_type, entity_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_task_due ON workflow_tasks(due_date) WHERE status = 'OPEN' AND due_date IS NOT NULL;
CREATE INDEX idx_task_priority_status ON workflow_tasks(priority, status) WHERE deleted_at IS NULL;
CREATE INDEX idx_task_requester ON workflow_tasks(requester_id) WHERE requester_id IS NOT NULL;

-- BPMN process definitions (managed by Camunda but we track metadata)
CREATE TABLE IF NOT EXISTS workflow_definitions (
    id                  UUID PRIMARY KEY,
    process_key         VARCHAR(100) NOT NULL UNIQUE,
    name                VARCHAR(200) NOT NULL,
    description         VARCHAR(500),
    category            VARCHAR(50),
    bpmn_xml            TEXT NOT NULL,
    version             INTEGER NOT NULL DEFAULT 1,
    active              BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by          VARCHAR(50)
);

CREATE INDEX idx_def_key ON workflow_definitions(process_key);
CREATE INDEX idx_def_active ON workflow_definitions(active) WHERE active = TRUE;

-- Workflow audit log
CREATE TABLE IF NOT EXISTS workflow_audit (
    id                  UUID PRIMARY KEY,
    task_id             UUID,
    action              VARCHAR(50) NOT NULL,
    actor_id            VARCHAR(50),
    actor_name          VARCHAR(200),
    details             TEXT,
    timestamp           TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_task ON workflow_audit(task_id) WHERE task_id IS NOT NULL;
CREATE INDEX idx_audit_actor ON workflow_audit(actor_id) WHERE actor_id IS NOT NULL;
CREATE INDEX idx_audit_time ON workflow_audit(timestamp);

COMMENT ON TABLE workflow_tasks IS 'Tasks in workflow system (BPMN) with 4-eyes approval';
COMMENT ON TABLE workflow_definitions IS 'Custom BPMN process definitions';
COMMENT ON TABLE workflow_audit IS 'Audit trail of all task actions';
