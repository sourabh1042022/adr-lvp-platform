# Detection Rule Versioning Policy

All rules in this repository MUST follow Semantic Versioning (SemVer) `MAJOR.MINOR.PATCH`.

- **Example:** `1.2.5`

---

### ## When to Increment the Version

#### **PATCH Version (`1.2.5` -> `1.2.6`)**

Increment the PATCH version for backward-compatible bug fixes or minor improvements that do not change the core detection logic.

- Fixing a typo in the description or a reference link.
- Adding a known false positive scenario.
- Reformatting the rule for better readability.
- Optimizing the rule slightly without changing what it detects.

#### **MINOR Version (`1.2.5` -> `1.3.0`)**

Increment the MINOR version when you add functionality in a backward-compatible manner. Reset PATCH to 0.

- Adding a new field or condition to the detection logic to catch more variations of a threat.
- Broadening the scope (e.g., a rule for "PowerShell" is updated to also cover `pwsh`).
- Adding a filter to reduce a small number of false positives, making the rule more precise.

#### **MAJOR Version (`1.2.5` -> `2.0.0`)**

Increment the MAJOR version when you make incompatible changes to the rule's logic or schema. Reset MINOR and PATCH to 0.

- A complete rewrite of the detection logic.
- Changing the primary `logsource` (e.g., from Windows Security events to Sysmon).
- Removing detection capabilities that users might have relied on. This is a breaking change.
