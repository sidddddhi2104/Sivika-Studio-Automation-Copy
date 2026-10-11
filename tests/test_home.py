import pytest

from pages.home_page import HomePage
from pages.register_page import RegisterPage

pytestmark = pytest.mark.home


@pytest.mark.smoke
def test_home_page_title(home_page):
    assert home_page.title == HomePage.EXPECTED_TITLE


@pytest.mark.smoke
def test_home_page_heading(home_page):
    assert "welcome to sivika studio" in home_page.heading_text().lower()


@pytest.mark.regression
def test_home_page_describes_handmade_products(home_page):
    assert "handmade" in home_page.body_text().lower()


@pytest.mark.smoke
def test_start_shopping_link_targets_register_page(home_page, base_url):
    assert home_page.start_shopping_href() == f"{base_url}{RegisterPage.PATH}"
