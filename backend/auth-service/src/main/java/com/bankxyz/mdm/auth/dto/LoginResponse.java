package com.bankxyz.mdm.auth.dto;

import io.swagger.v3.oas.annotations.media.Schema;

import java.time.Instant;
import java.util.UUID;

@Schema(description = "Login response")
public record LoginResponse(
    @Schema(description = "Access token (JWT)", example = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...")
    String accessToken,

    @Schema(description = "Refresh token", example = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...")
    String refreshToken,

    @Schema(description = "Token type", example = "Bearer")
    String tokenType,

    @Schema(description = "Access token expiry in seconds", example = "1800")
    Long expiresIn,

    @Schema(description = "Access token absolute expiry timestamp")
    Instant expiresAt,

    @Schema(description = "Refresh token expiry timestamp")
    Instant refreshExpiresAt,

    @Schema(description = "Session ID")
    UUID sessionId,

    @Schema(description = "MFA required (token will not be issued until MFA verified)")
    Boolean mfaRequired,

    @Schema(description = "MFA methods available (TOTP, SMS, EMAIL, WEBAUTHN)")
    String mfaMethod,

    @Schema(description = "User information")
    UserInfo user
) {
    @Schema(description = "Authenticated user information")
    public record UserInfo(
        UUID id,
        String username,
        String email,
        String fullName,
        String employeeId,
        String branchId,
        String[] roles
    ) {}
}
