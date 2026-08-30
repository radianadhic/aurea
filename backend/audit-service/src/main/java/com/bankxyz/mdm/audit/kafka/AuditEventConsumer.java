package com.bankxyz.mdm.audit.kafka;

import com.bankxyz.mdm.audit.dto.AuditDtos;
import com.bankxyz.mdm.audit.service.AuditService;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * Listens to all MDM events from Kafka and converts them to audit entries.
 *
 * Subscribed topics:
 *   - mdm.customer.events
 *   - mdm.match.events
 *   - mdm.kyc.events
 *   - mdm.workflow.events
 *   - mdm.notification.events
 *   - mdm.admin.events
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class AuditEventConsumer {

    private final AuditService auditService;
    private final ObjectMapper objectMapper;

    @KafkaListener(
        topics = {
            "${mdm.kafka.topics.customer:mdm.customer.events}",
            "${mdm.kafka.topics.match:mdm.match.events}",
            "${mdm.kafka.topics.kyc:mdm.kyc.events}",
            "${mdm.kafka.topics.workflow:mdm.workflow.events}",
            "${mdm.kafka.topics.notification:mdm.notification.events}",
            "${mdm.kafka.topics.admin:mdm.admin.events}"
        },
        groupId = "audit-service",
        containerFactory = "kafkaListenerContainerFactory"
    )
    public void onEvent(Map<String, Object> event) {
        try {
            log.debug("Received event for audit: {}", event);

            AuditDtos.AuditEventDto eventDto = objectMapper.convertValue(event, AuditDtos.AuditEventDto.class);
            auditService.recordFromEvent(eventDto);
        } catch (Exception e) {
            log.error("Failed to process audit event: {}", e.getMessage(), e);
        }
    }
}
