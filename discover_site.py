"""Read-only site discovery. Records the REAL links, forms and fields of each page so tests are
built on facts, not assumptions.

Examples (PowerShell):
    python discover_site.py
    python discover_site.py --headless
    python discover_site.py --login --after-login-paths /products /cart

Output: printed summary + reports/discovery_report.json (git-ignored).
SAFETY: only pass read-only pages to --after-login-paths. Never pass URLs that add to a cart,
delete, log out or pay. This script never clicks buttons other than the Login button."""
import argparse
import json
import sys
from datetime import datetime

from pages.login_page import LoginPage
from utils import config
from utils.driver_factory import create_driver
from utils.page_inspector import inspect_page


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--browser", default=config.BROWSER)
    parser.add_argument("--headless", action="store_true", default=config.HEADLESS)
    parser.add_argument("--base-url", default=config.BASE_URL)
    parser.add_argument("--paths", nargs="*", default=["/", "/register", "/login"])
    parser.add_argument("--login", action="store_true", help="log in with SIVIKA_TEST_* from .env")
    parser.add_argument("--after-login-paths", nargs="*", default=[])
    args = parser.parse_args()
    base = args.base_url.rstrip("/")

    driver = create_driver(args.browser, args.headless)
    report = {"generated_at": datetime.now().isoformat(timespec="seconds"), "base_url": base, "public": [], "authenticated": []}
    try:
        for path in args.paths:
            driver.get(base + path)
            report["public"].append({"path": path, **inspect_page(driver)})

        if args.login:
            if not (config.TEST_USERNAME and config.TEST_PASSWORD):
                print("Set SIVIKA_TEST_USERNAME and SIVIKA_TEST_PASSWORD in .env to use --login", file=sys.stderr)
                return 2
            login = LoginPage(driver, base).open()
            login.login(config.TEST_USERNAME, config.TEST_PASSWORD)
            if not login.left_login_page():
                print("Login did not leave /login - check the credentials.", file=sys.stderr)
            else:
                report["authenticated"].append({"path": "(landing page after login)", **inspect_page(driver)})
                for path in args.after_login_paths:
                    driver.get(base + path)
                    report["authenticated"].append({"path": path, **inspect_page(driver)})
    finally:
        driver.quit()

    config.REPORT_DIR.mkdir(exist_ok=True)
    out = config.REPORT_DIR / "discovery_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    for section in ("public", "authenticated"):
        for page in report[section]:
            print(f"\n=== [{section}] {page['path']}  ->  {page['url']}\n    title: {page['title']}")
            print("    headings:", page["headings"])
            for link in page["links"]:
                print(f"    LINK  {link['text']!r} -> {link['href']}")
            for form in page["forms"]:
                print(f"    FORM  action={form['action']} method={form['method']} novalidate={form['novalidate']}")
                for f in form["fields"]:
                    print(f"      FIELD {f}")
    print(f"\nSaved: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
