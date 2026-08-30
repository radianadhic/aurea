package com.bankxyz.mdm.matching.repository;

import com.bankxyz.mdm.common.repository.BaseRepository;
import com.bankxyz.mdm.matching.domain.MatchGroup;
import com.bankxyz.mdm.matching.domain.MatchStatus;
import com.bankxyz.mdm.matching.domain.MatchType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface MatchGroupRepository extends BaseRepository<MatchGroup, UUID> {

    @EntityGraph(attributePaths = {"candidates"})
    Optional<MatchGroup> findWithCandidatesById(UUID id);

    @EntityGraph(attributePaths = {"candidates"})
    Page<MatchGroup> findAllByStatus(MatchStatus status, Pageable pageable);

    @Query("""
        SELECT mg FROM MatchGroup mg
        WHERE (:status IS NULL OR mg.status = :status)
          AND (:matchType IS NULL OR mg.matchType = :matchType)
          AND (:minScore IS NULL OR mg.matchScore >= :minScore)
          AND (:maxScore IS NULL OR mg.matchScore <= :maxScore)
          AND (:algorithm IS NULL OR mg.algorithm = :algorithm)
        """)
    Page<MatchGroup> search(
        @Param("status") MatchStatus status,
        @Param("matchType") MatchType matchType,
        @Param("minScore") Integer minScore,
        @Param("maxScore") Integer maxScore,
        @Param("algorithm") String algorithm,
        Pageable pageable
    );

    @Query("SELECT mg.status, COUNT(mg) FROM MatchGroup mg WHERE mg.createdAt >= :since GROUP BY mg.status")
    List<Object[]> countByStatusSince(@Param("since") java.time.Instant since);

    long countByStatus(MatchStatus status);

    long countByMatchTypeAndStatus(MatchType type, MatchStatus status);
}
