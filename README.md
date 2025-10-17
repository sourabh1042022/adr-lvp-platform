# Automated Detection Rule Lifecycle & Validation Platform (ADR-LVP)

![CI Pipeline](https://github.com/YOUR_USERNAME/adr-lvp-platform/actions/workflows/validation_pipeline.yml/badge.svg)

ADR-LVP is a production-grade, polyglot CI/CD platform designed to automate the entire lifecycle of security detection rules. It addresses the critical challenges of false positives, performance degradation, and lack of governance in traditional SOC environments by treating detection logic as mission-critical software.

---

## 🎯 The Problem

In modern security operations, detection rules (like Sigma or YARA) are often managed manually. This leads to:
* **High False-Positive Rates:** Untested rules flood analysts with irrelevant alerts.
* **Performance Degradation:** Inefficient rules slow down production SIEMs.
* **Lack of Trust:** Analysts lose confidence in their tooling due to unreliable alerts.

This platform solves the problem by enforcing a rigorous, automated validation process for every rule change, ensuring only high-quality, performant rules are deployed.

---

## 🏛️ System Architecture

ADR-LVP is built on a decoupled, polyglot microservices architecture. A central GitHub Actions pipeline orchestrates a series of validation engines, each built with the best technology for the task.

**CI/CD Workflow:**
`Pull Request` -> `Trigger CI` -> `Lint (Python)` -> `Test Effectiveness (Rust)` -> `Calculate Metrics (Python)` -> `Verdict (Pass/Fail)`

---

## ✨ Key Features

* **Git-Backed Rule Repository:** Uses Git as the single source of truth for all detection logic, providing full versioning and provenance.
* **Web Dashboard:** A React-based UI for viewing and managing the rule set.
* **Polyglot Validation Engines:**
    * **Schema Linting (Python):** A fast, static analysis check to enforce rule structure and metadata requirements.
    * **Effectiveness Testing (Rust):** A high-performance log replayer to test rule accuracy against synthetic data and calculate TP/FP metrics.
    * **Performance Benchmarking (Java):** A utility to measure the latency and resource cost of rules.
* **CI/CD Automation:** A fully automated GitHub Actions pipeline that validates every rule change on every pull request, acting as a mandatory quality gate.

---

## 🛠️ Technology Stack

| Component      | Technology          | Purpose                                        |
| :------------- | :------------------ | :--------------------------------------------- |
| **Frontend UI** | React, CSS          | User interaction and rule dashboard.           |
| **Backend API** | Node.js, Express.js | Rule management and file system interaction. |
| **Linter** | Python, PyYAML      | Schema validation and syntax checking.       |
| **Replayer** | Rust, `serde`       | High-throughput log processing & matching.     |
| **Benchmarker** | Java, Maven         | Performance and latency measurement.           |
| **CI/CD** | GitHub Actions      | Automation and orchestration pipeline.         |

---

## 🚀 Getting Started

### Prerequisites

* Git
* Node.js (v18+) & npm
* Python (v3.10+)
* Java JDK (v17+)
* Rust & Cargo

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/adr-lvp-platform.git](https://github.com/YOUR_USERNAME/adr-lvp-platform.git)
    cd adr-lvp-platform
    ```

2.  **Install Backend Dependencies:**
    ```bash
    cd server && npm install
    ```

3.  **Install Frontend Dependencies:**
    ```bash
    cd ../client && npm install
    ```

4.  **Build the Rust Replayer:**
    ```bash
    cd ../replayer && cargo build --release
    ```

5.  **Build the Java Components:**
    ```bash
    cd ../translator && mvn clean package
    cd ../benchmark && mvn clean package
    ```

### Running Locally

1.  **Start the Backend API:**
    ```bash
    cd server && node index.js
    ```

2.  **Start the Frontend UI (in a new terminal):**
    ```bash
    cd client && npm start
    ```

---

## ⚙️ Usage Workflow

The primary interaction with the platform is through Git. The CI/CD pipeline handles all validation automatically.

1.  **Create a new branch** for your rule change.
    ```bash
    git checkout -b feature/new-detection-rule
    ```
2.  **Add or edit** a rule file in the `/rules/sigma/` directory.
3.  **Commit and push** your changes to GitHub.
    ```bash
    git add .
    git commit -m "FEAT: Add new rule for XYZ"
    git push origin feature/new-detection-rule
    ```
4.  **Open a Pull Request** on GitHub.
5.  The **GitHub Actions pipeline will automatically run**. The results will be displayed directly on the pull request page, blocking the merge if any checks fail.

---

## 🔮 Future Work

* **Full Web IDE:** Enhance the UI with rule editing and saving capabilities.
* **Metrics Dashboard:** Create a dedicated dashboard to visualize historical performance and FP rates for each rule.
* **Auto-Rollback:** Implement a CI step to automatically revert merges that cause a significant regression in quality.
* **Expanded Translator:** Add support for more complex Sigma logic and additional SIEM targets like Elasticsearch.
