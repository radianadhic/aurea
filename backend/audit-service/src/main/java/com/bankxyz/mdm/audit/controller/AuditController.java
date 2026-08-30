package com.bankxyz.mdm.audit.controller;

import com.bankxyz.mdm.audit.dto.AuditDtos.*;
import com.bankxyz.mdm.audit.service.AuditService;
import com.bankxyz.mdm.common.dto.PageResponse;
import com.bankxyz.mdm.common.security.JwtAuthContext;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/audit")
@RequiredArgsConstructor
@Tag(name = "Audit Trail", description = "Immutable audit log for compliance")
public class AuditController {

    private final AuditService auditService;
    private final JwtAuthContext authContext;

    @PostMapping("/search")
    @PreAuthorize("hasAnyAuthority('audit:read', 'admin:config:read')")
    @Operation(summary = "Search audit entries")
    public PageResponse<AuditEntryDto> search(@RequestBody AuditSearchRequest request) {
        return auditService.search(request);
    }

    @GetMapping("/entries/{id}")
    @PreAuthorize("hasAnyAuthority('audit:read')")
    @Operation(summary = "Get audit entry by ID")
    public AuditEntryDto getById(@PathVariable UUID id) {
        return auditService.getById(id);
    }

    @GetMapping("/entities/{entityType}/{entityId}")
    @PreAuthorize("hasAnyAuthority('audit:read')")
    @Operation(summary = "Get all audit entries for an entity")
    public List<AuditEntryDto> getByEntity(
        @PathVariable String entityType,
        @PathVariable String entityId
    ) {
        return auditService.getByEntity(entityType, entityId);
    }

    @PostMapping("/record")
    @PreAuthorize("isAuthenticated()")
    @Operation(summary = "Record a new audit entry")
    public ResponseEntity<Void> record(@Valid @RequestBody CreateAuditRequest request) {
        auditService.record(AuditDtos_AuditEntryBuilder.build(request, authContext));
        return ResponseEntity.accepted().build();
    }

    @PostMapping("/entries/{id}/soft-delete")
    @PreAuthorize("hasAuthority('audit:delete')")
    @Operation(summary = "Soft-delete audit entry (compliance)")
    public ResponseEntity<Void> softDelete(
        @PathVariable UUID id,
        @RequestParam String reason
    ) {
        auditService.softDelete(id, authContext.getUserId(), reason);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/export")
    @PreAuthorize("hasAuthority('audit:export')")
    @Operation(summary = "Export audit entries")
    public ResponseEntity<byte[]> export(@RequestBody ExportRequest request) {
        byte[] data = auditService.exportEntries(request.filter(), request.format());
        HttpHeaders headers = new HttpHeaders();
        headers.setContentDispositionFormData("attachment",
            "audit-export-" + System.currentTimeMillis() + "." + request.format().toLowerCase());
        if ("CSV".equalsIgnoreCase(request.format())) {
            return ResponseEntity.ok().headers(headers)
                .contentType(MediaType.parseMediaType("text/csv"))
                .body(data);
        }
        return ResponseEntity.ok().headers(headers)
            .contentType(MediaType.APPLICATION_JSON)
            .body(data);
    }

    @GetMapping("/stats")
    @PreAuthorize("hasAnyAuthority('audit:read', 'admin:config:read')")
    @Operation(summary = "Get audit statistics")
    public AuditStatsResponse getStats() {
        return auditService.getStats();
    }
}
