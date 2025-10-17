package com.gardiyan.translator;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.yaml.snakeyaml.Yaml;

import java.util.Map;

// Define a simple record to represent our incoming JSON request
record TranslationRequest(String ruleContent, String targetFormat) {}

@RestController
@RequestMapping("/api")
public class TranslatorController {

    @PostMapping("/translate")
    public ResponseEntity<String> translate(@RequestBody TranslationRequest request) {
        if (request.ruleContent() == null || request.targetFormat() == null) {
            return ResponseEntity.badRequest().body("'ruleContent' and 'targetFormat' are required.");
        }

        // --- Simple Translation Logic (MVP) ---
        try {
            Yaml yaml = new Yaml();
            Map<String, Object> rule = yaml.load(request.ruleContent());

            // For now, we only support a very simple Splunk translation
            if (!"splunk".equalsIgnoreCase(request.targetFormat())) {
                return ResponseEntity.badRequest().body("Unsupported target format. Try 'splunk'.");
            }

            // Get the 'detection' block from the YAML
            Map<String, Object> detection = (Map<String, Object>) rule.get("detection");

            // Get the 'selection' sub-block
            Map<String, Object> selection = (Map<String, Object>) detection.get("selection");

            // Assume the first key-value pair is what we want to translate
            String firstKey = selection.keySet().iterator().next();
            String firstValue = (String) selection.get(firstKey);

            // A very basic translation. 'Image|endswith' -> 'Image="*value"'
            String translatedField = firstKey.split("\\|")[0];
            String translatedQuery = String.format("%s=\"*%s\"", translatedField, firstValue);

            return ResponseEntity.ok(translatedQuery);

        } catch (Exception e) {
            return ResponseEntity.status(500).body("Failed to parse or translate rule: " + e.getMessage());
        }
    }
}
