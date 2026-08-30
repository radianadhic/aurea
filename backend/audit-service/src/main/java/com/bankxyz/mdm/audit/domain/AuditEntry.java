package com.bankxyz.mdm.audit.domain;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * AuditEntry - Immutable record of an action performed in the MDM system.
 *
 * Records cannot be modified or deleted (only soft-deleted with reason).
 * Designed for compliance with UU PDP, OJK, BI, and PPATK requirements.
 */
@Entity
@Table(name = "audit_entries", indexes = {
    @Index(name = "idx_audit_user", columnList = "user_id"),
    @Index(name = "idx_audit_action", columnList = "action"),
    @Index(name = "idx_audit_entity", columnList = "entity_type, entity_id"),
    @Index(name = "idx_audit_timestamp", columnList = "timestamp"),
    @Index(name = "idx_audit_result", columnList = "result"),
    @Index(name = "idx_audit_correlation", columnList = "correlation_id"),
    @Index(name = "idx_audit_session", columnList = "session_id")
})
@EntityListeners(AuditingEntityListener.class)
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class AuditEntry {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", updatable = false, nullable = false)
    private UUID id;

    /** When the action occurred */
    @Column(name = "timestamp", nullable = false)
    private Instant timestamp;

    /** User who performed the action */
    @Column(name = "user_id", length = 50)
    private String userId;

    @Column(name = "username", length = 100)
    private String username;

    @Column(name = "user_full_name", length = 200)
    private String userFullName;

    @Column(name = "user_role", length = 100)
    private String userRole;

    /** What action was performed */
    @Column(name = "action", nullable = false, length = 50)
    private String action;

    /** What entity was affected */
    @Column(name = "entity_type", nullable = false, length = 50)
    private String entityType;

    @Column(name = "entity_id", length = 100)
    private String entityId;

    /** HTTP context */
    @Column(name = "ip_address", length = 45)
    private String ipAddress;

    @Column(name = "user_agent", length = 500)
    private String userAgent;

    @Column(name = "request_method", length = 10)
    private String requestMethod;

    @Column(name = "request_path", length = 500)
    private String requestPath;

    @Column(name = "response_status", length = 3)
    private Integer responseStatus;

    /** Result of the action */
    @Enumerated(EnumType.STRING)
    @Column(name = "result", nullable = false, length = 20)
    @Builder.Default
    private AuditResult result = AuditResult.SUCCESS;

    @Column(name = "error_message", length = 2000)
    private String errorMessage;

    /** Trace context */
    @Column(name = "correlation_id", length = 50)
    private String correlationId;

    @Column(name = "session_id", length = 100)
    private String sessionId;

    /** Source service (e.g. customer-service, matching-service) */
    @Column(name = "source_service", length = 50)
    private String sourceService;

    /** Changes made (for update operations) - JSON */
    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "changes", columnDefinition = "jsonb")
    @Builder.Default
    private Map<String, Object> changes = new HashMap<>();

    /** Additional metadata - JSON */
    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "metadata", columnDefinition = "jsonb")
    @Builder.Default
    private Map<String, Object> metadata = new HashMap<>();

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @LastModifiedDate
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    /** Soft delete with reason - audit entries are never hard-deleted */
    @Column(name = "deleted_at")
    private Instant deletedAt;

    @Column(name = "deleted_by", length = 50)
    private String deletedBy;

    @Column(name = "deletion_reason", length = 500)
    private String deletionReason;

    /**
     * Audit entries are append-only. Any modification throws.
     */
    @PreUpdate
    void preventModification() {
        // Allow only soft delete updates
        if (deletedAt == null) {
            throw new UnsupportedOperationException(
                "Audit entries are immutable. Use soft delete with reason.");
        }
    }
}
