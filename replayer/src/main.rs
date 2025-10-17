// replayer/src/main.rs
use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

use serde::Deserialize;
use yaml_rust::{Yaml, YamlLoader};
use walkdir::WalkDir;

// Define structs to automatically parse our JSON log events.
// We only care about these specific fields for now.
#[derive(Deserialize, Debug)]
struct LogEvent {
    event_id: String,
    process: ProcessInfo,
}

#[derive(Deserialize, Debug)]
struct ProcessInfo {
    #[serde(rename = "Image")]
    image: String,
}

// Define a struct to hold our parsed rule information.
struct DetectionRule {
    id: String,
    image_contains: String, // The value we will check for in the log event
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <rules_directory> <log_file>", args[0]);
        return;
    }
    let rules_path = &args[1];
    let log_file_path = &args[2];

    // --- 1. Load All Rules ---
    let mut rules = Vec::new();
    for entry in WalkDir::new(rules_path).into_iter().filter_map(|e| e.ok()) {
        if entry.path().extension().map_or(false, |e| e == "yml" || e == "yaml") {
            let content = std::fs::read_to_string(entry.path()).expect("Could not read rule file");
            let docs = YamlLoader::load_from_str(&content).unwrap();
            let doc = &docs[0];

            // Super simple MVP logic: we assume the rule wants to match 'powershell.exe'
            if let Some(id) = doc["id"].as_str() {
                rules.push(DetectionRule {
                    id: id.to_string(),
                    image_contains: "powershell.exe".to_string(),
                });
            }
        }
    }

    // --- 2. Process Log File ---
    let file = File::open(log_file_path).expect("Could not open log file");
    for line in BufReader::new(file).lines() {
        let line = line.unwrap();
        if let Ok(event) = serde_json::from_str::<LogEvent>(&line) {
            // --- 3. Check for Matches ---
            for rule in &rules {
                // Our core detection logic for this MVP
                if event.process.image.contains(&rule.image_contains) {
                    // A match was found! Print the result as JSON.
                    println!(
                        "{{\"event_id\":\"{}\", \"matching_rule_id\":\"{}\"}}",
                        event.event_id, rule.id
                    );
                }
            }
        }
    }
}
