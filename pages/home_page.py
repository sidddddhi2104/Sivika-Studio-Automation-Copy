from pages.base_page import BasePage
from utils.locator_helpers import heading_with_text, link_with_text


class HomePage(BasePage):
    PATH = "/"
    EXPECTED_TITLE = "Welcome | Sivika Studio"

    # Text confirmed on the live home page
    HEADING = heading_with_text("Welcome To Sivika Studio")
    START_SHOPPING = link_with_text("Start Shopping")

    def heading_text(self) -> str:
        return self.find(self.HEADING).text

    def start_shopping_href(self) -> str:
        return self.find(self.START_SHOPPING).get_attribute("href")

    def click_start_shopping(self):
        self.click(self.START_SHOPPING)
