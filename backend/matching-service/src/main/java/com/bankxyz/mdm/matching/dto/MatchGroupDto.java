package com.bankxyz.mdm.matching.dto;

import com.bankxyz.mdm.matching.domain.MatchCandidate;
import com.bankxyz.mdm.matching.domain.MatchGroup;
import com.bankxyz.mdm.matching.domain.MatchStatus;
import com.bankxyz.mdm.matching.domain.MatchType;

import java.time.Instant;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

public record MatchGroupDto(
    UUID id,
    MatchType matchType,
    int matchScore,
    String algorithm,
    MatchStatus status,
    int memberCount,
    String reviewerId,
    String reviewerName,
    Instant reviewedAt,
    String resolutionNotes,
    String rejectionReason,
    boolean autoDetected,
    Instant createdAt,
    Instant updatedAt,
    List<MatchCandidateDto> candidates
) {
    public static MatchGroupDto from(MatchGroup group) {
        return new MatchGroupDto(
            group.getId(),
            group.getMatchType(),
            group.getMatchScore(),
            group.getAlgorithm(),
            group.getStatus(),
            group.getMemberCount(),
            group.getReviewerId(),
            group.getReviewerName(),
            group.getReviewedAt(),
            group.getResolutionNotes(),
            group.getRejectionReason(),
            group.getAutoDetected(),
            group.getCreatedAt(),
            group.getUpdatedAt(),
            group.getCandidates().stream()
                .map(MatchCandidateDto::from)
                .collect(Collectors.toList())
        );
    }

    public record MatchCandidateDto(
        UUID id,
        String customerId,
        String cifNumber,
        String fullName,
        LocalDate dateOfBirth,
        String nik,
        String email,
        String mobilePhone,
        String address,
        int matchScore,
        List<String> matchedFields,
        boolean isPrimary,
        boolean mergeSelected
    ) {
        public static MatchCandidateDto from(MatchCandidate c) {
            return new MatchCandidateDto(
                c.getId(),
                c.getCustomerId(),
                c.getCifNumber(),
                c.getFullName(),
                c.getDateOfBirth(),
                c.getNik(),
                c.getEmail(),
                c.getMobilePhone(),
                c.getAddress(),
                c.getMatchScore(),
                c.getMatchedFields() != null
                    ? List.of(c.getMatchedFields().split(","))
                    : List.of(),
                c.getIsPrimary(),
                c.getMergeSelected()
            );
        }
    }
}
