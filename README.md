# Amazon Selenium Automation Framework

## Overview

This project is an end-to-end web automation framework developed using **Python**, **Selenium WebDriver**, and **Pytest** following the **Page Object Model (POM)** design pattern.

The framework automates a complete user journey on Amazon, including login, product search, cart verification, checkout navigation, and order tracking. The project is designed to demonstrate reusable automation architecture, maintainability, and scalability rather than focusing on a single test case.

---

**Features**

- Page Object Model (POM) architecture
- Reusable Base Page with common Selenium methods
- Explicit waits for stable execution
- Cross-browser support (Chrome, Firefox, Edge)
- Environment-based configuration using `.env`
- Automatic HTML report generation
- Screenshot capture on test failures
- Modular and maintainable project structure

---

## Test Scenario

The automated test covers the following workflow:

1. Launch Amazon website
2. Sign in with valid credentials
3. Search for a product
4. Add the product to the cart
5. Verify the cart
6. Proceed to checkout
7. Select Cash on Delivery
8. Navigate to Orders
9. Track the latest order

> **Note** - The framework is made in a way that as we doing testing in real production we are not proceeding with real place order

---

## Technology Stack

- Python
- Selenium WebDriver
- Pytest
- WebDriver Manager
- Pytest HTML Reports
- Python Dotenv

---

## Project Structure

```
amazon_automation/
│
├── config/
├── drivers/
├── pages/
├── reports/
├── tests/
├── utils/
├── requirements.txt
├── pytest.ini
├── README.md
└── .env.example
```

---

## Setup Instructions

### Clone the Repository

```bash
git clone <repository-url>
cd amazon_automation
```

### Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Copy the example configuration.

```bash
cp .env.example .env
```

Update the following values inside `.env`:

```
AMAZON_MOBILE_NUMBER=
AMAZON_PASSWORD=
SEARCH_TERM=iphone
HEADLESS=false
PLACE_REAL_ORDER=false
```

---

## Running the Tests

Execute the complete test suite:

`bash
pytest
`

Generate an HTML report:

`bash
pytest --html=reports/report.html
`

---

## Framework Highlights

- Designed using the Page Object Model for better maintainability
- Reusable Selenium utility methods through a Base Page class
- Explicit waits used to improve execution stability
- Externalized configuration through environment variables
- Automatic HTML report generation after execution
- Screenshot capture for failed test cases
- Clean project structure suitable for real-world automation projects






Diwakar Reddy

Automation Test Engineer

Python | Selenium | Pytest | SQL | API Testing | Git | Jenkins
