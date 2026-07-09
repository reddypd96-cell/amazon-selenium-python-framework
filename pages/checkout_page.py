import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from config import config
from utils.logger import get_logger

log = get_logger(__name__)


class CheckoutPage(BasePage):

    #  Cash on Delivery
    _COD_CANDIDATES = [
        # Variant 1: radio input inside a label that contains "Cash on Delivery"
        (By.XPATH,
         "//span[contains(text(),'Cash on Delivery') or contains(text(),'Cash On Delivery')]"
         "/ancestor::label//input[@type='radio']"),
        # Variant 2: the label/span itself is clickable (Amazon sometimes renders it this way)
        (By.XPATH,
         "//span[contains(text(),'Cash on Delivery') or contains(text(),'Cash On Delivery')]"
         "/ancestor::label"),
        # Variant 3: payment method list item with COD text
        (By.XPATH,
         "//*[contains(@id,'CashOnDelivery') or contains(@value,'CashOnDelivery')]"),
        # Variant 4: aria-label
        (By.XPATH,
         "//*[contains(@aria-label,'Cash on Delivery') or contains(@aria-label,'Cash On Delivery')]"),
    ]

    # "Use this payment method and Continue button"
    _CONTINUE_PAYMENT_CANDIDATES = [
        (By.XPATH,
         "//input[@name='ppw-widgetEvent:SetPaymentPlanSelectContinueEvent']"),
        (By.XPATH,
         "//input[contains(@aria-labelledby,'ppw-widgetEvent')]"),
        (By.XPATH,
         "//input[@type='submit' and ("
         "contains(@value,'Use this payment method') or "
         "contains(@value,'Continue') or "
         "contains(@value,'Next'))]"),
        (By.XPATH,
         "//button[contains(normalize-space(),'Use this payment method') or "
         "contains(normalize-space(),'Continue')]"),
        (By.CSS_SELECTOR,
         "input[name='ppw-widgetEvent\\:SetPaymentPlanSelectContinueEvent']"),
    ]

    PLACE_ORDER_BUTTON = (By.NAME, "placeYourOrder1")

  

    def select_cash_on_delivery(self):
        """
        Finds and selects the Cash on Delivery payment option, then clicks
        the continue/confirm button. Handles Amazon's multi-step checkout
        where the payment step may load after an address step.
        """
        log.info(f"Checkout URL: {self.driver.current_url}")
        self.screenshot("checkout_page")

        # Wait for the page to settle after cart → checkout redirect
        time.sleep(2)

        # Try each COD locator
        selected = False
        for locator in self._COD_CANDIDATES:
            try:
                el = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", el
                )
                self.driver.execute_script("arguments[0].click();", el)
                log.info(f"Clicked COD element via locator: {locator}")
                selected = True
                break
            except TimeoutException:
                continue

        if not selected:
            log.warning(
                "Cash on Delivery option not found with any locator. "
                f"Current URL: {self.driver.current_url} | "
                f"Title: {self.driver.title}"
            )
            self.screenshot("cod_not_found")
            # Don't raise - maybe COD is pre-selected or unavailable;
            # attempt to continue anyway
        else:
            time.sleep(1)  # allow selection to register

        # Click the "Use this payment method" / Continue button
        continued = False
        for locator in self._CONTINUE_PAYMENT_CANDIDATES:
            try:
                btn = WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable(locator)
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn
                )
                self.driver.execute_script("arguments[0].click();", btn)
                log.info(f"Clicked continue payment button via locator: {locator}")
                continued = True
                break
            except TimeoutException:
                continue

        if not continued:
            log.warning(
                "Continue/payment method button not found - "
                "the page may have already advanced."
            )

        return self

    def place_order(self):
        """
        Gated by PLACE_REAL_ORDER flag - won't actually place the order
        unless explicitly enabled in .env.
        """
        if not config.PLACE_REAL_ORDER:
            log.warning(
                "PLACE_REAL_ORDER is false - stopping before the final "
                "'Place your order' click. Set PLACE_REAL_ORDER=true in "
                ".env to actually place the order."
            )
            return None

        self.click(self.PLACE_ORDER_BUTTON)
        from pages.order_tracking_page import OrderTrackingPage
        return OrderTrackingPage(self.driver)
