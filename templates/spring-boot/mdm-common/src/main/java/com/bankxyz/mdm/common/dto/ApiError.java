package com.bankxyz.mdm.common.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Data;

import java.time.Instant;
import java.util.List;
import java.util.Map;

/**
 * Standard API error response (RFC 7807 Problem Details inspired).
 * Used by GlobalExceptionHandler for all error responses.
 *
 * Example:
 * {
 *   "timestamp": "2026-08-26T10:00:00Z",
 *   "status": 400,
 *   "code": "VALIDATION_ERROR",
 *   "message": "Validation failed for one or more fields",
 *   "path": "/api/v1/customers",
 *   "traceId": "abc123",
 *   "fieldErrors": [
 *     {"field": "email", "message": "must be a valid email", "rejectedValue": "invalid"}
 *   ]
 * }
 */
@Data
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
@Schema(description = "Standard API error response")
public class ApiError {

    @Schema(description = "Error timestamp (UTC)")
    private Instant timestamp;

    @Schema(description = "HTTP status code", example = "400")
    private int status;

    @Schema(description = "Application-specific error code", example = "VALIDATION_ERROR")
    private String code;

    @Schema(description = "Human-readable error message")
    private String message;

    @Schema(description = "Detailed error description")
    private String detail;

    @Schema(description = "Request path that caused the error")
    private String path;

    @Schema(description = "Request method (GET, POST, etc)")
    private String method;

    @Schema(description = "Distributed tracing ID")
    private String traceId;

    @Schema(description = "User ID (if authenticated)")
    private String userId;

    @Schema(description = "Correlation ID for request tracking")
    private String correlationId;

    @Schema(description = "Field-level validation errors")
    private List<FieldError> fieldErrors;

    @Schema(description = "Additional error context")
    private Map<String, Object> context;

    @Data
    @Builder
    @Schema(description = "Field-level validation error")
    public static class FieldError {
        @Schema(description = "Field name", example = "email")
        private String field;
        @Schema(description = "Validation error message")
        private String message;
        @Schema(description = "Rejected value")
        private Object rejectedValue;
        @Schema(description = "Validation constraint code")
        private String code;
    }
}
