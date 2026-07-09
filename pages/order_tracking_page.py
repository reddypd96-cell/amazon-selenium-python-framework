from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import config


class OrderTrackingPage(BasePage):
    """
    Represents Amazon's 'Your Orders' page, reached via the
    "Returns & Orders" link in the nav bar.
    """

    ORDER_CARD = (By.CSS_SELECTOR, "div.order-card")
    TRACK_PACKAGE_BUTTON = (By.XPATH, "//span[contains(text(),'Track package')]")
    ORDER_STATUS_TEXT = (By.CSS_SELECTOR, "div.delivery-box__primary-text")

    def load(self):
        """Direct navigation, useful if you're not chaining from HomePage."""
        self.open(f"{config.BASE_URL}/gp/css/order-history")
        return self

    def has_orders(self):
        return self.is_visible(self.ORDER_CARD)

    def track_first_order(self):
        self.click(self.TRACK_PACKAGE_BUTTON)
        return self

    def get_status(self):
        return self.get_text(self.ORDER_STATUS_TEXT)
