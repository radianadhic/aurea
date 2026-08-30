package com.bankxyz.mdm.workflow.event;

import com.bankxyz.mdm.workflow.domain.WorkflowTask;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

@Component
@RequiredArgsConstructor
@Slf4j
public class WorkflowEventPublisher {

    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Value("${mdm.kafka.topics.workflow:mdm.workflow.events}")
    private String topic;

    public void publishTaskCreated(WorkflowTask t) {
        publish("task.created", Map.of(
            "taskId", t.getId(),
            "name", t.getName(),
            "assigneeId", t.getAssigneeId() != null ? t.getAssigneeId() : "",
            "requesterId", t.getRequesterId() != null ? t.getRequesterId() : "",
            "entityType", t.getEntityType() != null ? t.getEntityType() : "",
            "entityId", t.getEntityId() != null ? t.getEntityId() : "",
            "priority", t.getPriority().name()
        ));
    }

    public void publishTaskClaimed(WorkflowTask t) {
        publish("task.claimed", Map.of(
            "taskId", t.getId(),
            "assigneeId", t.getAssigneeId() != null ? t.getAssigneeId() : ""
        ));
    }

    public void publishTaskCompleted(WorkflowTask t, boolean approved) {
        publish(approved ? "task.approved" : "task.rejected", Map.of(
            "taskId", t.getId(),
            "approverId", t.getApproverId() != null ? t.getApproverId() : "",
            "approved", approved,
            "notes", t.getCompletionNotes() != null ? t.getCompletionNotes() : ""
        ));
    }

    public void publishTaskReassigned(WorkflowTask t) {
        publish("task.reassigned", Map.of(
            "taskId", t.getId(),
            "newAssigneeId", t.getAssigneeId() != null ? t.getAssigneeId() : ""
        ));
    }

    public void publishTaskCancelled(WorkflowTask t) {
        publish("task.cancelled", Map.of(
            "taskId", t.getId(),
            "reason", t.getCompletionNotes() != null ? t.getCompletionNotes() : ""
        ));
    }

    public void publishTaskExpired(WorkflowTask t) {
        publish("task.expired", Map.of(
            "taskId", t.getId(),
            "dueDate", t.getDueDate() != null ? t.getDueDate().toString() : ""
        ));
    }

    private void publish(String eventType, Map<String, Object> payload) {
        try {
            var event = Map.of(
                "eventType", eventType,
                "timestamp", Instant.now().toString(),
                "payload", payload
            );
            kafkaTemplate.send(topic, eventType, event);
            log.debug("Published workflow event: {}", eventType);
        } catch (Exception e) {
            log.error("Failed to publish workflow event: {}", eventType, e);
        }
    }
}
