package com.bankxyz.mdm.workflow.service;

import com.bankxyz.mdm.common.dto.PageResponse;
import com.bankxyz.mdm.common.exception.BusinessException;
import com.bankxyz.mdm.common.exception.ResourceNotFoundException;
import com.bankxyz.mdm.workflow.domain.TaskPriority;
import com.bankxyz.mdm.workflow.domain.TaskStatus;
import com.bankxyz.mdm.workflow.domain.WorkflowTask;
import com.bankxyz.mdm.workflow.dto.*;
import com.bankxyz.mdm.workflow.repository.WorkflowTaskRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Duration;
import java.time.Instant;
import java.util.*;

@Service
@RequiredArgsConstructor
@Slf4j
public class WorkflowService {

    private final WorkflowTaskRepository taskRepository;
    private final WorkflowEventPublisher eventPublisher;

    /**
     * Create a new task (e.g. approval request, manual review).
     */
    @Transactional
    public WorkflowTaskDto createTask(CreateTaskRequest request) {
        log.info("Creating task: {} for entity {}:{}",
            request.name(), request.entityType(), request.entityId());

        WorkflowTask task = WorkflowTask.builder()
            .name(request.name())
            .description(request.description())
            .status(TaskStatus.OPEN)
            .assigneeId(request.assigneeId())
            .assigneeName(request.assigneeName())
            .requesterId(request.requesterId())
            .requesterName(request.requesterName())
            .entityType(request.entityType())
            .entityId(request.entityId())
            .candidateGroup(request.candidateGroup())
            .priority(request.priority() != null ? request.priority() : TaskPriority.NORMAL)
            .dueDate(request.dueDate())
            .variables(request.variables() != null ? request.variables() : new HashMap<>())
            .build();

        WorkflowTask saved = taskRepository.save(task);
        eventPublisher.publishTaskCreated(saved);
        return WorkflowTaskDto.from(saved);
    }

    /**
     * Claim a task (assign to current user).
     */
    @Transactional
    public WorkflowTaskDto claimTask(UUID taskId, String userId, String userName) {
        WorkflowTask task = taskRepository.findById(taskId)
            .orElseThrow(() -> new ResourceNotFoundException("Task not found: " + taskId));

        if (task.getStatus() != TaskStatus.OPEN && task.getStatus() != TaskStatus.CLAIMED) {
            throw new BusinessException("INVALID_STATUS",
                "Task is in status " + task.getStatus() + " and cannot be claimed");
        }

        task.setAssigneeId(userId);
        task.setAssigneeName(userName);
        task.setStatus(TaskStatus.CLAIMED);
        task.setClaimedAt(Instant.now());

        WorkflowTask saved = taskRepository.save(task);
        eventPublisher.publishTaskClaimed(saved);
        return WorkflowTaskDto.from(saved);
    }

    /**
     * Complete a task with 4-eyes validation.
     */
    @Transactional
    public WorkflowTaskDto completeTask(UUID taskId, CompleteTaskRequest request) {
        WorkflowTask task = taskRepository.findById(taskId)
            .orElseThrow(() -> new ResourceNotFoundException("Task not found: " + taskId));

        if (task.getStatus() == TaskStatus.COMPLETED || task.getStatus() == TaskStatus.CANCELLED) {
            throw new BusinessException("ALREADY_COMPLETED",
                "Task already " + task.getStatus());
        }

        // 4-eyes principle: requester cannot approve their own request
        if (task.getRequesterId() != null
            && task.getRequesterId().equals(request.userId())) {
            throw new BusinessException("FOUR_EYES_VIOLATION",
                "Requester cannot approve their own request (4-eyes principle). Approver must be different user.");
        }

        task.setApproverId(request.userId());
        task.setApproverName(request.userName());
        task.setCompletionNotes(request.notes());
        task.setCompletedAt(Instant.now());
        task.setStatus(request.approved() ? TaskStatus.COMPLETED : TaskStatus.REJECTED);

        WorkflowTask saved = taskRepository.save(task);
        eventPublisher.publishTaskCompleted(saved, request.approved());
        return WorkflowTaskDto.from(saved);
    }

