package com.bankxyz.mdm.workflow.repository;

import com.bankxyz.mdm.common.repository.BaseRepository;
import com.bankxyz.mdm.workflow.domain.TaskPriority;
import com.bankxyz.mdm.workflow.domain.TaskStatus;
import com.bankxyz.mdm.workflow.domain.WorkflowTask;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

@Repository
public interface WorkflowTaskRepository extends BaseRepository<WorkflowTask, UUID> {

    @Query("""
        SELECT t FROM WorkflowTask t
        WHERE (:assigneeId IS NULL OR t.assigneeId = :assigneeId)
          AND (:status IS NULL OR t.status = :status)
          AND (:entityType IS NULL OR t.entityType = :entityType)
          AND (:entityId IS NULL OR t.entityId = :entityId)
          AND (:priority IS NULL OR t.priority = :priority)
          AND (:requesterId IS NULL OR t.requesterId = :requesterId)
          AND (:onlyOverdue = false OR (t.dueDate IS NOT NULL AND t.dueDate < :now AND t.status = 'OPEN'))
          AND t.deletedAt IS NULL
        """)
    Page<WorkflowTask> search(
        @Param("assigneeId") String assigneeId,
        @Param("status") TaskStatus status,
        @Param("entityType") String entityType,
        @Param("entityId") String entityId,
        @Param("priority") TaskPriority priority,
        @Param("requesterId") String requesterId,
        @Param("onlyOverdue") boolean onlyOverdue,
        Pageable pageable
    );

    List<WorkflowTask> findByAssigneeIdAndStatusInOrderByPriorityDesc(String assigneeId, List<TaskStatus> statuses);

    @Query("SELECT t FROM WorkflowTask t WHERE t.dueDate IS NOT NULL AND t.dueDate < :now AND t.status = 'OPEN' AND t.deletedAt IS NULL")
    List<WorkflowTask> findOverdueTasks(@Param("now") Instant now);

    long countByStatus(TaskStatus status);

    long countByAssigneeIdAndStatus(String assigneeId, TaskStatus status);
}
