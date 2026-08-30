package com.bankxyz.mdm.common.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

import java.util.Collections;
import java.util.Map;

/**
 * Base class for all business exceptions.
 * Use this instead of generic RuntimeException for predictable error handling.
 */
@Getter
public class BusinessException extends RuntimeException {

    private final HttpStatus status;
    private final String code;
    private final String detail;
    private final Map<String, Object> context;

    public BusinessException(HttpStatus status, String code, String message) {
        this(status, code, message, null, Collections.emptyMap());
    }

    public BusinessException(HttpStatus status, String code, String message, String detail) {
        this(status, code, message, detail, Collections.emptyMap());
    }

    public BusinessException(HttpStatus status, String code, String message, String detail, Map<String, Object> context) {
        super(message);
        this.status = status;
        this.code = code;
        this.detail = detail;
        this.context = context;
    }

    /**
     * Convenience method to create a 404 Not Found exception
     */
    public static BusinessException notFound(String resource, Object id) {
        return new BusinessException(
                HttpStatus.NOT_FOUND,
                "RESOURCE_NOT_FOUND",
                String.format("%s with id '%s' not found", resource, id)
        );
    }

    /**
     * Convenience method to create a 409 Conflict exception
     */
    public static BusinessException conflict(String message) {
        return new BusinessException(HttpStatus.CONFLICT, "CONFLICT", message);
    }

    /**
     * Convenience method to create a 400 Bad Request exception
     */
    public static BusinessException badRequest(String code, String message) {
        return new BusinessException(HttpStatus.BAD_REQUEST, code, message);
    }

    /**
     * Convenience method to create a 422 Unprocessable Entity (business rule violation)
     */
    public static BusinessException unprocessable(String code, String message) {
        return new BusinessException(HttpStatus.UNPROCESSABLE_ENTITY, code, message);
    }

    /**
     * Convenience method to create a 403 Forbidden exception
     */
    public static BusinessException forbidden(String message) {
        return new BusinessException(HttpStatus.FORBIDDEN, "FORBIDDEN", message);
    }
}
