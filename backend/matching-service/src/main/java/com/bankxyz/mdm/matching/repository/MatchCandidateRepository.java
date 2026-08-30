package com.bankxyz.mdm.matching.repository;

import com.bankxyz.mdm.common.repository.BaseRepository;
import com.bankxyz.mdm.matching.domain.MatchCandidate;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface MatchCandidateRepository extends BaseRepository<MatchCandidate, UUID> {

    @EntityGraph(attributePaths = {"matchGroup"})
    List<MatchCandidate> findByCustomerId(String customerId);

    List<MatchCandidate> findByMatchGroupId(UUID matchGroupId);

    long countByCifNumber(String cifNumber);
}
