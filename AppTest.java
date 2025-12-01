package com.mavenagi;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class AppTest {

    @Test
    void engineShouldRespondToPrompt() {
        AGIEngine engine = new AGIEngine();
        String answer = engine.think("hello");
        assertNotNull(answer);
        assertTrue(answer.toLowerCase().contains("mavenagi"));
    }
}
