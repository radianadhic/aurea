package com.bankxyz.mdm.workflow.domain;

import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "workflow_tasks", indexes = {
    @Index(name = "idx_task_assignee", columnList = "assignee_id"),
    @Index(name = "idx_task_status", columnList = "status"),
    @Index(name = "idx_task_process", columnList = "process_instance_id"),
    @Index(name = "idx_task_entity", columnList = "entity_type, entity_id"),
    @Index(name = "idx_task_due", columnList = "due_date")
})
@EntityListeners(AuditingEntityListener.class)
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class WorkflowTask {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "process_instance_id", length = 100)
    private String processInstanceId;

    @Column(name = "process_definition_key", length = 100)
    private String processDefinitionKey;

    @Column(name = "task_definition_key", length = 100)
    private String taskDefinitionKey;

    @Column(name = "name", nullable = false, length = 200)
    private String name;

    @Column(name = "description", length = 1000)
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 20)
    @Builder.Default
    private TaskStatus status = TaskStatus.OPEN;

    /** Who needs to action this */
    @Column(name = "assignee_id", length = 50)
    private String assigneeId;

    @Column(name = "assignee_name", length = 200)
    private String assigneeName;

    /** Original requester (for 4-eyes principle) */
    @Column(name = "requester_id", length = 50)
    private String requesterId;

    @Column(name = "requester_name", length = 200)
    private String requesterName;

    /** Entity this task relates to */
    @Column(name = "entity_type", length = 50)
    private String entityType;

    @Column(name = "entity_id", length = 100)
    private String entityId;

    @Column(name = "candidate_group", length = 100)
    private String candidateGroup;

    @Enumerated(EnumType.STRING)
    @Column(name = "priority", length = 20)
    @Builder.Default
    private TaskPriority priority = TaskPriority.NORMAL;

    @Column(name = "due_date")
    private Instant dueDate;

    @Column(name = "claimed_at")
    private Instant claimedAt;

    @Column(name = "completed_at")
    private Instant completedAt;

    @Column(name = "completion_notes", length = 2000)
    private String completionNotes;

    /** 4-eyes: ID of approver (must be != requester) */
    @Column(name = "approver_id", length = 50)
    private String approverId;

    @Column(name = "approver_name", length = 200)
    private String approverName;

    @jakarta.persistence.Convert(converter = JsonStringConverter.class)
    @Column(name = "variables", columnDefinition = "TEXT")
    @Builder.Default
    private Map<String, Object> variables = new HashMap<>();

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @LastModifiedDate
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    @Column(name = "deleted_at")
    private Instant deletedAt;

    public boolean isOverdue() {
        return dueDate != null && dueDate.isBefore(Instant.now()) && status == TaskStatus.OPEN;
    }

    public boolean needsFourEyesApproval() {
        return requesterId != null && assigneeId != null && !requesterId.equals(assigneeId);
    }
}
