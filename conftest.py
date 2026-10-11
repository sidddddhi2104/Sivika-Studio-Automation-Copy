"""Shared fixtures and hooks: browser setup, site warm-up, page fixtures,
failure screenshots (saved to screenshots/ and embedded in the HTML report)."""
import base64
import re
import urllib.request
import warnings
from datetime import datetime

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils import config
from utils.driver_factory import create_driver

try:  # pytest-html >= 4
    from pytest_html import extras as html_extras
except ImportError:  # pragma: no cover
    html_extras = None


def pytest_addoption(parser):
    parser.addoption("--browser", default=None, help="chrome (default), edge or firefox")
    parser.addoption("--headless", action="store_true", default=False, help="Run without a UI")
    parser.addoption("--base-url", default=None, help="Override BASE_URL for this run")


@pytest.fixture(scope="session")
def base_url(request) -> str:
    return (request.config.getoption("--base-url") or config.BASE_URL).rstrip("/")


@pytest.fixture(scope="session", autouse=True)
def warm_up_site(base_url):
    """Render's free tier sleeps when idle. One patient request up front keeps the first test
    from failing because of a cold start. Failure here only warns - tests will report the truth."""
    try:
        with urllib.request.urlopen(base_url, timeout=config.WARMUP_TIMEOUT) as response:
            response.read(1)
    except Exception as exc:  # noqa: BLE001 - any failure is just a warning
        warnings.warn(f"Warm-up request to {base_url} failed: {exc}")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser") or config.BROWSER
    headless = request.config.getoption("--headless") or config.HEADLESS
    web_driver = create_driver(browser, headless)

    try:
        yield web_driver
    finally:
        web_driver.quit()


@pytest.fixture
def home_page(driver, base_url):
    return HomePage(driver, base_url).open()


@pytest.fixture
def register_page(driver, base_url):
    return RegisterPage(driver, base_url).open()


@pytest.fixture
def login_page(driver, base_url):
    return LoginPage(driver, base_url).open()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    web_driver = item.funcargs.get("driver")
    if web_driver is None:
        return
    config.SCREENSHOT_DIR.mkdir(exist_ok=True)
    safe_name = re.sub(r"[^\w.-]+", "_", item.name)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = config.SCREENSHOT_DIR / f"{safe_name}_{stamp}.png"
    try:
        web_driver.save_screenshot(str(path))
        if html_extras is not None:
            extra = getattr(report, "extras", [])
            extra.append(html_extras.url(web_driver.current_url, name="Failed at URL"))
            extra.append(
                html_extras.png(base64.b64encode(path.read_bytes()).decode(), name="Screenshot")
            )
            report.extras = extra
    except Exception as exc:  # noqa: BLE001 - never mask the real test failure
        warnings.warn(f"Could not capture screenshot for {item.name}: {exc}")
