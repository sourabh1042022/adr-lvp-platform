# metrics/calculate_metrics.py
import sys
import json
import csv
from pathlib import Path

def main():
    """
    Calculates detection metrics by comparing replayer output with ground truth labels.
    """
    if len(sys.argv) != 2:
        print("Usage: ... | python calculate_metrics.py <path_to_labels.csv>")
        sys.exit(1)

    labels_path = Path(sys.argv[1])
    if not labels_path.exists():
        print(f"[!] Error: Labels file not found at '{labels_path}'")
        sys.exit(1)

    # --- 1. Load Ground Truth Labels ---
    # Stores { event_id: expected_rule_id }
    expected_matches = {}
    with open(labels_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            expected_matches[row['event_id']] = row['expected_match_rule_id']

    # --- 2. Load Actual Detections from Replayer ---
    # Stores { event_id: [list_of_actual_rule_ids] }
    actual_matches = {}
    print("[*] Reading replayer output from stdin...")
    for line in sys.stdin:
        try:
            detection = json.loads(line)
            event_id = detection.get('event_id')
            rule_id = detection.get('matching_rule_id')
            if event_id not in actual_matches:
                actual_matches[event_id] = []
            actual_matches[event_id].append(rule_id)
        except json.JSONDecodeError:
            # Ignore lines that aren't valid JSON
            continue

    # --- 3. Calculate Metrics ---
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for event_id, expected_rule_id in expected_matches.items():
        detected_rules = actual_matches.get(event_id, [])

        if expected_rule_id != "none":
            # This event was supposed to be a match.
            if expected_rule_id in detected_rules:
                true_positives += 1
            else:
                false_negatives += 1
            # Check for any extra, unexpected matches for this event
            false_positives += len([r for r in detected_rules if r != expected_rule_id])
        else:
            # This event was NOT supposed to be a match. Any detection is a False Positive.
            false_positives += len(detected_rules)

    print("\n--- Detection Metrics ---")
    print(f"✅ True Positives (TP):  {true_positives}")
    print(f"❌ False Positives (FP): {false_positives}")
    print(f"👻 False Negatives (FN): {false_negatives}")
    print("-------------------------")

if __name__ == "__main__":
    main()
