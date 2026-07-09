"""
Central configuration for the framework.
Keep environment-specific values here so tests never hardcode them.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # pulls values from a local .env file (never commit that file)

BASE_URL = os.getenv(
    "AMAZON_BASE_URL",
    "https://www.amazon.in",
)

# Login credentials - set these in a local .env file, never hardcode them here
MOBILE_NUMBER = os.getenv("AMAZON_MOBILE_NUMBER", "")
PASSWORD = os.getenv("AMAZON_PASSWORD", "")

# Safety switch. Cash on Delivery has no payment gateway to stop it, so the
# "Place your order" click is gated behind this flag. Defaults to False so
# nobody accidentally places a real order just by running the suite.
PLACE_REAL_ORDER = os.getenv("PLACE_REAL_ORDER", "false").lower() == "true"

# Browser: chrome | firefox | edge
BROWSER = os.getenv("BROWSER", "chrome")

# Run headless in CI, headed locally for debugging
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

IMPLICIT_WAIT = 5          # seconds, kept low - we rely on explicit waits
EXPLICIT_WAIT = 15         # seconds, default for WebDriverWait

# Search term used for the demo journey
SEARCH_TERM = os.getenv("SEARCH_TERM", "iphone")

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots")
