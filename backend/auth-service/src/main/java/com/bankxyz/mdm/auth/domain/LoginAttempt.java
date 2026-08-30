package com.bankxyz.mdm.auth.domain;

import com.bankxyz.mdm.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.time.Instant;
import java.util.UUID;

/**
 * Login attempt tracking.
 * Used for:
 * - Brute force detection
 * - Account lockout
 * - Audit trail
 * - Security analytics
 */
@Entity
@Table(name = "login_attempts", indexes = {
    @Index(name = "idx_login_attempts_username_time", columnList = "username, attempted_at DESC"),
    @Index(name = "idx_login_attempts_ip_time", columnList = "ip_address, attempted_at DESC"),
    @Index(name = "idx_login_attempts_success", columnList = "success, attempted_at DESC")
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@SuperBuilder
public class LoginAttempt extends BaseEntity {

    @Column(name = "username", length = 100)
    private String username;

    @Column(name = "user_id")
    private UUID userId;

    @Column(name = "success", nullable = false)
    private Boolean success;

    @Column(name = "failure_reason", length = 50)
    private String failureReason;
    // INVALID_CREDENTIALS, ACCOUNT_LOCKED, MFA_REQUIRED, MFA_FAILED, ACCOUNT_DISABLED

    @Column(name = "ip_address", length = 45)
    private String ipAddress;

    @Column(name = "user_agent", length = 500)
    private String userAgent;

    @Column(name = "attempted_at", nullable = false)
    private Instant attemptedAt;

    @Column(name = "mfa_attempted", nullable = false)
    private Boolean mfaAttempted;

    @Column(name = "mfa_success")
    private Boolean mfaSuccess;

    @Column(name = "correlation_id", length = 100)
    private String correlationId;

    @PrePersist
    public void prePersist() {
        if (attemptedAt == null) attemptedAt = Instant.now();
        if (success == null) success = false;
        if (mfaAttempted == null) mfaAttempted = false;
    }
}
