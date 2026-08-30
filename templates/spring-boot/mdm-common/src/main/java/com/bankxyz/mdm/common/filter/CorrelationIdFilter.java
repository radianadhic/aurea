package com.bankxyz.mdm.common.filter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.MDC;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.UUID;

/**
 * Request correlation filter.
 * - Generates/propagates correlation ID
 * - Captures user ID from JWT (if available)
 * - Adds to MDC for log correlation
 * - Adds to response headers
 */
@Slf4j
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class CorrelationIdFilter extends OncePerRequestFilter {

    public static final String CORRELATION_ID_HEADER = "X-Correlation-Id";
    public static final String REQUEST_ID_HEADER = "X-Request-Id";
    public static final String CORRELATION_ID_MDC = "correlationId";
    public static final String REQUEST_ID_MDC = "requestId";
    public static final String USER_ID_MDC = "userId";

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                     HttpServletResponse response,
                                     FilterChain filterChain) throws ServletException, IOException {
        try {
            // 1. Extract or generate correlation ID
            String correlationId = request.getHeader(CORRELATION_ID_HEADER);
            if (correlationId == null || correlationId.isBlank()) {
                correlationId = UUID.randomUUID().toString();
            }
            MDC.put(CORRELATION_ID_MDC, correlationId);

            // 2. Extract or generate request ID
            String requestId = request.getHeader(REQUEST_ID_HEADER);
            if (requestId == null || requestId.isBlank()) {
                requestId = UUID.randomUUID().toString();
            }
            MDC.put(REQUEST_ID_MDC, requestId);

            // 3. Extract user ID from JWT (if authenticated)
            Authentication auth = SecurityContextHolder.getContext().getAuthentication();
            if (auth instanceof JwtAuthenticationToken jwtAuth) {
                Jwt jwt = jwtAuth.getToken();
                String userId = jwt.getClaimAsString("sub");
                if (userId != null) {
                    MDC.put(USER_ID_MDC, userId);
                }
            }

            // 4. Add to response headers
            response.setHeader(CORRELATION_ID_HEADER, correlationId);
            response.setHeader(REQUEST_ID_HEADER, requestId);

            // 5. Log request start
            long startTime = System.currentTimeMillis();
            log.debug("→ {} {} from {}",
                    request.getMethod(),
                    request.getRequestURI(),
                    request.getRemoteAddr());

            // 6. Process request
            try {
                filterChain.doFilter(request, response);
            } finally {
                // 7. Log request completion
                long duration = System.currentTimeMillis() - startTime;
                log.debug("← {} {} - {} ({}ms)",
                        request.getMethod(),
                        request.getRequestURI(),
                        response.getStatus(),
                        duration);
            }
        } finally {
            // 8. Clean up MDC
            MDC.remove(CORRELATION_ID_MDC);
            MDC.remove(REQUEST_ID_MDC);
            MDC.remove(USER_ID_MDC);
        }
    }
}
