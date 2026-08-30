package com.bankxyz.mdm.common.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.bankxyz.mdm.common.dto.ApiError;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.convert.converter.Converter;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.authentication.AbstractAuthenticationToken;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.security.oauth2.server.resource.authentication.JwtGrantedAuthoritiesConverter;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.HttpStatusEntryPoint;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;

/**
 * OAuth2 Resource Server security configuration.
 * Validates JWT tokens from Keycloak, extracts roles, branches, etc.
 *
 * Token claims structure (from Keycloak):
 * - sub: User UUID
 * - preferred_username: Username
 * - email: Email
 * - name: Full name
 * - realm_access.roles: List of realm roles
 * - branch_id: User's branch
 * - employee_id: Employee number
 */
@Slf4j
@Configuration
@EnableMethodSecurity(prePostEnabled = true, securedEnabled = true)
@RequiredArgsConstructor
public class SecurityConfig {

    private final ObjectMapper objectMapper;

    @Value("${app.cors.allowed-origins}")
    private List<String> allowedOrigins;

    @Value("${spring.security.oauth2.resourceserver.jwt.issuer-uri}")
    private String issuerUri;

    @Value("${app.security.jwt.user-id-claim:sub}")
    private String userIdClaim;

    @Value("${app.security.jwt.username-claim:preferred_username}")
    private String usernameClaim;

    @Value("${app.security.jwt.roles-claim:realm_access.roles}")
    private String rolesClaim;

    @Value("${app.security.jwt.branch-id-claim:branch_id}")
    private String branchIdClaim;

    @Value("${app.security.jwt.employee-id-claim:employee_id}")
    private String employeeIdClaim;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http,
                                                   JwtAuthenticationConverter jwtAuthenticationConverter) throws Exception {
        http
            .csrf(AbstractHttpConfigurer::disable)
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                // Public endpoints
                .requestMatchers(
                    "/actuator/health/**",
                    "/actuator/info",
                    "/actuator/prometheus",
                    "/v3/api-docs/**",
                    "/swagger-ui/**",
                    "/swagger-ui.html"
                ).permitAll()
                // All other endpoints require authentication
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt
                    .jwtAuthenticationConverter(jwtAuthenticationConverter))
                .authenticationEntryPoint((request, response, authException) -> {
                    log.warn("Authentication failed on {} {}: {}",
                            request.getMethod(), request.getRequestURI(), authException.getMessage());
                    writeErrorResponse(response, request, HttpStatus.UNAUTHORIZED,
                            "UNAUTHORIZED", "Authentication required",
                            authException.getMessage());
                })
                .accessDeniedHandler((request, response, accessDeniedException) -> {
                    log.warn("Access denied on {} {}: {}",
                            request.getMethod(), request.getRequestURI(), accessDeniedException.getMessage());
                    writeErrorResponse(response, request, HttpStatus.FORBIDDEN,
                            "ACCESS_DENIED", "Insufficient permissions",
                            accessDeniedException.getMessage());
                }));

        return http.build();
    }

    /**
     * Custom JWT authentication converter that:
     * 1. Extracts roles from realm_access.roles
     * 2. Adds branch_id and employee_id to authentication details
     * 3. Maps roles to Spring Security authorities (prefix: ROLE_)
     */
    @Bean
    public JwtAuthenticationConverter jwtAuthenticationConverter() {
        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(jwtGrantedAuthoritiesConverter());
        converter.setPrincipalClaimName(userIdClaim);
        return converter;
    }

    /**
     * Converts JWT claims to Spring Security GrantedAuthorities
     * Maps realm roles to ROLE_<role> authorities
     */
    private Converter<Jwt, Collection<GrantedAuthority>> jwtGrantedAuthoritiesConverter() {
        JwtGrantedAuthoritiesConverter defaultConverter = new JwtGrantedAuthoritiesConverter();

        return jwt -> {
            Collection<GrantedAuthority> authorities = new ArrayList<>(defaultConverter.convert(jwt));

            // Extract roles from realm_access.roles
            Map<String, Object> realmAccess = jwt.getClaimAsMap("realm_access");
            if (realmAccess != null && realmAccess.containsKey("roles")) {
                @SuppressWarnings("unchecked")
                List<String> roles = (List<String>) realmAccess.get("roles");
                if (roles != null) {
                    roles.forEach(role ->
                        authorities.add(new SimpleGrantedAuthority("ROLE_" + role.toUpperCase())));
                }
            }

            // Extract roles from resource_access (client-specific)
            Map<String, Object> resourceAccess = jwt.getClaimAsMap("resource_access");
            if (resourceAccess != null) {
                resourceAccess.forEach((client, access) -> {
                    if (access instanceof Map) {
                        @SuppressWarnings("unchecked")
                        Map<String, Object> clientAccess = (Map<String, Object>) access;
                        if (clientAccess.containsKey("roles")) {
                            @SuppressWarnings("unchecked")
                            List<String> roles = (List<String>) clientAccess.get("roles");
                            if (roles != null) {
                                roles.forEach(role ->
                                    authorities.add(new SimpleGrantedAuthority("ROLE_" + role.toUpperCase())));
                            }
                        }
                    }
                });
            }

            // Extract scopes
            String scope = jwt.getClaimAsString("scope");
            if (scope != null && !scope.isBlank()) {
                Arrays.stream(scope.split(" "))
                      .forEach(s -> authorities.add(new SimpleGrantedAuthority("SCOPE_" + s)));
            }

            log.debug("JWT authorities for user {}: {}",
                    jwt.getClaimAsString(usernameClaim),
                    authorities.stream().map(GrantedAuthority::getAuthority).collect(Collectors.toList()));

            return authorities;
        };
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(allowedOrigins);
        config.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        config.setExposedHeaders(Arrays.asList("X-Correlation-Id", "X-Request-Id", "Location"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }

    private void writeErrorResponse(HttpServletResponse response, HttpServletRequest request,
                                     HttpStatus status, String code, String message, String detail) {
        try {
            response.setStatus(status.value());
            response.setContentType(MediaType.APPLICATION_JSON_VALUE);

            ApiError error = ApiError.builder()
                    .timestamp(Instant.now())
                    .status(status.value())
                    .code(code)
                    .message(message)
                    .detail(detail)
                    .path(request.getRequestURI())
                    .method(request.getMethod())
                    .build();

            objectMapper.writeValue(response.getWriter(), error);
        } catch (Exception e) {
            log.error("Failed to write error response", e);
        }
    }
}
