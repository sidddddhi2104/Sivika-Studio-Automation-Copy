"""Creates WebDriver instances. Selenium Manager (bundled with Selenium 4.6+) downloads the
matching driver automatically, so no manual chromedriver setup is needed."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils import config


def create_driver(browser: str = "chrome", headless: bool = False) -> webdriver.Remote:
    browser = browser.lower()
    if browser == "chrome":
        options = ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
    elif browser == "edge":
        options = EdgeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser '{browser}'. Use chrome, edge or firefox.")

    driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
    return driver
