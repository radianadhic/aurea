package com.bankxyz.mdm.notification.repository;

import com.bankxyz.mdm.common.repository.BaseRepository;
import com.bankxyz.mdm.notification.domain.Notification;
import com.bankxyz.mdm.notification.domain.NotificationChannel;
import com.bankxyz.mdm.notification.domain.NotificationStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

@Repository
public interface NotificationRepository extends BaseRepository<Notification, UUID> {

    @Query("""
        SELECT n FROM Notification n
        WHERE (:recipientId IS NULL OR n.recipientId = :recipientId)
          AND (:channel IS NULL OR n.channel = :channel)
          AND (:status IS NULL OR n.status = :status)
          AND (:fromDate IS NULL OR n.createdAt >= :fromDate)
          AND (:toDate IS NULL OR n.createdAt <= :toDate)
          AND n.deletedAt IS NULL
        """)
    Page<Notification> search(
        @Param("recipientId") String recipientId,
        @Param("channel") NotificationChannel channel,
        @Param("status") NotificationStatus status,
        @Param("fromDate") Instant fromDate,
        @Param("toDate") Instant toDate,
        Pageable pageable
    );

    List<Notification> findByStatusAndScheduledAtBefore(NotificationStatus status, Instant before);

    long countByStatus(NotificationStatus status);

    long countByChannelAndStatus(NotificationChannel channel, NotificationStatus status);

    @Query("SELECT n.channel, COUNT(n) FROM Notification n WHERE n.createdAt >= :since AND n.deletedAt IS NULL GROUP BY n.channel")
    List<Object[]> countByChannelSince(@Param("since") Instant since);

    @Query("SELECT n.status, COUNT(n) FROM Notification n WHERE n.createdAt >= :since AND n.deletedAt IS NULL GROUP BY n.status")
    List<Object[]> countByStatusSince(@Param("since") Instant since);
}
