package com.bankxyz.mdm.matching.engine;

import com.bankxyz.mdm.matching.domain.MatchType;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.text.similarity.JaroWinklerDistance;
import org.apache.commons.text.similarity.LevenshteinDistance;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.*;

/**
 * 3-Layer matching engine:
 *   Layer 1: Exact match on NIK (immediate)
 *   Layer 2: Fuzzy string match (Jaro-Winkler + Levenshtein)
 *   Layer 3: Phonetic + transaction pattern (deferred)
 */
@Component
@Slf4j
public class MatchingEngine {

    private final JaroWinklerDistance jaroWinkler = new JaroWinklerDistance();
    private final LevenshteinDistance levenshtein = new LevenshteinDistance();

    @Value("${mdm.matching.fuzzy-threshold:0.85}")
    private double fuzzyThreshold;

    @Value("${mdm.matching.phonetic-threshold:0.80}")
    private double phoneticThreshold;

    /**
     * Find potential matches for a customer.
     */
    public List<MatchResult> findMatches(
        String cifNumber, String fullName, LocalDate dateOfBirth,
        String nik, String email, String mobilePhone
    ) {
        log.debug("Finding matches for CIF: {}", cifNumber);

        List<MatchResult> results = new ArrayList<>();

        // In real impl, query Elasticsearch / Neo4j for candidates
        // For now, return mock result structure
        // candidates from ES/Neo4j index

        return results;
    }

    /**
     * Run batch matching across all customers.
     */
    public BatchMatchResult runBatch(int batchSize) {
        log.info("Running batch matching for size: {}", batchSize);
        // In real impl:
        // 1. Stream customers from DB in batches
        // 2. For each, find matches via ES
        // 3. Create match groups
        // 4. Auto-merge high-confidence groups
        return new BatchMatchResult(0, 0, 0, java.time.Duration.ZERO);
    }

    /**
     * Compute Jaro-Winkler score (0-1).
     */
    public double jaroWinkler(String s1, String s2) {
        if (s1 == null || s2 == null) return 0;
        if (s1.equalsIgnoreCase(s2)) return 1;
        return jaroWinkler.apply(s1.toLowerCase(), s2.toLowerCase());
    }

    /**
     * Compute Levenshtein-based similarity (0-1).
     */
    public double levenshteinSimilarity(String s1, String s2) {
        if (s1 == null || s2 == null) return 0;
        int maxLen = Math.max(s1.length(), s2.length());
        if (maxLen == 0) return 1;
        int distance = levenshtein.apply(s1, s2);
        return 1.0 - ((double) distance / maxLen);
    }

    /**
     * Combined score: average of Jaro-Winkler and Levenshtein.
     */
    public double combinedScore(String s1, String s2) {
        return (jaroWinkler(s1, s2) + levenshteinSimilarity(s1, s2)) / 2;
    }

    /**
     * Phonetic encoding (Soundex).
     */
    public String soundex(String s) {
        if (s == null || s.isEmpty()) return "";
        s = s.toUpperCase().charAt(0) + s.substring(1).toUpperCase()
            .replaceAll("[^A-Z]", "");
        if (s.isEmpty()) return "";

        StringBuilder code = new StringBuilder();
        code.append(s.charAt(0));
        char prev = soundexCode(s.charAt(0));

        for (int i = 1; i < s.length() && code.length() < 4; i++) {
            char c = soundexCode(s.charAt(i));
            if (c != '0' && c != prev) {
                code.append(c);
            }
            prev = c;
        }
        while (code.length() < 4) code.append('0');
        return code.toString();
    }

    private char soundexCode(char c) {
        return switch (c) {
            case 'B', 'F', 'P', 'V' -> '1';
            case 'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z' -> '2';
            case 'D', 'T' -> '3';
            case 'L' -> '4';
            case 'M', 'N' -> '5';
            case 'R' -> '6';
            default -> '0';
        };
    }

    /**
     * Determine if two soundex codes match phonetically.
     */
    public boolean soundexMatch(String s1, String s2) {
        return soundex(s1).equals(soundex(s2));
    }

    public record MatchResult(
        MatchType type,
        String algorithm,
        int score,
        List<CandidateInfo> candidates
    ) {}

    public record CandidateInfo(
        String customerId,
        String cifNumber,
        String fullName,
        LocalDate dateOfBirth,
        String nik,
        String email,
        String mobilePhone,
        int score,
        List<String> matchedFields
    ) {}

    public record BatchMatchResult(
        int customersProcessed,
        int groupsCreated,
        int autoMerged,
        java.time.Duration duration
    ) {}
}
