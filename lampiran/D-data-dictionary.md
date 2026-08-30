# Lampiran D — Kamus Data (DDL PostgreSQL)

## D.1 `party_master` — Tabel Induk CIF

```sql
CREATE TABLE party_master (
  global_party_id      UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  party_type           VARCHAR(16)  NOT NULL
                        CHECK (party_type IN ('INDIVIDUAL','ORGANIZATION')),
  status               VARCHAR(16)  NOT NULL DEFAULT 'ACTIVE'
                        CHECK (status IN ('ACTIVE','INACTIVE','DECEASED','MERGED','BLOCKED')),
  -- Identifiers
  nik                  VARCHAR(32)  UNIQUE,
  npwp                 VARCHAR(32)  UNIQUE,
  nib                  VARCHAR(32)  UNIQUE,
  passport             VARCHAR(32),
  -- Identity attributes
  nama_lengkap         VARCHAR(255) NOT NULL,
  nama_lengkap_norm    VARCHAR(255) NOT NULL,  -- hasil standarisasi
  jenis_kelamin        VARCHAR(16),
  tanggal_lahir        DATE,
  tempat_lahir         VARCHAR(128),
  nama_ibu             VARCHAR(255),
  -- Contact
  alamat               TEXT,
  alamat_norm          TEXT,
  kota                 VARCHAR(128),
  provinsi             VARCHAR(128),
  kode_pos             VARCHAR(16),
  phone_e164           VARCHAR(32),
  email_norm           VARCHAR(255),
  -- Compliance
  kyc_status           VARCHAR(32)  NOT NULL DEFAULT 'PENDING',
  kyc_last_reviewed_at TIMESTAMPTZ,
  risk_grade           VARCHAR(8),
  consent_flags        JSONB        NOT NULL DEFAULT '{}',
  -- Audit
  source_trust_score   NUMERIC(3,2) NOT NULL DEFAULT 1.00,
  created_at           TIMESTAMPTZ  NOT NULL DEFAULT now(),
  updated_at           TIMESTAMPTZ  NOT NULL DEFAULT now(),
  steward_verified     BOOLEAN      NOT NULL DEFAULT FALSE,
  -- Soft delete
  deleted_at           TIMESTAMPTZ
);

CREATE INDEX idx_pm_nama_norm    ON party_master USING gin (nama_lengkap_norm gin_trgm_ops);
CREATE INDEX idx_pm_alamat_norm  ON party_master USING gin (alamat_norm gin_trgm_ops);
CREATE INDEX idx_pm_status       ON party_master (status);
CREATE INDEX idx_pm_kyc          ON party_master (kyc_status);
CREATE INDEX idx_pm_updated      ON party_master (updated_at DESC);

-- Trigram extension untuk fuzzy nama/alamat
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

## D.2 `party_identifier` — Multi-ID per CIF

```sql
CREATE TABLE party_identifier (
  id                   BIGSERIAL    PRIMARY KEY,
  global_party_id      UUID         NOT NULL REFERENCES party_master(global_party_id),
  id_type              VARCHAR(32)  NOT NULL  -- NIK / NPWP / PASSPORT / NIB / ALT_ID
                        CHECK (id_type IN ('NIK','NPWP','PASSPORT','NIB','ALT_ID')),
  id_value             VARCHAR(64)  NOT NULL,
  id_value_hash        VARCHAR(128) NOT NULL,  -- SHA-256(salt+value)
  issued_by            VARCHAR(64),
  issued_at            DATE,
  expires_at           DATE,
  verified_at          TIMESTAMPTZ,
  verified_by          VARCHAR(64),
  created_at           TIMESTAMPTZ  NOT NULL DEFAULT now(),
  UNIQUE (id_type, id_value_hash)
);

