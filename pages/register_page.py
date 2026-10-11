from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.locator_helpers import button_with_text, heading_with_text, link_with_text


class RegisterPage(BasePage):
    PATH = "/register"
    EXPECTED_TITLE = "Register | Sivika Art Studio"

    # Text / assets confirmed on the live register page
    HEADING = heading_with_text("Create Account")
    SUBMIT_BUTTON = button_with_text("Register")
    LOGIN_LINK = link_with_text("Login")
    HOME_LINK = link_with_text("Home")
    HERO_IMAGE = (By.XPATH, "//img[contains(@src,'hero.jpg')]")

    def heading_text(self) -> str:
        return self.find(self.HEADING).text

    def hero_image_loaded(self) -> bool:
        image = self.find(self.HERO_IMAGE)
        self.wait.until(
            lambda d: d.execute_script(
                "return arguments[0].complete && arguments[0].naturalWidth > 0;", image
            ),
            message="Hero image did not finish loading",
        )
        return True

    def submit(self) -> bool:
        """Clicks Register. Returns True if the browser navigated/reloaded."""
        return self.click_and_detect_navigation(self.SUBMIT_BUTTON)

    def go_to_login(self):
        self.click(self.LOGIN_LINK)

    def go_home(self):
        self.click(self.HOME_LINK)
