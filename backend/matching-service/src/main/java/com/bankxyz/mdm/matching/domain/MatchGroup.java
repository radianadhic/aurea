package com.bankxyz.mdm.matching.domain;

import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * MatchGroup - Group of customer records identified as potential duplicates.
 *
 * Status flow:
 *   PENDING → IN_REVIEW → AUTO_MERGED | MANUALLY_MERGED | REJECTED
 *                          ↓
 *                       ESCALATED
 */
@Entity
@Table(name = "match_groups", indexes = {
    @Index(name = "idx_match_groups_status", columnList = "status"),
    @Index(name = "idx_match_groups_score", columnList = "match_score"),
    @Index(name = "idx_match_groups_created", columnList = "created_at")
})
@EntityListeners(AuditingEntityListener.class)
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class MatchGroup {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", updatable = false, nullable = false)
    private UUID id;

    /** Type of matching algorithm that identified this group */
    @Enumerated(EnumType.STRING)
    @Column(name = "match_type", nullable = false, length = 20)
    private MatchType matchType;

    /** Confidence score 0-100 */
    @Column(name = "match_score", nullable = false)
    private Integer matchScore;

    /** Algorithm used (e.g. Jaro-Winkler, Levenshtein) */
    @Column(name = "algorithm", nullable = false, length = 50)
    private String algorithm;

    /** Current workflow status */
    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 30)
    @Builder.Default
    private MatchStatus status = MatchStatus.PENDING;

    /** Number of distinct customer records in this group */
    @Column(name = "member_count", nullable = false)
    private Integer memberCount;

    /** Reviewer (userId who picked this up) */
    @Column(name = "reviewer_id", length = 50)
    private String reviewerId;

    @Column(name = "reviewer_name", length = 200)
    private String reviewerName;

    @Column(name = "reviewed_at")
    private Instant reviewedAt;

    @Column(name = "resolution_notes", length = 2000)
    private String resolutionNotes;

    @Column(name = "rejection_reason", length = 500)
    private String rejectionReason;

    /** True if created by automatic batch job (vs manual) */
    @Column(name = "auto_detected", nullable = false)
    @Builder.Default
    private Boolean autoDetected = true;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @LastModifiedDate
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    @Version
    @Column(name = "version", nullable = false)
    @Builder.Default
    private Long version = 0L;

    @OneToMany(mappedBy = "matchGroup", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    @Builder.Default
    private List<MatchCandidate> candidates = new ArrayList<>();

    // Helper methods
    public void addCandidate(MatchCandidate candidate) {
        candidates.add(candidate);
        candidate.setMatchGroup(this);
        this.memberCount = candidates.size();
    }

    public void removeCandidate(MatchCandidate candidate) {
        candidates.remove(candidate);
        candidate.setMatchGroup(null);
        this.memberCount = candidates.size();
    }

    public boolean isResolved() {
        return status == MatchStatus.AUTO_MERGED
            || status == MatchStatus.MANUALLY_MERGED
            || status == MatchStatus.REJECTED;
    }
}
