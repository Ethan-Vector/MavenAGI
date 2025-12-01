package com.mavenagi;

public class App {

    public static void main(String[] args) {
        System.out.println("Welcome to MavenAGI!");
        AGIEngine engine = new AGIEngine();
        String response = engine.think("Hello, AGI!");
        System.out.println("AGI says: " + response);
    }
}
