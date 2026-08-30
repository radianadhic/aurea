package com.bankxyz.mdm.common.security;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;

import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Utility class to extract authentication context from JWT.
 * Use in services/controllers to get current user info.
 *
 * Example:
 * String userId = JwtAuthContext.getCurrentUserId();
 * String branchId = JwtAuthContext.getCurrentUserBranch();
 * boolean isAdmin = JwtAuthContext.hasRole("ADMIN");
 */
public final class JwtAuthContext {

    private JwtAuthContext() {
        // Utility class
    }

    /**
     * Get the current JWT token
     */
    public static Optional<Jwt> getCurrentJwt() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth instanceof JwtAuthenticationToken jwtAuth) {
            return Optional.of(jwtAuth.getToken());
        }
        return Optional.empty();
    }

    /**
     * Get the current authenticated user ID (UUID)
     */
    public static Optional<String> getCurrentUserId() {
        return getCurrentJwt().map(jwt -> jwt.getClaimAsString("sub"));
    }

    /**
     * Get the current username
     */
    public static Optional<String> getCurrentUsername() {
        return getCurrentJwt().map(jwt -> jwt.getClaimAsString("preferred_username"));
    }

    /**
     * Get the current user's full name
     */
    public static Optional<String> getCurrentUserFullName() {
        return getCurrentJwt().map(jwt -> jwt.getClaimAsString("name"));
    }

    /**
     * Get the current user's email
     */
    public static Optional<String> getCurrentUserEmail() {
        return getCurrentJwt().map(jwt -> jwt.getClaimAsString("email"));
    }

    /**
     * Get the current user's branch ID
     */
    public static Optional<String> getCurrentUserBranch() {
        return getCurrentJwt().map(jwt -> jwt.getClaimAsString("branch_id"));
    }

    /**
     * Get the current user's employee ID
     */
    public static Optional<String> getCurrentEmployeeId() {
        return getCurrentJwt().map(jwt -> jwt.getClaimAsString("employee_id"));
    }

    /**
     * Get all realm roles for the current user
     */
    @SuppressWarnings("unchecked")
    public static Set<String> getCurrentUserRoles() {
        return getCurrentJwt()
            .map(jwt -> {
                List<String> roles = jwt.getClaimAsStringList("realm_access.roles");
                return roles == null ? Set.<String>of() : Set.copyOf(roles);
            })
            .orElse(Set.of());
    }

    /**
     * Check if current user has a specific role
     */
    public static boolean hasRole(String role) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null) return false;
        String targetRole = "ROLE_" + role.toUpperCase();
        return auth.getAuthorities().stream()
                .anyMatch(a -> a.getAuthority().equalsIgnoreCase(targetRole) ||
                              a.getAuthority().equalsIgnoreCase(role));
    }

    /**
     * Check if current user has any of the specified roles
     */
    public static boolean hasAnyRole(String... roles) {
        for (String role : roles) {
            if (hasRole(role)) return true;
        }
        return false;
    }

    /**
     * Check if current user has all of the specified roles
     */
    public static boolean hasAllRoles(String... roles) {
        for (String role : roles) {
            if (!hasRole(role)) return false;
        }
        return true;
    }

    /**
     * Check if current user is authenticated
     */
    public static boolean isAuthenticated() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        return auth != null && auth.isAuthenticated() && !"anonymousUser".equals(auth.getPrincipal());
    }

    /**
     * Require authentication or throw exception
     */
    public static void requireAuthenticated() {
        if (!isAuthenticated()) {
            throw new IllegalStateException("No authenticated user in context");
        }
    }
}
