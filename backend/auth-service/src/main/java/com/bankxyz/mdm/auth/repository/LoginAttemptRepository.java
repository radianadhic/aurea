package com.bankxyz.mdm.auth.repository;

import com.bankxyz.mdm.auth.domain.LoginAttempt;
import com.bankxyz.mdm.common.repository.BaseRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

@Repository
public interface LoginAttemptRepository extends BaseRepository<LoginAttempt, UUID> {

    @Query("SELECT count(la) FROM LoginAttempt la WHERE la.username = :username AND la.success = false AND la.attemptedAt > :since")
    long countFailedAttemptsSince(@Param("username") String username, @Param("since") Instant since);

    @Query("SELECT count(la) FROM LoginAttempt la WHERE la.ipAddress = :ipAddress AND la.success = false AND la.attemptedAt > :since")
    long countFailedAttemptsByIpSince(@Param("ipAddress") String ipAddress, @Param("since") Instant since);

    @Query("SELECT la FROM LoginAttempt la WHERE la.username = :username ORDER BY la.attemptedAt DESC")
    List<LoginAttempt> findRecentByUsername(@Param("username") String username);
}
