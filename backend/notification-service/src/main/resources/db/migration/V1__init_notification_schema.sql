-- ===========================================================================
-- V1: notification-service initial schema
-- ===========================================================================

CREATE TABLE IF NOT EXISTS notifications (
    id                  UUID PRIMARY KEY,
    channel             VARCHAR(20) NOT NULL,
    status              VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    template_code       VARCHAR(100),
    subject             VARCHAR(500),
    body                TEXT,
    recipient_id        VARCHAR(100),
    recipient_address   VARCHAR(200),
    recipient_name      VARCHAR(200),
    locale              VARCHAR(10) DEFAULT 'id',
    variables           TEXT DEFAULT '{}',
    priority            VARCHAR(20) DEFAULT 'NORMAL',
    scheduled_at        TIMESTAMP WITH TIME ZONE,
    sent_at             TIMESTAMP WITH TIME ZONE,
    delivered_at        TIMESTAMP WITH TIME ZONE,
    read_at             TIMESTAMP WITH TIME ZONE,
    provider_message_id VARCHAR(200),
    error_message       VARCHAR(2000),
    retry_count         INTEGER NOT NULL DEFAULT 0,
    max_retries         INTEGER NOT NULL DEFAULT 3,
    correlation_id      VARCHAR(50),
    source_service      VARCHAR(50),
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    version             BIGINT NOT NULL DEFAULT 0,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    created_by          VARCHAR(50),
    updated_by          VARCHAR(50),

    CONSTRAINT chk_channel CHECK (channel IN ('EMAIL', 'SMS', 'WHATSAPP', 'PUSH', 'IN_APP', 'WEBHOOK')),
    CONSTRAINT chk_notif_status CHECK (status IN ('PENDING', 'QUEUED', 'SENDING', 'SENT', 'DELIVERED', 'READ', 'FAILED', 'CANCELLED'))
);

CREATE INDEX idx_notif_recipient ON notifications(recipient_id);
CREATE INDEX idx_notif_status ON notifications(status);
CREATE INDEX idx_notif_channel ON notifications(channel);
CREATE INDEX idx_notif_created ON notifications(created_at DESC);
CREATE INDEX idx_notif_correlation ON notifications(correlation_id) WHERE correlation_id IS NOT NULL;
CREATE INDEX idx_notif_scheduled ON notifications(scheduled_at) WHERE status = 'QUEUED';
CREATE INDEX idx_notif_pending ON notifications(status, created_at) WHERE status IN ('PENDING', 'QUEUED');

CREATE TABLE IF NOT EXISTS notification_templates (
    id                  UUID PRIMARY KEY,
    code                VARCHAR(100) NOT NULL,
    name                VARCHAR(200) NOT NULL,
    description         VARCHAR(500),
    channel             VARCHAR(20) NOT NULL,
    locale              VARCHAR(10) NOT NULL DEFAULT 'id',
    subject             VARCHAR(500),
    body                TEXT NOT NULL,
    version             INTEGER NOT NULL DEFAULT 1,
    active              BOOLEAN NOT NULL DEFAULT TRUE,
    approved_by         VARCHAR(50),
    approved_at         TIMESTAMP WITH TIME ZONE,
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    version_lock        BIGINT NOT NULL DEFAULT 0,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    created_by          VARCHAR(50),
    updated_by          VARCHAR(50),

    CONSTRAINT uk_tmpl_code_locale UNIQUE (code, locale)
);

CREATE INDEX idx_tmpl_code ON notification_templates(code);
CREATE INDEX idx_tmpl_locale ON notification_templates(locale);
CREATE INDEX idx_tmpl_active ON notification_templates(active) WHERE active = TRUE;

-- WebSocket sessions
CREATE TABLE IF NOT EXISTS websocket_sessions (
    id                  UUID PRIMARY KEY,
    user_id             VARCHAR(50) NOT NULL,
    session_id          VARCHAR(100) NOT NULL UNIQUE,
    connected_at        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_active_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    disconnected_at     TIMESTAMP WITH TIME ZONE,
    ip_address          VARCHAR(45),
    user_agent          VARCHAR(500)
);

CREATE INDEX idx_ws_user ON websocket_sessions(user_id) WHERE disconnected_at IS NULL;
CREATE INDEX idx_ws_session ON websocket_sessions(session_id);

-- Sample templates
INSERT INTO notification_templates (id, code, name, description, channel, locale, subject, body, version, active) VALUES
  (gen_random_uuid(), 'WELCOME_NEW_CUSTOMER', 'Welcome Email for New Customer', 'Sent when new customer is created', 'EMAIL', 'id', 'Selamat Datang di Bank XYZ, {{name}}!', '<h1>Selamat Datang, {{name}}!</h1><p>Terima kasih telah menjadi nasabah Bank XYZ. Nomor CIF Anda: <strong>{{cifNumber}}</strong></p><p>Untuk aktivasi layanan, silakan login ke aplikasi mobile kami.</p>', 1, TRUE),
  (gen_random_uuid(), 'KYC_APPROVED', 'KYC Approved Notification', 'Sent when KYC is approved', 'EMAIL', 'id', 'KYC Anda Telah Disetujui', '<h1>KYC Disetujui</h1><p>Halo {{name}},</p><p>KYC Anda telah disetujui. Anda sekarang dapat menikmati semua layanan Bank XYZ.</p>', 1, TRUE),
  (gen_random_uuid(), 'KYC_REJECTED', 'KYC Rejected Notification', 'Sent when KYC is rejected', 'EMAIL', 'id', 'KYC Anda Ditolak', '<h1>KYC Ditolak</h1><p>Halo {{name}},</p><p>Mohon maaf, KYC Anda ditolak dengan alasan: {{reason}}</p><p>Silakan hubungi cabang terdekat untuk informasi lebih lanjut.</p>', 1, TRUE),
  (gen_random_uuid(), 'KYC_EXPIRING', 'KYC Expiring Reminder', 'Sent 30 days before KYC expires', 'EMAIL', 'id', 'KYC Akan Segera Berakhir', '<h1>Reminder KYC</h1><p>Halo {{name}},</p><p>KYC Anda akan berakhir pada {{expiryDate}}. Mohon perbarui sebelum tanggal tersebut.</p>', 1, TRUE),
  (gen_random_uuid(), 'BLACKLIST_NOTIFICATION', 'Blacklist Notification', 'Customer blacklisted', 'EMAIL', 'id', 'Pemberitahuan Blacklist', '<h1>Pemberitahuan Penting</h1><p>Halo {{name}},</p><p>Akun Anda telah di-blacklist. Alasan: {{reason}}</p>', 1, TRUE);

COMMENT ON TABLE notifications IS 'Multi-channel notification records (email/SMS/WhatsApp/push/in-app)';
COMMENT ON TABLE notification_templates IS 'FreeMarker templates for notifications';
COMMENT ON TABLE websocket_sessions IS 'Active WebSocket sessions for real-time in-app notifications';
