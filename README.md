# Playwright Python BDD Automation Framework

A senior-grade, highly optimized test automation harness combining **Playwright Python**, **Pytest-BDD**, and **Pytest-XDist**. This project validates both end-to-end user frontend journeys on **SauceDemo** and backend microservices integration on **DummyJSON**.

---

## 🚀 Key Framework Features

* **Behavior-Driven Development (BDD)**: Human-readable test design via Gherkin `.feature` syntax powered by `pytest-bdd`.
* **Zero Hardcoding Architecture**: Core metrics, data arrays, and pricing components are parsed dynamically via regex, list comprehensions, and runtime DOM calculations.
* **Parallel Execution Matrix**: Out-of-the-box support for multi-threaded core scheduling via `pytest-xdist`.
* **Defensive Pipeline Protections**: Embedded flaky-test retries via `pytest-rerunfailures` and visual capture troubleshooting.
* **CI/CD Distributed Architecture**: Configured with a GitHub Actions parallel matrix strategy, spinning up independent UI and API nodes concurrently to maximize execution speed.

---

## 📁 Project Directory Structure

```text
playwright-tests/
├── .github/
│   └── workflows/
│       └── playwright-ci.yml    # GitHub Actions matrix execution configuration
├── features/
│   ├── checkout.feature         # Frontend user E2E checkout scenarios
│   ├── inventory.feature        # Frontend item catalog sorting scenarios
│   ├── login_failure.feature    # Frontend authentication edge-cases
│   ├── api_cart.feature         # Chained REST state API integration scenarios
│   ├── api_login.feature        # REST token authentication validation
│   ├── api_negative_scenarios.feature # Backend API defensive error boundaries
│   └── api_products.feature     # Backend API database asset contract scenarios
├── pages/                       # Page Object Models (POM) tracking frontend locators
│   ├── login_page.py
│   ├── inventory_page.py
│   └── checkout_page.py
├── tests/                       # Pytest-BDD step definition implementation layers
│   ├── test_checkout.py
│   ├── test_inventory.py
│   ├── test_login_failure.py
│   ├── test_api_cart.py
│   ├── test_api_login.py
│   └── test_api_negative_scenarios.py
├── conftest.py                  # Global shared fixtures & contextual cleanups
├── pyproject.toml               # Engine configuration mapping, settings, and markers
└── requirements.txt             # Pinned, immutable project dependencies
```

---

## 🛠️ Local Environment Setup

Ensure you have **Python 3.11+** installed on your machine. Open your IDE terminal inside the project root directory and execute the setup loop:

```bash
# 1. Initialize an isolated virtual environment
python3 -m venv .venv

# 2. Activate the environment
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# 3. Install the immutable framework dependencies
pip install -r requirements.txt

# 4. Download Playwright's browser engines and system drivers
playwright install
```

---

## 🏃 Running Tests Locally

The execution configuration is fully governed by the `pyproject.toml` file. By default, typing just `pytest` will scan your cores, use multithreading, run browsers in **headed mode** using Chromium, and create an output report.

### Targeted Execution via Custom Markers

Use the `-m` tag to isolate your execution layer:

```bash
# Run ONLY frontend UI tests across your available computer processor cores
pytest -m ui

# Run ONLY backend API tests (instantly bypasses browser allocation loops)
pytest -m api

# Run a single specific test suite file
pytest tests/test_api_cart.py
```

### Useful CLI Control Overrides

```bash
# Force sequential single-thread runtime execution (disables parallel workers)
pytest -n 0

# Run in headless mode (perfect for background executions)
pytest --headed=false

# Apply an intentional lag between steps to watch UI actions clearly (in milliseconds)
pytest --slowmo 1000
```

---

## 📊 Reporting & Debugging Artifacts

Every time the test suite concludes, `pytest-html` generates a self-contained web dashboard in the root directory named **`report.html`**. 

* **Failure Screenshots**: If any frontend `ui` marked test encounters an assertion error, Playwright automatically snaps a viewport image and saves it to the `test-results/` folder, linking it dynamically directly inside your HTML report row.
* **Console Payload Inspecting**: Print statements and JSON logs are unlocked permanently via the `-s` capture flag. API request/response footprints can be inspected directly in your IDE terminal.

---

## 🤖 Continuous Integration (GitHub Actions)

On every single `push` or `pull_request` targeting your primary branches, GitHub Action scales a matrix strategy:

1. **`ui` Worker**: Generates a Linux agent, runs a pip restore layer, provisions Ubuntu graphics dependencies, installs Chromium, and executes `pytest -m ui -n 2`.
2. **`api` Worker**: Simultaneously launches an independent container, drops browser downloads completely to preserve processing minutes, and targets backend routing via `pytest -m api`.

Reports are collected from both nodes and stored separately as zip file artifacts inside the specific GitHub Actions execution panel.

---

## 🏛️ Rationale Behind Key Architectural Decisions

This framework was built with an intentional selection of modern tools designed to balance engineering depth with project maintainability:

* **Playwright, Python, and Pytest (Versatility & Future-Proofing)**: This core stack was selected over legacy tools (like Selenium) due to its native speed, automatic waiting mechanisms, and excellent support for modern web applications. Python and Pytest provide a highly scalable ecosystem that is widely adopted, easy to learn for onboarding engineers, and perfectly equipped to handle both web-first UI interactions and lightweight REST API validations in a single codebase.
* **Behavior-Driven Development (BDD)**: Implementing `pytest-bdd` bridges the gap between technical and non-technical stakeholders. By translating code execution into a neatly readable, human-friendly Gherkin format, user journeys become self-documenting. This enables seamless, data-driven scaling where complex user variations and API payloads can be modified directly within plain-text matrices without writing new automation code.
* **Page Object Model (POM)**: To guarantee long-term reusability and eliminate code duplication, frontend UI locators and actions are strictly encapsulated within dedicated Page Object classes. This structural isolation ensures that if an element or locator changes on the target website, it only needs to be updated once inside the Page Object file, shielding the step definitions from breaking and ensuring long-term maintenance scalability.

---

## 🤖 AI-Assisted Architecture & Engineering Disclosure

This test automation framework was architected and developed using an advanced AI-pair programming model. Rather than relying on boilerplate code generators, the framework was systematically built through a deliberate, iterative prompting strategy. As the lead test engineer, I provided structural guardrails, defined strict design constraints (such as enforcing a single line of data entry per Gherkin scenario, demanding comprehensive Senior QA assertions, and separating UI and API concerns), and rigorously troubleshooted environment configurations. The AI acted as an adaptive technical collaborator—translating these high-level architectural requirements into production-ready Page Object Models, custom Pytest configurations, data-driven Gherkin matrices, and a parallelized CI/CD GitHub Actions matrix. This collaborative engineering approach resulted in a highly scalable, non-hardcoded, and optimized automation harness built to strict modern software engineering standards.
