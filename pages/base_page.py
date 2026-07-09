"""
Base class for all Page Objects.
Provides reusable Selenium wrapper methods with explicit waits.
"""

import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)

from config import config


class BasePage:

    CART_ICON = (By.ID, "nav-cart")
    RETURNS_AND_ORDERS_LINK = (By.ID, "nav-orders")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)

    # ------------------------
    # Browser
    # ------------------------

    def open(self, url):
        self.driver.get(url)

    # ------------------------
    # Find Elements
    # ------------------------

    def find(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def find_clickable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    def find_all(self, locator):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )

    # ------------------------
    # Actions
    # ------------------------

    def click(self, locator):
        element = self.find_clickable(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", element
        )
        try:
            element.click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            element = self.find_clickable(locator)
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text, clear_first=True):
        element = self.find_clickable(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", element
        )
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

    # ------------------------
    # Visibility
    # ------------------------

    def is_visible(self, locator, timeout=None):
        try:
            wait = (
                self.wait if timeout is None
                else WebDriverWait(self.driver, timeout)
            )
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # ------------------------
    # Navigation
    # ------------------------

    def go_to_cart(self):
        from pages.cart_page import CartPage
        # Navigate directly — more reliable than clicking the nav icon
        # after an inline add-to-cart which can trigger page redraws.
        self.open(f"{config.BASE_URL}/gp/cart/view.html")
        return CartPage(self.driver)

    def go_to_orders(self):
        from pages.order_tracking_page import OrderTrackingPage
        self.click(self.RETURNS_AND_ORDERS_LINK)
        return OrderTrackingPage(self.driver)

    # ------------------------
    # Screenshot
    # ------------------------

    def screenshot(self, name):
        os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
        path = os.path.join(
            config.SCREENSHOT_DIR,
            f"{name}_{int(time.time())}.png"
        )
        self.driver.save_screenshot(path)
        return path

    # ------------------------
    # Utilities
    # ------------------------

    def wait_for_url_contains(self, text):
        self.wait.until(EC.url_contains(text))
