package com.bankxyz.mdm.auth.service;

import com.bankxyz.mdm.auth.domain.LoginAttempt;
import com.bankxyz.mdm.auth.domain.MfaSetting;
import com.bankxyz.mdm.auth.domain.UserSession;
import com.bankxyz.mdm.auth.dto.LoginRequest;
import com.bankxyz.mdm.auth.dto.LoginResponse;
import com.bankxyz.mdm.auth.repository.LoginAttemptRepository;
import com.bankxyz.mdm.auth.repository.MfaSettingRepository;
import com.bankxyz.mdm.auth.repository.UserSessionRepository;
import com.bankxyz.mdm.common.exception.BusinessException;
import com.bankxyz.mdm.common.security.JwtAuthContext;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.HexFormat;
import java.util.Optional;
import java.util.UUID;

/**
 * Authentication service.
 * Handles login, logout, token validation, session management.
 * Delegates actual authentication to Keycloak via OAuth2.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserSessionRepository sessionRepository;
    private final MfaSettingRepository mfaRepository;
    private final LoginAttemptRepository loginAttemptRepository;
    private final KeycloakAdminService keycloakService;
    private final PasswordEncoder passwordEncoder;

    @Value("${app.security.max-failed-attempts:5}")
    private int maxFailedAttempts;

    @Value("${app.security.lockout-duration-minutes:15}")
    private int lockoutDurationMinutes;

    @Value("${app.security.session-timeout-minutes:30}")
    private int sessionTimeoutMinutes;

    @Value("${app.security.refresh-token-days:7}")
    private int refreshTokenDays;

    /**
     * Authenticate user and create session.
     */
    @Transactional
    public LoginResponse login(LoginRequest request, String ipAddress, String userAgent, String correlationId) {
        log.info("Login attempt for username: {}", request.username());

        // 1. Check for brute force / lockout
        checkLockout(request.username(), ipAddress);

        // 2. Authenticate via Keycloak
        KeycloakTokenResponse tokenResponse = keycloakService.authenticate(
                request.username(), request.password());

        boolean success = tokenResponse != null;
        LoginAttempt.FailureReason failureReason = null;

        if (!success) {
            failureReason = LoginAttempt.FailureReason.INVALID_CREDENTIALS;
            recordLoginAttempt(request.username(), null, false, failureReason, ipAddress, userAgent, false, null, correlationId);
            throw BusinessException.unprocessable("INVALID_CREDENTIALS", "Invalid username or password");
        }

        // 3. Check MFA
        Optional<MfaSetting> mfaOpt = mfaRepository.findByUsernameAndDeletedAtIsNull(request.username());
        boolean mfaRequired = mfaOpt.map(MfaSetting::getMfaEnabled).orElse(false);
        boolean mfaVerified = false;

        if (mfaRequired) {
            if (request.mfaCode() == null || request.mfaCode().isBlank()) {
                recordLoginAttempt(request.username(), null, false,
                        LoginAttempt.FailureReason.MFA_REQUIRED, ipAddress, userAgent, true, false, correlationId);
                // Return partial response indicating MFA required
                return buildMfaRequiredResponse(mfaOpt.get());
            }
            mfaVerified = verifyMfa(mfaOpt.get(), request.mfaCode());
            if (!mfaVerified) {
                recordLoginAttempt(request.username(), null, false,
                        LoginAttempt.FailureReason.MFA_FAILED, ipAddress, userAgent, true, false, correlationId);
                throw BusinessException.unprocessable("MFA_FAILED", "Invalid MFA code");
            }
        }

        // 4. Get user info from Keycloak
        KeycloakUserInfo userInfo = keycloakService.getUserInfo(tokenResponse.accessToken());

        // 5. Create session
        UserSession session = createSession(
                UUID.fromString(userInfo.id()),
                userInfo.username(),
                tokenResponse,
                ipAddress,
                userAgent,
                mfaVerified,
                mfaOpt.map(MfaSetting::getMfaMethod).orElse(null));

        // 6. Record success
        recordLoginAttempt(userInfo.username(), session.getUserId(), true, null, ipAddress, userAgent, mfaRequired, mfaVerified, correlationId);

        log.info("Login successful for user: {} (session: {})", userInfo.username(), session.getId());

        // 7. Build response
        return new LoginResponse(
                tokenResponse.accessToken(),
                tokenResponse.refreshToken(),
                "Bearer",
                tokenResponse.expiresIn(),
                Instant.now().plusSeconds(tokenResponse.expiresIn()),
                Instant.now().plus(refreshTokenDays, ChronoUnit.DAYS),
                session.getId(),
                false,
                mfaOpt.map(MfaSetting::getMfaMethod).orElse(null),
                new LoginResponse.UserInfo(
                        UUID.fromString(userInfo.id()),
                        userInfo.username(),
                        userInfo.email(),
                        userInfo.fullName(),
                        userInfo.employeeId(),
                        userInfo.branchId(),
                        userInfo.realmRoles()
                )
        );
    }

    /**
     * Logout current session.
     */
    @Transactional
    public void logout(UUID sessionId, String reason) {
        log.info("Logout session: {} (reason: {})", sessionId, reason);
        int updated = sessionRepository.logoutSession(sessionId, Instant.now(), reason);
        if (updated == 0) {
            log.warn("Session {} not found or already logged out", sessionId);
        }
    }

    /**
     * Logout all sessions for a user.
     */
    @Transactional
    public int logoutAllSessions(UUID userId) {
        log.info("Logout all sessions for user: {}", userId);
        return sessionRepository.logoutAllUserSessions(userId, Instant.now());
    }

    /**
     * Validate access token.
     */
    @Transactional(readOnly = true)
    public UserSession validateToken(String accessToken) {
        String tokenHash = hashToken(accessToken);
        return sessionRepository.findByTokenHash(tokenHash)
                .filter(s -> s.getActive())
                .filter(s -> s.getExpiresAt().isAfter(Instant.now()))
                .orElseThrow(() -> BusinessException.unprocessable("INVALID_TOKEN", "Token is invalid or expired"));
    }

    /**
     * Refresh access token.
     */
    @Transactional
    public LoginResponse refreshToken(String refreshToken, String ipAddress, String userAgent) {
        String refreshHash = hashToken(refreshToken);
        UserSession session = sessionRepository.findByTokenHash(refreshHash)
                .orElseThrow(() -> BusinessException.unprocessable("INVALID_REFRESH_TOKEN", "Invalid refresh token"));

        if (!session.getActive() || session.getExpiresAt().isBefore(Instant.now())) {
            throw BusinessException.unprocessable("EXPIRED_REFRESH_TOKEN", "Refresh token expired");
        }

        // Call Keycloak to refresh
        KeycloakTokenResponse newTokens = keycloakService.refreshToken(refreshToken);

        // Update session
        session.setTokenHash(hashToken(newTokens.accessToken()));
        session.setRefreshTokenHash(newTokens.refreshToken() != null ? hashToken(newTokens.refreshToken()) : session.getRefreshTokenHash());
        session.setExpiresAt(Instant.now().plusSeconds(newTokens.expiresIn()));
        session.setLastActivityAt(Instant.now());
        sessionRepository.save(session);

        KeycloakUserInfo userInfo = keycloakService.getUserInfo(newTokens.accessToken());

        return new LoginResponse(
                newTokens.accessToken(),
                newTokens.refreshToken(),
                "Bearer",
                newTokens.expiresIn(),
                Instant.now().plusSeconds(newTokens.expiresIn()),
                session.getExpiresAt(),
                session.getId(),
                false,
                null,
                new LoginResponse.UserInfo(
                        UUID.fromString(userInfo.id()),
                        userInfo.username(),
                        userInfo.email(),
                        userInfo.fullName(),
                        userInfo.employeeId(),
                        userInfo.branchId(),
                        userInfo.realmRoles()
                )
        );
    }

    // ============================================================
    // PRIVATE HELPERS
    // ============================================================

    private void checkLockout(String username, String ipAddress) {
        Instant since = Instant.now().minus(lockoutDurationMinutes, ChronoUnit.MINUTES);

        long failedByUser = loginAttemptRepository.countFailedAttemptsSince(username, since);
        long failedByIp = loginAttemptRepository.countFailedAttemptsByIpSince(ipAddress, since);

        if (failedByUser >= maxFailedAttempts) {
            log.warn("Account locked due to {} failed attempts for username: {}", failedByUser, username);
            throw BusinessException.unprocessable("ACCOUNT_LOCKED",
                    "Account temporarily locked due to too many failed attempts. Try again in " + lockoutDurationMinutes + " minutes.");
        }

        if (failedByIp >= maxFailedAttempts * 3) {
            log.warn("IP blocked due to {} failed attempts from: {}", failedByIp, ipAddress);
            throw BusinessException.unprocessable("IP_BLOCKED",
                    "IP temporarily blocked due to suspicious activity.");
        }
    }

    private boolean verifyMfa(MfaSetting mfa, String code) {
        // TODO: Implement TOTP verification (Google Authenticator)
        // For now, accept any 6-digit code for testing
        return code != null && code.matches("^\\d{6}$");
    }

    private UserSession createSession(UUID userId, String username, KeycloakTokenResponse tokens,
                                      String ipAddress, String userAgent, boolean mfaVerified, String mfaMethod) {
        UserSession session = UserSession.builder()
                .userId(userId)
                .username(username)
                .keycloakSessionId(tokens.sessionState())
                .tokenHash(hashToken(tokens.accessToken()))
                .refreshTokenHash(tokens.refreshToken() != null ? hashToken(tokens.refreshToken()) : null)
                .ipAddress(ipAddress)
                .userAgent(userAgent)
                .loginAt(Instant.now())
                .lastActivityAt(Instant.now())
                .expiresAt(Instant.now().plusSeconds(tokens.expiresIn()))
                .active(true)
                .mfaVerified(mfaVerified)
                .mfaMethod(mfaMethod)
                .build();
        return sessionRepository.save(session);
    }

    private void recordLoginAttempt(String username, UUID userId, boolean success,
                                     LoginAttempt.FailureReason reason, String ipAddress, String userAgent,
                                     boolean mfaAttempted, Boolean mfaSuccess, String correlationId) {
        LoginAttempt attempt = LoginAttempt.builder()
                .username(username)
                .userId(userId)
                .success(success)
                .failureReason(reason != null ? reason.name() : null)
                .ipAddress(ipAddress)
                .userAgent(userAgent)
                .attemptedAt(Instant.now())
                .mfaAttempted(mfaAttempted)
                .mfaSuccess(mfaSuccess)
                .correlationId(correlationId)
                .build();
        loginAttemptRepository.save(attempt);
    }

    private LoginResponse buildMfaRequiredResponse(MfaSetting mfa) {
        return new LoginResponse(
                null, null, "Bearer", 0L, null, null, null,
                true, mfa.getMfaMethod(), null
        );
    }

    private String hashToken(String token) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(token.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException("SHA-256 not available", e);
        }
    }
}
