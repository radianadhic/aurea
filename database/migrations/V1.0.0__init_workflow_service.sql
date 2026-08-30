-- =============================================
-- WORKFLOW SERVICE - Initial Schema
-- =============================================
-- Service: workflow-service (Port 8086)
-- BPMN workflow engine (Camunda-compatible)

CREATE TABLE workflow_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    code VARCHAR(100) UNIQUE NOT NULL,  -- e.g., 'KYC_APPROVAL'
    description TEXT,
    category VARCHAR(50),
    bpmn_xml TEXT NOT NULL,  -- BPMN 2.0 XML
    form_schema JSONB DEFAULT '{}'::jsonb,
    version INT NOT NULL DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'PUBLISHED', 'DEPRECATED', 'ARCHIVED')),
    published_at TIMESTAMPTZ,
    created_by UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE workflow_instances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_definition_id UUID NOT NULL,
    business_key VARCHAR(200),  -- e.g., customer_id, account_number
    status VARCHAR(20) NOT NULL DEFAULT 'RUNNING' CHECK (status IN (
        'RUNNING', 'SUSPENDED', 'COMPLETED', 'CANCELLED', 'FAILED'
    )),
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    started_by UUID,
    completed_at TIMESTAMPTZ,
    due_date TIMESTAMPTZ,
    variables JSONB DEFAULT '{}'::jsonb,
    
    CONSTRAINT fk_workflow_instances_def FOREIGN KEY (workflow_definition_id) REFERENCES workflow_definitions(id)
);

CREATE INDEX idx_workflow_instances_status ON workflow_instances(status);
CREATE INDEX idx_workflow_instances_business_key ON workflow_instances(business_key);
CREATE INDEX idx_workflow_instances_definition ON workflow_instances(workflow_definition_id);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_instance_id UUID NOT NULL,
    task_definition_key VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    assignee UUID,
    candidate_groups TEXT[],
    candidate_users UUID[],
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (status IN (
        'PENDING', 'CLAIMED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'FAILED', 'DELEGATED', 'ESCALATED'
    )),
    priority INT NOT NULL DEFAULT 50,
    form_schema JSONB DEFAULT '{}'::jsonb,
    form_data JSONB DEFAULT '{}'::jsonb',
    due_date TIMESTAMPTZ,
    claimed_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    completed_by UUID,
    completion_decision VARCHAR(50),  -- APPROVED, REJECTED, etc
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_tasks_workflow_instance FOREIGN KEY (workflow_instance_id) REFERENCES workflow_instances(id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_assignee ON tasks(assignee, status);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due ON tasks(due_date) WHERE status IN ('PENDING', 'CLAIMED', 'IN_PROGRESS');
CREATE INDEX idx_tasks_workflow ON tasks(workflow_instance_id);

CREATE TABLE task_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL,  -- CLAIMED, COMPLETED, DELEGATED, ESCALATED, etc
    actor UUID NOT NULL,
    from_assignee UUID,
    to_assignee UUID,
    comment TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_task_history_task FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);
