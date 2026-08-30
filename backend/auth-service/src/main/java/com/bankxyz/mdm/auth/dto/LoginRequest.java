package com.bankxyz.mdm.auth.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

@Schema(description = "Login request")
public record LoginRequest(
    @NotBlank
    @Size(min = 3, max = 100)
    @Schema(description = "Username or email", example = "admin")
    String username,

    @NotBlank
    @Size(min = 8, max = 100)
    @Schema(description = "Password", example = "Admin@123")
    String password,

    @Schema(description = "MFA code (TOTP, SMS, etc) - optional, required if MFA enabled")
    String mfaCode,

    @Schema(description = "Remember me (extends session duration)")
    Boolean rememberMe
) {}
