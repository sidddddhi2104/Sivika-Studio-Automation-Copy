"""BasePage: shared waits, element helpers and generic form helpers used by every page object."""
from urllib.parse import urlparse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import config


class BasePage:
    PATH = "/"
    EXPECTED_TITLE = ""

    # Text-like fields inside any <form>. Hidden/submit/checkbox/radio/file inputs are excluded.
    FILLABLE_FIELDS = (
        By.XPATH,
        "//form//input[not(@type='hidden' or @type='submit' or @type='button' or @type='reset'"
        " or @type='image' or @type='checkbox' or @type='radio' or @type='file')]"
        " | //form//textarea",
    )

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, config.DEFAULT_TIMEOUT)

    # ---- page state -------------------------------------------------------------------
    @property
    def url(self) -> str:
        return f"{self.base_url}{self.PATH}"

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def current_path(self) -> str:
        return urlparse(self.driver.current_url).path.rstrip("/") or "/"

    def open(self):
        self.driver.get(self.url)
        self.wait_until_loaded()
        return self

    def wait_until_loaded(self):
        """Waits for the expected URL path and a fully loaded document (no sleep())."""
        self.wait.until(
            lambda d: self.current_path == self.PATH,
            message=f"Expected path {self.PATH!r} but was {self.current_path!r}",
        )
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete",
            message="Document did not reach readyState 'complete'",
        )

    # ---- generic element helpers --------------------------------------------------------
    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def is_displayed(self, locator) -> bool:
        try:
            return self.find(locator).is_displayed()
        except TimeoutException:
            return False

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def body_text(self) -> str:
        return self.find((By.TAG_NAME, "body")).text

    @staticmethod
    def type_text(element, text: str):
        element.clear()
        if text:
            element.send_keys(text)

    # ---- form helpers (driven by what is actually in the DOM) ----------------------------
    def fillable_fields(self):
        return [
            e
            for e in self.driver.find_elements(*self.FILLABLE_FIELDS)
            if e.is_displayed() and e.is_enabled()
        ]

    def fields_of_type(self, input_type: str):
        return [
            e
            for e in self.fillable_fields()
            if (e.get_attribute("type") or "text").lower() == input_type
        ]

    def fill_all_fields(self, value: str):
        for field in self.fillable_fields():
            self.type_text(field, value)

    def click_and_detect_navigation(self, locator) -> bool:
        """Clicks and returns True if the browser navigated / reloaded, False if it did not
        (e.g. HTML5 validation blocked the submit). Uses an explicit staleness wait rather than
        sleep(); the short timeout is only the 'nothing happened' cut-off."""
        old_page = self.driver.find_element(By.TAG_NAME, "html")
        self.click(locator)
        try:
            WebDriverWait(self.driver, config.NO_NAVIGATION_TIMEOUT).until(
                EC.staleness_of(old_page)
            )
        except TimeoutException:
            return False
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True
