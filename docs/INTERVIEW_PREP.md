# Interview Prep - Sivika Studio Automation

Answers describe what this repository really contains. Replace the "challenges" answer with your own experience after you run it.

**Why Selenium?** It is the industry-standard browser automation tool, supports multiple browsers and languages, and is widely requested in QA job descriptions. Selenium 4's Selenium Manager removed manual driver setup.

**Why Pytest?** Plain `assert` statements with rich failure output, fixtures for setup/teardown, `parametrize` for data-driven tests, markers for selecting suites, and plugins such as pytest-html.

**Explain your framework.** Page Objects in `pages/` hold locators and actions; tests in `tests/` hold flow and assertions; `conftest.py` provides the driver, page fixtures and failure hook; `utils/` has config, driver factory and locator helpers; `test_data/` feeds parameterized tests; config comes from `.env`.

**Explain Page Object Model.** Each page is a class that encapsulates its locators and behaviour. If the UI changes, I update one class instead of every test, and tests read like user journeys.

**Why fixtures?** `driver` guarantees a clean browser per test and always quits it, even on failure. Page fixtures (`login_page`, etc.) open the page once so tests don't repeat setup. `warm_up_site` is session-scoped to handle Render's cold start.

**How did you handle waits?** Only explicit waits (`WebDriverWait` + expected conditions): visibility, clickability, URL path, `readyState`, and staleness to detect whether a submit navigated. No `time.sleep()`.

**How did you handle failures?** A `pytest_runtest_makereport` hook saves a PNG to `screenshots/` and embeds it, with the failing URL, in the HTML report.

**How did you generate reports?** pytest-html, configured in `pytest.ini`, produces a self-contained `reports/report.html` with pass/fail/skip status and durations.

**How did you reduce duplication?** `BasePage` shares waits and form helpers; `locator_helpers` builds locators once; parametrization replaces copy-pasted tests (5 navigation cases, 5 invalid logins, 5 invalid e-mails); shared page fixtures.

**What did you automate?** The verified public flows: home, register and login pages, navigation, and negative form behaviour. See `docs/TEST_PLAN.md`.

**What did you leave for manual testing?** Visual design, real registration, payments, exploratory and usability testing, and everything behind login that I had not yet verified.

**What challenges did you face?** (Candidates drawn from the design - confirm against your real run.) The site sleeps on Render's free tier, so I added a warm-up and generous waits. Form field names were unknown, so I resolved fields from the DOM at runtime and built a read-only discovery script instead of guessing. I avoided creating real accounts on a live site.

**How would you improve the framework?** Cover cart/product flows after inspection, assert on real error messages, add API-level setup for test data, CI on GitHub Actions, cross-browser matrix, parallel runs with pytest-xdist, and retry-on-flake reporting.
