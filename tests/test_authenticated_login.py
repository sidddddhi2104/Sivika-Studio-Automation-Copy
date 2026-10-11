"""Authenticated tests. Skipped automatically unless SIVIKA_TEST_USERNAME and
SIVIKA_TEST_PASSWORD are set in your local .env (use a dedicated test account).

Only login behaviour is covered because no post-login pages have been verified yet.
Add cart / product / logout tests here after running `python discover_site.py --login`."""
import pytest

from pages.login_page import LoginPage
from utils import config

pytestmark = pytest.mark.auth


@pytest.fixture(scope="module")
def credentials():
    if not (config.TEST_USERNAME and config.TEST_PASSWORD):
        pytest.skip("SIVIKA_TEST_USERNAME / SIVIKA_TEST_PASSWORD not set - authenticated tests skipped")
    return config.TEST_USERNAME, config.TEST_PASSWORD


def test_valid_login_leaves_login_page(login_page, credentials):
    login_page.login(*credentials)
    assert login_page.left_login_page(), "Still on /login after submitting valid credentials"


def test_valid_username_with_wrong_password_is_rejected(login_page, credentials):
    username, _ = credentials
    login_page.login(username, "definitely-not-the-password-123!")
    assert login_page.current_path == LoginPage.PATH
