package com.bankxyz.mdm.matching.domain;

import com.bankxyz.mdm.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.*;

import java.util.UUID;

/**
 * MatchCandidate - A customer record that is part of a match group.
 */
@Entity
@Table(name = "match_candidates", indexes = {
    @Index(name = "idx_match_cand_group", columnList = "match_group_id"),
    @Index(name = "idx_match_cand_customer", columnList = "customer_id"),
    @Index(name = "idx_match_cand_cif", columnList = "cif_number")
})
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class MatchCandidate extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "match_group_id", nullable = false, foreignKey = @ForeignKey(name = "fk_match_cand_group"))
    private MatchGroup matchGroup;

    @Column(name = "customer_id", nullable = false, length = 50)
    private String customerId;

    @Column(name = "cif_number", nullable = false, length = 30)
    private String cifNumber;

    @Column(name = "full_name", nullable = false, length = 200)
    private String fullName;

    @Column(name = "date_of_birth")
    private java.time.LocalDate dateOfBirth;

    @Column(name = "nik", length = 16)
    private String nik;

    @Column(name = "email", length = 200)
    private String email;

    @Column(name = "mobile_phone", length = 20)
    private String mobilePhone;

    @Column(name = "address", length = 500)
    private String address;

    /** Match score 0-100 for this candidate */
    @Column(name = "match_score", nullable = false)
    private Integer matchScore;

    /** Comma-separated list of matched fields */
    @Column(name = "matched_fields", length = 500)
    private String matchedFields;

    /** True if marked as primary (the "winner" record) */
    @Column(name = "is_primary", nullable = false)
    @Builder.Default
    private Boolean isPrimary = false;

    /** True if marked for merge (will be merged into primary) */
    @Column(name = "merge_selected", nullable = false)
    @Builder.Default
    private Boolean mergeSelected = false;
}
