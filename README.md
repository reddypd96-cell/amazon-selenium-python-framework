# Amazon Automation Framework

End-to-end test automation for amazon.in built with Python, Selenium WebDriver, and pytest.

## Journey Covered

1. Open Amazon and sign in
2. Search for a product (default: iphone)
3. Add the first result to cart (handles Max Quantity popup)
4. Navigate to cart and verify item is present
5. Proceed to checkout and select Cash on Delivery
6. Place order (gated by `PLACE_REAL_ORDER` flag)
7. Verify order appears on the Orders page
8. Track the first package and assert status

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Language |
| Selenium WebDriver | Browser automation |
| pytest | Test runner |
| pytest-html | HTML reports |
| webdriver-manager | Auto ChromeDriver management |
| python-dotenv | Environment config |

## Project Structure

```
amazon_automation/
├── config/
│   └── config.py           # Centralized config loaded from .env
├── drivers/
│   └── driver_factory.py   # Creates browser instances (Chrome/Firefox/Edge)
├── pages/
│   ├── base_page.py        # Reusable Selenium wrappers (Page Object base)
│   ├── home_page.py
│   ├── login_page.py
│   ├── search_results_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   └── order_tracking_page.py
├── tests/
│   ├── conftest.py         # Fixtures: driver setup, auto-screenshot on failure
│   └── test_order_journey.py
├── utils/
│   └── logger.py
├── requirements.txt
└── .env.example
```

## Setup

**1. Clone the repo**
```bash
git clone <repo-url>
cd amazon_automation
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure credentials**
```bash
cp .env.example .env
# Edit .env and add your Amazon mobile number and password
```

## Running Tests

```bash
# Run the full journey
pytest tests/test_order_journey.py -v

# Run with HTML report
pytest tests/test_order_journey.py -v --html=reports/report.html
```

> **Note:** `PLACE_REAL_ORDER` defaults to `false`. The test will complete all steps up to the final "Place your order" button without actually placing an order. Set it to `true` in `.env` only when you intentionally want to place a real order.

## Key Design Decisions

- **Page Object Model** — locators and actions are encapsulated per page; tests only orchestrate
- **BasePage** — shared Selenium wrappers with stale element retry and JS click fallback
- **Inline Add to Cart** — clicks the button directly on the search results card rather than navigating into the product page
- **Bot detection mitigation** — disables `AutomationControlled` flag, hides `navigator.webdriver`, uses a fresh temp Chrome profile per session
- **Auto screenshot on failure** — conftest captures a screenshot whenever a test fails
