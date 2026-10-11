import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

pytestmark = [pytest.mark.navigation]

NAVIGATION_CASES = [
    pytest.param(HomePage, "click_start_shopping", RegisterPage, id="home-start-shopping->register"),
    pytest.param(RegisterPage, "go_to_login", LoginPage, id="register-login-link->login"),
    pytest.param(RegisterPage, "go_home", HomePage, id="register-home-link->home"),
    pytest.param(LoginPage, "go_to_register", RegisterPage, id="login-register-link->register"),
    pytest.param(LoginPage, "go_home", HomePage, id="login-home-link->home"),
]


@pytest.mark.smoke
@pytest.mark.parametrize("source_cls, action, target_cls", NAVIGATION_CASES)
def test_link_navigates_to_expected_page(driver, base_url, source_cls, action, target_cls):
    source = source_cls(driver, base_url).open()
    getattr(source, action)()

    target = target_cls(driver, base_url)
    target.wait_until_loaded()

    assert target.current_path == target_cls.PATH
    assert target.title == target_cls.EXPECTED_TITLE


@pytest.mark.regression
@pytest.mark.parametrize("page_cls", [HomePage, RegisterPage, LoginPage])
def test_page_is_reachable_by_direct_url(driver, base_url, page_cls):
    page = page_cls(driver, base_url).open()
    assert page.current_path == page_cls.PATH
    assert page.title == page_cls.EXPECTED_TITLE


@pytest.mark.regression
def test_browser_back_returns_to_previous_page(driver, base_url):
    home = HomePage(driver, base_url).open()
    home.click_start_shopping()
    register = RegisterPage(driver, base_url)
    register.wait_until_loaded()

    driver.back()

    home.wait_until_loaded()
    assert home.title == HomePage.EXPECTED_TITLE
