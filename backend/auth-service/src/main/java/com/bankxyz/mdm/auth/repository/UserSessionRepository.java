package com.bankxyz.mdm.auth.repository;

import com.bankxyz.mdm.auth.domain.UserSession;
import com.bankxyz.mdm.common.repository.BaseRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface UserSessionRepository extends BaseRepository<UserSession, UUID> {

    @Query("SELECT s FROM UserSession s WHERE s.tokenHash = :tokenHash AND s.active = true AND s.deletedAt IS NULL")
    Optional<UserSession> findByTokenHash(@Param("tokenHash") String tokenHash);

    @Query("SELECT s FROM UserSession s WHERE s.userId = :userId AND s.active = true AND s.deletedAt IS NULL ORDER BY s.lastActivityAt DESC")
    List<UserSession> findActiveSessionsByUserId(@Param("userId") UUID userId);

    @Query("SELECT s FROM UserSession s WHERE s.active = true AND s.expiresAt < :now AND s.deletedAt IS NULL")
    List<UserSession> findExpiredSessions(@Param("now") Instant now);

    @Modifying
    @Query("UPDATE UserSession s SET s.active = false, s.loggedOutAt = :now, s.logoutReason = :reason, s.updatedAt = :now WHERE s.id = :id")
    int logoutSession(@Param("id") UUID id, @Param("now") Instant now, @Param("reason") String reason);

    @Modifying
    @Query("UPDATE UserSession s SET s.active = false, s.loggedOutAt = :now, s.logoutReason = 'LOGGED_OUT_ALL', s.updatedAt = :now WHERE s.userId = :userId AND s.active = true")
    int logoutAllUserSessions(@Param("userId") UUID userId, @Param("now") Instant now);

    @Modifying
    @Query("UPDATE UserSession s SET s.lastActivityAt = :now, s.updatedAt = :now WHERE s.id = :id")
    int updateLastActivity(@Param("id") UUID id, @Param("now") Instant now);

    @Query("SELECT count(s) FROM UserSession s WHERE s.userId = :userId AND s.active = true AND s.deletedAt IS NULL")
    long countActiveSessionsByUserId(@Param("userId") UUID userId);
}
