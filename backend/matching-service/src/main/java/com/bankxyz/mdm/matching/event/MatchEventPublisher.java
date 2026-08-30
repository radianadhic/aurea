package com.bankxyz.mdm.matching.event;

import com.bankxyz.mdm.matching.domain.MatchGroup;
import com.bankxyz.mdm.matching.dto.MatchRequests;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.List;
import java.util.Map;

/**
 * Publishes match-related events to Kafka.
 * Topics: match.assigned, match.merged, match.rejected, match.escalated
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class MatchEventPublisher {

    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Value("${mdm.kafka.topics.match:mdm.match.events}")
    private String matchTopic;

    public void publishAssigned(MatchGroup group) {
        publish("match.assigned", Map.of(
            "matchGroupId", group.getId(),
            "reviewerId", group.getReviewerId() != null ? group.getReviewerId() : "",
            "status", group.getStatus().name()
        ));
    }

    public void publishMerge(MatchGroup group, String primaryId, List<String> secondaryIds) {
        publish("match.merged", Map.of(
            "matchGroupId", group.getId(),
            "primaryCustomerId", primaryId,
            "secondaryCustomerIds", secondaryIds,
            "status", group.getStatus().name(),
            "mergedAt", Instant.now().toString()
        ));
    }

    public void publishRejected(MatchGroup group) {
        publish("match.rejected", Map.of(
            "matchGroupId", group.getId(),
            "reason", group.getRejectionReason() != null ? group.getRejectionReason() : ""
        ));
    }

    public void publishEscalated(MatchGroup group) {
        publish("match.escalated", Map.of(
            "matchGroupId", group.getId(),
            "assignedTo", group.getReviewerId() != null ? group.getReviewerId() : "",
            "reason", group.getResolutionNotes() != null ? group.getResolutionNotes() : ""
        ));
    }

    private void publish(String eventType, Map<String, Object> payload) {
        try {
            var event = Map.of(
                "eventType", eventType,
                "timestamp", Instant.now().toString(),
                "payload", payload
            );
            kafkaTemplate.send(matchTopic, eventType, event);
            log.debug("Published event: {}", eventType);
        } catch (Exception e) {
            log.error("Failed to publish event: {}", eventType, e);
        }
    }
}
