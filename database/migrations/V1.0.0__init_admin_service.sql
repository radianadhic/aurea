-- =============================================
-- ADMIN SERVICE - Initial Schema
-- =============================================
-- Service: admin-service (Port 8093)
-- Users, roles, business rules, config

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    employee_id VARCHAR(50),
    phone VARCHAR(20),
    branch_id VARCHAR(50),
    department VARCHAR(100),
    position VARCHAR(100),
    mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    password_last_changed_at TIMESTAMPTZ,
    password_expires_at TIMESTAMPTZ,
    must_change_password BOOLEAN NOT NULL DEFAULT FALSE,
    failed_login_count INT NOT NULL DEFAULT 0,
    locked_until TIMESTAMPTZ,
    last_login_at TIMESTAMPTZ,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    deactivated_at TIMESTAMPTZ,
    deactivated_reason TEXT,
    keycloak_user_id VARCHAR(100),  -- Link to Keycloak
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by UUID
);

CREATE INDEX idx_users_active ON users(active) WHERE active = TRUE;
CREATE INDEX idx_users_branch ON users(branch_id);
CREATE INDEX idx_users_keycloak ON users(keycloak_user_id);

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_system_role BOOLEAN NOT NULL DEFAULT FALSE,  -- Cannot be deleted
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(100) UNIQUE NOT NULL,  -- e.g., 'customer:read', 'customer:write'
    name VARCHAR(200) NOT NULL,
    description TEXT,
    resource VARCHAR(50) NOT NULL,  -- customer, product, audit, etc
    action VARCHAR(20) NOT NULL,  -- read, write, delete, approve, etc
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_permissions_resource ON permissions(resource, action);

CREATE TABLE user_roles (
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,
    granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    granted_by UUID,
    expires_at TIMESTAMPTZ,
    
    PRIMARY KEY (user_id, role_id),
    CONSTRAINT fk_user_roles_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_roles_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

CREATE TABLE role_permissions (
    role_id UUID NOT NULL,
    permission_id UUID NOT NULL,
    granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    PRIMARY KEY (role_id, permission_id),
    CONSTRAINT fk_role_perms_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    CONSTRAINT fk_role_perms_perm FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);

CREATE TABLE business_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    code VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    rule_type VARCHAR(30) NOT NULL CHECK (rule_type IN (
        'VALIDATION', 'TRANSFORMATION', 'ENRICHMENT', 'ROUTING', 'APPROVAL', 'NOTIFICATION', 'SLA'
    )),
    scope VARCHAR(200) NOT NULL,  -- e.g., 'CUSTOMER.IDENTIFIER.NIK'
    condition_expression TEXT NOT NULL,  -- DSL or expression
    action VARCHAR(30) NOT NULL CHECK (action IN ('ALLOW', 'BLOCK', 'WARN', 'TRANSFORM', 'ROUTE', 'NOTIFY')),
    error_message TEXT,
    priority INT NOT NULL DEFAULT 100,
    active BOOLEAN NOT NULL DEFAULT FALSE,
    version INT NOT NULL DEFAULT 1,
    published_at TIMESTAMPTZ,
    published_by UUID,
    created_by UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_business_rules_active ON business_rules(active, scope) WHERE active = TRUE;

CREATE TABLE business_rule_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_id UUID NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    result VARCHAR(20) NOT NULL CHECK (result IN ('PASSED', 'FAILED', 'WARNING', 'ERROR')),
    execution_time_ms INT,
    error_message TEXT,
    context JSONB DEFAULT '{}'::jsonb,
    executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_rule_exec_rule FOREIGN KEY (rule_id) REFERENCES business_rules(id)
);

CREATE INDEX idx_rule_exec_rule ON business_rule_executions(rule_id, executed_at DESC);

CREATE TABLE system_config (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    config_key VARCHAR(200) UNIQUE NOT NULL,
    config_value JSONB NOT NULL,
    description TEXT,
    is_sensitive BOOLEAN NOT NULL DEFAULT FALSE,
    updated_by UUID,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE menus (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    parent_id UUID,
    app_id VARCHAR(50) NOT NULL,  -- admin, steward, analytics, etc
    path VARCHAR(500),
    icon VARCHAR(100),
    display_order INT NOT NULL DEFAULT 0,
    required_permissions TEXT[] NOT NULL DEFAULT '{}',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_menus_parent FOREIGN KEY (parent_id) REFERENCES menus(id)
);
