-- =============================================
-- DOCUMENT SERVICE - Initial Schema
-- =============================================
-- Service: document-service (Port 8092)

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID,
    type VARCHAR(50) NOT NULL CHECK (type IN (
        'KTP', 'NPWP', 'PASSPORT', 'KITAS', 'AKTA_LAHIR', 'AKTA_NIKAH',
        'SELFIE', 'SIGNATURE', 'BUKTI_TF', 'KONTRAK', 'LAINNYA'
    )),
    file_name VARCHAR(500) NOT NULL,
    file_path VARCHAR(1000) NOT NULL,  -- MinIO path
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    file_hash VARCHAR(64) NOT NULL,  -- SHA256
    upload_status VARCHAR(20) NOT NULL DEFAULT 'UPLOADED' CHECK (upload_status IN (
        'UPLOADING', 'UPLOADED', 'SCANNING', 'CLEAN', 'INFECTED', 'FAILED'
    )),
    virus_scan_result VARCHAR(50),
    ocr_status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (ocr_status IN (
        'PENDING', 'PROCESSING', 'COMPLETED', 'NEEDS_REVIEW', 'FAILED', 'NOT_APPLICABLE'
    )),
    ocr_result JSONB,
    ocr_confidence DECIMAL(5,2),
    verification_status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (verification_status IN (
        'PENDING', 'IN_REVIEW', 'VERIFIED', 'REJECTED'
    )),
    verified_by UUID,
    verified_at TIMESTAMPTZ,
    rejection_reason TEXT,
    expiry_date DATE,
    is_encrypted BOOLEAN NOT NULL DEFAULT TRUE,
    encryption_key_id VARCHAR(100),
    uploaded_by UUID NOT NULL,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_documents_customer ON documents(customer_id, type) WHERE deleted_at IS NULL;
CREATE INDEX idx_documents_type ON documents(type) WHERE deleted_at IS NULL;
CREATE INDEX idx_documents_ocr ON documents(ocr_status) WHERE ocr_status IN ('PENDING', 'PROCESSING');
CREATE INDEX idx_documents_expiry ON documents(expiry_date) WHERE expiry_date IS NOT NULL AND deleted_at IS NULL;
CREATE INDEX idx_documents_hash ON documents(file_hash);

CREATE TABLE document_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL,
    version_number INT NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    file_size BIGINT NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    replaced_by UUID,
    replace_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_doc_versions_doc FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);

CREATE TABLE document_access_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL,
    accessed_by UUID NOT NULL,
    access_type VARCHAR(20) NOT NULL CHECK (access_type IN ('VIEW', 'DOWNLOAD', 'UPDATE', 'DELETE')),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_access_log_doc FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);

CREATE INDEX idx_access_log_doc ON document_access_log(document_id, created_at DESC);
