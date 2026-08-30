package com.bankxyz.mdm.matching.domain;

/**
 * Type of matching algorithm.
 */
public enum MatchType {
    /** Exact match on identifier (NIK, CIF) */
    EXACT,
    /** Fuzzy string matching (Jaro-Winkler, Levenshtein) */
    FUZZY,
    /** Phonetic matching (Metaphone, Soundex) */
    PHONETIC,
    /** Transaction pattern based matching */
    TRANSACTION
}
