package com.bankxyz.mdm.audit.service;

import com.bankxyz.mdm.audit.domain.AuditEntry;
import com.bankxyz.mdm.audit.domain.AuditResult;
import com.bankxyz.mdm.audit.dto.*;
import com.bankxyz.mdm.audit.repository.AuditEntryRepository;
import com.bankxyz.mdm.common.dto.PageResponse;
import com.bankxyz.mdm.common.exception.BusinessException;
import com.bankxyz.mdm.common.exception.ResourceNotFoundException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.*;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuditService {

    private final AuditEntryRepository repository;
    private final ObjectMapper objectMapper;

    /**
     * Persist a new audit entry. Async to not block main flow.
     */
    @Async
    @Transactional
    public void record(AuditEntry entry) {
        try {
            if (entry.getTimestamp() == null) {
                entry.setTimestamp(Instant.now());
            }
            repository.save(entry);
            log.debug("Audit recorded: {} by {} on {}",
                entry.getAction(), entry.getUsername(), entry.getEntityType());
        } catch (Exception e) {
            log.error("Failed to record audit entry: {}", e.getMessage(), e);
        }
    }

    @Async
    @Transactional
    public void recordFromEvent(AuditEventDto event) {
        try {
            AuditEntry entry = AuditEntry.builder()
                .timestamp(event.timestamp() != null ? event.timestamp() : Instant.now())
                .userId(event.userId())
                .username(event.username())
                .userFullName(event.userFullName())
                .userRole(event.userRole())
                .action(event.action())
                .entityType(event.entityType())
                .entityId(event.entityId())
                .ipAddress(event.ipAddress())
                .userAgent(event.userAgent())
                .correlationId(event.correlationId())
                .sessionId(event.sessionId())
                .sourceService(event.sourceService())
                .result(event.result() != null
                    ? AuditResult.valueOf(event.result())
                    : AuditResult.SUCCESS)
                .errorMessage(event.errorMessage())
                .changes(event.changes() != null ? event.changes() : new HashMap<>())
                .metadata(event.metadata() != null ? event.metadata() : new HashMap<>())
                .build();
            repository.save(entry);
        } catch (Exception e) {
            log.error("Failed to record audit from event: {}", e.getMessage(), e);
        }
    }

    /**
     * Search audit entries.
     */
    @Transactional(readOnly = true)
    public PageResponse<AuditEntryDto> search(AuditSearchRequest request) {
        Pageable pageable = PageRequest.of(
            request.page() != null ? request.page() : 0,
            request.size() != null ? request.size() : 50,
            Sort.by(Sort.Direction.DESC, "timestamp")
        );

        Page<AuditEntry> page = repository.search(
            request.userId(),
            request.username(),
            request.action(),
            request.entityType(),
            request.entityId(),
            request.result() != null ? AuditResult.valueOf(request.result()) : null,
            request.fromDate(),
            request.toDate(),
            pageable
        );

        List<AuditEntryDto> content = page.getContent().stream()
            .map(AuditEntryDto::from)
            .toList();

        return PageResponse.<AuditEntryDto>builder()
            .content(content)
            .page(page.getNumber())
            .size(page.getSize())
            .totalElements(page.getTotalElements())
            .totalPages(page.getTotalPages())
            .first(page.isFirst())
            .last(page.isLast())
            .numberOfElements(page.getNumberOfElements())
            .empty(page.isEmpty())
            .build();
    }

    @Transactional(readOnly = true)
    public AuditEntryDto getById(UUID id) {
        AuditEntry entry = repository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Audit entry not found: " + id));
        return AuditEntryDto.from(entry);
    }

    /**
     * Get all entries for a specific entity (e.g. all changes to a customer).
     */
    @Transactional(readOnly = true)
    public List<AuditEntryDto> getByEntity(String entityType, String entityId) {
        return repository.findByEntityTypeAndEntityId(entityType, entityId).stream()
            .map(AuditEntryDto::from)
            .toList();
    }

    /**
     * Get statistics for dashboard.
     */
    @Transactional(readOnly = true)
    public AuditStatsResponse getStats() {
        Instant last24h = Instant.now().minusSeconds(24 * 3600);
        Instant last7d = Instant.now().minusSeconds(7 * 24 * 3600);

        Map<String, Long> byAction = new HashMap<>();
        repository.countByActionSince(last7d).forEach(row ->
            byAction.put((String) row[0], (Long) row[1])
        );

        Map<String, Long> byUser = new HashMap<>();
        repository.countByUserSince(last7d).stream().limit(10).forEach(row -> {
            String username = (String) row[1];
            Long count = (Long) row[2];
            byUser.put(username, count);
        });

        Map<String, Long> byResult = new HashMap<>();
        repository.countByResultSince(last7d).forEach(row ->
            byResult.put(((AuditResult) row[0]).name(), (Long) row[1])
        );

        return new AuditStatsResponse(
            repository.count(),
            byAction,
            byUser,
            byResult
        );
    }

    /**
     * Soft delete (for compliance reasons like GDPR right-to-be-forgotten).
     * Audit entries are never hard-deleted.
     */
    @Transactional
    public void softDelete(UUID id, String userId, String reason) {
        AuditEntry entry = repository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Audit entry not found: " + id));
        if (entry.getDeletedAt() != null) {
            throw new BusinessException("ALREADY_DELETED", "Entry already soft-deleted");
        }
        entry.setDeletedAt(Instant.now());
        entry.setDeletedBy(userId);
        entry.setDeletionReason(reason);
        repository.save(entry);
        log.info("Audit entry soft-deleted: {} by {} reason: {}", id, userId, reason);
    }

    /**
     * Export audit entries to CSV/Excel for compliance reporting.
     */
    @Transactional(readOnly = true)
    public byte[] exportEntries(AuditSearchRequest request, String format) {
        log.info("Exporting audit entries: format={}, request={}", format, request);

        Pageable pageable = PageRequest.of(0, 100_000); // Max 100k records
        Page<AuditEntry> page = repository.search(
            request.userId(),
            request.username(),
            request.action(),
            request.entityType(),
            request.entityId(),
            request.result() != null ? AuditResult.valueOf(request.result()) : null,
            request.fromDate(),
            request.toDate(),
            pageable
        );

        if ("CSV".equalsIgnoreCase(format)) {
            return toCsv(page.getContent());
        } else if ("JSON".equalsIgnoreCase(format)) {
            try {
                return objectMapper.writeValueAsBytes(page.getContent().stream()
                    .map(AuditEntryDto::from)
                    .toList());
            } catch (Exception e) {
                throw new BusinessException("EXPORT_FAILED", "Failed to export: " + e.getMessage());
            }
        }
        throw new BusinessException("UNSUPPORTED_FORMAT", "Format not supported: " + format);
    }

    private byte[] toCsv(List<AuditEntry> entries) {
        StringBuilder sb = new StringBuilder();
        sb.append("ID,Timestamp,UserId,Username,Action,EntityType,EntityId,Result,IPAddress,CorrelationId\n");
        for (AuditEntry e : entries) {
            sb.append(e.getId()).append(",")
              .append(e.getTimestamp()).append(",")
              .append(escape(e.getUserId())).append(",")
              .append(escape(e.getUsername())).append(",")
              .append(escape(e.getAction())).append(",")
              .append(escape(e.getEntityType())).append(",")
              .append(escape(e.getEntityId())).append(",")
              .append(e.getResult()).append(",")
              .append(escape(e.getIpAddress())).append(",")
              .append(escape(e.getCorrelationId())).append("\n");
        }
        return sb.toString().getBytes();
    }

    private String escape(String s) {
        if (s == null) return "";
        if (s.contains(",") || s.contains("\"") || s.contains("\n")) {
            return "\"" + s.replace("\"", "\"\"") + "\"";
        }
        return s;
    }
}
