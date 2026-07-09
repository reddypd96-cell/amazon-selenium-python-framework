from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_TITLE = (By.ID, "sc-active-cart")
    # "Proceed to Buy" on amazon.in submits this same form field.
    PROCEED_TO_BUY_BUTTON = (By.NAME, "proceedToRetailCheckout")

    def is_item_in_cart(self):
        return self.is_visible(self.CART_TITLE)

    def proceed_to_buy(self):
        self.click(self.PROCEED_TO_BUY_BUTTON)
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)
