package com.bankxyz.mdm.audit.repository;

import com.bankxyz.mdm.audit.domain.AuditEntry;
import com.bankxyz.mdm.audit.domain.AuditResult;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

@Repository
public interface AuditEntryRepository extends JpaRepository<AuditEntry, UUID> {

    @Query("""
        SELECT a FROM AuditEntry a
        WHERE a.deletedAt IS NULL
          AND (:userId IS NULL OR a.userId = :userId)
          AND (:username IS NULL OR LOWER(a.username) LIKE LOWER(CONCAT('%', :username, '%')))
          AND (:action IS NULL OR a.action = :action)
          AND (:entityType IS NULL OR a.entityType = :entityType)
          AND (:entityId IS NULL OR a.entityId = :entityId)
          AND (:result IS NULL OR a.result = :result)
          AND (:fromDate IS NULL OR a.timestamp >= :fromDate)
          AND (:toDate IS NULL OR a.timestamp <= :toDate)
        """)
    Page<AuditEntry> search(
        @Param("userId") String userId,
        @Param("username") String username,
        @Param("action") String action,
        @Param("entityType") String entityType,
        @Param("entityId") String entityId,
        @Param("result") AuditResult result,
        @Param("fromDate") Instant fromDate,
        @Param("toDate") Instant toDate,
        Pageable pageable
    );

    List<AuditEntry> findByCorrelationId(String correlationId);

    List<AuditEntry> findByEntityTypeAndEntityId(String entityType, String entityId);

    @Query("""
        SELECT a.action, COUNT(a) FROM AuditEntry a
        WHERE a.deletedAt IS NULL
          AND a.timestamp >= :since
        GROUP BY a.action
        ORDER BY COUNT(a) DESC
        """)
    List<Object[]> countByActionSince(@Param("since") Instant since);

    @Query("""
        SELECT a.userId, a.username, COUNT(a) FROM AuditEntry a
        WHERE a.deletedAt IS NULL
          AND a.timestamp >= :since
        GROUP BY a.userId, a.username
        ORDER BY COUNT(a) DESC
        """)
    List<Object[]> countByUserSince(@Param("since") Instant since);

    @Query("""
        SELECT a.result, COUNT(a) FROM AuditEntry a
        WHERE a.deletedAt IS NULL
          AND a.timestamp >= :since
        GROUP BY a.result
        """)
    List<Object[]> countByResultSince(@Param("since") Instant since);
}
