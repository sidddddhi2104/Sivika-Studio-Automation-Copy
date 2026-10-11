"""Read-only inspection of whatever page the driver is currently on.
Used by discover_site.py to document REAL links, forms and fields before tests rely on them.
Input values are never recorded (so passwords/usernames cannot leak into reports)."""
from selenium.webdriver.common.by import By


def _describe_element(el) -> dict:
    tag = el.tag_name
    el_type = (el.get_attribute("type") or "").lower()
    info = {
        "tag": tag,
        "type": el_type,
        "name": el.get_attribute("name"),
        "id": el.get_attribute("id"),
        "placeholder": el.get_attribute("placeholder"),
        "required": el.get_attribute("required") is not None,
        "displayed": el.is_displayed(),
    }
    if tag == "button" or el_type in ("submit", "button"):
        info["text"] = (el.text or el.get_attribute("value") or "").strip()
    return info


def inspect_page(driver) -> dict:
    forms = []
    for form in driver.find_elements(By.TAG_NAME, "form"):
        forms.append(
            {
                "id": form.get_attribute("id"),
                "action": form.get_attribute("action"),
                "method": (form.get_attribute("method") or "get").lower(),
                "novalidate": form.get_attribute("novalidate") is not None,
                "fields": [
                    _describe_element(e)
                    for e in form.find_elements(By.CSS_SELECTOR, "input, textarea, select, button")
                ],
            }
        )
    return {
        "url": driver.current_url,
        "title": driver.title,
        "headings": [
            h.text.strip()
            for h in driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3")
            if h.text.strip()
        ],
        "links": [
            {"text": a.text.strip(), "href": a.get_attribute("href")}
            for a in driver.find_elements(By.TAG_NAME, "a")
        ],
        "images": [i.get_attribute("src") for i in driver.find_elements(By.TAG_NAME, "img")],
        "forms": forms,
    }
