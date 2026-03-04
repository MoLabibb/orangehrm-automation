# OrangeHRM Test Automation Framework

[![API Tests](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/ci.yml)

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
| Driver Manager | WebDriver Manager | Auto-downloads ChromeDriver |
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
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
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

> ChromeDriver is downloaded automatically by WebDriver Manager —
> no manual driver setup needed.

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

> After every run, an HTML report is automatically generated at:
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

Tests the Recruitment Candidates API directly via HTTP:

| Test | Action | Verification |
|------|--------|-------------|
| `test_add_candidate_increases_count_by_one` | POST new candidate | Count increases by 1 |
| `test_delete_candidate_decreases_count_by_one` | DELETE candidate by id | Count decreases by 1 |

---

## HTML Test Report

Every test run automatically generates a report at `reports/report.html`.

The report includes:
- **Environment table** — project name, URL, browser, Python version
- **Results summary** — total passed, failed, errors
- **Per-test details** — duration, status, captured logs
- **Failure details** — full traceback when a test fails

Open the report after any run:
```bash
# Windows
start reports/report.html

# Mac
open reports/report.html
```

---

## Design Principles

### Page Object Model (POM)
Each page of the application has one class. Locators and actions are
defined inside that class. Tests call human-readable methods —
no raw XPATHs or Selenium calls appear in test files.
```
Test calls:          admin_page.add_user(username, password)
POM handles:         click add button → fill form → save → wait for redirect
Test never knows:    XPATHs, waits, browser mechanics
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
token that only exists after JavaScript runs. The `requests` library
has no JavaScript engine.

**Solution:** Selenium logs in via a real headless browser → we extract
the authenticated session cookie → inject it into `requests.Session()` →
close the browser. The `requests` session makes all API calls authenticated.
No browser visible during API tests.

---

## CI/CD — GitHub Actions

The workflow at `.github/workflows/ci.yml` runs automatically on every push to `main`.

**What it does:**
1. Spins up a clean Ubuntu VM
2. Installs Python and Chrome
3. Installs all dependencies
4. Runs the API tests
5. Uploads the HTML report as a downloadable artifact
6. Shows pass/fail badge on the repo page

**Why API tests only in CI:**
UI tests require a visible browser window. Headless Chrome on Linux
for UI tests requires additional display server setup (Xvfb).
API tests use headless Chrome natively — they run perfectly in CI
without any extra configuration.

**View results:**
Go to your repo → Actions tab → latest workflow run → download artifact `test-report-N`

---

## Challenges Solved

| Challenge | Problem | Solution |
|-----------|---------|----------|
| Vue SPA login | `requests` cannot execute JavaScript to get the login token | Cookie bridge — Selenium logs in, we extract the session cookie |
| Session expiry | New login invalidates the previous session | `scope="class"` fixture — one login shared across all API tests |
| ChromeDriver version | Driver version must match installed Chrome | WebDriver Manager auto-downloads the correct version |
| Custom dropdowns | OrangeHRM uses Vue.js custom dropdowns, not native `<select>` | Click wrapper div → wait for `role='option'` → click by text |
| Autocomplete field | Employee Name field requires API call after typing | `send_keys()` to type → wait for `role='option'` → keyboard select |