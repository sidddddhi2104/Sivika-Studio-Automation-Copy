"""Central configuration. Values come from environment variables / .env, with safe defaults."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

BASE_URL = os.getenv("BASE_URL", "https://sivika.onrender.com").rstrip("/")
BROWSER = os.getenv("BROWSER", "chrome").lower()
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# Explicit-wait timeout (seconds). Generous because the site is hosted on Render,
# which can be slow after idle periods.
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "20"))
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "90"))
# How long to wait to decide "the click did NOT navigate" (e.g. blocked by HTML5 validation).
NO_NAVIGATION_TIMEOUT = int(os.getenv("NO_NAVIGATION_TIMEOUT", "4"))
WARMUP_TIMEOUT = int(os.getenv("WARMUP_TIMEOUT", "120"))

TEST_USERNAME = os.getenv("SIVIKA_TEST_USERNAME", "")
TEST_PASSWORD = os.getenv("SIVIKA_TEST_PASSWORD", "")

SCREENSHOT_DIR = ROOT_DIR / "screenshots"
REPORT_DIR = ROOT_DIR / "reports"
