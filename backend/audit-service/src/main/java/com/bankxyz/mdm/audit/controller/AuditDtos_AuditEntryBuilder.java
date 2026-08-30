package com.bankxyz.mdm.audit.controller;

import com.bankxyz.mdm.audit.domain.AuditEntry;
import com.bankxyz.mdm.audit.dto.AuditDtos;
import com.bankxyz.mdm.common.security.JwtAuthContext;

import java.time.Instant;
import java.util.HashMap;

/**
 * Builder helper for converting DTOs to entities in controllers.
 */
class AuditDtos_AuditEntryBuilder {
    static AuditEntry build(AuditDtos.CreateAuditRequest req, JwtAuthContext auth) {
        return AuditEntry.builder()
            .timestamp(Instant.now())
            .userId(auth.getUserId())
            .username(auth.getUsername())
            .userFullName(auth.getFullName())
            .userRole(auth.getRole())
            .action(req.action())
            .entityType(req.entityType())
            .entityId(req.entityId())
            .ipAddress(auth.getIpAddress())
            .userAgent(auth.getUserAgent())
            .correlationId(auth.getCorrelationId())
            .sessionId(auth.getSessionId())
            .sourceService("audit-service")
            .changes(req.changes() != null ? req.changes() : new HashMap<>())
            .metadata(req.metadata() != null ? req.metadata() : new HashMap<>())
            .build();
    }
}