CREATE INDEX idx_pi_party  ON party_identifier (global_party_id);
CREATE INDEX idx_pi_hash   ON party_identifier (id_value_hash);
```

## D.3 `party_lineage` — Crosswalk ke Sistem Sumber

```sql
CREATE TABLE party_lineage (
  global_party_id      UUID         NOT NULL REFERENCES party_master(global_party_id),
  source_system        VARCHAR(64)  NOT NULL,
  source_record_id     VARCHAR(128) NOT NULL,
  source_timestamp     TIMESTAMPTZ NOT NULL,
  trust_score          NUMERIC(3,2) NOT NULL,
  steward_verified     BOOLEAN      NOT NULL DEFAULT FALSE,
  created_at           TIMESTAMPTZ  NOT NULL DEFAULT now(),
  PRIMARY KEY (global_party_id, source_system, source_record_id)
);

CREATE INDEX idx_lineage_src ON party_lineage (source_system, source_record_id);
```

## D.4 `local_cif_xref` — Pemetaan Local CIF

```sql
CREATE TABLE local_cif_xref (
  global_party_id      UUID         NOT NULL REFERENCES party_master(global_party_id),
  system_code          VARCHAR(32)  NOT NULL,   -- 'CBS','CARD','TREAS','TF','LN'
  local_cif            VARCHAR(64)  NOT NULL,
  local_cif_hash       VARCHAR(128) NOT NULL,
  is_primary           BOOLEAN      NOT NULL DEFAULT FALSE,
  created_at           TIMESTAMPTZ  NOT NULL DEFAULT now(),
  PRIMARY KEY (system_code, local_cif)
);

CREATE INDEX idx_xref_party ON local_cif_xref (global_party_id);
```

## D.5 `party_relationship` — Relasi (Household, UBO, dll)

```sql
CREATE TABLE party_relationship (
  relationship_id      BIGSERIAL    PRIMARY KEY,
  global_party_id      UUID         NOT NULL REFERENCES party_master(global_party_id),
  related_party_id     UUID         NOT NULL REFERENCES party_master(global_party_id),
  rel_type             VARCHAR(32)  NOT NULL
                        CHECK (rel_type IN ('HOUSEHOLD_MEMBER','BENEFICIAL_OWNER',
                                            'EMPLOYED_BY','PARENT_OF','MANDATE_OF','RELATED')),
  rel_attributes       JSONB        NOT NULL DEFAULT '{}',  -- {percent, since, until, role}
  confidence_score     NUMERIC(4,3) NOT NULL,
  source_system        VARCHAR(64)  NOT NULL,
  created_at           TIMESTAMPTZ  NOT NULL DEFAULT now(),
  steward_verified     BOOLEAN      NOT NULL DEFAULT FALSE,
  UNIQUE (global_party_id, related_party_id, rel_type, source_system)
);

CREATE INDEX idx_rel_party   ON party_relationship (global_party_id);
CREATE INDEX idx_rel_related ON party_relationship (related_party_id);
CREATE INDEX idx_rel_type    ON party_relationship (rel_type);
```

## D.6 `cif_match_exception` — Antrian Stewardship

```sql
CREATE TABLE cif_match_exception (
  exception_id         UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  incoming_event       JSONB        NOT NULL,
  candidate_cifs       JSONB        NOT NULL,
  top_score            NUMERIC(4,3) NOT NULL,
  decision             VARCHAR(16)  NOT NULL DEFAULT 'PENDING'
                        CHECK (decision IN ('PENDING','MERGED','NEW','REJECTED')),
  priority             VARCHAR(16)  NOT NULL DEFAULT 'NORMAL'
                        CHECK (priority IN ('LOW','NORMAL','HIGH','URGENT')),
  assigned_to          VARCHAR(64),
  decided_at           TIMESTAMPTZ,
  decided_by           VARCHAR(64),
  decision_note        TEXT,
  created_at           TIMESTAMPTZ  NOT NULL DEFAULT now(),
  SLA_deadline         TIMESTAMPTZ  NOT NULL
);

