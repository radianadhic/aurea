package com.bankxyz.mdm.common.exception;

/**
 * Exception thrown when a requested resource is not found.
 * Will be translated to HTTP 404 by GlobalExceptionHandler.
 */
public class ResourceNotFoundException extends BusinessException {

    public ResourceNotFoundException(String resource, Object id) {
        super(org.springframework.http.HttpStatus.NOT_FOUND,
              "RESOURCE_NOT_FOUND",
              String.format("%s with id '%s' not found", resource, id));
    }

    public ResourceNotFoundException(String message) {
        super(org.springframework.http.HttpStatus.NOT_FOUND,
              "RESOURCE_NOT_FOUND",
              message);
    }

    public static ResourceNotFoundException forResource(String resource, Object id) {
        return new ResourceNotFoundException(resource, id);
    }
}
