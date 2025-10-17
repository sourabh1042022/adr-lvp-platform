package com.gardiyan;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.time.Duration;
import java.time.Instant;

public class App {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Usage: java -jar benchmark.jar <log_file_path> <search_term>");
            System.exit(1);
        }

        String logFilePath = args[0];
        String searchTerm = args[1];
        int eventCount = 0;

        System.out.println("[*] Starting benchmark...");
        System.out.printf("[*] Log file: %s%n", logFilePath);
        System.out.printf("[*] Search Term (Rule): '%s'%n", searchTerm);

        // Record the start time
        Instant start = Instant.now();

        try (BufferedReader reader = new BufferedReader(new FileReader(logFilePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                // This is our simulated "rule evaluation"
                if (line.contains(searchTerm)) {
                    // In a real scenario, you would do something with the match
                }
                eventCount++;
            }
        } catch (IOException e) {
            System.err.println("Error reading log file: " + e.getMessage());
            System.exit(1);
        }

        // Record the end time and calculate duration
        Instant end = Instant.now();
        long totalDurationMillis = Duration.between(start, end).toMillis();
        double avgLatencyMicros = (double) (totalDurationMillis * 1000) / eventCount;

        System.out.println("\n--- Benchmark Results ---");
        System.out.printf("Processed %d events in %d ms.%n", eventCount, totalDurationMillis);
        System.out.printf("Average Latency: %.2f microseconds per event.%n", avgLatencyMicros);
        System.out.println("-------------------------");
    }
}
