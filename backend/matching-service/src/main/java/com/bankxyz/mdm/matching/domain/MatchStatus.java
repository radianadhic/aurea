package com.bankxyz.mdm.matching.domain;

/**
 * Workflow status of a match group.
 */
public enum MatchStatus {
    /** Newly created, awaiting review */
    PENDING,
    /** Currently being reviewed by a steward */
    IN_REVIEW,
    /** Automatically merged by batch job (high confidence) */
    AUTO_MERGED,
    /** Manually merged by steward after review */
    MANUALLY_MERGED,
    /** Confirmed not duplicate, rejected */
    REJECTED,
    /** Escalated to senior steward / compliance */
    ESCALATED
}
