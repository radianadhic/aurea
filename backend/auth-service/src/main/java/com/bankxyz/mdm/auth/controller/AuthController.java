package com.bankxyz.mdm.auth.controller;

import com.bankxyz.mdm.auth.dto.LoginRequest;
import com.bankxyz.mdm.auth.dto.LoginResponse;
import com.bankxyz.mdm.auth.service.AuthService;
import com.bankxyz.mdm.auth.service.KeycloakAdminService;
import com.bankxyz.mdm.common.dto.ApiError;
import com.bankxyz.mdm.common.security.JwtAuthContext;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.MDC;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.UUID;

/**
 * Authentication REST controller.
 * Endpoints:
 * - POST /api/v1/auth/login
 * - POST /api/v1/auth/refresh
 * - POST /api/v1/auth/logout
 * - POST /api/v1/auth/logout-all
 * - GET  /api/v1/auth/me
 * - GET  /api/v1/auth/validate
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/auth")
@RequiredArgsConstructor
@Tag(name = "Authentication", description = "Login, logout, token operations")
public class AuthController {

    private final AuthService authService;
    private final KeycloakAdminService keycloakService;

    @PostMapping("/login")
    @Operation(summary = "Login", description = "Authenticate user with username/password and optional MFA code")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Login successful (may require MFA)"),
        @ApiResponse(responseCode = "401", description = "Invalid credentials",
                content = @Content(schema = @Schema(implementation = ApiError.class))),
        @ApiResponse(responseCode = "422", description = "Account locked or MFA required",
                content = @Content(schema = @Schema(implementation = ApiError.class))),
        @ApiResponse(responseCode = "429", description = "Too many failed attempts",
                content = @Content(schema = @Schema(implementation = ApiError.class)))
    })
    public ResponseEntity<LoginResponse> login(
            @Valid @RequestBody LoginRequest request,
            HttpServletRequest httpRequest) {
        log.info("Login attempt for: {}", request.username());
        String correlationId = MDC.get("correlationId");
        LoginResponse response = authService.login(
                request,
                getClientIp(httpRequest),
                httpRequest.getHeader(HttpHeaders.USER_AGENT),
                correlationId);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/refresh")
    @Operation(summary = "Refresh access token", description = "Exchange refresh token for new access token")
    public ResponseEntity<LoginResponse> refreshToken(
            @RequestBody Map<String, String> request,
            HttpServletRequest httpRequest) {
        String refreshToken = request.get("refreshToken");
        if (refreshToken == null || refreshToken.isBlank()) {
            throw new com.bankxyz.mdm.common.exception.BusinessException(
                    org.springframework.http.HttpStatus.BAD_REQUEST,
                    "MISSING_REFRESH_TOKEN",
                    "refreshToken is required");
        }
        LoginResponse response = authService.refreshToken(
                refreshToken,
                getClientIp(httpRequest),
                httpRequest.getHeader(HttpHeaders.USER_AGENT));
        return ResponseEntity.ok(response);
    }

    @PostMapping("/logout")
    @SecurityRequirement(name = "bearerAuth")
    @Operation(summary = "Logout", description = "Logout current session")
    public ResponseEntity<Void> logout(
            @Parameter(description = "Session ID (optional, defaults to current)")
            @RequestHeader(value = "X-Session-Id", required = false) String sessionId) {
        UUID sessionUuid = sessionId != null
                ? UUID.fromString(sessionId)
                : UUID.fromString(JwtAuthContext.getCurrentUserId()
                        .orElseThrow(() -> new com.bankxyz.mdm.common.exception.BusinessException(
                                org.springframework.http.HttpStatus.UNAUTHORIZED,
                                "NO_SESSION",
                                "No active session")));
        authService.logout(sessionUuid, "USER_LOGOUT");
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/logout-all")
    @SecurityRequirement(name = "bearerAuth")
    @Operation(summary = "Logout all sessions", description = "Logout all active sessions for the current user")
    public ResponseEntity<Map<String, Object>> logoutAll() {
        UUID userId = UUID.fromString(JwtAuthContext.getCurrentUserId()
                .orElseThrow(() -> new com.bankxyz.mdm.common.exception.BusinessException(
                        org.springframework.http.HttpStatus.UNAUTHORIZED,
                        "NO_USER",
                        "No authenticated user")));
        int count = authService.logoutAllSessions(userId);
        return ResponseEntity.ok(Map.of(
                "message", "All sessions logged out",
                "sessionsLoggedOut", count));
    }

    @GetMapping("/me")
    @SecurityRequirement(name = "bearerAuth")
    @Operation(summary = "Get current user", description = "Get information about the currently authenticated user")
    public ResponseEntity<Map<String, Object>> me() {
        return ResponseEntity.ok(Map.of(
                "userId", JwtAuthContext.getCurrentUserId().orElse(null),
                "username", JwtAuthContext.getCurrentUsername().orElse(null),
                "email", JwtAuthContext.getCurrentUserEmail().orElse(null),
                "fullName", JwtAuthContext.getCurrentUserFullName().orElse(null),
                "branchId", JwtAuthContext.getCurrentUserBranch().orElse(null),
                "employeeId", JwtAuthContext.getCurrentEmployeeId().orElse(null),
                "roles", JwtAuthContext.getCurrentUserRoles()
        ));
    }

    @GetMapping("/validate")
    @Operation(summary = "Validate token", description = "Validate an access token (used by API Gateway)")
    public ResponseEntity<Map<String, Object>> validateToken(
            @RequestHeader(HttpHeaders.AUTHORIZATION) String authHeader) {
        String token = authHeader.replace("Bearer ", "");
        var session = authService.validateToken(token);
        return ResponseEntity.ok(Map.of(
                "valid", true,
                "sessionId", session.getId(),
                "userId", session.getUserId(),
                "username", session.getUsername(),
                "expiresAt", session.getExpiresAt()
        ));
    }

    @GetMapping("/health")
    @Operation(summary = "Health check", description = "Service health check")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "UP", "service", "auth-service"));
    }

    private String getClientIp(HttpServletRequest request) {
        String ip = request.getHeader("X-Forwarded-For");
        if (ip != null && !ip.isBlank() && !"unknown".equalsIgnoreCase(ip)) {
            // X-Forwarded-For may contain multiple IPs (client, proxy1, proxy2)
            return ip.split(",")[0].trim();
        }
        ip = request.getHeader("X-Real-IP");
        if (ip != null && !ip.isBlank()) {
            return ip;
        }
        return request.getRemoteAddr();
    }
}
