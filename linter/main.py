# linter/main.py
import sys
import yaml
from pathlib import Path

def validate_rule(rule_path: Path, schema_path: Path):
    """
    Validates a rule file against a schema.
    Checks for presence of all top-level keys defined in the schema.
    """
    print(f"[*] Validating rule: {rule_path.name}")

    # --- Load Schema ---
    try:
        with open(schema_path, 'r') as f:
            # We only care about the keys from the schema file
            schema_keys = yaml.safe_load(f).keys()
    except Exception as e:
        print(f"[!] Error: Could not load or parse schema file at {schema_path}.")
        print(e)
        return False

    # --- Load Rule ---
    try:
        with open(rule_path, 'r') as f:
            rule_data = yaml.safe_load(f)
            if not isinstance(rule_data, dict):
                print("[!] Error: Rule file is not a valid key-value structure.")
                return False
    except yaml.YAMLError as e:
        print(f"[!] Error: Invalid YAML syntax in {rule_path.name}.")
        print(e)
        return False

    # --- Validate Keys ---
    missing_keys = []
    for key in schema_keys:
        if key not in rule_data:
            missing_keys.append(key)

    if missing_keys:
        print(f"[!] Validation FAILED. Missing required fields: {', '.join(missing_keys)}")
        return False

    print(f"[*] Validation PASSED for {rule_path.name}")
    return True

def main():
    # Expecting a single command-line argument: the path to the rule file
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_rule_file>")
        sys.exit(1)

    rule_file = Path(sys.argv[1])
    # The schema is located in the parent directory's 'spec' folder
    schema_file = Path(__file__).parent.parent / "spec/rule_schema.yaml"

    if not rule_file.exists():
        print(f"[!] Error: Rule file not found at '{rule_file}'")
        sys.exit(1)

    if not schema_file.exists():
        print(f"[!] Error: Schema file not found at '{schema_file}'")
        sys.exit(1)

    if not validate_rule(rule_file, schema_file):
        sys.exit(1) # Exit with an error code for automation

if __name__ == "__main__":
    main()
