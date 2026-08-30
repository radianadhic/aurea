package com.bankxyz.mdm.auth.domain;

import com.bankxyz.mdm.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.time.Instant;
import java.util.UUID;

/**
 * MFA (Multi-Factor Authentication) settings per user.
 * Supports TOTP, SMS, Email, and WebAuthn.
 */
@Entity
@Table(name = "mfa_settings", indexes = {
    @Index(name = "idx_mfa_settings_user_id", columnList = "user_id", unique = true)
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@SuperBuilder
public class MfaSetting extends BaseEntity {

    @Column(name = "user_id", nullable = false, unique = true)
    private UUID userId;

    @Column(name = "username", nullable = false, length = 100)
    private String username;

    @Column(name = "mfa_enabled", nullable = false)
    private Boolean mfaEnabled;

    @Column(name = "mfa_method", length = 20)
    private String mfaMethod;  // TOTP, SMS, EMAIL, WEBAUTHN

    @Column(name = "totp_secret", length = 100)
    private String totpSecret;  // Base32 encoded, encrypted at rest

    @Column(name = "totp_verified", nullable = false)
    private Boolean totpVerified;

    @Column(name = "backup_codes", columnDefinition = "TEXT")
    private String backupCodes;  // JSON array of hashed backup codes

    @Column(name = "phone_number", length = 20)
    private String phoneNumber;

    @Column(name = "phone_verified", nullable = false)
    private Boolean phoneVerified;

    @Column(name = "email", length = 200)
    private String email;

    @Column(name = "email_verified", nullable = false)
    private Boolean emailVerified;

    @Column(name = "webauthn_credential_id", length = 500)
    private String webauthnCredentialId;

    @Column(name = "webauthn_public_key", columnDefinition = "TEXT")
    private String webauthnPublicKey;

    @Column(name = "last_used_at")
    private Instant lastUsedAt;

    @Column(name = "enrolled_at")
    private Instant enrolledAt;

    @PrePersist
    public void prePersist() {
        if (mfaEnabled == null) mfaEnabled = false;
        if (totpVerified == null) totpVerified = false;
        if (phoneVerified == null) phoneVerified = false;
        if (emailVerified == null) emailVerified = false;
    }
}
