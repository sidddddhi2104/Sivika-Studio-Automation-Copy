from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from utils.locator_helpers import button_with_text, heading_with_text, link_with_text


class LoginPage(BasePage):
    PATH = "/login"
    EXPECTED_TITLE = "Login | Sivika Art Studio"

    # Text confirmed on the live login page
    HEADING = heading_with_text("Welcome Back")
    SUBMIT_BUTTON = button_with_text("Login")
    REGISTER_LINK = link_with_text("Register")
    HOME_LINK = link_with_text("Home")

    def heading_text(self) -> str:
        return self.find(self.HEADING).text

    def password_field(self):
        fields = self.fields_of_type("password")
        assert fields, "No visible input[type=password] found on the login form"
        return fields[0]

    def identity_field(self):
        """The first visible non-password text field (username or email). Resolved from the
        DOM at runtime, so no field name/id is assumed."""
        candidates = [
            f for f in self.fillable_fields() if (f.get_attribute("type") or "") != "password"
        ]
        assert candidates, "No visible username/email field found on the login form"
        return candidates[0]

    def enter_credentials(self, identity: str, password: str):
        self.type_text(self.identity_field(), identity)
        self.type_text(self.password_field(), password)

    def submit(self) -> bool:
        """Clicks Login. Returns True if the browser navigated/reloaded."""
        return self.click_and_detect_navigation(self.SUBMIT_BUTTON)

    def login(self, identity: str, password: str) -> bool:
        self.enter_credentials(identity, password)
        return self.submit()

    def left_login_page(self) -> bool:
        """Waits (explicitly) for the browser to leave /login; True if it did."""
        try:
            self.wait.until(lambda d: self.current_path != self.PATH)
            return True
        except TimeoutException:
            return False

    def go_to_register(self):
        self.click(self.REGISTER_LINK)

    def go_home(self):
        self.click(self.HOME_LINK)
