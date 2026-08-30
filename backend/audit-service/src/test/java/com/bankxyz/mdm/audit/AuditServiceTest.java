package com.bankxyz.mdm.audit;

import com.bankxyz.mdm.audit.domain.AuditEntry;
import com.bankxyz.mdm.audit.domain.AuditResult;
import com.bankxyz.mdm.audit.dto.AuditDtos;
import com.bankxyz.mdm.audit.repository.AuditEntryRepository;
import com.bankxyz.mdm.audit.service.AuditService;
import com.bankxyz.mdm.common.dto.PageResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class AuditServiceTest {

    @Mock
    private AuditEntryRepository repository;

    @InjectMocks
    private AuditService auditService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    @DisplayName("Record creates and saves audit entry")
    void testRecord() {
        AuditEntry entry = AuditEntry.builder()
            .action("CUSTOMER_UPDATE")
            .entityType("Customer")
            .entityId("CIF-001")
            .username("test.user")
            .result(AuditResult.SUCCESS)
            .build();

        auditService.record(entry);

        ArgumentCaptor<AuditEntry> captor = ArgumentCaptor.forClass(AuditEntry.class);
        verify(repository, times(1)).save(captor.capture());
        assertEquals("CUSTOMER_UPDATE", captor.getValue().getAction());
        assertNotNull(captor.getValue().getTimestamp());
    }

    @Test
    @DisplayName("Record from event maps fields correctly")
    void testRecordFromEvent() {
        AuditDtos.AuditEventDto event = new AuditDtos.AuditEventDto(
            Instant.now(), "U-001", "test.user", "Test User", "STEWARD_CIF",
            "CUSTOMER_UPDATE", "Customer", "CIF-001", "10.20.30.40", "Mozilla/5.0",
            "corr-123", "sess-abc", "customer-service", "SUCCESS", null,
            Map.of("field", "value"), Map.of("key", "val")
        );

        auditService.recordFromEvent(event);

        ArgumentCaptor<AuditEntry> captor = ArgumentCaptor.forClass(AuditEntry.class);
        verify(repository).save(captor.capture());
        AuditEntry saved = captor.getValue();
        assertEquals("CUSTOMER_UPDATE", saved.getAction());
        assertEquals("CIF-001", saved.getEntityId());
        assertEquals(AuditResult.SUCCESS, saved.getResult());
        assertEquals("test.user", saved.getUsername());
    }

    @Test
    @DisplayName("Search returns paginated results")
    void testSearch() {
        AuditEntry entry = AuditEntry.builder()
            .id(UUID.randomUUID())
            .timestamp(Instant.now())
            .action("TEST")
            .entityType("Test")
            .username("test")
            .result(AuditResult.SUCCESS)
            .build();
        Page<AuditEntry> page = new PageImpl<>(List.of(entry), PageRequest.of(0, 20), 1);

        when(repository.search(any(), any(), any(), any(), any(), any(), any(), any(), any(Pageable.class)))
            .thenReturn(page);

        PageResponse<AuditDtos.AuditEntryDto> result = auditService.search(
            new AuditDtos.AuditSearchRequest(null, null, null, null, null, null, null, null, 0, 20));

        assertEquals(1, result.content().size());
        assertEquals(1L, result.totalElements());
    }

    @Test
    @DisplayName("Soft delete marks entry as deleted with reason")
    void testSoftDelete() {
        UUID id = UUID.randomUUID();
        AuditEntry entry = AuditEntry.builder()
            .id(id)
            .action("TEST")
            .entityType("Test")
            .result(AuditResult.SUCCESS)
            .build();
        when(repository.findById(id)).thenReturn(java.util.Optional.of(entry));

        auditService.softDelete(id, "compliance.officer", "GDPR request");

        ArgumentCaptor<AuditEntry> captor = ArgumentCaptor.forClass(AuditEntry.class);
        verify(repository).save(captor.capture());
        assertNotNull(captor.getValue().getDeletedAt());
        assertEquals("compliance.officer", captor.getValue().getDeletedBy());
        assertEquals("GDPR request", captor.getValue().getDeletionReason());
    }

    @Test
    @DisplayName("Cannot soft delete already deleted entry")
    void testDoubleSoftDelete() {
        UUID id = UUID.randomUUID();
        AuditEntry entry = AuditEntry.builder()
            .id(id)
            .deletedAt(Instant.now())
            .deletedBy("someone")
            .build();
        when(repository.findById(id)).thenReturn(java.util.Optional.of(entry));

        assertThrows(
            com.bankxyz.mdm.common.exception.BusinessException.class,
            () -> auditService.softDelete(id, "user", "reason")
        );
    }

    @Test
    @DisplayName("Export to CSV produces valid CSV")
    void testExportCsv() {
        AuditEntry entry = AuditEntry.builder()
            .id(UUID.randomUUID())
            .timestamp(Instant.now())
            .action("CUSTOMER_UPDATE")
            .entityType("Customer")
            .entityId("CIF-001")
            .username("test,user") // contains comma
            .result(AuditResult.SUCCESS)
            .ipAddress("10.20.30.40")
            .build();
        Page<AuditEntry> page = new PageImpl<>(List.of(entry), PageRequest.of(0, 100), 1);
        when(repository.search(any(), any(), any(), any(), any(), any(), any(), any(), any(Pageable.class)))
            .thenReturn(page);

        byte[] csv = auditService.exportEntries(
            new AuditDtos.AuditSearchRequest(null, null, null, null, null, null, null, null, 0, 100),
            "CSV"
        );

        String csvStr = new String(csv);
        assertTrue(csvStr.contains("Action,EntityType"));
        assertTrue(csvStr.contains("CUSTOMER_UPDATE"));
        assertTrue(csvStr.contains("\"test,user\"")); // properly escaped
    }
}
