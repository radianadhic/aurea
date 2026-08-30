-- =============================================
-- ML SERVICE - Initial Schema
-- =============================================
-- Service: ml-service (Port 8090, Python FastAPI)

CREATE TABLE ml_model_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,  -- e.g., 'churn_prediction', 'credit_scoring'
    version VARCHAR(20) NOT NULL,  -- e.g., '2.3.0'
    framework VARCHAR(30) NOT NULL CHECK (framework IN ('SKLEARN', 'TENSORFLOW', 'PYTORCH', 'XGBOOST', 'LIGHTGBM', 'CATBOOST')),
    model_type VARCHAR(50),  -- Classification, Regression, etc
    model_artifact_path VARCHAR(500) NOT NULL,  -- S3/MinIO path
    metrics JSONB DEFAULT '{}'::jsonb,  -- accuracy, f1, etc
    hyperparameters JSONB DEFAULT '{}'::jsonb,
    training_dataset_path VARCHAR(500),
    training_dataset_size INT,
    feature_columns JSONB DEFAULT '[]'::jsonb,
    target_column VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'STAGING' CHECK (status IN ('STAGING', 'PRODUCTION', 'ARCHIVED', 'FAILED')),
    activated_at TIMESTAMPTZ,
    activated_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID NOT NULL,
    
    CONSTRAINT uq_ml_model_version UNIQUE (name, version)
);

CREATE INDEX idx_ml_model_active ON ml_model_registry(name, status) WHERE status = 'PRODUCTION';

CREATE TABLE ml_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_id UUID NOT NULL,
    customer_id UUID,
    input_features JSONB NOT NULL,
    prediction JSONB NOT NULL,  -- Output (probability, class, etc)
    confidence DECIMAL(5,4),
    explanation JSONB,  -- SHAP values
    latency_ms INT,
    served_by VARCHAR(50) NOT NULL,  -- REST, BATCH, SCHEDULED
    request_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_ml_predictions_model FOREIGN KEY (model_id) REFERENCES ml_model_registry(id)
);

CREATE INDEX idx_ml_predictions_model ON ml_predictions(model_id, created_at DESC);
CREATE INDEX idx_ml_predictions_customer ON ml_predictions(customer_id, created_at DESC);

CREATE TABLE ml_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prediction_id UUID NOT NULL,
    actual_outcome JSONB,  -- Ground truth
    feedback_by UUID NOT NULL,
    feedback_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_ml_feedback_prediction FOREIGN KEY (prediction_id) REFERENCES ml_predictions(id) ON DELETE CASCADE
);
