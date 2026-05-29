# RR QA Automation Assignment

Automated test suite for the TMDB Discover demo website (https://tmdb-discover.surge.sh/) using **Python**, **Pytest**, and **Playwright**.

---

## Table of Contents
- [Testing Strategy](#testing-strategy)
- [Test Cases Generated](#test-cases-generated)
- [Framework Architecture](#framework-architecture)
- [Setup & Installation](#setup--installation)
- [Running Tests](#running-tests)
- [Reports](#reports)
- [Test Design Techniques](#test-design-techniques)
- [Design Patterns](#design-patterns)
- [Defects Found](#defects-found)
- [CI/CD Integration Approach](#cicd-integration-approach)

---

## Testing Strategy

### Approach
The testing strategy follows a **risk-based testing** approach combined with **exploratory testing** for defect discovery:

1. **Smoke Tests** - Verify the application loads and core elements are present
2. **Functional Tests** - Validate each feature (categories, filters, pagination)
3. **API Validation** - Intercept and verify browser API calls
4. **Negative Tests** - Document known defects and test edge cases
5. **Regression Tests** - Full suite covering all functional areas

### Scope
- UI functional testing via Playwright browser automation
- API call validation via network interception
- Known defect documentation and verification
- Edge case and security input testing

### Out of Scope
- Performance/load testing
- Accessibility testing
- Cross-browser testing (framework supports it, not implemented)

---

## Test Cases Generated

| Suite | Count | Description |
|-------|-------|-------------|
| Page Load & Smoke | 4 | Core loading and element verification |
| Categories | 7 | Category tab selection and content updates |
| Title/Search Filter | 4 | Search functionality and edge cases |
| Type Filter | 3 | Movies/TV Shows toggle |
| Year Filter | 2 | Year of release filtering |
| Rating Filter | 2 | Rating-based filtering |
| Genre Filter | 4 | Genre selection filtering |
| Pagination | 7 | Page navigation and boundary tests |
| Negative/Defects | 9 | Known bugs and edge cases |
| API Validation | 5 | Network request verification |
| **Total** | **~47** | |

### Why These Cases?
- **Categories & Filters** - Core functionality users interact with most frequently
- **Pagination** - Critical for content discovery; known to have defects
- **API Validation** - Ensures data integrity between frontend and backend
- **Negative Tests** - Documents known issues for stakeholder visibility
- **Security Inputs** - Validates application resilience against injection attacks

See [docs/TEST_DESCRIPTIONS.md](docs/TEST_DESCRIPTIONS.md) for detailed step-by-step descriptions.

---

## Framework Architecture

```
rr-qa-automation-assignment/
├── conftest.py              # Pytest fixtures (browser setup, page factory)
├── pytest.ini               # Pytest configuration (markers, reporting, logging)
├── requirements.txt         # Python dependencies
├── config/
│   └── settings.py          # Test configuration constants
├── pages/
│   ├── base_page.py         # Base Page Object with common methods
│   └── discover_page.py     # Discover page POM (selectors + actions)
├── utils/
│   └── api_helper.py        # API interception and validation helper
├── tests/
│   ├── ui/
│   │   ├── test_page_load.py      # Smoke tests
│   │   ├── test_categories.py     # Category filtering tests
│   │   ├── test_filters.py        # Title, type, year, rating, genre tests
│   │   └── test_pagination.py     # Pagination tests
│   ├── api/
│   │   └── test_api_validation.py # API call validation tests
│   └── negative/
│       └── test_negative.py       # Negative and edge case tests
├── docs/
│   ├── TEST_DESCRIPTIONS.md # Detailed test case descriptions
│   └── DEFECTS.md           # Defect report
└── reports/                 # Generated Allure reports
```

### Libraries Used

| Library | Version | Purpose |
|---------|---------|---------|
| pytest | 7.4.4 | Test framework and runner |
| playwright | 1.44.0 | Browser automation |
| pytest-playwright | 0.5.0 | Pytest-Playwright integration |
| pytest-xdist | 3.5.0 | Parallel test execution |
| allure-pytest | 2.13.2 | Allure report generation |
| python-dotenv | 1.0.1 | Environment variable management |

---

## Setup & Installation

### Prerequisites
- Python 3.9+
- pip

### Installation Steps

```bash
# 1. Navigate to the project
cd ~/Documents/rr-qa-automation-assignment

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install chromium
```

---

## Running Tests

### Run All Tests
```bash
pytest
```

### Run by Marker (Category)
```bash
# Smoke tests only
pytest -m smoke

# Regression suite
pytest -m regression

# Filter tests
pytest -m filters

# Pagination tests
pytest -m pagination

# API validation tests
pytest -m api

# Negative/edge case tests
pytest -m negative
```

### Run Specific Test Directory/File
```bash
# All UI tests
pytest tests/ui/

# All API tests
pytest tests/api/

# All negative/edge case tests
pytest tests/negative/

# Single test file
pytest tests/ui/test_page_load.py
pytest tests/ui/test_pagination.py
```

### Run with Headed Browser (visible)
```bash
pytest --headed
```

### Run in Parallel
```bash
pytest -n 3
```

### Generate Allure Report
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## Reports

### Console Output
Tests produce verbose console output with real-time logging:
```
tests/test_page_load.py::TestPageLoad::test_page_loads_successfully PASSED
tests/test_page_load.py::TestPageLoad::test_content_cards_displayed PASSED
```

### Allure Reports
Generated automatically after each test run. Allure is used as the reporting tool (replacing traditional HTML reports) as it provides a richer, interactive experience. To view:
```bash
allure serve reports/allure-results
```

Rich interactive reports with:
- Test execution timeline
- Failure screenshots (auto-captured)
- Step-by-step execution details
- Historical trends
- Pass/fail summary by suite

To install Allure CLI:
```bash
brew install allure
```

---

## Test Design Techniques

| Technique | Application |
|-----------|-------------|
| **Equivalence Partitioning** | Grouping genres, categories into representative cases |
| **Boundary Value Analysis** | First page, last page, page 0, max pages |
| **Error Guessing** | XSS/SQL injection inputs, rapid actions |
| **State Transition** | Category switches, pagination, browser history |
| **Decision Table** | Filter combinations and expected outcomes |
| **Exploratory Testing** | Ad-hoc interaction to discover unknown defects |

---

## Design Patterns

| Pattern | Implementation |
|---------|---------------|
| **Page Object Model (POM)** | `pages/` directory - encapsulates selectors and actions |
| **Base Page** | Common methods inherited by all page objects |
| **Factory Pattern** | Pytest fixtures create page instances |
| **Observer Pattern** | API Helper listens for network events |
| **AAA Pattern** | Tests follow Arrange-Act-Assert structure |
| **Configuration Object** | Centralized settings in `config/settings.py` |

---

## Defects Found

| ID | Defect | Severity | Status |
|----|--------|----------|--------|
| DEF-001 | Direct URL slug access fails (SPA routing issue) | Medium | Open |
| DEF-002 | Pagination fails on last pages | Medium | Open |
| DEF-003 | Page refresh on category loses state | Low | Open |
| DEF-004 | No empty state message for zero results | Low | To Verify |

See [docs/DEFECTS.md](docs/DEFECTS.md) for full defect details with reproduction steps.

---

## CI/CD Integration Approach

### Recommended Pipeline (GitHub Actions)

```yaml
# .github/workflows/test.yml
name: QA Automation Suite

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1-5'  # Weekdays at 6 AM

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps ${{ matrix.browser }}

      - name: Run tests
        run: pytest --browser ${{ matrix.browser }}

      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results-${{ matrix.browser }}
          path: reports/allure-results/
```

### CI/CD Strategy

1. **Trigger Points:**
   - On every push to main branch
   - On pull request creation/update
   - Scheduled daily run (regression)

2. **Environment:**
   - Docker container with Python + Playwright
   - Cross-browser matrix (Chromium, Firefox, WebKit)

3. **Reporting:**
   - Allure reports deployed to GitHub Pages
   - Slack/Teams notifications on failure
   - Screenshots auto-attached on failure

4. **Optimization:**
   - Smoke tests on every PR (~2 min)
   - Full regression on merge to main (~10 min)
   - Parallel execution across browsers
   - Test result caching for flaky test detection

5. **Failure Handling:**
   - Auto-retry for flaky tests (max 2 retries)
   - Screenshot capture on failure
   - Detailed logs attached to CI artifacts
   - Failed pipeline blocks merge

---
