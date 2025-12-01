package com.mavenagi;

/**
 * Very simple "AGI" playground class.
 * For now it just echoes some basic pattern-based responses.
 */
public class AGIEngine {

    public String think(String prompt) {
        if (prompt == null || prompt.isBlank()) {
            return "Please give me something to think about.";
        }

        String normalized = prompt.toLowerCase();

        if (normalized.contains("hello") || normalized.contains("ciao")) {
            return "Hi, I'm MavenAGI – your tiny Java AGI playground.";
        }

        if (normalized.contains("help")) {
            return "I can’t do much yet, but you can extend my reasoning logic in AGIEngine.java!";
        }

        return "I received: \"" + prompt + "\". Teach me how I should reason about this!";
    }
}