    /**
     * Reassign a task to a different user.
     */
    @Transactional
    public WorkflowTaskDto reassignTask(UUID taskId, ReassignTaskRequest request) {
        WorkflowTask task = taskRepository.findById(taskId)
            .orElseThrow(() -> new ResourceNotFoundException("Task not found: " + taskId));

        if (task.getStatus() == TaskStatus.COMPLETED || task.getStatus() == TaskStatus.CANCELLED) {
            throw new BusinessException("ALREADY_COMPLETED", "Task already completed");
        }

        task.setAssigneeId(request.newAssigneeId());
        task.setAssigneeName(request.newAssigneeName());
        task.setStatus(TaskStatus.OPEN); // back to open for the new assignee to claim

        WorkflowTask saved = taskRepository.save(task);
        eventPublisher.publishTaskReassigned(saved);
        return WorkflowTaskDto.from(saved);
    }

    /**
     * Cancel a task.
     */
    @Transactional
    public WorkflowTaskDto cancelTask(UUID taskId, String reason) {
        WorkflowTask task = taskRepository.findById(taskId)
            .orElseThrow(() -> new ResourceNotFoundException("Task not found: " + taskId));
        task.setStatus(TaskStatus.CANCELLED);
        task.setCompletionNotes("Cancelled: " + reason);
        task.setCompletedAt(Instant.now());
        WorkflowTask saved = taskRepository.save(task);
        eventPublisher.publishTaskCancelled(saved);
        return WorkflowTaskDto.from(saved);
    }

    /**
     * Get task by ID.
     */
    @Transactional(readOnly = true)
    public WorkflowTaskDto getById(UUID id) {
        WorkflowTask task = taskRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Task not found: " + id));
        return WorkflowTaskDto.from(task);
    }

    /**
     * Search tasks.
     */
    @Transactional(readOnly = true)
    public PageResponse<WorkflowTaskDto> search(TaskSearchRequest request) {
        Pageable pageable = PageRequest.of(
            request.page() != null ? request.page() : 0,
            request.size() != null ? request.size() : 20);
        Page<WorkflowTask> page = taskRepository.search(
            request.assigneeId(),
            request.status(),
            request.entityType(),
            request.entityId(),
            request.priority(),
            request.requesterId(),
            request.onlyOverdue() != null && request.onlyOverdue(),
            pageable);
        List<WorkflowTaskDto> content = page.getContent().stream()
            .map(WorkflowTaskDto::from).toList();
        return PageResponse.<WorkflowTaskDto>builder()
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

    /**
     * Get my tasks (assigneeId = current user).
     */
    @Transactional(readOnly = true)
    public List<WorkflowTaskDto> getMyTasks(String userId, boolean includeCompleted) {
        return taskRepository.findByAssigneeIdAndStatusInOrderByPriorityDesc(
            userId,
            includeCompleted
                ? List.of(TaskStatus.OPEN, TaskStatus.CLAIMED, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED)
                : List.of(TaskStatus.OPEN, TaskStatus.CLAIMED, TaskStatus.IN_PROGRESS)
        ).stream().map(WorkflowTaskDto::from).toList();
    }

    /**
     * Get workflow statistics.
     */
    @Transactional(readOnly = true)
    public WorkflowStatsResponse getStats() {
        long total = taskRepository.count();
        long open = taskRepository.countByStatus(TaskStatus.OPEN);
        long claimed = taskRepository.countByStatus(TaskStatus.CLAIMED);
        long completed = taskRepository.countByStatus(TaskStatus.COMPLETED);
        long overdue = taskRepository.findOverdueTasks(Instant.now()).size();
        return new WorkflowStatsResponse(total, open, claimed, completed, overdue);
    }

    /**
     * Auto-expire overdue tasks (scheduled job).
     */
    @org.springframework.scheduling.annotation.Scheduled(fixedDelay = 300000) // every 5 min
    @Transactional
    public void expireOverdueTasks() {
        List<WorkflowTask> overdue = taskRepository.findOverdueTasks(Instant.now());
        for (WorkflowTask task : overdue) {
            task.setStatus(TaskStatus.EXPIRED);
            taskRepository.save(task);
            eventPublisher.publishTaskExpired(task);
        }
        if (!overdue.isEmpty()) {
            log.info("Expired {} overdue tasks", overdue.size());
        }
    }
}