CREATE INDEX idx_exc_status    ON cif_match_exception (decision, created_at);
CREATE INDEX idx_exc_assigned  ON cif_match_exception (assigned_to, decision);
CREATE INDEX idx_exc_sla       ON cif_match_exception (SLA_deadline)
  WHERE decision = 'PENDING';
```

## D.7 `match_audit_log` — Log Keputusan Matching

```sql
CREATE TABLE match_audit_log (
  audit_id             BIGSERIAL    PRIMARY KEY,
  event_id             UUID         NOT NULL,
  global_party_id      UUID,
  match_layer          VARCHAR(16)  NOT NULL   -- EXACT, FUZZY, GRAPH, STEWARD
                        CHECK (match_layer IN ('EXACT','FUZZY','GRAPH','STEWARD','SYSTEM')),
  decision             VARCHAR(16)  NOT NULL,  -- AUTO_MATCH, POSSIBLE_MATCH, NEW, MERGED, REJECTED
  match_score          NUMERIC(4,3),
  reason_code          VARCHAR(64),
  candidates           JSONB,
  source_system        VARCHAR(64),
  decided_by           VARCHAR(64)  NOT NULL,  -- 'system' atau username steward
  decided_at           TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX idx_audit_event  ON match_audit_log (event_id);
CREATE INDEX idx_audit_party  ON match_audit_log (global_party_id);
CREATE INDEX idx_audit_time   ON match_audit_log (decided_at DESC);
CREATE INDEX idx_audit_layer  ON match_audit_log (match_layer, decision);
```

## D.8 `processed_events` — Idempotency

```sql
CREATE TABLE processed_events (
  event_id             UUID         PRIMARY KEY,
  correlation_id       UUID         NOT NULL,
  processed_at         TIMESTAMPTZ  NOT NULL DEFAULT now(),
  outcome              VARCHAR(16)  NOT NULL
);

CREATE INDEX idx_pe_corr  ON processed_events (correlation_id);
CREATE INDEX idx_pe_time  ON processed_events (processed_at);
```

## D.9 `consent` — Manajemen Persetujuan (UU PDP)

```sql
CREATE TABLE consent (
  consent_id           UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  global_party_id      UUID         NOT NULL REFERENCES party_master(global_party_id),
  purpose              VARCHAR(64)  NOT NULL,   -- MARKETING, KYC, DATA_SHARING
  granted              BOOLEAN      NOT NULL,
  granted_at           TIMESTAMPTZ,
  expires_at           TIMESTAMPTZ,
  evidence_url         TEXT,                    -- tautan ke formulir persetujuan
  source_channel       VARCHAR(64)  NOT NULL,
  created_at           TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX idx_consent_party ON consent (global_party_id, purpose);
```

## D.10 View untuk Stewardship Dashboard

```sql
CREATE OR REPLACE VIEW v_pending_exceptions AS
SELECT
  e.exception_id,
  e.priority,
  e.created_at,
  e.SLA_deadline,
  EXTRACT(EPOCH FROM (e.SLA_deadline - now()))/3600 AS hours_to_sla,
  e.incoming_event->>'nama_lengkap' AS nama,
  e.incoming_event->>'nik'          AS nik,
  e.top_score,
  jsonb_array_length(e.candidate_cifs) AS num_candidates,
  e.assigned_to
FROM cif_match_exception e
WHERE e.decision = 'PENDING'
ORDER BY
  CASE e.priority
    WHEN 'URGENT' THEN 1
    WHEN 'HIGH'   THEN 2
    WHEN 'NORMAL' THEN 3
    ELSE 4
  END,
  e.created_at;

CREATE OR REPLACE VIEW v_match_kpi_daily AS
SELECT
  date_trunc('day', decided_at) AS day,
  match_layer,
  decision,
  count(*) AS total,
  avg(match_score)::numeric(5,3) AS avg_score
FROM match_audit_log
WHERE decided_at >= now() - interval '30 days'
GROUP BY 1, 2, 3
ORDER BY 1 DESC, 2, 3;
```
EOF
