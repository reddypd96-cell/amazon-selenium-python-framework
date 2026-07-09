

import os
from dotenv import load_dotenv

load_dotenv()  # pulls values from a local .env file (never commit that file)

BASE_URL = os.getenv(
    "AMAZON_BASE_URL",
    "https://www.amazon.in",
)

MOBILE_NUMBER = os.getenv("AMAZON_MOBILE_NUMBER", "")
PASSWORD = os.getenv("AMAZON_PASSWORD", "")


PLACE_REAL_ORDER = os.getenv("PLACE_REAL_ORDER", "false").lower() == "true"

# Browser: chrome
BROWSER = os.getenv("BROWSER", "chrome")


HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

IMPLICIT_WAIT = 5         
EXPLICIT_WAIT = 15        


SEARCH_TERM = os.getenv("SEARCH_TERM", "earbuds")

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots")
