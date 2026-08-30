package com.bankxyz.mdm.workflow.controller;

import com.bankxyz.mdm.common.dto.PageResponse;
import com.bankxyz.mdm.common.security.JwtAuthContext;
import com.bankxyz.mdm.workflow.dto.WorkflowDtos.*;
import com.bankxyz.mdm.workflow.service.WorkflowService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/workflow")
@RequiredArgsConstructor
@Tag(name = "Workflow", description = "Task management with 4-eyes approval")
public class WorkflowController {

    private final WorkflowService workflowService;
    private final JwtAuthContext authContext;

    @PostMapping("/tasks")
    @PreAuthorize("hasAnyAuthority('workflow:write', 'admin:config:write')")
    @Operation(summary = "Create a new task")
    public WorkflowTaskDto createTask(@Valid @RequestBody CreateTaskRequest request) {
        return workflowService.createTask(request);
    }

    @PostMapping("/tasks/{id}/claim")
    @PreAuthorize("isAuthenticated()")
    @Operation(summary = "Claim a task")
    public WorkflowTaskDto claimTask(@PathVariable UUID id) {
        return workflowService.claimTask(id, authContext.getUserId(), authContext.getFullName());
    }

    @PostMapping("/tasks/{id}/complete")
    @PreAuthorize("isAuthenticated()")
    @Operation(summary = "Complete a task (4-eyes enforced)")
    public WorkflowTaskDto completeTask(@PathVariable UUID id, @Valid @RequestBody CompleteTaskRequest request) {
        return workflowService.completeTask(id, request);
    }

    @PostMapping("/tasks/{id}/reassign")
    @PreAuthorize("hasAnyAuthority('workflow:write')")
    @Operation(summary = "Reassign a task")
    public WorkflowTaskDto reassignTask(@PathVariable UUID id, @Valid @RequestBody ReassignTaskRequest request) {
        return workflowService.reassignTask(id, request);
    }

    @PostMapping("/tasks/{id}/cancel")
    @PreAuthorize("hasAnyAuthority('workflow:write')")
    @Operation(summary = "Cancel a task")
    public WorkflowTaskDto cancelTask(@PathVariable UUID id, @RequestParam String reason) {
        return workflowService.cancelTask(id, reason);
    }

    @GetMapping("/tasks/{id}")
    @PreAuthorize("hasAnyAuthority('workflow:read', 'workflow:write')")
    @Operation(summary = "Get task by ID")
    public WorkflowTaskDto getById(@PathVariable UUID id) {
        return workflowService.getById(id);
    }

    @PostMapping("/tasks/search")
    @PreAuthorize("hasAnyAuthority('workflow:read', 'workflow:write')")
    @Operation(summary = "Search tasks")
    public PageResponse<WorkflowTaskDto> search(@RequestBody TaskSearchRequest request) {
        return workflowService.search(request);
    }

    @GetMapping("/tasks/my")
    @PreAuthorize("isAuthenticated()")
    @Operation(summary = "Get my tasks")
    public List<WorkflowTaskDto> getMyTasks(@RequestParam(defaultValue = "false") boolean includeCompleted) {
        return workflowService.getMyTasks(authContext.getUserId(), includeCompleted);
    }

    @GetMapping("/stats")
    @PreAuthorize("hasAnyAuthority('workflow:read', 'admin:config:read')")
    @Operation(summary = "Get workflow statistics")
    public WorkflowStatsResponse getStats() {
        return workflowService.getStats();
    }
}
