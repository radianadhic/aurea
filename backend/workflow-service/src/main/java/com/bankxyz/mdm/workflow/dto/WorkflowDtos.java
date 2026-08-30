package com.bankxyz.mdm.workflow.dto;

import com.bankxyz.mdm.workflow.domain.TaskPriority;
import com.bankxyz.mdm.workflow.domain.TaskStatus;
import com.bankxyz.mdm.workflow.domain.WorkflowTask;
import jakarta.validation.constraints.*;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class WorkflowDtos {

    public record WorkflowTaskDto(
        UUID id,
        String processInstanceId,
        String processDefinitionKey,
        String taskDefinitionKey,
        String name,
        String description,
        TaskStatus status,
        String assigneeId,
        String assigneeName,
        String requesterId,
        String requesterName,
        String entityType,
        String entityId,
        String candidateGroup,
        TaskPriority priority,
        Instant dueDate,
        Instant claimedAt,
        Instant completedAt,
        String completionNotes,
        String approverId,
        String approverName,
        Map<String, Object> variables,
        boolean overdue,
        boolean needsFourEyesApproval,
        Instant createdAt,
        Instant updatedAt
    ) {
        public static WorkflowTaskDto from(WorkflowTask t) {
            boolean overdue = t.getDueDate() != null
                && t.getDueDate().isBefore(Instant.now())
                && t.getStatus() == TaskStatus.OPEN;
            boolean needsApproval = t.getRequesterId() != null
                && t.getAssigneeId() != null
                && !t.getRequesterId().equals(t.getAssigneeId());
            return new WorkflowTaskDto(
                t.getId(), t.getProcessInstanceId(), t.getProcessDefinitionKey(),
                t.getTaskDefinitionKey(), t.getName(), t.getDescription(),
                t.getStatus(), t.getAssigneeId(), t.getAssigneeName(),
                t.getRequesterId(), t.getRequesterName(),
                t.getEntityType(), t.getEntityId(), t.getCandidateGroup(),
                t.getPriority(), t.getDueDate(), t.getClaimedAt(), t.getCompletedAt(),
                t.getCompletionNotes(), t.getApproverId(), t.getApproverName(),
                t.getVariables(), overdue, needsApproval,
                t.getCreatedAt(), t.getUpdatedAt()
            );
        }
    }

    public record CreateTaskRequest(
        @NotBlank @Size(max = 200) String name,
        @Size(max = 1000) String description,
        String assigneeId,
        String assigneeName,
        String requesterId,
        String requesterName,
        String entityType,
        String entityId,
        String candidateGroup,
        TaskPriority priority,
        Instant dueDate,
        Map<String, Object> variables
    ) {
        public CreateTaskRequest {
            if (variables == null) variables = new HashMap<>();
            if (priority == null) priority = TaskPriority.NORMAL;
        }
    }

    public record CompleteTaskRequest(
        @NotBlank String userId,
        @NotBlank String userName,
        boolean approved,
        @Size(max = 2000) String notes
    ) {}

    public record ReassignTaskRequest(
        @NotBlank String newAssigneeId,
        @NotBlank String newAssigneeName,
        String reason
    ) {}

    public record TaskSearchRequest(
        String assigneeId,
        TaskStatus status,
        String entityType,
        String entityId,
        TaskPriority priority,
        String requesterId,
        Boolean onlyOverdue,
        Integer page,
        Integer size
    ) {}

    public record WorkflowStatsResponse(
        long totalTasks,
        long open,
        long claimed,
        long completed,
        long overdue
    ) {}
}
