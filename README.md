# Sivika Studio - Selenium + Pytest Automation Framework

UI test automation for **Sivika Studio**, a Flask-based handmade-art store, built with Python, Selenium WebDriver and Pytest using the Page Object Model (POM).

- **Website under test:** https://sivika.onrender.com/
- **GitHub repository:** https://github.com/sidddddhi2104/Sivika-Studio-Automation-Copy
- **Status:** The framework has been executed against the live website. Latest recorded full-suite run: 31 tests collected, 29 passed, 2 skipped, 0 failed.

## Tech stack

- Python 3.14.2
- Selenium 4
- Selenium Manager
- Pytest
- pytest-html
- python-dotenv
- Git and GitHub

## What is automated

Only functionality verified on the live website is automated. Product, cart and checkout pages are not included because authenticated functionality has not been fully inspected.

| Area | Automated checks |
|---|---|
| Home | Page title, heading, handmade-products copy and Start Shopping link |
| Navigation | Parameterized link journeys, direct URL access and browser Back |
| Register | Page title, heading, hero image, form fields, submit button, login link, empty submission and malformed email validation |
| Login | Page title, heading, identity and password fields, submit button, register link, empty submission and invalid-credential cases |
| Authenticated login | Optional tests for valid login and wrong-password rejection; skipped unless dedicated test credentials are configured |

**Safety rules:** No real purchases or payments are performed. The tests do not submit a valid registration, avoiding unnecessary test data in the live database.

## Architecture

- `pages/` - Page Objects containing locators and page actions.
- `tests/` - Test flows and assertions.
- `utils/` - Configuration, driver factory, locator helpers and page inspector.
- `test_data/` - Parameterized test data; no secrets.
- `conftest.py` - Browser and page fixtures, site warm-up and screenshot-on-failure handling.
- `discover_site.py` - Read-only inspector for links, forms and fields.

The framework uses explicit waits instead of `sleep()`. Form fields are resolved from the page DOM, and locators are based on the live site inspection.

## Folder structure

```text
Sivika-Studio-Automation/
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   ├── register_page.py
│   └── login_page.py
├── tests/
│   ├── test_home.py
│   ├── test_navigation.py
│   ├── test_register.py
│   ├── test_login.py
│   └── test_authenticated_login.py
├── utils/
│   ├── config.py
│   ├── driver_factory.py
│   ├── locator_helpers.py
│   └── page_inspector.py
├── test_data/
│   └── form_data.py
├── screenshots/
├── reports/
├── docs/
│   ├── TEST_PLAN.md
│   ├── INTERVIEW_PREP.md
│   └── RESUME_AND_METRICS_TEMPLATE.md
├── discover_site.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .env.example
└── .gitignore
```

## Installation (Windows, VS Code and PowerShell)

Prerequisites: Python, Google Chrome, Git and VS Code with the Python extension.

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

If PowerShell blocks virtual-environment activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

In VS Code, open **Ctrl + Shift + P**, choose **Python: Select Interpreter**, and select `.\venv\Scripts\python.exe`.

## Inspect the live website

Run:

```powershell
python discover_site.py
```

The inspector prints information about the website's links, forms and fields. Review the output before adding automation for pages that have not yet been verified.

## Running tests

Run the full test suite:

```powershell
pytest
```

Generate an HTML report:

```powershell
pytest --html=reports/report.html
```

Run smoke tests:

```powershell
pytest -m smoke
```

Skip authenticated tests:

```powershell
pytest -m "not auth"
```

Run navigation tests:

```powershell
pytest -m navigation
```

Run invalid-login tests:

```powershell
pytest tests/test_login.py -k invalid
```

Run without opening a browser window:

```powershell
pytest --headless
```

The website is hosted on Render, so the first request may take longer if the site is asleep. The test suite warms up the website automatically.

## Authenticated tests (optional)

The authenticated tests require a dedicated QA account. Configure these values in your local `.env` file:

```text
SIVIKA_TEST_USERNAME=your_test_username
SIVIKA_TEST_PASSWORD=your_test_password
```

Never commit `.env` or publish credentials to GitHub. These tests are skipped when the required credentials are not configured.

## Reports and failure handling

The HTML report is generated at `reports/report.html`. It includes test outcomes and per-test durations.

When a UI test fails, the framework saves a screenshot in `screenshots/` and embeds it in the report alongside failure information.

Generated report files and screenshots are excluded from Git through `.gitignore`.

## Results

Latest recorded full-suite execution:

| Metric | Value |
|---|---|
| Python | 3.14.2 |
| Platform | Windows 11 |
| Pytest | 9.1.1 |
| Tests collected | 31 |
| Passed | 29 |
| Failed | 0 |
| Skipped | 2 |
| Errors | 0 |
| Duration | Approximately 2 minutes 53 seconds |

The two skipped tests are the optional authenticated-login tests. They require `SIVIKA_TEST_USERNAME` and `SIVIKA_TEST_PASSWORD` to be configured for a dedicated QA account.

These results reflect the latest recorded run and should be updated after future test executions.

## Future improvements

- Inspect and automate product browsing, search, cart and checkout, stopping before payment.
- Add assertions for login and registration error messages after verifying the actual page elements.
- Add an opt-in registration test using a disposable account and cleanup.
- Configure GitHub Actions to run tests automatically.
- Add cross-browser testing and parallel test execution.
- Expand test coverage as additional website functionality is verified.