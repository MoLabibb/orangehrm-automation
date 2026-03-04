# OrangeHRM Test Automation Framework

[![API Tests](https://github.com/molabibb/orangehrm-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/molabibb/orangehrm-automation/actions/workflows/ci.yml)

> Automated test suite covering **UI automation** (Selenium) and **REST API testing**
> (Requests + Pytest) for [OrangeHRM Demo](https://opensource-demo.orangehrmlive.com/)

---

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Language | Python 3.11+ | Core language |
| UI Automation | Selenium 4 | Browser interaction |
| API Testing | Requests | HTTP calls to REST API |
| Test Runner | Pytest | Test discovery and execution |
| Design Pattern | Page Object Model | UI layer structure |
| Driver Manager | WebDriver Manager | Auto-downloads ChromeDriver locally |
| Reporting | pytest-html | HTML test report generation |

---

## Project Structure

```
orangehrm_automation/
│
├── api/
│   ├── __init__.py
│   └── candidates_api.py         # REST API client — add/delete candidates
│
├── pages/
│   ├── __init__.py
│   ├── base_page.py              # Shared Selenium helpers (DRY principle)
│   ├── login_page.py             # Login page — Page Object
│   └── admin_page.py             # Admin users page — Page Object
│
├── utils/
│   ├── __init__.py
│   └── data_generator.py         # Generates unique test data per run
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Test order — API tests run before UI tests
│   ├── test_admin_user_flow.py   # UI test — create and delete a system user
│   └── test_api_candidates.py    # API test — create and delete a candidate
│
├── reports/
│   └── .gitkeep                  # Keeps folder in git — reports are generated here
│
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions — runs API tests on every push
│
├── conftest.py                   # Pytest fixtures — driver and api_client
├── pytest.ini                    # Pytest config — report path, log level, paths
├── requirements.txt              # All Python dependencies
├── .gitignore                    # Excludes venv, cache, generated reports
└── README.md                     # This file
```

---

## Prerequisites

Before running the tests you need:

- **Python 3.11 or higher** — [download here](https://www.python.org/downloads/)
- **Google Chrome browser** — [download here](https://www.google.com/chrome/)
- **Internet connection** — tests run against the live demo site
- **Git** — [download here](https://git-scm.com/)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/molabibb/orangehrm-automation.git
cd orangehrm-automation
```

### 2. Create and activate a virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> ChromeDriver is downloaded automatically by WebDriver Manager locally.
> No manual driver setup needed.

---

## Running Tests

### Run all tests

```bash
pytest
```

### Run UI test only

```bash
pytest tests/test_admin_user_flow.py -v
```

### Run API tests only

```bash
pytest tests/test_api_candidates.py -v
```

### Run with visible output

```bash
pytest -s
```

> After every run an HTML report is automatically generated at
> `reports/report.html` — open it in any browser.

---

## Test Coverage

### UI Test — `test_admin_user_flow.py`

Tests the Admin > User Management page end-to-end:

| Step | Action | Verification |
|------|--------|-------------|
| 1 | Login as Admin | Dashboard loads |
| 2 | Navigate to Admin tab | User list displays |
| 3 | Read initial record count | Count captured |
| 4 | Click Add and fill the form | Form submitted successfully |
| 5 | Save new user | Redirected to user list |
| 6 | Read new record count | Count increased by exactly 1 |
| 7 | Search for the new user | User found in results |
| 8 | Delete the user | Deletion confirmed |
| 9 | Read final record count | Count returned to original |

### API Test — `test_api_candidates.py`

Tests the Recruitment Candidates API directly via HTTP — no browser involved:

| Test | Action | Verification |
|------|--------|-------------|
| `test_add_candidate_increases_count_by_one` | POST new candidate via API | Count increases by 1 |
| `test_delete_candidate_decreases_count_by_one` | DELETE candidate by id via API | Count decreases by 1 |

---

## HTML Test Report

Every test run automatically generates a report at `reports/report.html`.

The report includes:

- **Environment table** — project name, URL, browser, Python version
- **Results summary** — total passed, failed, errors
- **Per-test details** — duration, status, captured output
- **Failure details** — full traceback when a test fails

Open the report after any run:

```bash
# Windows
start reports/report.html

# Mac/Linux
open reports/report.html
```

---

## Design Principles

### Page Object Model (POM)

Each page of the application has one class. Locators and actions are
defined inside that class. Tests call human-readable methods —
no raw XPATHs or Selenium calls appear in test files.

```
Test calls:       admin_page.add_user(username, password)
POM handles:      click add → fill form → save → wait for redirect
Test never knows: XPATHs, waits, browser mechanics
```

### DRY — Don't Repeat Yourself

`BasePage` holds all shared Selenium helpers (`click`, `enter_text`, `get_text`).
Every page inherits from `BasePage` — helpers are written once, used everywhere.

### Single Responsibility

Each class does exactly one thing:

- `LoginPage` — handles login page only
- `AdminPage` — handles admin page only
- `CandidatesAPI` — handles HTTP calls only
- `DataGenerator` — generates test data only

### Cookie Bridge Authentication

OrangeHRM is a Vue.js SPA — the login form requires a server-generated
`_token` that only exists after JavaScript runs. The `requests` library
has no JavaScript engine and cannot get this token.

**Solution:** Selenium logs in via a real headless browser → we extract
the authenticated session cookie → inject it into `requests.Session()` →
close the browser. The `requests` session makes all subsequent API calls
as the authenticated user. No browser window is visible during API tests.

### Test Execution Order

The demo site allows only one active Admin session at a time. If the UI
test logs in while the API session is active, the API session is invalidated.

**Solution:** API tests always run before UI tests. This is enforced in
`tests/conftest.py` via `pytest_collection_modifyitems` which reorders
collected tests at runtime — no manual intervention needed.

---

## CI/CD — GitHub Actions

The workflow at `.github/workflows/ci.yml` runs automatically on every
push to `main` and on every pull request.

### What it does

| Step | Action |
|------|--------|
| 1 | Checks out the repository code onto a clean Ubuntu VM |
| 2 | Installs Python 3.11 with pip caching for faster reruns |
| 3 | Installs all project dependencies from `requirements.txt` |
| 4 | Installs the latest stable Google Chrome |
| 5 | Downloads and installs the matching ChromeDriver onto PATH |
| 6 | Runs the API tests in headless mode |
| 7 | Uploads the HTML report as a downloadable artifact |
| 8 | Shows a pass/fail badge on the repository README |

### Why API tests only in CI

UI tests open a visible browser window. Running headed Chrome on a
Linux VM requires a display server (Xvfb) which adds significant
complexity to the CI setup. API tests use headless Chrome — they run
perfectly on a Linux VM with no display server needed.

### ChromeDriver in CI vs locally

| Environment | ChromeDriver source | Why |
|-------------|--------------------|----|
| Local (Windows/Mac) | WebDriver Manager downloads automatically | No Chrome on PATH locally |
| CI (GitHub Actions) | Installed by workflow step, available on PATH | WebDriver Manager has a known Linux bug — points to a text file instead of the binary |

The framework detects the environment automatically using the `CI`
environment variable that GitHub Actions sets on every run. No manual
changes are needed when switching between local and CI.

### View CI results

```
GitHub repo → Actions tab → latest run → download artifact "test-report-N"
```

---

## Challenges Solved

| Challenge | Problem | Solution |
|-----------|---------|----------|
| Vue SPA login | `requests` has no JavaScript engine — cannot get the login `_token` from the HTML shell | Cookie bridge — Selenium logs in via real browser, we extract the session cookie and inject into `requests.Session()` |
| Single session per user | Demo site invalidates the existing session when a new login happens | `scope="class"` fixture — one browser login per test class, session reused across all tests |
| Session race condition | UI test login runs and invalidates the API session mid-suite | `pytest_collection_modifyitems` — API tests always run before UI tests |
| ChromeDriver Linux bug | WebDriver Manager on Linux CI points to `THIRD_PARTY_NOTICES.chromedriver` (a text file) instead of the binary | Detect `CI` environment variable — use chromedriver from PATH in CI, WebDriver Manager locally |
| Custom Vue dropdowns | OrangeHRM uses Vue.js custom dropdowns, not native `<select>` elements | Click the wrapper div to open, wait for `role='option'`, click option by exact text |
| Employee Name autocomplete | Field requires an API call after typing before suggestions appear | `send_keys()` to type search text → wait for `role='option'` → keyboard ARROW_DOWN + ENTER |
| Slow demo server | Post-save redirect occasionally takes longer than default timeout | Three-step explicit wait: URL leaves save page → URL reaches list page → records label visible |
