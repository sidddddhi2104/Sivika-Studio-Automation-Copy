"""Builds locators from the visible text that was confirmed on the live site.

Matching is case-insensitive so the locators survive CSS text-transform / copy tweaks.
Only <a>, headings (h1-h3) and buttons / submit inputs are targeted, never arbitrary elements.
"""
from selenium.webdriver.common.by import By

_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LOWER = "abcdefghijklmnopqrstuvwxyz"


def _lower(expr: str) -> str:
    return f"translate({expr},'{_UPPER}','{_LOWER}')"


def link_with_text(text: str):
    return (By.XPATH, f"//a[contains({_lower('normalize-space(.)')},'{text.lower()}')]")


def heading_with_text(text: str):
    return (
        By.XPATH,
        "//*[self::h1 or self::h2 or self::h3]"
        f"[contains({_lower('normalize-space(.)')},'{text.lower()}')]",
    )


def button_with_text(text: str):
    t = text.lower()
    return (
        By.XPATH,
        f"//button[contains({_lower('normalize-space(.)')},'{t}')]"
        f" | //input[(@type='submit' or @type='button') and contains({_lower('@value')},'{t}')]",
    )
