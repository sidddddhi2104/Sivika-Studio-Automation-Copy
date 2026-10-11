# Sivika Studio - Selenium + Pytest Automation Framework

UI test automation for **Sivika Studio**, a Flask-based handmade-art store, built with Python, Selenium WebDriver and Pytest using the Page Object Model.

- **Website under test:** https://sivika.onrender.com/
- **Status:** the framework and tests are written. **They have not been executed yet** - see [Results](#results).

## Tech stack
Python 3.10+, Selenium 4 (Selenium Manager handles the browser driver), Pytest, pytest-html, python-dotenv, Git/GitHub.

## What is automated (and why only this)
Only functionality that was **verified on the live site** is automated: the public home, register and login pages and the navigation between them. Product, cart and checkout pages sit behind authentication and have not been inspected yet, so they are deliberately **not** automated (see Future improvements).

| Area | Automated checks |
|---|---|
| Home | exact page title, heading, handmade-products copy, "Start Shopping" link target |
| Navigation | 5 link journeys (parameterized), direct URL access for 3 pages, browser Back |
| Register | title, heading, hero image renders, submit button + login link, fillable fields exist, empty submit rejected, malformed e-mails rejected (parameterized) |
| Login | title, heading, identity + password fields exist, submit + register link, empty submit rejected, 5 invalid-credential cases (parameterized) |
| Authenticated (opt-in) | valid login leaves `/login`; valid user + wrong password rejected. Skipped unless a local test account is configured |

**Safety rules:** no real purchases or payments, and no test submits a *valid* registration, so the live database is not polluted.

## Architecture
- `pages/` - Page Objects: locators + actions only (`BasePage` holds waits and form helpers).
- `tests/` - test flow and assertions only; no raw locators.
- `utils/` - config, driver factory, locator helpers, read-only page inspector.
- `test_data/` - parameterized data (no secrets).
- `conftest.py` - `driver`, `base_url`, page fixtures, site warm-up (Render cold start), screenshot-on-failure hook.
- `discover_site.py` - read-only inspector that lists the real links/forms/fields of each page.

Design decisions: explicit waits only (no `sleep()`); locators are built from text confirmed on the live site; form fields are resolved from the DOM at runtime (`input[type=password]`, first other visible input) rather than guessing `name`/`id` attributes.

## Folder structure
```
Sivika-Studio-Automation/
├── pages/            base_page.py, home_page.py, register_page.py, login_page.py
├── tests/            test_home.py, test_navigation.py, test_register.py, test_login.py, test_authenticated_login.py
├── utils/            config.py, driver_factory.py, locator_helpers.py, page_inspector.py
├── test_data/        form_data.py
├── screenshots/      failure screenshots (git-ignored)
├── reports/          HTML report (git-ignored)
├── docs/             TEST_PLAN.md, INTERVIEW_PREP.md, RESUME_AND_METRICS_TEMPLATE.md
├── discover_site.py
├── conftest.py  pytest.ini  requirements.txt  .env.example  .gitignore
```

## Installation (Windows + VS Code, PowerShell)
Prerequisites: Python 3.10+ (tick "Add to PATH"), Google Chrome, VS Code with the Python extension.

```powershell
cd path\to\Sivika-Studio-Automation
code .
py -m venv venv
# if activation is blocked:  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```
In VS Code: `Ctrl+Shift+P` -> **Python: Select Interpreter** -> pick `.\venv\Scripts\python.exe`.

## Step 1 - inspect the real forms first (recommended)
```powershell
python discover_site.py
```
This prints and saves (`reports\discovery_report.json`) every real link, form and field. Check that the register/login fields look as expected before trusting the form tests.

## Running tests
```powershell
pytest                                   # everything; HTML report -> reports\report.html
pytest --html=reports/report.html        # explicit report path
pytest -m smoke                          # critical checks only
pytest -m "not auth"                     # skip authenticated tests
pytest -m navigation
pytest tests/test_login.py -k invalid
pytest --headless                        # no browser window
pytest --browser edge                    # chrome (default) | edge | firefox
```
The first request may be slow: the site is on Render and can be asleep. The suite warms it up once automatically.

### Authenticated tests (optional)
Edit your local `.env` (never committed) and use a **dedicated test account**:
```
SIVIKA_TEST_USERNAME=...
SIVIKA_TEST_PASSWORD=...
```
Then `pytest -m auth`. Without these values the tests are skipped.

## Reports and failure handling
`reports\report.html` is a self-contained report showing passed / failed / skipped and per-test duration. On any failed UI test a screenshot is saved to `screenshots\` and embedded in the report together with the failing URL.

## Results
**Not executed yet.** Fill this table only from your own real run:

| Metric | Value |
|---|---|
| Date / browser / headless | |
| Total tests | |
| Passed | |
| Failed | |
| Skipped | |
| Total duration | |

Collected by pytest (not executed): 36 tests. Real outcomes - including any genuine failures - go in the table above after you run `pytest`.

## Future improvements
- Automate product browsing, search, cart and checkout (up to, but excluding, payment) once the authenticated pages are inspected with `discover_site.py --login`.
- Assert on error/flash messages once their real elements are known.
- Add an opt-in registration test using a disposable account and cleanup.
- Run in GitHub Actions on a schedule; add cross-browser matrix and `pytest-xdist`.
