package com.bankxyz.mdm.matching.engine;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;

import static org.junit.jupiter.api.Assertions.*;

class MatchingEngineTest {

    private MatchingEngine engine;

    @BeforeEach
    void setUp() {
        engine = new MatchingEngine();
        ReflectionTestUtils.setField(engine, "fuzzyThreshold", 0.85);
        ReflectionTestUtils.setField(engine, "phoneticThreshold", 0.80);
    }

    @Test
    @DisplayName("Jaro-Winkler returns 1.0 for identical strings")
    void testJaroWinklerIdentical() {
        assertEquals(1.0, engine.jaroWinkler("Budi Santoso", "Budi Santoso"));
    }

    @Test
    @DisplayName("Jaro-Winkler returns high score for similar strings")
    void testJaroWinklerSimilar() {
        double score = engine.jaroWinkler("Budi Santoso", "Budi Santosa");
        assertTrue(score > 0.95, "Expected > 0.95, got " + score);
    }

    @Test
    @DisplayName("Jaro-Winkler returns low score for different strings")
    void testJaroWinklerDifferent() {
        double score = engine.jaroWinkler("Budi Santoso", "Siti Aminah");
        assertTrue(score < 0.5, "Expected < 0.5, got " + score);
    }

    @Test
    @DisplayName("Jaro-Winkler handles null gracefully")
    void testJaroWinklerNull() {
        assertEquals(0, engine.jaroWinkler(null, "Budi"));
        assertEquals(0, engine.jaroWinkler("Budi", null));
        assertEquals(0, engine.jaroWinkler(null, null));
    }

    @Test
    @DisplayName("Jaro-Winkler is case-insensitive")
    void testJaroWinklerCaseInsensitive() {
        assertEquals(1.0, engine.jaroWinkler("BUDI SANTOSO", "budi santoso"));
    }

    @Test
    @DisplayName("Levenshtein similarity returns 1.0 for identical")
    void testLevenshteinIdentical() {
        assertEquals(1.0, engine.levenshteinSimilarity("Budi", "Budi"));
    }

    @Test
    @DisplayName("Levenshtein similarity returns 0.0 for completely different")
    void testLevenshteinDifferent() {
        assertEquals(0.0, engine.levenshteinSimilarity("abc", "xyz"));
    }

    @Test
    @DisplayName("Combined score averages Jaro-Winkler and Levenshtein")
    void testCombinedScore() {
        double combined = engine.combinedScore("Budi Santoso", "Budi Santosa");
        assertTrue(combined > 0.9, "Expected > 0.9, got " + combined);
    }

    @Test
    @DisplayName("Soundex produces 4-character codes")
    void testSoundexFormat() {
        String code = engine.soundex("Budi");
        assertEquals(4, code.length());
        assertEquals('B', code.charAt(0));
    }

    @Test
    @DisplayName("Soundex matches phonetically similar names")
    void testSoundexMatchSimilar() {
        assertTrue(engine.soundexMatch("Budi", "Boody"));
    }

    @Test
    @DisplayName("Soundex handles empty input")
    void testSoundexEmpty() {
        assertEquals("", engine.soundex(""));
        assertEquals("", engine.soundex(null));
    }

    @Test
    @DisplayName("Soundex codes are case-insensitive")
    void testSoundexCaseInsensitive() {
        assertEquals(engine.soundex("BUDI"), engine.soundex("budi"));
    }
}
