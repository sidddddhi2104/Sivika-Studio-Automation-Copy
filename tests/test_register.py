import pytest

from pages.register_page import RegisterPage
from test_data.form_data import INVALID_EMAILS
from selenium.webdriver.common.by import By
pytestmark = pytest.mark.registration


@pytest.mark.smoke
def test_register_page_title(register_page):
    assert register_page.title == RegisterPage.EXPECTED_TITLE


@pytest.mark.smoke
def test_register_page_heading(register_page):
    assert "create account" in register_page.heading_text().lower()


@pytest.mark.regression
def test_register_page_hero_image_renders(register_page):
    assert register_page.hero_image_loaded()


@pytest.mark.regression
def test_register_page_has_submit_button_and_login_link(register_page):
    assert register_page.is_displayed(RegisterPage.SUBMIT_BUTTON)
    assert register_page.is_displayed(RegisterPage.LOGIN_LINK)


@pytest.mark.regression
def test_register_form_exposes_fillable_fields(register_page):
    fields = register_page.fillable_fields()
    assert fields, "Expected at least one visible input inside the registration form"

@pytest.mark.regression
def test_empty_registration_is_not_accepted(register_page):
    register_page.submit()

    form_is_valid = register_page.driver.execute_script(
        "return document.querySelector('form').checkValidity();"
    )

    assert not form_is_valid, (
        "An empty registration form should fail native HTML5 validation"
    )
    assert register_page.current_path == RegisterPage.PATH