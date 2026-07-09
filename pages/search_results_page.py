import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class SearchResultsPage(BasePage):

    RESULT_ITEMS = (
        By.XPATH,
        "//div[@data-component-type='s-search-result']"
    )

    # Inline "Add to cart" button on a search result card
    _ADD_TO_CART_ON_CARD = [
        (By.XPATH,
         "(//div[@data-component-type='s-search-result']"
         "//input[@type='submit' and contains(@value,'Add to cart')])[1]"),
        (By.XPATH,
         "(//div[@data-component-type='s-search-result']"
         "//button[contains(normalize-space(),'Add to cart')])[1]"),
        (By.XPATH,
         "(//div[@data-component-type='s-search-result']"
         "//*[contains(@aria-label,'Add to cart') or contains(@title,'Add to cart')])[1]"),
    ]

    # "Maximum Quantity Reached" modal close button
    _MAX_QTY_POPUP_CLOSE = [
        (By.XPATH, "//button[@data-action='a-popover-close']"),
        (By.XPATH,
         "//div[contains(@class,'a-popover') or contains(@class,'a-modal')]"
         "//button[contains(@class,'a-button-close') or contains(@class,'close')]"),
        (By.XPATH, "//button[@aria-label='Close' or @title='Close']"),
        (By.XPATH, "//button[normalize-space(.)='×' or normalize-space(.)='✕']"),
        (By.CSS_SELECTOR,
         "button.a-button-close, button.a-popover-close, "
         "div.a-popover-wrapper button[data-action='a-popover-close']"),
    ]

    def results_count(self):
        products = self.driver.find_elements(*self.RESULT_ITEMS)
        return len(products)

    def add_first_result_to_cart(self):
        """
        Clicks the inline 'Add to cart' button on the first search result card,
        dismisses the 'Maximum Quantity Reached' popup if it appears, then
        returns a ProductPage so the caller can chain go_to_cart().
        """
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located(self.RESULT_ITEMS)
        )

        for locator in self._ADD_TO_CART_ON_CARD:
            try:
                btn = WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable(locator)
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn
                )
                time.sleep(0.3)
                self.driver.execute_script("arguments[0].click();", btn)
                self._dismiss_max_quantity_popup()

                from pages.product_page import ProductPage
                return ProductPage(self.driver)

            except TimeoutException:
                continue

        raise TimeoutException(
            "Could not find an 'Add to cart' button on any search result card."
        )

    def _dismiss_max_quantity_popup(self):
        """
        Closes the 'Maximum Quantity Reached' modal if it appears.
        Silently returns if the popup is not present.
        """
        for locator in self._MAX_QTY_POPUP_CLOSE:
            try:
                btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(locator)
                )
                self.driver.execute_script("arguments[0].click();", btn)
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located(locator)
                )
                return
            except TimeoutException:
                continue
