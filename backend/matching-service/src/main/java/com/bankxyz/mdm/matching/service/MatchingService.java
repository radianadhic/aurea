package com.bankxyz.mdm.matching.service;

import com.bankxyz.mdm.matching.domain.*;
import com.bankxyz.mdm.matching.dto.*;
import com.bankxyz.mdm.matching.engine.MatchingEngine;
import com.bankxyz.mdm.matching.repository.MatchGroupRepository;
import com.bankxyz.mdm.matching.event.MatchEventPublisher;
import com.bankxyz.mdm.common.dto.PageResponse;
import com.bankxyz.mdm.common.exception.BusinessException;
import com.bankxyz.mdm.common.exception.ResourceNotFoundException;
import com.bankxyz.mdm.matching.repository.MatchCandidateRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class MatchingService {

    private final MatchGroupRepository matchGroupRepository;
    private final MatchCandidateRepository matchCandidateRepository;
    private final MatchingEngine matchingEngine;
    private final MatchEventPublisher eventPublisher;

    @Value("${mdm.matching.auto-merge-threshold:95}")
    private int autoMergeThreshold;

    @Value("${mdm.matching.review-threshold:70}")
    private int reviewThreshold;

    /**
     * Search match groups with filters.
     */
    @Transactional(readOnly = true)
    public PageResponse<MatchGroupDto> search(MatchSearchRequest request) {
        Pageable pageable = PageRequest.of(
            request.page(),
            request.size(),
            Sort.by(Sort.Direction.fromString(request.direction() != null ? request.direction() : "desc"),
                request.sortBy() != null ? request.sortBy() : "createdAt")
        );

        Page<MatchGroup> page = matchGroupRepository.search(
            request.status(),
            request.matchType(),
            request.minScore(),
            request.maxScore(),
            request.algorithm(),
            pageable
        );

        List<MatchGroupDto> content = page.getContent().stream()
            .map(MatchGroupDto::from)
            .collect(Collectors.toList());

        return PageResponse.<MatchGroupDto>builder()
            .content(content)
            .page(page.getNumber())
            .size(page.getSize())
            .totalElements(page.getTotalElements())
            .totalPages(page.getTotalPages())
            .first(page.isFirst())
            .last(page.isLast())
            .numberOfElements(page.getNumberOfElements())
            .empty(page.isEmpty())
            .build();
    }

    /**
     * Get match group by ID with candidates.
     */
    @Transactional(readOnly = true)
    public MatchGroupDto getById(UUID id) {
        MatchGroup group = matchGroupRepository.findWithCandidatesById(id)
            .orElseThrow(() -> new ResourceNotFoundException("MatchGroup not found: " + id));
        return MatchGroupDto.from(group);
    }

    /**
     * Run matching for a customer to find potential duplicates.
     */
    @Transactional
    public List<MatchGroupDto> findMatchesForCustomer(CustomerMatchRequest request) {
        log.info("Finding matches for customer: {}", request.cifNumber());

        List<MatchEngine.MatchResult> results = matchingEngine.findMatches(
            request.cifNumber(),
            request.fullName(),
            request.dateOfBirth(),
            request.nik(),
            request.email(),
            request.mobilePhone()
        );

        if (results.isEmpty()) {
            return List.of();
        }

        // Create match groups
        return results.stream()
            .map(this::createMatchGroup)
            .map(MatchGroupDto::from)
            .collect(Collectors.toList());
    }

    /**
     * Manually trigger batch matching for all customers.
     */
    @Transactional
    public BatchMatchResult runBatchMatching(int batchSize) {
        log.info("Starting batch matching with size: {}", batchSize);
        long startTime = System.currentTimeMillis();

        BatchMatchResult result = matchingEngine.runBatch(batchSize);

        long duration = System.currentTimeMillis() - startTime;
        log.info("Batch matching completed: {} groups in {}ms", result.groupsCreated(), duration);
        return result;
    }

    /**
     * Assign match group to current user for review.
     */
    @Transactional
    public MatchGroupDto assignToMe(UUID id, String userId, String userName) {
        MatchGroup group = matchGroupRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("MatchGroup not found: " + id));

        if (group.getStatus() != MatchStatus.PENDING && group.getStatus() != MatchStatus.IN_REVIEW) {
            throw new BusinessException("INVALID_STATUS",
                "Match group is in status " + group.getStatus() + " and cannot be assigned");
        }

        group.setReviewerId(userId);
        group.setReviewerName(userName);
        group.setStatus(MatchStatus.IN_REVIEW);

        MatchGroup saved = matchGroupRepository.save(group);
        eventPublisher.publishAssigned(saved);
        return MatchGroupDto.from(saved);
    }

    /**
     * Merge match group - merge secondary records into primary.
     */
    @Transactional
    public MergeResult merge(UUID id, MergeRequest request) {
        MatchGroup group = matchGroupRepository.findWithCandidatesById(id)
            .orElseThrow(() -> new ResourceNotFoundException("MatchGroup not found: " + id));

        if (group.isResolved()) {
            throw new BusinessException("ALREADY_RESOLVED",
                "Match group already resolved: " + group.getStatus());
        }

        // Validate primary and secondaries
        UUID primaryId = request.primaryId();
        List<UUID> secondaryIds = request.secondaryIds();

        if (secondaryIds == null || secondaryIds.isEmpty()) {
            throw new BusinessException("INVALID_MERGE", "At least one secondary record required");
        }

        MatchCandidate primary = group.getCandidates().stream()
            .filter(c -> c.getId().equals(primaryId))
            .findFirst()
            .orElseThrow(() -> new BusinessException("INVALID_PRIMARY", "Primary record not in match group"));

        primary.setIsPrimary(true);

        List<MatchCandidate> secondaries = group.getCandidates().stream()
            .filter(c -> secondaryIds.contains(c.getId()))
            .collect(Collectors.toList());

        if (secondaries.size() != secondaryIds.size()) {
            throw new BusinessException("INVALID_SECONDARIES", "Some secondary records not in match group");
        }

        for (MatchCandidate secondary : secondaries) {
            secondary.setMergeSelected(true);
        }

        group.setStatus(request.manual() ? MatchStatus.MANUALLY_MERGED : MatchStatus.AUTO_MERGED);
        group.setReviewedAt(Instant.now());
        if (request.notes() != null) {
            group.setResolutionNotes(request.notes());
        }

        MatchGroup saved = matchGroupRepository.save(group);

        // Publish event to customer-service to perform actual merge
        eventPublisher.publishMerge(saved, primary.getCustomerId(),
            secondaries.stream().map(MatchCandidate::getCustomerId).collect(Collectors.toList()));

        return new MergeResult(
            saved.getId(),
            primary.getCustomerId(),
            secondaryIds,
            saved.getStatus().name(),
            Instant.now()
        );
    }

    /**
     * Reject match group - confirmed not duplicate.
     */
    @Transactional
    public MatchGroupDto reject(UUID id, RejectRequest request) {
        MatchGroup group = matchGroupRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("MatchGroup not found: " + id));

        if (group.isResolved()) {
            throw new BusinessException("ALREADY_RESOLVED",
                "Match group already resolved");
        }

        if (request.reason() == null || request.reason().length() < 5) {
            throw new BusinessException("INVALID_REASON", "Rejection reason must be at least 5 characters");
        }

        group.setStatus(MatchStatus.REJECTED);
        group.setRejectionReason(request.reason());
        group.setReviewedAt(Instant.now());
        if (request.notes() != null) {
            group.setResolutionNotes(request.notes());
        }

        MatchGroup saved = matchGroupRepository.save(group);
        eventPublisher.publishRejected(saved);
        return MatchGroupDto.from(saved);
    }

    /**
     * Escalate to senior reviewer.
     */
    @Transactional
    public MatchGroupDto escalate(UUID id, EscalateRequest request) {
        MatchGroup group = matchGroupRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("MatchGroup not found: " + id));

        group.setStatus(MatchStatus.ESCALATED);
        group.setReviewerId(request.assignedTo());
        group.setReviewerName(request.assignedToName());
        group.setResolutionNotes(request.reason());

        MatchGroup saved = matchGroupRepository.save(group);
        eventPublisher.publishEscalated(saved);
        return MatchGroupDto.from(saved);
    }

    /**
     * Get statistics.
     */
    @Transactional(readOnly = true)
    public MatchStatsResponse getStats() {
        return new MatchStatsResponse(
            matchGroupRepository.countByStatus(MatchStatus.PENDING),
            matchGroupRepository.countByStatus(MatchStatus.IN_REVIEW),
            matchGroupRepository.countByStatus(MatchStatus.AUTO_MERGED),
            matchGroupRepository.countByStatus(MatchStatus.MANUALLY_MERGED),
            matchGroupRepository.countByStatus(MatchStatus.REJECTED),
            matchGroupRepository.countByStatus(MatchStatus.ESCALATED),
            // Last 30 days auto-merged
            matchCandidateRepository.count() // placeholder
        );
    }

    private MatchGroup createMatchGroup(MatchingEngine.MatchResult result) {
        MatchGroup group = MatchGroup.builder()
            .matchType(result.type())
            .matchScore(result.score())
            .algorithm(result.algorithm())
            .status(result.score() >= autoMergeThreshold ? MatchStatus.AUTO_MERGED : MatchStatus.PENDING)
            .autoDetected(true)
            .build();

        result.candidates().forEach(c -> {
            MatchCandidate candidate = MatchCandidate.builder()
                .customerId(c.customerId())
                .cifNumber(c.cifNumber())
                .fullName(c.fullName())
                .dateOfBirth(c.dateOfBirth())
                .nik(c.nik())
                .email(c.email())
                .mobilePhone(c.mobilePhone())
                .matchScore(c.score())
                .matchedFields(String.join(",", c.matchedFields()))
                .build();
            group.addCandidate(candidate);
        });

        return matchGroupRepository.save(group);
    }
}
