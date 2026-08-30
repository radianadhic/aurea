package com.bankxyz.mdm.auth.service;

import com.bankxyz.mdm.common.exception.BusinessException;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClient;

import java.util.Arrays;
import java.util.Map;
import java.util.UUID;

/**
 * Keycloak Admin Service.
 * Handles communication with Keycloak for:
 * - User authentication (password grant, exchange code for token)
 * - Token refresh
 * - User info retrieval
 * - Admin operations (user CRUD, role management)
 *
 * In production, use Keycloak's service account with admin-cli client
 * or use the user's own credentials via password grant.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class KeycloakAdminService {

    @Value("${spring.security.oauth2.resourceserver.jwt.issuer-uri}")
    private String keycloakIssuerUri;

    @Value("${app.keycloak.realm:mdm-dev}")
    private String realm;

    @Value("${app.keycloak.client-id:mdm-gateway}")
    private String clientId;

    @Value("${app.keycloak.client-secret:}")
    private String clientSecret;

    @Value("${app.keycloak.admin-username:admin}")
    private String adminUsername;

    @Value("${app.keycloak.admin-password:admin}")
    private String adminPassword;

    /**
     * Authenticate user via Keycloak (Resource Owner Password Credentials Grant).
     * Returns tokens or null if authentication fails.
     */
    public KeycloakTokenResponse authenticate(String username, String password) {
        try {
            String tokenUrl = keycloakIssuerUri + "/protocol/openid-connect/token";

            MultiValueMap<String, String> formData = new LinkedMultiValueMap<>();
            formData.add("grant_type", "password");
            formData.add("client_id", clientId);
            if (!clientSecret.isBlank()) {
                formData.add("client_secret", clientSecret);
            }
            formData.add("username", username);
            formData.add("password", password);
            formData.add("scope", "openid email profile");

            KeycloakTokenResponse response = RestClient.create()
                    .post()
                    .uri(tokenUrl)
                    .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_FORM_URLENCODED_VALUE)
                    .body(formData)
                    .retrieve()
                    .body(KeycloakTokenResponse.class);

            log.debug("Keycloak auth response received for user: {}", username);
            return response;
        } catch (Exception e) {
            log.warn("Keycloak authentication failed for user: {} - {}", username, e.getMessage());
            return null;
        }
    }

    /**
     * Refresh access token.
     */
    public KeycloakTokenResponse refreshToken(String refreshToken) {
        try {
            String tokenUrl = keycloakIssuerUri + "/protocol/openid-connect/token";

            MultiValueMap<String, String> formData = new LinkedMultiValueMap<>();
            formData.add("grant_type", "refresh_token");
            formData.add("client_id", clientId);
            if (!clientSecret.isBlank()) {
                formData.add("client_secret", clientSecret);
            }
            formData.add("refresh_token", refreshToken);

            return RestClient.create()
                    .post()
                    .uri(tokenUrl)
                    .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_FORM_URLENCODED_VALUE)
                    .body(formData)
                    .retrieve()
                    .body(KeycloakTokenResponse.class);
        } catch (Exception e) {
            log.error("Token refresh failed", e);
            throw BusinessException.unprocessable("TOKEN_REFRESH_FAILED", "Failed to refresh token");
        }
    }

    /**
     * Get user info from access token.
     */
    public KeycloakUserInfo getUserInfo(String accessToken) {
        try {
            String userInfoUrl = keycloakIssuerUri + "/protocol/openid-connect/userinfo";

            Map<String, Object> response = RestClient.create()
                    .get()
                    .uri(userInfoUrl)
                    .header(HttpHeaders.AUTHORIZATION, "Bearer " + accessToken)
                    .retrieve()
                    .body(Map.class);

            KeycloakUserInfo info = new KeycloakUserInfo();
            info.setId((String) response.get("sub"));
            info.setUsername((String) response.get("preferred_username"));
            info.setEmail((String) response.get("email"));
            info.setFullName((String) response.get("name"));
            info.setEmployeeId((String) response.get("employee_id"));
            info.setBranchId((String) response.get("branch_id"));
            // Realm roles would need separate call to /authz/entitlement or token introspection
            info.setRealmRoles(new String[0]);
            return info;
        } catch (Exception e) {
            log.error("Failed to get user info", e);
            throw BusinessException.unprocessable("USERINFO_FAILED", "Failed to get user info");
        }
    }

    /**
     * Logout user (revoke refresh token) in Keycloak.
     */
    public void logout(String refreshToken) {
        try {
            String logoutUrl = keycloakIssuerUri + "/protocol/openid-connect/logout";

            MultiValueMap<String, String> formData = new LinkedMultiValueMap<>();
            formData.add("client_id", clientId);
            if (!clientSecret.isBlank()) {
                formData.add("client_secret", clientSecret);
            }
            formData.add("refresh_token", refreshToken);

            RestClient.create()
                    .post()
                    .uri(logoutUrl)
                    .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_FORM_URLENCODED_VALUE)
                    .body(formData)
                    .retrieve()
                    .toBodilessEntity();

            log.debug("Keycloak logout successful");
        } catch (Exception e) {
            log.warn("Keycloak logout failed (non-critical): {}", e.getMessage());
        }
    }

    @Data
    public static class KeycloakTokenResponse {
        @JsonProperty("access_token")
        private String accessToken;
        @JsonProperty("refresh_token")
        private String refreshToken;
        @JsonProperty("token_type")
        private String tokenType;
        @JsonProperty("expires_in")
        private Long expiresIn;
        @JsonProperty("refresh_expires_in")
        private Long refreshExpiresIn;
        @JsonProperty("session_state")
        private String sessionState;
        @JsonProperty("not-before-policy")
        private Integer notBeforePolicy;
        private String scope;
    }

    @Data
    public static class KeycloakUserInfo {
        private String id;
        private String username;
        private String email;
        @JsonProperty("name")
        private String fullName;
        @JsonProperty("employee_id")
        private String employeeId;
        @JsonProperty("branch_id")
        private String branchId;
        @JsonProperty("realm_access")
        private Map<String, Object> realmAccess;

        public String[] getRealmRoles() {
            if (realmAccess == null) return new String[0];
            Object roles = realmAccess.get("roles");
            if (roles instanceof java.util.List<?> list) {
                return list.stream().map(Object::toString).toArray(String[]::new);
            }
            return new String[0];
        }
    }
}
