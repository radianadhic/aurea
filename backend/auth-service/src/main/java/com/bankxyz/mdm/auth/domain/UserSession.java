package com.bankxyz.mdm.auth.domain;

import com.bankxyz.mdm.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.time.Instant;
import java.util.UUID;

/**
 * User session entity. Tracks active user sessions.
 * Each successful login creates a session record.
 * Sessions are automatically invalidated after idle timeout.
 */
@Entity
@Table(name = "user_sessions", indexes = {
    @Index(name = "idx_user_sessions_user_id", columnList = "user_id"),
    @Index(name = "idx_user_sessions_token_hash", columnList = "token_hash", unique = true),
    @Index(name = "idx_user_sessions_active", columnList = "active, expires_at")
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@SuperBuilder
public class UserSession extends BaseEntity {

    @Column(name = "user_id", nullable = false)
    private UUID userId;

    @Column(name = "username", nullable = false, length = 100)
    private String username;

    @Column(name = "keycloak_session_id", length = 100)
    private String keycloakSessionId;

    @Column(name = "token_hash", nullable = false, length = 64)
    private String tokenHash;  // SHA-256 hash of access token

    @Column(name = "refresh_token_hash", length = 64)
    private String refreshTokenHash;

    @Column(name = "ip_address", length = 45)
    private String ipAddress;

    @Column(name = "user_agent", length = 500)
    private String userAgent;

    @Column(name = "device_fingerprint", length = 100)
    private String deviceFingerprint;

    @Column(name = "login_at", nullable = false)
    private Instant loginAt;

    @Column(name = "last_activity_at", nullable = false)
    private Instant lastActivityAt;

    @Column(name = "expires_at", nullable = false)
    private Instant expiresAt;

    @Column(name = "logged_out_at")
    private Instant loggedOutAt;

    @Column(name = "logout_reason", length = 50)
    private String logoutReason;

    @Column(name = "active", nullable = false)
    private Boolean active;

    @Column(name = "mfa_verified", nullable = false)
    private Boolean mfaVerified;

    @Column(name = "mfa_method", length = 20)
    private String mfaMethod;  // TOTP, SMS, EMAIL, WEBAUTHN

    @PrePersist
    public void prePersist() {
        if (loginAt == null) loginAt = Instant.now();
        if (lastActivityAt == null) lastActivityAt = loginAt;
        if (active == null) active = true;
        if (mfaVerified == null) mfaVerified = false;
    }
}
