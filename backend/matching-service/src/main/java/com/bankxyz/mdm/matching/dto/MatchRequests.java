package com.bankxyz.mdm.matching.dto;

import com.bankxyz.mdm.matching.domain.MatchStatus;
import com.bankxyz.mdm.matching.domain.MatchType;
import jakarta.validation.constraints.*;

import java.time.Instant;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

public class MatchRequests {

    public record MatchSearchRequest(
        MatchStatus status,
        MatchType matchType,
        Integer minScore,
        Integer maxScore,
        String algorithm,
        Integer page,
        Integer size,
        String sortBy,
        String direction
    ) {
        public MatchSearchRequest {
            if (page == null) page = 0;
            if (size == null) size = 20;
        }
    }

    public record CustomerMatchRequest(
        @NotBlank String cifNumber,
        @NotBlank String fullName,
        LocalDate dateOfBirth,
        String nik,
        String email,
        String mobilePhone
    ) {}

    public record MergeRequest(
        @NotNull UUID primaryId,
        @NotEmpty List<UUID> secondaryIds,
        boolean manual,
        @Size(max = 2000) String notes
    ) {}

    public record RejectRequest(
        @NotBlank @Size(min = 5, max = 500) String reason,
        @Size(max = 2000) String notes
    ) {}

    public record EscalateRequest(
        @NotBlank String assignedTo,
        String assignedToName,
        @NotBlank String reason
    ) {}

    public record MergeResult(
        UUID matchGroupId,
        String primaryCustomerId,
        List<UUID> secondaryIds,
        String status,
        Instant mergedAt
    ) {}

    public record MatchStatsResponse(
        long pending,
        long inReview,
        long autoMerged,
        long manuallyMerged,
        long rejected,
        long escalated,
        long total
    ) {}

    public record BatchMatchRequest(
        @Min(1) @Max(100000) int batchSize,
        boolean autoMerge
    ) {}
}
