import pytest

from pages.login_page import LoginPage
from test_data.form_data import INVALID_LOGINS

pytestmark = pytest.mark.login


@pytest.mark.smoke
def test_login_page_title(login_page):
    assert login_page.title == LoginPage.EXPECTED_TITLE


@pytest.mark.smoke
def test_login_page_heading(login_page):
    assert "welcome back" in login_page.heading_text().lower()


@pytest.mark.regression
def test_login_form_has_identity_and_password_fields(login_page):
    assert len(login_page.fillable_fields()) >= 2
    assert login_page.fields_of_type("password"), "Expected a password input on the login form"


@pytest.mark.regression
def test_login_page_has_submit_button_and_register_link(login_page):
    assert login_page.is_displayed(LoginPage.SUBMIT_BUTTON)
    assert login_page.is_displayed(LoginPage.REGISTER_LINK)



@pytest.mark.regression
def test_empty_login_is_rejected(login_page):
    login_page.submit()

    form_is_valid = login_page.driver.execute_script(
        "return document.querySelector('form').checkValidity();"
    )

    assert not form_is_valid, (
        "An empty login form should fail native HTML5 validation"
    )
    assert login_page.current_path == LoginPage.PATH



@pytest.mark.regression
@pytest.mark.parametrize("identity, password", INVALID_LOGINS)
def test_invalid_credentials_do_not_log_in(login_page, identity, password):
    login_page.login(identity, password)

    assert login_page.current_path == LoginPage.PATH, (
        f"Invalid credentials unexpectedly navigated away from {LoginPage.PATH}"
    )
