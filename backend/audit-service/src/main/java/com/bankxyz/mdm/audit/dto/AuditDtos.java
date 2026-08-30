package com.bankxyz.mdm.audit.dto;

import com.bankxyz.mdm.audit.domain.AuditEntry;
import jakarta.validation.constraints.*;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public class AuditDtos {

    public record AuditEntryDto(
        UUID id,
        Instant timestamp,
        String userId,
        String username,
        String userFullName,
        String userRole,
        String action,
        String entityType,
        String entityId,
        String ipAddress,
        String userAgent,
        String requestMethod,
        String requestPath,
        Integer responseStatus,
        String result,
        String errorMessage,
        String correlationId,
        String sessionId,
        String sourceService,
        Map<String, Object> changes,
        Map<String, Object> metadata,
        Instant createdAt
    ) {
        public static AuditEntryDto from(AuditEntry e) {
            return new AuditEntryDto(
                e.getId(),
                e.getTimestamp(),
                e.getUserId(),
                e.getUsername(),
                e.getUserFullName(),
                e.getUserRole(),
                e.getAction(),
                e.getEntityType(),
                e.getEntityId(),
                e.getIpAddress(),
                e.getUserAgent(),
                e.getRequestMethod(),
                e.getRequestPath(),
                e.getResponseStatus(),
                e.getResult() != null ? e.getResult().name() : null,
                e.getErrorMessage(),
                e.getCorrelationId(),
                e.getSessionId(),
                e.getSourceService(),
                e.getChanges(),
                e.getMetadata(),
                e.getCreatedAt()
            );
        }
    }

    public record AuditSearchRequest(
        String userId,
        String username,
        String action,
        String entityType,
        String entityId,
        String result,
        Instant fromDate,
        Instant toDate,
        Integer page,
        Integer size
    ) {}

    public record CreateAuditRequest(
        @NotBlank String action,
        @NotBlank String entityType,
        String entityId,
        Map<String, Object> changes,
        Map<String, Object> metadata
    ) {}

    public record AuditEventDto(
        Instant timestamp,
        String userId,
        String username,
        String userFullName,
        String userRole,
        String action,
        String entityType,
        String entityId,
        String ipAddress,
        String userAgent,
        String correlationId,
        String sessionId,
        String sourceService,
        String result,
        String errorMessage,
        Map<String, Object> changes,
        Map<String, Object> metadata
    ) {}

    public record AuditStatsResponse(
        long totalEntries,
        Map<String, Long> byActionLast7Days,
        Map<String, Long> byUserLast7Days,
        Map<String, Long> byResultLast7Days
    ) {}

    public record ExportRequest(
        String format,
        AuditSearchRequest filter
    ) {}
}
