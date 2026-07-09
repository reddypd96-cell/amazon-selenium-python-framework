from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    """
    Represents an Amazon product detail page.
    In the current flow the driver may still be on the search results page
    after an inline add-to-cart — go_to_cart() on BasePage works from any
    page via the nav bar, so no product-page-specific actions are needed.
    """
    pass
